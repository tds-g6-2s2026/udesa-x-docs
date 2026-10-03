# Arquitectura

```{image} images/arquitectura.png
:alt: Diagrama de arquitectura de UdeSA-X
:width: 100%
```

UdeSA-X está armado con microservicios separados por responsabilidad, y cada uno tiene su propia base. La app habla solo con el gateway. Los servicios se llaman entre sí por HTTP dentro del cluster.

## Contexto

| Elemento | Tipo | Relación con UdeSA-X |
|---|---|---|
| Usuario de la app | Persona | Usa la app mobile para publicar, seguir y leer su feed. |
| Administrador | Persona | Usa el backoffice web para gestionar administradores. |
| Gmail | Sistema externo | Envía los mails de verificación y de recuperación de contraseña. |
| AWS | Sistema externo | Aloja la plataforma: CloudFront, el balanceador, el cluster EKS y las imágenes en ECR. |
| GitHub | Sistema externo | Guarda el código y corre la integración y el despliegue continuos. |

## Capas

### 1. Clientes

- **App mobile:** React Native con Expo y TypeScript. Usa TanStack Query y Zustand, y guarda el token cifrado en SecureStore.
- **Backoffice web:** se usa desde el navegador del administrador. El portal lo sirve admin-service.

### 2. Borde de AWS

- **CloudFront:** recibe el tráfico por HTTPS con el dominio del grupo. Las rutas `/api/*` van al ALB.
- **ALB compartido:** es el balanceador de la cátedra, en el IngressGroup `tds-shared`. Manda `/api` al api-gateway.

### 3. Cluster EKS

Todo corre en el cluster `tds-cluster`, en el namespace `tds-group-6`. Hay un pod por servicio, con estrategia Recreate y una cuota de 8 pods. Cada servicio es una imagen Docker.

| Servicio | Puerto | Lenguaje | Qué hace | Rutas que recibe del gateway | Datos |
|---|---|---|---|---|---|
| api-gateway | 8080 | Python, FastAPI | Rutea por la primera palabra de la ruta, verifica el token con auth y lo guarda 30 segundos, y agrega `X-User-Id`. | Todo lo que llega a `/api` | Ninguno |
| auth-service | 8000 | Python | Identidad y sesión: registro, login, perfil y baja. | `/auth` | PostgreSQL y Redis |
| posts-service | 8001 | Python | Contenido y feed: posts, likes, retweets y hashtags. | `/posts` | PostgreSQL y Redis |
| social-service | 8002 | Python | Grafo social: follows, solicitudes y sugerencias. | `/follows`, `/follow-requests`, `/users` | PostgreSQL y Redis |
| media-service | 8003 | Python | Archivos: subida de imágenes. | `/media`, `/files` | Ninguno por ahora |
| admin-service | 8004 | Go | Backoffice: administradores y portal web. | `/admin` | PostgreSQL |

Los puertos son los de cada Service de Kubernetes. Adentro del contenedor, los servicios Python escuchan en el 8000. Las rutas `auth` y `admin` pasan sin que el gateway verifique el token, porque esos servicios manejan su propia autenticación.

### Llamadas entre servicios

Todas son pedidos HTTP sincrónicos.

| Número | Llamada | Para qué |
|---|---|---|
| 1 | posts → auth | Pedir los datos de los autores, en lote. |
| 2 | posts → social | Saber a quién sigue el usuario. |
| 3 | social → auth | Saber si la cuenta es pública. |
| G | gateway → auth | Verificar el token; la respuesta se guarda 30 segundos. |

### 4. Fuera del cluster

Desde el cluster se llega por el NAT.

- **PostgreSQL:** una base por servicio: auth, posts, social y admin. No hay claves foráneas entre bases.
- **Redis gestionado:** guarda datos que vencen solos, como links de verificación, límites por hora, bloqueos y tokens revocados.
- **Gmail SMTP:** auth manda los mails de verificación y de recuperación de contraseña.
- **Amazon S3:** pendiente. Es para las imágenes de media-service, que hoy las guarda en disco.
- **Cola de eventos:** pendiente. auth publicaría el evento `user_deleted`, y posts y social lo consumirían.

### 5. Integración y despliegue continuos

1. **GitHub:** 7 repositorios, uno por servicio más la app.
2. **GitHub Actions, CI:** en cada pull request corre Ruff, los tests unitarios y de integración, y exige cobertura de 85% o más.
3. **GitHub Actions, CD:** en cada merge a main asume un rol de AWS por OIDC, construye la imagen, la sube a ECR, aplica los manifiestos con kubectl y espera el rollout.
4. **Amazon ECR:** guarda una imagen por servicio, etiquetada con el commit. El cluster descarga la imagen desde ahí.

## Pendiente

- La observabilidad: métricas, logs y trazas.
- La cola de eventos y el almacenamiento en S3.
- Al 2 de octubre de 2026, auth ya está desplegado en EKS y los demás servicios están en proceso.

Las decisiones detrás de este diseño están en los [ADRs](adrs.md).
