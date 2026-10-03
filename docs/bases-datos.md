# Bases de datos

```{image} images/modelo-datos.png
:alt: Modelo de datos de UdeSA-X
:width: 100%
```

Cada servicio tiene su propia base PostgreSQL, y hay un Redis compartido para los datos que vencen.

**Entre servicios no hay claves foráneas: solo se guardan los UUID. Cada servicio es dueño de su base, y para leer datos de otro servicio usa su API.**

Referencias de la columna Claves:

- **PK:** clave primaria.
- **FK:** clave foránea dentro de la misma base.
- **UQ:** valor único.
- **IX:** índice.
- **CK:** restricción CHECK.
- **→ users:** guarda el id de un usuario de auth, sin clave foránea.

## auth-service

Identidad y cuenta.

### users

| Columna | Tipo | Claves |
|---|---|---|
| id | UUID | PK |
| email | VARCHAR(255) | |
| email_normalized | VARCHAR(255) | UQ |
| handle | VARCHAR(16) | UQ |
| display_name | VARCHAR(50) | |
| bio | VARCHAR(160), puede ser null | |
| password_hash | Argon2id | |
| is_verified | BOOLEAN | |
| is_suspended | BOOLEAN | |
| profile_visibility | public o protected | |
| feed_language | VARCHAR(8) | |
| accepted_terms | BOOLEAN | |
| accepted_terms_at | TIMESTAMPTZ, puede ser null | |
| token_version | INTEGER | |
| created_at | TIMESTAMPTZ | |
| deleted_at | TIMESTAMPTZ, puede ser null | |

- `email_normalized` guarda el email en minúsculas y es único, así no puede haber dos cuentas con el mismo email escrito con distintas mayúsculas.
- `deleted_at` marca la baja lógica de la cuenta.
- `token_version` permite invalidar todos los tokens de un usuario.

## posts-service

Contenido, interacciones y feed. Las claves foráneas internas borran en cascada las filas hijas si se borra un post.

### posts

| Columna | Tipo | Claves |
|---|---|---|
| id | UUID | PK |
| author_id | UUID | IX, → users |
| content | TEXT | |
| parent_id | UUID, puede ser null | FK a posts.id |
| like_count | INTEGER | |
| retweet_count | INTEGER | |
| reply_count | INTEGER | |
| created_at | TIMESTAMPTZ | |
| deleted_at | TIMESTAMPTZ, puede ser null | |

- `parent_id` apunta al post al que responde; es null si es un post raíz.
- Índices: `(parent_id, created_at, id)` y `(author_id, created_at, id)`.
- Los contadores se guardan y se suman de forma atómica.

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
| author_id | UUID | PK, → users |
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

### post_hashtags

| Columna | Tipo | Claves |
|---|---|---|
| post_id | UUID | PK, FK a posts.id |
| tag | VARCHAR(280) | PK |
| created_at | TIMESTAMPTZ | |

- El tag se guarda en minúsculas. Índice `(tag, created_at)`.

## social-service

Grafo social.

### follows

| Columna | Tipo | Claves |
|---|---|---|
| follower_id | UUID | PK, → users |
| followee_id | UUID | PK, IX, → users |
| status | active o pending | IX |
| created_at | TIMESTAMPTZ | |

- `pending` es una solicitud a una cuenta protegida.

### follow_counters

| Columna | Tipo | Claves |
|---|---|---|
| user_id | UUID | PK, → users |
| followers_count | INTEGER | |
| following_count | INTEGER | |

## admin-service

Administradores del backoffice. Está escrito en Go.

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

## media-service

Sin tablas por ahora. Guarda los archivos en disco; el almacenamiento en S3 y la tabla de archivos están pendientes.

## Redis

Es una instancia gestionada y compartida. Cada servicio usa su propio prefijo, y todas las claves vencen solas.

| Clave | Servicio | Para qué | Vence en |
|---|---|---|---|
| `verify:<token>` | auth-service | Link de verificación de email | 24 h |
| `reset:<token>` | auth-service | Link para restablecer la contraseña | 10 min |
| `reset_rate:<id>` | auth-service | Pedidos de reseteo por hora | 1 h |
| `auth:login-attempts:<id>` | auth-service | Intentos de login fallidos | 15 min |
| `auth:account-lock:user:<id>` | auth-service | Cuenta bloqueada por intentos | 15 min |
| `auth:password-change-attempts:<id>` | auth-service | Intentos de cambio de contraseña | 15 min |
| `auth:revoked-token:<jti>` | auth-service | Token cerrado con logout | Lo que le quede al token |
| `posts:rate:<user_id>` | posts-service | Límite de 30 posts por hora | 1 h |
| `social:follows:rate:<user_id>` | social-service | Límite de 50 follows por hora | 1 h |
