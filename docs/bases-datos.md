# Bases de datos

```{image} images/modelo-datos.png
:alt: Modelo de datos de UdeSA-X
:width: 100%
```

Estado de `main` al 24 de noviembre de 2026, según los modelos y las migraciones de cada repositorio. Las tablas que todavía están en un pull request abierto figuran al final, en la sección Pendiente.

Cada servicio tiene su propia base PostgreSQL, y hay un Redis compartido para los datos que vencen. api-gateway, backoffice-agent y udesa-mcp no tienen base.

**Entre servicios no hay claves foráneas: solo se guardan los UUID. Cada servicio es dueño de su base, y para leer datos de otro servicio usa su API.**

Referencias de la columna Claves:

- **PK:** clave primaria.
- **FK:** clave foránea dentro de la misma base.
- **UQ:** valor único.
- **IX:** índice.
- **CK:** restricción CHECK.
- **→ users:** guarda el id de un usuario de auth, sin clave foránea. Lo mismo con **→ posts** y **→ media**.

## auth-service

Identidad, cuenta y sanciones.

### users

| Columna | Tipo | Claves |
|---|---|---|
| id | UUID | PK |
| email | VARCHAR(255) | |
| email_normalized | VARCHAR(255) | UQ |
| handle | VARCHAR(16) | UQ |
| display_name | VARCHAR(50) | |
| bio | VARCHAR(160), puede ser null | |
| avatar_media_id | UUID, puede ser null | → media |
| avatar_url | VARCHAR(512), puede ser null | |
| cover_media_id | UUID, puede ser null | → media |
| cover_url | VARCHAR(512), puede ser null | |
| password_hash | Argon2id | |
| is_verified | BOOLEAN | |
| is_suspended | BOOLEAN | |
| suspended_until | TIMESTAMPTZ, puede ser null | |
| under_review_at | TIMESTAMPTZ, puede ser null | |
| review_version | BIGINT | |
| profile_visibility | public o protected | |
| feed_language | VARCHAR(8) | |
| interests | VARCHAR(32)[] | |
| onboarding_completed_at | TIMESTAMPTZ, puede ser null | |
| accepted_terms | BOOLEAN | |
| accepted_terms_at | TIMESTAMPTZ, puede ser null | |
| token_version | INTEGER | |
| last_login_at | TIMESTAMPTZ, puede ser null | |
| created_at | TIMESTAMPTZ | |
| deleted_at | TIMESTAMPTZ, puede ser null | |

