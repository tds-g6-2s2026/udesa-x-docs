# Historias y responsables

Estado al 2 de octubre de 2026. Fuente: backlog y pull requests de la organización `tds-g6-2s2026`.
Archivo vivo: `historias-y-responsables.xlsx` (hojas Resumen, Historias, Requisitos técnicos).

## Resumen

| Puntos | Total | Hechos | % hecho |
|---|---|---|---|
| Obligatorias | - | - | - |
| Optativas | - | - | - |

Referencia de la cátedra para la intermedia: 65 pts.

### Por integrante (15 optativos requeridos al final c/u)

| Integrante | Oblig. hechos | Opt. hechos | Faltan |
|---|---|---|---|
| Joaquín Szterensus | - | - | - |
| Santino Domato | - | - | - |
| Tomás Díaz | - | - | - |
| Facundo Vulcano | - | - | - |

Regla: cada historia suma una sola vez, a nombre de su responsable (asignado en GitHub).

## Historias hechas / en curso (ejemplo, completar con el xlsx)

| Épica | H | Título | Tipo | Estado | Responsable | Backend | App | PRs | Issue |
|---|---|---|---|---|---|---|---|---|---|
| E.5 | H1 | Creación de Administradores | Obligatoria | Hecha | Joaquín Szterensus | Joaquín, Santino | Santino | admin #2, #3, #6 | #45 |
| E.5 | H2 | Login como Administrador | Obligatoria | Hecha | Santino Domato | Santino | Santino | admin #6 | #46 |
| E.3 | H1 | Seguir a un Usuario | Obligatoria | Hecha | Joaquín Szterensus | Joaquín (social, auth) | Tomás Díaz | social #1, auth #17, mobile #14 #15 | #30 |
| E.2 | H6 | Like a un Post | Obligatoria | Hecha | Joaquín Szterensus | Joaquín | Joaquín | posts #4, mobile #3 | #20 |
| E.2 | H5 | Retweet / Repost | Obligatoria | Hecha (falta cerrar issue) | Santino Domato | Santino, Facundo | Facundo | posts #3 #14 #16, mobile #9 #13 | #19 |
| E.2 | H4 | Responder a un Post | Obligatoria | Hecha (falta cerrar issue) | Joaquín Szterensus | Joaquín | Joaquín | posts #5, mobile #4 | #18 |
| E.2 | H8 | Hashtags | Optativa | Hecha | Facundo Vulcano | Facundo | Facundo | posts #11, mobile #11 | #22 |
| E.2 | H12 | Guardar Posts (Bookmarks) | Optativa | Hecha | Facundo Vulcano | Facundo | Facundo | posts #6, mobile #10 #13 | #26 |
| E.2 | H7 | Post con Imagen | Obligatoria | En curso | Tomás Díaz | Tomás | Tomás | posts #10, media #1, mobile #7 | #21 |

Las issues 57 a 60 son la parte de app de historias que ya figuran (retweet, guardados, seguir, hashtags), no se suman aparte.

## Requisitos técnicos (resumen)

| Requisito | Estado | Responsable |
|---|---|---|
| App principal exclusivamente mobile | Cumplido | Equipo (base Joaquín) |
| Backoffice web | En curso | Santino, Tomás |
| Microservicios | Cumplido | Equipo |
| 2 tipos de BD | Cumplido | Equipo (Postgres + Redis) |
| Backend en más de una tecnología | Cumplido | Python + Go (admin) |
| Desplegada en la nube + Docker | En curso | Joaquín |
| Seguridad OWASP | Parcial | Equipo |
| Tests + cobertura 85% | Parcial | Equipo (mobile 61%) |
| Rate limiting | Cumplido | posts 30/h, social 50/h |
| Cola asincrónica | Pendiente | - |
| IA | Pendiente | - |
