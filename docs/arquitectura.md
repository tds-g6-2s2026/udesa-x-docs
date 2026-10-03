# Arquitectura

Microservicios por responsabilidad, cada uno con su base. La app habla solo con el gateway; los servicios se llaman entre sí por HTTP dentro del cluster.

> Pegar acá el PNG: `images/arquitectura.png` (el diagrama UdeSA-X · Arquitectura).

```{image} images/arquitectura.jpeg
:alt: Diagrama de arquitectura UdeSA-X
:width: 100%
```

## Capas

- **Clientes:** App mobile (React Native + Expo, TanStack Query, Zustand) y Backoffice web (portal de admin-service).
- **Borde AWS:** CloudFront + ALB compartido. Rutas `/api/*` van al gateway.
- **EKS `tds-cluster`, namespace `tds-group-6`:** un Deployment por servicio, 1 réplica, estrategia Recreate, probes en `/health`.
- **Fuera del cluster:** PostgreSQL (una base por servicio), Redis gestionado, Gmail SMTP, S3 (pendiente, hoy disco local), cola de eventos (pendiente).

## Servicios

| Servicio | Puerto | Stack | Base | Rutas |
|---|---|---|---|---|
| api-gateway | 8080 | Python FastAPI | - | `/api/*`, rutea por primera palabra |
| auth-service | 8000 | Python | Postgres + Redis | `/auth` identidad y sesión |
| posts-service | 8001 | Python | Postgres + Redis | `/posts` contenido y feed |
| social-service | 8002 | Python | Postgres + Redis | `/follows`, `/users` grafo social |
| media-service | 8003 | Python | Postgres (pendiente tabla) | `/media`, `/files` archivos |
| admin-service | 8004 | Go + chi | Postgres | `/admin` backoffice |

## Llamadas entre servicios

1. `posts → auth`: datos de los autores, en lote (`POST /auth/users/batch`).
2. `posts → social`: a quién sigue el usuario.
3. `social → auth`: si la cuenta es pública.
4. `gateway → auth`: verifica el token (`GET /auth/introspect`, caché 30s), reenvía `X-User-Id`.

## CI/CD

GitHub → Actions CI (Ruff, tests, cobertura ≥85%) → CD (rol OIDC, build, push a ECR, `kubectl apply`, rollout).
