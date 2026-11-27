# Historias y responsables

Estado de `main` al 27 de noviembre de 2026. Fuente: las issues del backlog (`udesa-x-project`) y los pull requests de la organización `tds-g6-2s2026`. Lo que todavía está en un pull request abierto figura como **pendiente**, con la referencia al PR. Planilla: [historias-y-responsables.xlsx](https://github.com/tds-g6-2s2026/udesa-x-docs/raw/main/entrega-final/historias-y-responsables.xlsx), con las hojas Resumen, Historias y Requisitos técnicos.

## Resumen

### Puntos

| Puntos | Total del backlog | Hechos | Hechos con la issue cerrada | % hecho |
|---|---|---|---|---|
| Obligatorias | 82 | 82 | 75 | 100% |
| Optativas | 91 | 68 | 44 | 75% |
| Total | 173 | 150 | 119 | 87% |

- Para aprobar hacen falta los **82** puntos obligatorios con todos sus criterios de aceptación y **15** optativos por integrante.
- Los **82** puntos obligatorios están en `main` y desplegados. Los últimos entraron el 23/11 con la cola de eventos: las tres historias de notificaciones (#40, #41 y #42) y los criterios CA.2 y CA.5 de Eliminación de Cuenta (#4). Falta probarlos de punta a punta en producción y cerrar las issues de notificaciones.

### Por integrante

| Por integrante | Obligatorios hechos | Optativos hechos | Optativos requeridos al final | Optativos que faltan |
|---|---|---|---|---|
| Joaquín Szterensus | 41 | 16 | 15 | 0 |
| Santino Domato | 12 | 11 | 15 | 4 |
| Tomás Díaz | 13 | 23 | 15 | 0 |
| Facundo Vulcano | 16 | 15 | 15 | 0 |

Cómo se cuenta: cada historia suma una sola vez, a nombre de su responsable, que es la persona asignada en la issue de GitHub. Quién hizo el backend y quién la app figura en la tabla de abajo y en la hoja Historias.

- Onboarding Inicial (#14) y Visualización de Perfil (#28) se asignaron a Joaquín el 25/11.
- Santino tiene 11 optativos a su nombre. Su trabajo en el asistente de IA (épica #62, issues IA-01 a IA-14) no tiene puntos en GitHub.
- El 26/11 Santino hizo Listas Personalizadas (#37) y el backend de Invitar Usuarios Externos (#38). #37 no suma a nadie porque no tiene a nadie asignado. Si se le asigna, Santino llega a 14, y a 16 si también se le asigna #38 cuando entre la app.
- El 27/11 Santino hizo Menciones a Usuarios (#23), que tiene asignada.
- Preferencias de Notificación (#44) la hizo primero Santino (notifications #4, mobile #48), pero la revirtió (notifications #5, mobile #51). La terminó Tomás, que está asignado, sobre la misma tabla de preferencias que había quedado en producción.
- Las issues 57 a 60 del backlog son la parte de app de historias que ya figuran (retweet, guardados, seguir y hashtags), por eso no se suman aparte.

## Historias hechas y en curso

| Épica | H | Título | Tipo | Estado | Responsable | Backend | App | PRs | Issue |
|---|---|---|---|---|---|---|---|---|---|
| E.1 | H1 | Registro de Usuarios | Obligatoria | Hecha | Joaquín Szterensus | Joaquín Szterensus | Joaquín Szterensus | auth #1, #3, #14 · mobile #1 · **pendiente** mobile #46 (CA.6) | #1 |
| E.1 | H2 | Inicio de Sesión | Obligatoria | Hecha | Santino Domato | Santino Domato; refresh token: Joaquín Szterensus | Joaquín Szterensus | auth #2, #8 · refresh token: auth #45, #46 · mobile #45 | #2 |
| E.1 | H3 | Cierre de Sesión | Obligatoria | Hecha | Joaquín Szterensus | Joaquín Szterensus | Joaquín Szterensus | auth #9 · mobile #2 | #3 |
| E.1 | H4 | Eliminación de Cuenta | Obligatoria | Hecha (falta probar la cola en producción) | Facundo Vulcano | Facundo Vulcano, Tomás Díaz | Joaquín Szterensus, Facundo Vulcano, Tomás Díaz | auth #5, #29, #30, #36 · social #13 · posts #33 · media #14 · mobile #24, #44 | #4 |
| E.1 | H5 | Olvidé Mi Contraseña | Obligatoria | Hecha | Tomás Díaz | Tomás Díaz, Joaquín Szterensus | Joaquín Szterensus | auth #6, #7 · mobile #1 | #5 |
| E.1 | H6 | Editar mi perfil | Obligatoria | Hecha | Facundo Vulcano | Facundo Vulcano | Joaquín Szterensus, Facundo Vulcano | auth #11 · mobile #24 | #6 |
| E.1 | H7 | Preferencias | Optativa | Hecha | Tomás Díaz | Tomás Díaz | Tomás Díaz, Joaquín Szterensus | auth #13 | #7 |
| E.1 | H8 | Foto de Perfil | Optativa | Hecha | Tomás Díaz | Tomás Díaz (auth, media, gateway) | Tomás Díaz | auth #39 · media #11 · gateway #11 · mobile #33 | #8 |
| E.1 | H10 | Tema de la Aplicación | Optativa | Hecha | Tomás Díaz |  | Tomás Díaz | mobile #5 | #10 |
| E.1 | H11 | Enviar Feedback o Reportar Error | Optativa | Hecha | Facundo Vulcano | Facundo Vulcano (auth, admin) | Facundo Vulcano | auth #34 · admin #24 · mobile #28 | #11 |
| E.1 | H12 | Aceptación de Términos y Política de Privacidad | Obligatoria | Hecha | Facundo Vulcano | Facundo Vulcano | Joaquín Szterensus, Facundo Vulcano | auth #12 · mobile #22 | #12 |
| E.1 | H13 | Cambiar Contraseña | Optativa | Hecha | Santino Domato | Santino Domato | Joaquín Szterensus | auth #10 | #13 |
| E.1 | H14 | Onboarding Inicial | Optativa | Hecha (falta cerrar la issue) | Joaquín Szterensus | Joaquín Szterensus | Joaquín Szterensus | auth #42 · mobile #38, #39, #40 | #14 |
| E.2 | H1 | Crear Post (Tweet) | Obligatoria | Hecha | Joaquín Szterensus | Joaquín Szterensus | Joaquín Szterensus | posts #1 | #15 |
| E.2 | H2 | Feed Principal (Timeline) | Obligatoria | Hecha | Santino Domato | Santino Domato (posts, auth, social) | Santino Domato | posts #12 · auth #18 · social #2 · mobile #8 | #16 |
| E.2 | H3 | Eliminar Post | Obligatoria | Hecha | Santino Domato | Santino Domato; adjuntos: Tomás Díaz | Santino Domato | posts #3, #9, #39 · mobile #6 | #17 |
| E.2 | H4 | Responder a un Post | Obligatoria | Hecha | Joaquín Szterensus | Joaquín Szterensus | Joaquín Szterensus | posts #5 · mobile #4 · posts #37 (CA.3) | #18 |
| E.2 | H5 | Retweet / Repost | Obligatoria | Hecha | Santino Domato | Santino Domato, Facundo Vulcano | Facundo Vulcano, Santino Domato | posts #3, #14, #16 · mobile #9, #13, #25 | #19 |
| E.2 | H6 | Like a un Post | Obligatoria | Hecha | Joaquín Szterensus | Joaquín Szterensus | Joaquín Szterensus | posts #4 · mobile #3 | #20 |
| E.2 | H7 | Post con Imagen | Obligatoria | Hecha | Tomás Díaz | Tomás Díaz | Tomás Díaz | posts #10, #26 · media #1 · mobile #7, #29, #30 | #21 |
| E.2 | H8 | Hashtags | Optativa | Hecha | Facundo Vulcano | Facundo Vulcano | Facundo Vulcano | posts #11 · mobile #11 | #22 |
| E.2 | H9 | Menciones a Usuarios | Optativa | Hecha | Santino Domato | Santino Domato (auth, posts, notifications) | Santino Domato; Guardados: Tomás Díaz | auth #48 · posts #41 · notifications #6 · mobile #52 | #23 |
| E.2 | H10 | Búsqueda de Posts y Usuarios | Obligatoria | Hecha | Joaquín Szterensus | Joaquín Szterensus (auth, posts) | Joaquín Szterensus | auth #26 · posts #21 · mobile #19 | #24 |
| E.2 | H11 | Trending Topics | Optativa | Hecha | Facundo Vulcano | Facundo Vulcano | Facundo Vulcano | posts #23 · mobile #23 | #25 |
| E.2 | H12 | Guardar Posts (Bookmarks) | Optativa | Hecha | Facundo Vulcano | Facundo Vulcano | Facundo Vulcano | posts #6 · mobile #10, #13 | #26 |
| E.2 | H13 | Citar Post (Quote Tweet) | Optativa | Hecha (falta cerrar la issue) | Joaquín Szterensus | Joaquín Szterensus | Joaquín Szterensus | posts #34, #35 · mobile #36, #37 | #27 |
| E.2 | H14 | Visualización de Perfil de Usuario | Obligatoria | Hecha | Joaquín Szterensus | Joaquín Szterensus (auth, posts) | Joaquín Szterensus | auth #27 · posts #20 · mobile #20 | #28 |
| E.2 | H15 | Post con Video | Optativa | Hecha (falta cerrar la issue) | Tomás Díaz | Tomás Díaz (media, posts, gateway) | Tomás Díaz | posts #31, #39 · media #13, #15 · gateway #14 · mobile #35 | #29 |
| E.3 | H1 | Seguir a un Usuario | Obligatoria | Hecha | Joaquín Szterensus | Joaquín Szterensus (social, auth) | Tomás Díaz | social #1 · auth #17 · mobile #14, #15 | #30 |
| E.3 | H2 | Dejar de Seguir a un Usuario | Obligatoria | Hecha | Santino Domato | Santino Domato | Santino Domato | social #9 · mobile #21 | #31 |
| E.3 | H3 | Listado de Seguidores y Seguidos | Obligatoria | Hecha | Facundo Vulcano | Facundo Vulcano | Facundo Vulcano | social #11 · mobile #26 | #32 |
| E.3 | H4 | Bloquear Usuario | Obligatoria | Hecha | Tomás Díaz | Tomás Díaz | Tomás Díaz | auth #43, #44 · social #17, #18 · posts #37, #38 · mobile #41, #42 · docs #9 | #33 |
| E.3 | H5 | Denunciar Usuario | Obligatoria | Hecha | Joaquín Szterensus | Joaquín Szterensus (social, admin, auth) | Joaquín Szterensus | social #12 · admin #22 · auth #33 · mobile #27 | #34 |
| E.3 | H8 | Listas Personalizadas | Optativa | Hecha (falta cerrar la issue) | Sin asignar | Santino Domato (social, posts) | Santino Domato | social #19 · posts #40 · mobile #50 | #37 |
| E.3 | H9 | Invitar Usuarios Externos | Optativa | En curso (falta la app: mobile #49, con cambios pedidos) | Joaquín Szterensus | Santino Domato (auth, social) | Santino Domato | auth #47 · social #20 · **pendiente** mobile #49 | #38 |
| E.3 | H10 | Silenciar Usuario | Optativa | Hecha | Tomás Díaz | Tomás Díaz (social, posts, notifications) | Tomás Díaz | social #21 · posts #43 · notifications #7 · mobile #55 · docs #13 | #39 |
| E.4 | H1 | Recibir notificaciones de nuevo seguidor | Obligatoria | Hecha (falta probarla en producción y cerrar la issue) | Facundo Vulcano | Facundo Vulcano; deploy: Tomás Díaz | Facundo Vulcano | notifications #1 · social #15 · mobile #32 | #40 |
| E.4 | H2 | Notificación de interacción | Obligatoria | Hecha (falta probarla en producción y cerrar la issue) | Facundo Vulcano | Facundo Vulcano, Tomás Díaz (citas); deploy: Tomás Díaz | Facundo Vulcano | notifications #1 · posts #27 · mobile #32 | #41 |
| E.4 | H3 | Centro de Notificaciones In-App | Obligatoria | Hecha (falta probarla en producción y cerrar la issue) | Facundo Vulcano | Facundo Vulcano; deploy: Tomás Díaz | Facundo Vulcano | notifications #1 · gateway #9 · mobile #31 | #42 |
| E.4 | H5 | Configurar Preferencias de Notificación | Optativa | Hecha | Tomás Díaz | Tomás Díaz; primera versión, revertida: Santino Domato | Tomás Díaz; primera versión, revertida: Santino Domato | notifications #7 · mobile #56 · docs #13 · revertidos: notifications #4 y #5, mobile #48 y #51 | #44 |
| E.5 | H1 | Creación de Administradores | Obligatoria | Hecha | Joaquín Szterensus | Joaquín Szterensus, Santino Domato | Santino Domato | admin #2, #3, #6 | #45 |
| E.5 | H2 | Inicio de sesión como Administrador | Obligatoria | Hecha | Joaquín Szterensus | Santino Domato, Tomás Díaz | Santino Domato, Tomás Díaz | admin #6, #7, #9 | #46 |
| E.5 | H3 | Visualización de Métricas | Optativa | Hecha (falta cerrar la issue) | Joaquín Szterensus | Joaquín Szterensus (gateway, auth, posts, admin) | Joaquín Szterensus (portal) | gateway #15 · auth #41 · posts #32 · admin #39, #40 | #47 |
| E.5 | H4 | Buscador y Detalles de Usuarios | Obligatoria | Hecha | Joaquín Szterensus | Joaquín Szterensus (auth, posts, social, admin) | Joaquín Szterensus (portal) | auth #28 · posts #22 · social #8 · admin #14, #15 | #48 |
| E.5 | H5 | Bloqueo de Usuarios por Admin | Obligatoria | Hecha | Joaquín Szterensus | Joaquín Szterensus (admin, auth, gateway) | Joaquín Szterensus (portal) | admin #18 · auth #31 · gateway #7 | #49 |
| E.5 | H6 | Logs de Auditoría | Obligatoria | Hecha | Tomás Díaz | Tomás Díaz | Tomás Díaz (portal) | admin: commit 4672045 de Tomás, entró a main con admin #13 | #50 |
| E.5 | H7 | Gestión de Denuncias | Obligatoria | Hecha | Joaquín Szterensus | Joaquín Szterensus | Joaquín Szterensus (portal) | admin #23 | #51 |
| E.5 | H8 | Exportar Datos | Optativa | Hecha | Tomás Díaz | Tomás Díaz | Tomás Díaz (portal) | admin #21 | #52 |
| E.5 | H9 | Registro de Ultima Conexión | Optativa | Hecha | Tomás Díaz | Tomás Díaz (auth, admin) | Tomás Díaz (portal) | auth #35 · admin #31 | #53 |
| E.5 | H10 | Borrado Forzado de Contenido | Optativa | Hecha (falta cerrar la issue) | Joaquín Szterensus | Joaquín Szterensus | Joaquín Szterensus (portal) | auth #40 · posts #29, #39 · admin #37, #38 | #54 |
| E.5 | H11 | Estado de los Microservicios | Optativa | Hecha | Santino Domato | Santino Domato | Santino Domato (portal) | admin #19 · /healthcheck: auth #32, posts #24, social #10, media #9, gateway #8 | #55 |
| E.5 | H12 | Gestión de Feedback/Reportes | Optativa | Hecha | Facundo Vulcano | Facundo Vulcano | Facundo Vulcano (portal) | admin #25 | #56 |

En el backoffice, la columna App indica quién hizo el portal web.

## Historias sin empezar

| Épica | H | Título | Tipo | Puntos | Estado | Responsable | Issue |
|---|---|---|---|---|---|---|---|
| E.1 | H9 | Social Login | Optativa | 5 | Sin asignar |  | #9 |
| E.3 | H6 | Mensajes Directos (DM) | Optativa | 8 | Sin asignar |  | #35 |
| E.3 | H7 | Usuarios en línea | Optativa | 3 | Sin asignar |  | #36 |
| E.4 | H4 | Notificación de mención | Optativa | 5 | Asignada | Tomás Díaz | #43 |

Notificación de Mención (#43): desde el 27/11 posts publica `post_mentioned` (#23) y notifications lo guarda en la campanita. Una mención de alguien silenciado (#39) o con el interruptor de Menciones apagado (#44) no manda push.

## Pendientes y aclaraciones

| Historia | Título | Pendiente o aclaración |
|---|---|---|
| E.1 H1 | Registro de Usuarios | CA.6: el botón para reenviar el mail de verificación está en **pendiente** mobile #46, abierto el 25/11 (el endpoint ya existe en auth). |
| E.1 H4 | Eliminación de Cuenta | CA.2 (borrar los follows de la cuenta) y CA.5 (en hilos y retweets el contenido queda y el autor pasa a "[Usuario eliminado]", criterio del tutor) entraron con la cola el 23/11: auth #36, social #13, posts #33 y media #14, que además borra la foto de perfil y la portada. La app ya muestra la lápida con el contenido (mobile #31 y #44). Falta probar una baja de punta a punta en producción. |
| E.1 H14 | Onboarding Inicial | En main desde el 21/11. Faltan tildar los CA y cerrar la issue. |
| E.2 H9 | Menciones a Usuarios | En producción desde el 27/11. Las menciones se resuelven al leer el post: un handle que cambia de dueño pasa a apuntar a la cuenta nueva, y el handle tiene que escribirse con las mismas mayúsculas. La suscripción de `tds-group-6-notifications-events` deja pasar `post_mentioned` desde la noche del 27/11; las menciones publicadas antes no llegaron a notifications. Falta probar una mención de punta a punta en producción. |
| E.2 H13 | Citar Post (Quote Tweet) | En main desde el 21/11. Faltan tildar los CA y cerrar la issue. |
| E.2 H15 | Post con Video | Entró el 26/11. La app sube los archivos directo a S3 con una URL firmada, sin pasar por el gateway. Decisión del equipo: solo se aceptan JPG, PNG y MP4, los formatos que piden los CA, así que en iPhone se rechazan las fotos HEIC y los videos MOV. Desde el 26/11, media borra a las 24 h los archivos que no quedaron en ningún post (posts #39 y media #15). Falta cerrar la issue. |
| E.3 H8 | Listas Personalizadas | Entró el 26/11 (social #19, posts #40 y mobile #50). Solo se puede agregar a una lista a alguien que seguís; dejar de seguirlo, bloquearlo o la baja de la cuenta lo saca solo (CA.3). El feed de una lista trae los posts originales de sus integrantes, sin retweets. La issue no tiene a nadie asignado. Faltan tildar los CA y cerrar la issue. |
| E.3 H9 | Invitar Usuarios Externos | El backend entró el 26/11 (auth #47 y social #20). Falta la app, en **pendiente** mobile #49: el 26/11 se pidieron cambios porque el código de invitación se pierde si la persona sale de la pantalla de registro (afecta el CA.2), pegar el enlace completo da un error en inglés y, después de cerrar sesión, aparece Registro con el código viejo. Además, el deep link `udesax://` necesita una APK nueva, porque Expo Go no lo abre. |
| E.3 H10 | Silenciar Usuario | Silenciar oculta al usuario del feed principal y de "Para vos", y corta el push de su actividad. Su perfil, la búsqueda, los hashtags, el detalle y los feeds de listas lo siguen mostrando, y la campanita también, por decisión del equipo. |
| E.4 H1 | Recibir notificaciones de nuevo seguidor | notifications #1 y social #15 entraron y se desplegaron el 23/11. Falta probar el push en un celular Android: en Expo Go no funciona, hace falta una build propia. |
| E.4 H2 | Notificación de interacción | notifications #1 y posts #27 entraron y se desplegaron el 23/11. Avisa likes, retweets, respuestas y citas. Falta probarla en producción. |
| E.4 H3 | Centro de Notificaciones In-App | notifications #1 y gateway #9 entraron y se desplegaron el 23/11; la campanita de la app ya tiene su ruta. Falta probarla en producción. |
| E.4 H5 | Configurar Preferencias de Notificación | Entró el 26/11 (notifications #4 y mobile #48). Los interruptores cortan solo el push: la notificación se guarda igual en la campanita. Las citas usan el interruptor de retweets. Los de menciones y mensajes directos se guardan pero hoy no hacen nada, porque ningún servicio publica esos eventos. La issue está asignada a Tomás; el backend y la app los hizo Santino. Falta cerrar la issue. |
| E.4 H5 | Configurar Preferencias de Notificación | Hay un interruptor por cada tipo que existe: likes, retweets, respuestas, citas, menciones y nuevos seguidores. Mensajes directos no existe, así que CA.1 se da por completo sin ese interruptor. Apagar un tipo corta solo el push: la notificación sigue llegando a la campanita. |
| E.5 H2 | Inicio de sesión como Administrador | La issue ahora está asignada a Joaquín; en la entrega intermedia figuraba a nombre de Santino, que hizo admin #6. |
| E.5 H3 | Visualización de Métricas | En main desde el 21/11. Faltan tildar los CA y cerrar la issue. |
| E.5 H10 | Borrado Forzado de Contenido | posts #29, admin #37 y admin #38 entraron el 23/11. Desde el 26/11, limpiar un post también borra sus archivos de S3 (posts #39). Queda abierto lo que se pidió en la review: el POST interno de posts que vacía un post no pide credencial y confía en la red. Falta cerrar la issue. |

## Requisitos técnicos

| Requisito | Estado | Responsable | Evidencia |
|---|---|---|---|
| App principal exclusivamente mobile | Cumplido | Joaquín Szterensus (base), todo el equipo | mobile-app: React Native con Expo y TypeScript. Push en Android con Firebase Cloud Messaging (mobile #32). |
| Backoffice web para administradores | Cumplido | Joaquín Szterensus, Santino Domato, Tomás Díaz, Facundo Vulcano | El portal vive en admin-service y se publica como sitio estático en S3 con CloudFront. Tiene usuarios, denuncias, auditoría, exportación, feedback, métricas, estado de los servicios y el asistente de IA. |
| Arquitectura de microservicios | Cumplido | Equipo | En EKS corren api-gateway, auth, posts, social, media, admin, notifications, backoffice-agent y udesa-mcp. notifications-service se desplegó el 23/11. |
| Al menos dos tipos de base de datos | Cumplido | Equipo | PostgreSQL, una base por servicio (auth, posts, social, media, admin y notifications), y Redis para datos que vencen. |
| Backend en más de una tecnología | Cumplido | Joaquín Szterensus, Santino Domato, Tomás Díaz | admin-service está escrito en Go; el resto, en Python con FastAPI. |
| Desplegada en la nube, cada servicio en Docker | Cumplido | Joaquín Szterensus (manifiestos), cada dueño de servicio | Cada servicio tiene su Dockerfile y sus manifiestos de Kubernetes. Las imágenes están en ECR y corren en el cluster EKS de la cátedra, namespace tds-group-6. |
| Seguridad según OWASP Top 10 | Parcial | Equipo | Argon2id, JWT firmados y revocables en el acto, refresh tokens con rotación y detección de reuso (auth #45 y #46), bloqueo por intentos, rate limiting, escape de HTML, cookie HttpOnly con anti-CSRF en el backoffice, firma de admin-service para la moderación y credenciales de AWS por IRSA. Falta impedir el secreto JWT por defecto en producción, activar Dependabot y pedir credencial en el POST interno de posts que vacía un post (#54). |
| Metodología ágil y herramientas de seguimiento | Cumplido | Equipo | Sprints semanales, GitHub Project, issues con etiquetas de épica, puntos y servicio, y pull requests con review. |
| Documentación técnica y funcional | Cumplido | Equipo | README y guía de contribución por repo, 17 ADRs, este sitio y los diagramas de arquitectura y de datos. |
| Tests unitarios, de integración y de estrés | Parcial | Equipo; estrés: Facundo Vulcano | Unitarios e integración en todos los backends. Estrés: **pendiente** load-tests #1, con Locust contra el gateway y datos en volumen (5.000 usuarios, 100.000 posts). Hasta 30 usuarios a la vez el p95 queda debajo de 1 s; con 100, el sistema colapsa. |
| Tests de integración en todos los backends | Cumplido | Equipo | Corren contra un PostgreSQL real en la CI de cada servicio. Los servicios de la cola prueban SNS y SQS con moto, un simulador de AWS. |
| Cobertura mínima del 85% en cada servicio y en el frontend, dentro de la CI | Cumplido | Equipo; app: Facundo Vulcano | Los nueve backends exigen 85% en la CI. La app exige 85% de líneas y de sentencias desde el 25/11 (mobile-app #43) y está en alrededor de 92% de líneas. |
| Cobertura visible en cada repositorio | Parcial | Tomás Díaz | Badge de Codecov en el README de auth, posts, social, media, api-gateway, admin y mobile-app. Falta en backoffice-agent, udesa-mcp y notifications-service. |
| Integración y despliegue continuos con GitHub Actions | Parcial | Joaquín Szterensus; agente y MCP: Santino Domato; notifications: Tomás Díaz | CI en cada pull request de todos los repos. CD al mergear a main en auth, posts, social, media, admin, notifications y api-gateway: rol por OIDC, imagen en ECR, kubectl y espera del rollout. backoffice-agent y udesa-mcp se despliegan con un workflow manual desde main. La app no tiene CD, como permite la cátedra. |
| Observabilidad: métricas, logs y trazas en Grafana, IA en Langfuse, con acceso del tutor | Parcial | Joaquín Szterensus | OpenTelemetry en todos los servicios salvo notifications. En EKS, api-gateway, auth, posts, social, media y admin mandan trazas, métricas y logs a Grafana Cloud. El agente tiene el exportador a Langfuse, solo con metadatos. Falta confirmar que el agente y el MCP exporten en EKS: sus manifiestos no definen las variables OTEL_* ni LANGFUSE_*. IA-14 (#77): backoffice-agent #12 (mergeado el 22/11) deja listo el envío a Langfuse desde EKS; falta cargar la variable `LANGFUSE_BASE_URL` y las dos claves en GitHub Actions y correr el deploy del agente, que es manual. notifications-service todavía no tiene observabilidad. En **pendiente**: notifications-service #2 (su observabilidad), backoffice-agent #14 y udesa-mcp #9 (las variables `OTEL_*` de sus manifiestos), los tres abiertos. |
| Rate limiting en al menos un microservicio | Cumplido | Joaquín Szterensus, Santino Domato, Tomás Díaz, Facundo Vulcano | posts: 30 posts por hora. social: 50 follows por hora y una denuncia por par cada 24 h. auth: bloqueo tras 5 logins fallidos, 3 intentos de cambio de contraseña y 3 de baja; 2 mensajes de feedback por hora y 10 invitaciones por día. media: 30 subidas de imágenes y 5 de videos cada 10 minutos por usuario. |
| Al menos una cola asincrónica entre dos microservicios | Cumplido | Facundo Vulcano (diseño y código), Tomás Díaz (recursos de AWS y deploy) | Un tópico de Amazon SNS y una cola de SQS por consumidor ({doc}`ADR-0016 <adr-0016>`). Entró y se desplegó el 23/11: auth #36, social #13 y #15, posts #27 y #33, media #14 y notifications #1. auth, social y posts publican; social, posts, media y notifications consumen. Desde el 26/11, posts también avisa a media qué archivos usa cada post, con un outbox para no perder avisos (posts #39). Falta probarla de punta a punta en producción. |
| Buena experiencia de usuario en app y backoffice | Cumplido | Equipo | Sistema de diseño propio, tema claro y oscuro, español e inglés y onboarding para cuentas nuevas. |
| Al menos una funcionalidad con inteligencia artificial | Cumplido | Santino Domato | Asistente del backoffice ({doc}`ADR-0015 <adr-0015>`): backoffice-agent y udesa-mcp corren en EKS con Amazon Bedrock. Propone sanciones con la evidencia de las denuncias y un administrador las confirma. Desde el 21/11 está activado por completo en producción. |
| Smoke tests (recomendados) | Pendiente |  | No hay smoke tests en los pipelines. |
| Release con un tag que sube la versión mayor | Pendiente | Equipo | Los repos están en 1.x. Falta el tag 2.0.0 de la entrega final. |
