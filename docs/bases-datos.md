# Bases de datos

Una base PostgreSQL por servicio, más un Redis compartido para datos que vencen. **Entre servicios no hay claves foráneas: se guardan los UUID y cada servicio es dueño de sus datos.**

> Pegar acá el PNG: `images/modelo-datos.png` (el diagrama UdeSA-X · Modelo de datos).

```{image} images/modelo-de-datos.jpeg
:alt: Modelo de datos UdeSA-X
:width: 100%
```

## auth-service (Postgres: identidad y cuenta)

`users(id PK, email, email_normalized UQ, handle UQ, display_name, bio, password_hash Argon2id, is_verified, is_suspended, profile_visibility, token_version, created_at, deleted_at)`

## posts-service (Postgres: contenido y feed)

`posts(id PK, author_id → users sin FK, content, parent_id FK interna, like_count, retweet_count, reply_count, created_at, deleted_at)`, `post_likes(post_id, author_id) PK compuesta`, `post_bookmarks(post_id, author_id) PK compuesta`, `retweets(id, user_id, post_id UQ(user_id, post_id))`, `post_hashtags(post_id, tag) PK compuesta`.

## social-service (Postgres: grafo social)

`follows(follower_id, followee_id PK compuesta, status, created_at)`, `follow_counters(user_id PK, followers_count, following_count)`.

## media-service

Sin tablas por ahora. Guarda en disco local; S3 y tabla de archivos pendientes.

## admin-service Go (Postgres: backoffice)

`admins(id PK, email, email_normalized UQ, role CK superadmin|moderator, password_hash, must_change_password, temp_password_expires_at, created_by FK interna, failed_login_attempts, locked_until, created_at, updated_at)`.

## Redis gestionado (con TTL y prefijo por servicio)

`verify:<token>` 24h, `reset:<token>` 10min, `auth:login-attempts:<id>` 15min, `auth:account-lock:user:<id>` 15min, `auth:revoked-token:<jti>`, `posts:rate:<user_id>` 1h (30 posts/h), `social:follows:rate:<user_id>` 1h (50 follows/h).

Referencias: PK primaria, FK foránea dentro de la misma base, UQ único, IX índice, CK check, `users` guarda el id de auth sin FK.