- `email_normalized` guarda el email en minúsculas y es único, así no puede haber dos cuentas con el mismo email escrito con distintas mayúsculas.
- `deleted_at` marca la baja lógica de la cuenta.
- `token_version` permite invalidar todos los tokens de un usuario.
- Las columnas `avatar_*` y `cover_*` guardan el archivo actual de media-service y su URL, para no consultar a media en cada lectura del perfil (E.1 H8).
- Sanciones: `is_suspended` es el bloqueo, `suspended_until` la suspensión temporal y `under_review_at` la cuenta en revisión por denuncias. `review_version` evita que una orden vieja de admin pise una más nueva.
- `interests` guarda los ids del catálogo de intereses del onboarding y `onboarding_completed_at` marca que ya lo hizo (#14). La migración 0011 dio por hecho el onboarding de las cuentas verificadas que ya existían.
- `last_login_at` es el último login exitoso (E.5 H9).

### sanction_operations

| Columna | Tipo | Claves |
|---|---|---|
| id | UUID | PK |
| user_id | UUID | FK a users.id, IX |
| input | JSONB | |
| result | JSONB | |
| created_at | TIMESTAMPTZ | |
| delivery_deadline | TIMESTAMPTZ, puede ser null | |

- Cada orden de moderación que llega de admin-service queda guardada con su resultado. El `id` lo manda admin, así un reintento devuelve el mismo resultado sin aplicar la sanción dos veces.
- `delivery_deadline` solo se usa en las advertencias por mail: es el plazo para confirmar el envío.

## posts-service

Contenido, interacciones y feed. Las claves foráneas de las tablas hijas borran en cascada si se borra un post.

### posts

| Columna | Tipo | Claves |
|---|---|---|
| id | UUID | PK |
| author_id | UUID | IX, → users |
| content | TEXT | |
| parent_id | UUID, puede ser null | FK a posts.id, IX |
| quoted_post_id | UUID, puede ser null | FK a posts.id |
| like_count | INTEGER | |
| retweet_count | INTEGER | |
| reply_count | INTEGER | |
| quote_count | INTEGER | |
| created_at | TIMESTAMPTZ | |
| deleted_at | TIMESTAMPTZ, puede ser null | |

- `parent_id` apunta al post al que responde; es null si es un post raíz.
- `quoted_post_id` apunta al post citado (E.2 H13). Como el borrado es lógico, la cita conserva el vínculo aunque el original se borre.
- Índices: `(parent_id, created_at, id)` y `(author_id, created_at, id)`.
- Los contadores se guardan y se suman de forma atómica.

### post_media

| Columna | Tipo | Claves |
|---|---|---|
| post_id | UUID | PK, FK a posts.id |
| media_id | UUID | PK, → media |
| position | INTEGER | |
| media_type | VARCHAR(16) | |
| url | VARCHAR(500) | |

- Las imágenes adjuntas a un post, en orden (E.2 H7). El archivo vive en media-service; acá se guarda la referencia ya validada y su URL.
- Índice `(post_id, position)`.

### post_likes

| Columna | Tipo | Claves |
|---|---|---|
| post_id | UUID | PK, FK a posts.id |
| author_id | UUID | PK, IX, → users |
| created_at | TIMESTAMPTZ | |

### post_bookmarks

| Columna | Tipo | Claves |
|---|---|---|
| post_id | UUID | PK, FK a posts.id |
| author_id | UUID | PK, IX, → users |
| created_at | TIMESTAMPTZ | |

- Índice `(author_id, created_at)`: lista los guardados por fecha de guardado.

### retweets

| Columna | Tipo | Claves |
|---|---|---|
| id | UUID | PK |
| user_id | UUID | IX, → users |
| post_id | UUID | FK a posts.id, IX |
| created_at | TIMESTAMPTZ | |

- Único `(user_id, post_id)`: un retweet por persona.
- Índices `(user_id, created_at)` y `(user_id, created_at, id)`, para el feed y el perfil.

### post_hashtags

| Columna | Tipo | Claves |
|---|---|---|
| post_id | UUID | PK, FK a posts.id |
| tag | VARCHAR(280) | PK, IX |
| created_at | TIMESTAMPTZ | |

- El tag se guarda en minúsculas. Índice `(tag, created_at)`.

### deleted_authors

| Columna | Tipo | Claves |
|---|---|---|
| author_id | UUID | PK, → users |
| deleted_at | TIMESTAMPTZ | |

- posts la llena con las bajas que le llegan por la cola. Con ella, las respuestas y los retweets de una cuenta borrada conservan su contenido y muestran como autor "[Usuario eliminado]", sin handle ni foto (CA.5 de E.1 H4, con el criterio del tutor). Entró el 23/11 con la cola (posts #33, migración `0010`).

## social-service

Grafo social. Las denuncias pasan por social pero se guardan en admin-service.

### follows

| Columna | Tipo | Claves |
|---|---|---|
| follower_id | UUID | PK, IX, → users |
| followee_id | UUID | PK, IX, → users |
| status | active o pending | |
| created_at | TIMESTAMPTZ | |

- `pending` es una solicitud a una cuenta protegida.
- Índices `(followee_id, status, created_at)` para los seguidores y `(follower_id, status, created_at)` para los seguidos.

### follow_counters

| Columna | Tipo | Claves |
|---|---|---|
| user_id | UUID | PK, → users |
| followers_count | INTEGER | |
| following_count | INTEGER | |

### blocks

| Columna | Tipo | Claves |
|---|---|---|
| blocker_id | UUID | PK, → users |
| blocked_id | UUID | PK, IX, → users |
| created_at | TIMESTAMPTZ | |

- Quién bloqueó a quién (E.3 H4). Índice `(blocker_id, created_at)` para la lista "Usuarios bloqueados", del más reciente al más viejo.
- Bloquear borra los follows y las solicitudes entre los dos, en los dos sentidos, en la misma transacción. Desbloquear borra la fila y no restaura los follows.
- Para el resto de los servicios, un bloqueo vale en los dos sentidos: posts-service pide los ids con `GET /internal/users/{id}/blocked-ids` (interna: incluye a quienes bloquearon a ese usuario, y eso no se puede mostrar) y oculta esos posts. El perfil (`GET /users/{id}/profile`) da 404 solo a quien fue bloqueado.

## media-service

Metadatos de los archivos. El archivo en sí está en Amazon S3.

### media

| Columna | Tipo | Claves |
|---|---|---|
| id | UUID | PK |
| owner_id | UUID | IX, → users |
| context | VARCHAR(32) | |
| storage_key | VARCHAR(255) | UQ |
| mime_type | VARCHAR(64) | |
| size_bytes | INTEGER | |
| created_at | TIMESTAMPTZ | |

- `context` es el uso del archivo: `post_image`, `avatar` o `cover`. Define el tamaño y los formatos permitidos.
- `storage_key` es la clave del objeto en S3. Se genera con un UUID, nunca con el nombre original del archivo.
- `mime_type` sale del contenido del archivo, no de lo que declara el cliente.

## admin-service

Backoffice. Está escrito en Go y sus migraciones son SQL (goose).

### admins

| Columna | Tipo | Claves |
|---|---|---|
| id | UUID | PK |
| email | TEXT | |
| email_normalized | TEXT | UQ |
| role | superadmin o moderator | CK |
| password_hash | Argon2id | |
| must_change_password | BOOLEAN | |
| temp_password_expires_at | TIMESTAMPTZ, puede ser null | |
| created_by | UUID, puede ser null | FK a admins.id |
| failed_login_attempts | INTEGER | CK |
| locked_until | TIMESTAMPTZ, puede ser null | |
| created_at | TIMESTAMPTZ | |
| updated_at | TIMESTAMPTZ | |

### admin_sessions

| Columna | Tipo | Claves |
|---|---|---|
| id | UUID | PK |
| admin_id | UUID | FK a admins.id |
| expires_at | TIMESTAMPTZ | IX |
| revoked_at | TIMESTAMPTZ, puede ser null | |

- El token del backoffice lleva el id de su sesión. Cerrar la sesión la marca revocada y desde ahí ninguna copia del token vale.

### audit_logs

| Columna | Tipo | Claves |
|---|---|---|
| id | UUID | PK |
| admin_id | UUID, puede ser null | |
| admin_email | TEXT | |
| action | TEXT | |
| entity_type | TEXT | |
| entity_id | TEXT | IX |
| entity_label | TEXT | |
| details | TEXT, puede ser null | |
| created_at | TIMESTAMPTZ | IX |

- Registro de auditoría (E.5 H6). Es de solo lectura: un trigger rechaza UPDATE, DELETE y TRUNCATE.
- `admin_id` no es clave foránea a propósito: el registro tiene que sobrevivir a cualquier cambio en las cuentas.

### user_reports

| Columna | Tipo | Claves |
|---|---|---|
| id | UUID | PK |
| reporter_id | UUID | → users |
| reported_id | UUID | IX, → users |
| reason | spam, acoso, contenido_inapropiado o suplantacion | CK |
| reported_at | TIMESTAMPTZ | |
| status | pendiente, descartada o resuelta | CK |
| closed_by | UUID, puede ser null | |
| closed_at | TIMESTAMPTZ, puede ser null | |
| received_at | TIMESTAMPTZ | |

- Denuncias que llegan de social-service (E.3 H5 y E.5 H7). El `id` es el del evento, así un envío repetido no las duplica.

### user_feedback

| Columna | Tipo | Claves |
|---|---|---|
| id | UUID | PK |
| user_id | UUID | → users |
| handle | TEXT | |
| message | TEXT, de 1 a 500 caracteres | CK |
| platform | ios o android | CK |
| app_version | TEXT | |
| status | nuevo, leido o resuelto | CK, IX |
| submitted_at | TIMESTAMPTZ | |
| received_at | TIMESTAMPTZ | |
| email_attempts | INTEGER | |
| email_next_attempt_at | TIMESTAMPTZ | IX |
| email_sent_at | TIMESTAMPTZ, puede ser null | |

- Feedback que llega de auth-service (E.1 H11 y E.5 H12). El handle se copia para que el mensaje siga identificado si la cuenta se da de baja.
- Las columnas `email_*` son la cola del aviso a soporte.

### service_health y service_alerts

| Tabla | Columnas | Claves |
|---|---|---|
| service_health | name, state (up o down), checked_at, incident | PK name; CK state |
| service_alerts | id, service, incident, admin_id, detected_at, attempts, next_attempt_at, sent_at | PK id; FK admin_id a admins.id; UQ (service, incident, admin_id) |

- Monitor de los servicios (E.5 H11): el último estado de cada servicio y los mails de alerta pendientes por administrador.

### sanction_operations y review_sync

| Tabla | Columnas | Claves |
|---|---|---|
| sanction_operations | id, user_id, actor_id, action, input, result, status, audited, created_at, updated_at | PK id; IX (user_id, created_at); CK action y status |
| review_sync | user_id, version, active, operation_id, pending | PK user_id |

- `sanction_operations` registra cada sanción que admin manda a auth: advertencia, suspensión, bloqueo o desbloqueo. `status` va de `pending` a `applied`, `failed`, `unknown`, `sending` o `simulated`.
- `review_sync` guarda la última versión de "cuenta en revisión" que hay que sincronizar con auth.

### Asistente de IA

Tablas del asistente del backoffice ({doc}`ADR-0015 <adr-0015>`). Las conversaciones vencen y se borran en cascada con sus ejecuciones; la evidencia, las evaluaciones y las propuestas no se pueden modificar, porque las protege un trigger.

| Tabla | Para qué | Columnas principales |
|---|---|---|
| ai_conversations | Conversación de un administrador con el asistente. | id, admin_id (FK a admins), created_at, last_human_message_at, expires_at |
| ai_runs | Cada pedido al agente, con su estado. Un administrador tiene como mucho una ejecución activa. | id, conversation_id y admin_id (FK a ai_conversations), client_message_id, request_hash, status, tool_permissions, result, error, deadline_at |
| ai_messages | El mensaje del administrador y la respuesta de cada ejecución. | id, seq, run_id (FK a ai_runs), role (user o assistant), content |
| ai_run_targets | El usuario que eligió el administrador para la consulta. | run_id (PK, FK a ai_runs), user_id (→ users) |
| ai_evidence | Copia de los posts y antecedentes del usuario que vio el agente. | id, run_id, user_id, kind (posts o history), payload, fetched_at |
| ai_run_trace | Pasos de la ejecución: cada llamada a una herramienta. | run_id, call_id, step, phase, payload, recorded_at |
| ai_evaluations | Evaluación de la evidencia con Bedrock. | id, run_id, user_id, request_hash, model_version, input, context, state, result, completion |
| ai_report_case_versions | Versión del caso de denuncias de cada usuario; un trigger la sube cuando cambia una denuncia. | user_id (PK), version |
| ai_case_snapshots | Qué denuncias había cuando el agente armó la propuesta. | id, run_id, user_id, version, report_ids |
| ai_proposals | Propuesta de sanción del agente. Vence si nadie la confirma. | id, run_id, user_id, request_hash, payload, status (pending, cancelled, expired o confirmed), expires_at |
| ai_sanction_confirmations | Confirmación de un administrador. Sobrevive a la conversación y a la evidencia. | id, actor_id, user_id, proposal_version, proposal, report_ids, confirmed_at, case_closed |

## notifications-service

Tokens de los celulares y la campanita de cada usuario. Desplegado el 23/11 (notifications #1).

### device_tokens y notifications

| Columna | Tipo | Claves |
|---|---|---|
| token | TEXT | PK |
| user_id | UUID | IX, → users |
| platform | VARCHAR(16) | |
| created_at | TIMESTAMPTZ | |
| updated_at | TIMESTAMPTZ | |

- `device_tokens`: el token de Firebase de cada celular. Si otra cuenta inicia sesión en el mismo celular, el token cambia de dueño.

| Columna | Tipo | Claves |
|---|---|---|
| id | UUID | PK |
| user_id | UUID | IX, → users |
| type | follow, like, retweet, reply o quote | CK |
| actor_id | UUID | IX, → users |
| actor_handle | VARCHAR(32) | |
| post_id | UUID, puede ser null | → posts |
| event_key | VARCHAR(128) | UQ |
| created_at | TIMESTAMPTZ | |
| read_at | TIMESTAMPTZ, puede ser null | |
| deleted_at | TIMESTAMPTZ, puede ser null | |

- `notifications`: la campanita de cada usuario. `event_key` es único por hecho, así un evento repetido de la cola no duplica la notificación. Índice `(user_id, created_at, id)` para paginar de a 20.
- `post_id` es null solo en los follows.

## Redis

Es una instancia gestionada y compartida. Cada servicio usa su propio prefijo, y todas las claves vencen solas.

| Clave | Servicio | Para qué | Vence en |
|---|---|---|---|
| `verify:<token>` | auth-service | Link de verificación de email | 24 h |
| `reset:<token>` | auth-service | Link para restablecer la contraseña | 10 min |
| `reset_rate:<email>` | auth-service | Pedidos de reseteo por hora (hasta 3) | 1 h |
| `auth:login-attempts:<id>` | auth-service | Intentos de login fallidos | 15 min |
| `auth:account-lock:user:<id>` | auth-service | Cuenta bloqueada por intentos | 15 min |
| `auth:password-change-attempts:<id>` | auth-service | Intentos de cambio de contraseña | 15 min |
| `auth:account-deletion-attempts:<id>` | auth-service | Intentos de baja con la contraseña equivocada | 15 min |
| `auth:revoked-token:<jti>` | auth-service | Token cerrado con logout | Lo que le quede al token |
| `auth:min-token-version:user:<id>` | auth-service | Versión mínima de token aceptada: corta todas las sesiones de una cuenta | 1 h 5 min |
| `auth:feedback-rate:<id>` | auth-service | Mensajes de feedback por hora (hasta 2) | 1 h |
| `auth:feedback-pending:<id>:<hash>` | auth-service | Feedback con entrega incierta, para no duplicarlo al reintentar | 24 h |
| `gateway:online-users` | api-gateway | Usuarios activos en los últimos 5 minutos, para Métricas | 10 min |
| `posts:rate:<user_id>` | posts-service | Límite de 30 posts por hora | 1 h |
| `posts:trending` | posts-service | Ranking de tendencias ya calculado | 15 min |
| `social:follows:rate:<user_id>` | social-service | Límite de 50 follows por hora | 1 h |
| `social:reports:dedupe:<denunciante>:<denunciado>` | social-service | Una denuncia por par cada 24 horas | 24 h |

- Contrato entre auth y el gateway: el gateway lee en cada pedido `auth:revoked-token`, `auth:min-token-version` y `auth:account-lock`, y auth lee `gateway:online-users` para contar los usuarios en línea. Si cambia el formato de una clave, hay que cambiarlo en los dos servicios.
- `gateway:online-users` es un sorted set: el miembro es el id del usuario y el puntaje, la hora de su último pedido. Cada escritura borra a los que pasaron los 5 minutos.

## Pendiente

Tablas que todavía están en un pull request abierto.

### pending_uploads (media-service, media #13)

| Columna | Tipo | Claves |
|---|---|---|
| id | UUID | PK |
| owner_id | UUID | → users |
| context | VARCHAR(32) | |
| storage_key | VARCHAR(255) | UQ |
| mime_type | VARCHAR(64) | |
| size_bytes | INTEGER | |
| expires_at | TIMESTAMPTZ | IX |
| rejected | BOOLEAN | |
| created_at | TIMESTAMPTZ | |

- Subidas directas a S3 con URL firmada que todavía no se confirmaron (E.2 H15, videos).
