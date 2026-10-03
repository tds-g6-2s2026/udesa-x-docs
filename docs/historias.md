# Historias y responsables

Estado al 2 de octubre de 2026. Fuente: backlog y pull requests de la organización `tds-g6-2s2026`. Planilla original: [historias-y-responsables.xlsx](https://github.com/tds-g6-2s2026/udesa-x-docs/raw/main/entrega-intermedia/historias-y-responsables.xlsx), con las hojas Resumen, Historias y Requisitos técnicos.

## Resumen

### Puntos

| Puntos | Total del backlog | Hechos | Hechos con la issue cerrada | % hecho |
|---|---|---|---|---|
| Obligatorias | 82 | 42 | 38 | 51% |
| Optativas | 91 | 12 | 12 | 13% |
| Total | 173 | 54 | 50 | 31% |

- Referencia de la cátedra para la entrega intermedia: **65** puntos.
- Diferencia contra la referencia: **-11** puntos.

### Por integrante

| Por integrante | Obligatorios hechos | Optativos hechos | Optativos requeridos al final | Optativos que faltan |
|---|---|---|---|---|
| Joaquín Szterensus | 21 | 0 | 15 | 15 |
| Santino Domato | 12 | 3 | 15 | 12 |
| Tomás Díaz | 3 | 3 | 15 | 12 |
| Facundo Vulcano | 6 | 6 | 15 | 9 |

Cómo se cuenta: cada historia suma una sola vez, a nombre de su responsable (la persona asignada en GitHub). Quién hizo el backend y quién la app figura en la hoja Historias.

Las issues 57 a 60 del backlog son la parte de app de historias que ya figuran (retweet, guardados, seguir y hashtags), por eso no se suman aparte.

## Historias hechas y en curso

| Épica | H | Título | Tipo | Estado | Responsable | Backend | App | PRs | Issue |
|---|---|---|---|---|---|---|---|---|---|
| E.1 | H1 | Registro de Usuarios | Obligatoria | Hecha | Joaquín Szterensus | Joaquín Szterensus | Joaquín Szterensus | auth #1, #3, #14 · mobile #1 | #1 |
| E.1 | H2 | Inicio de Sesión | Obligatoria | Hecha | Santino Domato | Santino Domato | Joaquín Szterensus | auth #2, #8 | #2 |
| E.1 | H3 | Cierre de Sesión | Obligatoria | Hecha | Joaquín Szterensus | Joaquín Szterensus | Joaquín Szterensus | auth #9 · mobile #2 | #3 |
| E.1 | H4 | Eliminación de Cuenta | Obligatoria | Hecha | Facundo Vulcano | Facundo Vulcano | Joaquín Szterensus | auth #5 | #4 |
| E.1 | H5 | Olvidé Mi Contraseña | Obligatoria | Hecha | Tomás Díaz | Tomás Díaz, Joaquín Szterensus | Joaquín Szterensus | auth #6, #7 · mobile #1 | #5 |
| E.1 | H6 | Editar mi perfil | Obligatoria | Hecha | Facundo Vulcano | Facundo Vulcano | Joaquín Szterensus | auth #11 | #6 |
| E.1 | H7 | Preferencias | Optativa | Hecha | Tomás Díaz | Tomás Díaz | Tomás Díaz, Joaquín Szterensus | auth #13 | #7 |
| E.1 | H10 | Tema de la Aplicación | Optativa | Hecha | Tomás Díaz |  | Tomás Díaz | mobile #5 | #10 |
| E.1 | H12 | Aceptación de Términos y Política de Privacidad | Obligatoria | Hecha | Facundo Vulcano | Facundo Vulcano | Joaquín Szterensus | auth #12 | #12 |
| E.1 | H13 | Cambiar Contraseña | Optativa | Hecha | Santino Domato | Santino Domato | Joaquín Szterensus | auth #10 | #13 |
| E.2 | H1 | Crear Post (Tweet) | Obligatoria | Hecha | Joaquín Szterensus | Joaquín Szterensus | Joaquín Szterensus | posts #1 | #15 |
| E.2 | H2 | Feed Principal (Timeline) | Obligatoria | Hecha | Santino Domato | Santino Domato (posts, auth, social) | Santino Domato | posts #12 · auth #18 · social #2 · mobile #8 | #16 |
| E.2 | H3 | Eliminar Post | Obligatoria | Hecha | Santino Domato | Santino Domato | Santino Domato | posts #3, #9 · mobile #6 | #17 |
| E.2 | H4 | Responder a un Post | Obligatoria | Hecha (falta cerrar la issue) | Joaquín Szterensus | Joaquín Szterensus | Joaquín Szterensus | posts #5 · mobile #4 | #18 |
| E.2 | H5 | Retweet / Repost | Obligatoria | Hecha (falta cerrar la issue) | Santino Domato | Santino Domato, Facundo Vulcano | Facundo Vulcano | posts #3, #14, #16 · mobile #9, #13 | #19 |
| E.2 | H6 | Like a un Post | Obligatoria | Hecha | Joaquín Szterensus | Joaquín Szterensus | Joaquín Szterensus | posts #4 · mobile #3 | #20 |
| E.2 | H7 | Post con Imagen | Obligatoria | En curso | Tomás Díaz | Tomás Díaz | Tomás Díaz | posts #10 · media #1 · mobile #7 (abiertos) | #21 |
| E.2 | H8 | Hashtags | Optativa | Hecha | Facundo Vulcano | Facundo Vulcano | Facundo Vulcano | posts #11 · mobile #11 | #22 |
| E.2 | H12 | Guardar Posts (Bookmarks) | Optativa | Hecha | Facundo Vulcano | Facundo Vulcano | Facundo Vulcano | posts #6 · mobile #10, #13 | #26 |
| E.3 | H1 | Seguir a un Usuario | Obligatoria | Hecha | Joaquín Szterensus | Joaquín Szterensus (social, auth) | Tomás Díaz | social #1 · auth #17 · mobile #14, #15 | #30 |
| E.5 | H1 | Creación de Administradores | Obligatoria | Hecha | Joaquín Szterensus | Joaquín Szterensus, Santino Domato | Santino Domato | admin #2, #3, #6 | #45 |
| E.5 | H2 | Inicio de sesión como Administrador | Obligatoria | Hecha | Santino Domato | Santino Domato | Santino Domato | admin #6 (+ #7, #9 abiertos de Tomás) | #46 |

### Pendientes y aclaraciones

| Historia | Título | Pendiente o aclaración |
|---|---|---|
| E.1 H1 | Registro de Usuarios | CA.6: la app no tiene el botón para reenviar el mail de verificación (el endpoint ya existe en auth). |
| E.1 H4 | Eliminación de Cuenta | CA.2: los follows del usuario borrado siguen en social. CA.5: sus respuestas desaparecen del hilo en vez de mostrar "[Usuario eliminado]". Ambos dependen de la cola de eventos. |
| E.1 H12 | Aceptación de Términos y Política de Privacidad | CA.1: el checkbox del registro no tiene links a los textos y el botón no se deshabilita. |
| E.2 H2 | Feed Principal (Timeline) | La issue no tiene responsable asignado en GitHub. |
| E.2 H4 | Responder a un Post | Implementada y mergeada; falta cerrar la issue. |
| E.2 H5 | Retweet / Repost | Implementada y mergeada; falta cerrar la issue. CA.3 pide que el retweet desaparezca del perfil, pero la pantalla de perfil (E.2 H14) no existe todavía. |
| E.2 H7 | Post con Imagen | En curso: pull requests abiertos. |
| E.5 H2 | Inicio de sesión como Administrador | La issue no tiene responsable asignado en GitHub. |

## Requisitos técnicos

| Requisito | Estado | Responsable | Evidencia |
|---|---|---|---|
| App principal exclusivamente mobile | Cumplido | Joaquín Szterensus (base), todo el equipo | mobile-app: React Native con Expo y TypeScript. |
| Backoffice web para administradores | En curso | Santino Domato, Tomás Díaz | admin-service sirve el portal web (admin #6 mergeado; #9 abierto). |
| Arquitectura de microservicios | Cumplido | Equipo | auth, posts, social, media y admin, más un api-gateway. |
| Al menos dos tipos de base de datos | Cumplido | Equipo | PostgreSQL, una base por servicio, y Redis para datos con vencimiento. |
| Backend en más de una tecnología | Cumplido | Joaquín Szterensus, Santino Domato, Tomás Díaz | admin-service está escrito en Go; el resto, en Python con FastAPI. |
| Desplegada en la nube, cada servicio en Docker | En curso | Joaquín Szterensus | Dockerfile en cada servicio. Manifiestos de Kubernetes para EKS mergeados el 02/10; auth ya desplegado, el resto falla en el último despliegue. |
| Seguridad según OWASP Top 10 | Parcial | Equipo | Argon2id, JWT firmados y revocables, bloqueo por intentos, rate limiting, sanitización y secretos por GitHub Secrets. Falta impedir el secreto JWT por defecto en producción y activar Dependabot. |
| Metodología ágil y herramientas de seguimiento | Cumplido | Equipo | Sprints semanales, GitHub Project, issues con etiquetas de épica, puntos y servicio, y pull requests con review. |
| Documentación técnica y funcional | En curso | Equipo | README y guía de contribución por repo; ADRs y diagramas de esta entrega. |
| Tests unitarios, de integración y de estrés | Parcial | Equipo | Unitarios e integración en todos los backends. Pruebas de estrés pendientes. |
| Tests de integración en todos los backends | Cumplido | Equipo | Corren contra un PostgreSQL real en la CI de cada servicio. |
| Cobertura mínima del 85% en cada servicio y en el frontend, dentro de la CI | Parcial | Equipo | Backends entre 89,9% y 99,3% con mínimo exigido en la CI. App mobile en 61%, sin mínimo en la CI. |
| Cobertura visible en cada repositorio | En curso | Tomás Díaz | Codecov con badge en admin-service; pull requests abiertos en los demás repos. |
| Despliegue continuo con GitHub Actions | En curso | Joaquín Szterensus | Workflow de deploy en los 6 servicios: OIDC, imagen en ECR, aplicar en EKS y esperar el rollout. |
| Observabilidad: métricas, logs y trazas, con acceso del tutor | Pendiente |  | Todavía no implementado. |
| Rate limiting en al menos un microservicio | Cumplido | Joaquín Szterensus, Santino Domato | posts: 30 posts por hora. social: 50 follows por hora. auth: bloqueo tras 5 intentos de login fallidos. |
| Al menos una cola asincrónica entre dos microservicios | Pendiente |  | auth ya publica el evento user_deleted a través de una interfaz, hoy solo registrado en el log; falta el broker y el consumidor. |
| Buena experiencia de usuario en app y backoffice | En curso | Equipo | Sistema de diseño propio, tema claro y oscuro, idiomas español e inglés. |
| Al menos una funcionalidad con inteligencia artificial | Pendiente |  | Se propone en la semana 11, acordada con el tutor. |
