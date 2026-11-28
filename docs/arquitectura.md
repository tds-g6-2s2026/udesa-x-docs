# Arquitectura

```{image} images/arquitectura.png
:alt: Diagrama de arquitectura de UdeSA-X
:width: 100%
```

Estado de `main` al 27 de noviembre de 2026, más los PR de Silenciar Usuario (E.3 H10: social #21, posts #43, notifications #7, mobile #55) y Preferencias de Notificación (E.4 H5: notifications #7, mobile #56), que ya se cuentan como hechos. El resto de lo que todavía está en un pull request abierto figura como **pendiente**, con la referencia al PR.

UdeSA-X está armado con microservicios separados por responsabilidad, y cada uno tiene su propia base. La app habla con el gateway, salvo para subir archivos: los sube directo a S3 con una URL firmada que le da media-service. Los servicios se llaman entre sí por HTTP dentro del cluster. El backoffice suma un asistente de IA: un agente y un servidor MCP que usan Amazon Bedrock.

## Contexto

| Elemento | Tipo | Relación con UdeSA-X |
|---|---|---|
| Usuario de la app | Persona | Usa la app mobile para publicar, seguir, leer su feed y recibir notificaciones. |
| Administrador | Persona | Usa el backoffice web para moderar cuentas, ver métricas y consultar al asistente de IA. |
| Gmail | Sistema externo | Envía los mails de verificación, de recuperación de contraseña y de advertencias de moderación, los avisos a soporte y las alertas de servicios caídos. |
| AWS | Sistema externo | Aloja la plataforma: CloudFront, el balanceador, el cluster EKS, las imágenes en ECR, los archivos en S3 y el modelo de Amazon Bedrock, y la cola de eventos en SNS y SQS. |
| Firebase Cloud Messaging | Sistema externo | Entrega las notificaciones push en Android. Lo usa notifications-service. |
| Grafana Cloud | Sistema externo | Recibe las trazas, métricas y logs de los servicios por OpenTelemetry. |
| Langfuse | Sistema externo | Recibe las trazas del agente de IA, solo con metadatos. |
| GitHub | Sistema externo | Guarda el código y corre la integración y el despliegue continuos. |

## Capas

### 1. Clientes

- **App mobile:** React Native con Expo y TypeScript. Usa TanStack Query y Zustand, y guarda el token cifrado en SecureStore. Registra el token de Firebase para el push en Android (mobile #32) y tiene la campanita de notificaciones (mobile #31). Renueva la sesión con el refresh token (mobile #45) y sube las fotos y los videos directo a S3 (mobile #35). Las menciones abren el perfil de la persona mencionada (mobile #52). La app tiene CI con cobertura mínima de 85% (mobile #43), pero no despliegue continuo.
- **Backoffice web:** se usa desde el navegador del administrador. El código está en admin-service; se publica como sitio estático en S3 y lo sirve CloudFront. Llama a la API de admin en `/api/admin`.

### 2. Borde de AWS

- **CloudFront:** recibe el tráfico por HTTPS con el dominio del grupo. Las rutas `/api/*` van al ALB. Desde S3 sirve el backoffice estático y los archivos de media-service, en `/media`.
- **ALB compartido:** es el balanceador de la cátedra, en el IngressGroup `tds-shared`. Manda `/api` al api-gateway.

### 3. Cluster EKS

Todo corre en el cluster `tds-cluster`, en el namespace `tds-group-6`. Hay un pod por servicio, con estrategia Recreate. Cada servicio es una imagen Docker. La cuota del namespace es de 9 pods y 4,5 núcleos de CPU en límites (gateway #9), y hoy corren 9 servicios.

| Servicio | Puerto | Lenguaje | Qué hace | Rutas que recibe del gateway | Datos |
|---|---|---|---|---|---|
| api-gateway | 8080 | Python, FastAPI | Rutea por la primera palabra de la ruta. Verifica el token con auth y guarda el resultado hasta 5 minutos, pero en cada pedido consulta en Redis si la sesión fue revocada. Agrega `X-User-Id` y `X-User-Handle` y anota a cada usuario activo para la vista Métricas. Corta en 1 MB el body de los pedidos (gateway #14), salvo los de media, que reenvía en streaming. | Todo lo que llega a `/api` | Redis |
| auth-service | 8000 | Python | Identidad y cuenta: registro, login con refresh token, perfil, fotos, preferencias, onboarding, invitaciones, baja, feedback, sanciones y estadísticas internas. | `/auth` | PostgreSQL y Redis |
| posts-service | 8001 | Python | Contenido y feed: posts, respuestas, citas, likes, retweets, guardados, hashtags, menciones, tendencias, búsqueda y el feed de cada lista. Saca del feed a quienes el usuario bloqueó o silenció. | `/posts` | PostgreSQL y Redis |
| social-service | 8002 | Python | Grafo social: follows, solicitudes, sugerencias, seguidores y seguidos, bloqueos, silenciados, listas personalizadas, el follow de las invitaciones y denuncias. | `/follows`, `/follow-requests`, `/users` | PostgreSQL y Redis |
| media-service | 8003 | Python | Archivos: imágenes y videos de los posts, fotos de perfil y portadas. Da las URL firmadas para subir directo a S3, valida lo subido y borra lo que no quedó en ningún post. | `/media`, `/files` | PostgreSQL y S3 |
| admin-service | 8004 | Go | Backoffice: administradores, usuarios, denuncias, auditoría, feedback, métricas, monitor de servicios, sanciones y conversaciones con el asistente. | `/admin`, `/backoffice` | PostgreSQL |
| backoffice-agent | 8005 | Python | Agente de IA: resuelve las consultas del asistente con Amazon Bedrock y las herramientas del MCP. | Ninguna | Ninguno |
| udesa-mcp | 8006 | Python | Servidor MCP: herramientas de evidencia, estado de los servicios, evaluación con Bedrock y propuestas de sanción. | Ninguna | Ninguno |
| notifications-service | 8005 | Python | Notificaciones: lee su cola de eventos, guarda la campanita de cada usuario y manda el push por Firebase si sus preferencias lo permiten y si no silenció a quien actuó. Desplegado el 23/11. | `/notifications` | PostgreSQL |

Los puertos son los de cada Service de Kubernetes; backoffice-agent y notifications usan el mismo número en Services distintos. Adentro del contenedor, los servicios Python escuchan en el 8000, salvo el agente y el MCP. Las rutas de auth y de admin pasan sin que el gateway verifique el token, porque esos servicios manejan su propia autenticación. El agente y el MCP no tienen rutas públicas y solo aceptan un token interno firmado por admin-service.

### Llamadas entre servicios

Todas son pedidos HTTP sincrónicos dentro del cluster. Los números son los del diagrama.

| Número | Llamada | Para qué |
|---|---|---|
| 1 | posts → auth | Pedir los datos de los autores, en lote, y resolver los handles de las menciones (`POST /auth/users/by-handles`, auth #48). |
| 2 | posts → social | Saber a quién sigue el usuario, a quién bloqueó y a quién silenció (`GET /internal/users/{id}/muted-ids`). Para el feed de una lista, pedir sus integrantes con el token de quien mira (`GET /users/me/lists/{id}/member-ids`): si la lista no es suya o no existe, da 404, y si social no responde en 3 s, 503. |
| 3 | posts → media | Validar que las imágenes o el video de un post sean del autor. |
| 4 | social → auth | Saber si la cuenta es pública y pedir datos de usuarios en lote. |
| 5 | social → admin | Entregar las denuncias, con un token de servicio. |
| 6 | auth → media | Validar la foto de perfil o la portada nueva y borrar la anterior. |
| 7 | auth → admin | Entregar el feedback que mandan los usuarios. |
| 8 | admin → auth, posts y social | Buscador y detalle de usuarios, bloqueos, sanciones, estadísticas y evidencia de publicaciones. |
| 9 | admin ⇄ backoffice-agent | admin le pasa al agente una consulta del asistente; el agente toma la ejecución y guarda el resultado en admin. |
| 10 | backoffice-agent → udesa-mcp | Usar las herramientas del asistente. |
| 11 | udesa-mcp → admin | Leer la evidencia y guardar las propuestas de sanción, siempre a través de admin. |
| G | gateway → auth | Verificar el token. |
| 12 | auth → social | Avisar que una cuenta invitada verificó el email, para que siga a quien la invitó (`POST /internal/referrals`). Va con un JWT de alcance limitado: solo sirve para esa ruta (aud `udesa-social-referrals`) y vence a los 60 s. Si social no responde, auth reintenta cada 30 s. |
| 13 | notifications → auth y social | A auth, pedir el handle de quien generó el aviso. A social, antes de cada push, preguntar si quien recibe silenció a quien actuó (`GET /internal/users/{id}/mutes/{other_id}`). |
| M | admin → todos | Monitor: consulta el `/healthcheck` de cada servicio y avisa por mail si alguno cae. |

Además, el gateway y auth comparten dos datos en Redis: auth publica las revocaciones de sesión que lee el gateway, y el gateway anota los usuarios en línea que auth cuenta para Métricas.

### 4. Fuera del cluster

Desde el cluster se llega por el NAT.

- **PostgreSQL:** una base por servicio: auth, posts, social, media, admin y notifications. No hay claves foráneas entre bases.
- **Redis gestionado:** guarda datos que vencen solos, como links de verificación, límites por hora, bloqueos, tokens revocados y el ranking de tendencias, y la lista de usuarios en línea del gateway.
- **Gmail SMTP:** auth manda los mails de verificación, de recuperación de contraseña y las advertencias de moderación. admin manda los avisos a soporte por cada feedback y las alertas de servicios caídos.
- **Amazon S3:** guarda los archivos de media-service. El pod accede con IRSA, sin claves en el código, y CloudFront sirve los archivos. La app sube cada archivo directo a S3 con una URL firmada que vence a los diez minutos; después media lo valida y lo registra ({doc}`ADR-0019 <adr-0019>`).
- **Amazon Bedrock:** modelo del agente y evaluador del MCP, en us-east-2. Los dos pods usan un rol de IAM por IRSA.
- **Firebase Cloud Messaging:** notifications-service manda los push con la API HTTP v1 de FCM; la app registra el token del celular.
- **Grafana Cloud:** recibe por OTLP las trazas, métricas y logs de api-gateway, auth, posts, social, media y admin, y desde el 27/11 también los del agente y el MCP (backoffice-agent #14 y udesa-mcp #9, ya desplegados). Falta notifications (ver Pendiente). La decisión está en {doc}`ADR-0018 <adr-0018>`.
- **Langfuse:** recibe las trazas del agente con el modelo, los tokens, la duración y las herramientas usadas, nunca el texto del chat. Activo en EKS: backoffice-agent #12 lo dejó listo, la URL y las claves se cargaron el 26/11 y backoffice-agent #15 (desplegado el 27/11) ordena y agrega filtros a las trazas.
- **Cola de eventos:** entró el 23/11. Un tópico de Amazon SNS y una cola de Amazon SQS por cada servicio que consume ({doc}`ADR-0016 <adr-0016>`). auth publica `user_deleted`, social publica `follow_created` y posts publica `post_liked`, `post_retweeted`, `post_replied`, `post_quoted` y, desde el 27/11, `post_mentioned` (posts #41). La baja de cuenta llega a cuatro servicios: social borra los follows y los bloqueos de la cuenta, posts muestra sus respuestas y los retweets de sus posts con su contenido y el autor como "[Usuario eliminado]" (criterio del tutor para el CA.5), media borra la foto de perfil y la portada, y notifications borra los tokens y las notificaciones de la cuenta. La cola de notifications recibe además los follows, las interacciones y las menciones, para avisarle a cada usuario ({doc}`ADR-0017 <adr-0017>`): su filtro en SNS acepta siete tipos. Desde el 26/11, posts también publica `post_media_attached` y `post_media_removed` para que media sepa qué archivos usa cada post y borre los que se sacaron. posts los guarda primero en una tabla outbox, en la misma transacción que el post, y un proceso los publica después, así no se pierde ningún aviso. `post_mentioned` usa el mismo outbox.

### 5. Integración y despliegue continuos

1. **GitHub:** un repositorio por servicio (nueve) y otro para la app, más `load-tests` (pruebas de carga), `udesa-x-docs` (esta documentación) y `udesa-x-project` (backlog y GitHub Project).
2. **GitHub Actions, CI:** en cada pull request corre el lint (Ruff, o golangci-lint en admin), los tests unitarios y de integración, y exige cobertura de 85% o más. La cobertura se publica en Codecov.
3. **GitHub Actions, CD:** en cada merge a main de auth, posts, social, media, admin, notifications y api-gateway asume un rol de AWS por OIDC, construye la imagen, la sube a ECR, aplica los manifiestos con kubectl y espera el rollout. backoffice-agent y udesa-mcp se despliegan automáticamente después de que pasa la CI del mismo commit de main. Ambos verifican la cuota y los permisos; MCP conserva la configuración de evidencia aplicada en el clúster y el agente espera las ejecuciones aceptadas al apagarse.
   Hay además tres workflows manuales de operación: `seed-demo` en auth carga datos de demo en producción (auth #49), `recover-superadmin` en admin le da acceso de emergencia a un SuperAdmin que perdió su contraseña, y `ai-signing` en admin carga en el cluster la clave privada con la que admin firma los tokens del agente y del MCP, y la pública (JWKS) con la que ellos los verifican.
4. **Amazon ECR:** guarda una imagen por servicio, etiquetada con el commit. El cluster descarga la imagen desde ahí.

## Pendiente

- **Observabilidad de notifications-service:** todavía no exporta a Grafana Cloud. Está en **pendiente** notifications-service #2, abierto.
- **Pruebas de carga:** el repositorio `load-tests` tiene las pruebas con Locust en **pendiente** load-tests #1, abierto.

Las decisiones detrás de este diseño están en los [ADRs](adrs.md).
