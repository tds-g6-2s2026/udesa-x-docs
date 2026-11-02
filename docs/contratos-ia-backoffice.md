# Contratos del asistente de backoffice

Esquemas propuestos para el [ADR-0015](adr-0015.md) y [IA-01 / #63](https://github.com/tds-g6-2s2026/udesa-x-project/issues/63). Deben revisarse antes de implementar IA-02 a IA-13. Los nombres de campos son parte de esta propuesta, no APIs ya desplegadas.

## Convenciones comunes

- `uuid`: identificador UUID; `datetime`: RFC 3339 en UTC; `cursor`: string opaco o `null`.
- Los campos indicados son obligatorios salvo que se marque `?`. `null` expresa ausencia conocida y no equivale a una lista vacía ni a cero.
- Los objetos de entrada rechazan campos desconocidos. Strings, páginas, pasos, tokens y tiempos tienen máximos configurados por backend y documentados antes de implementar; el llamador no puede ampliarlos.
- Cada llamada tiene contexto autenticado de administrador, conversación, ejecución, permisos y expiración. Ese contexto llega por el canal confiable, separado de los argumentos de la tool.
- Los resultados se validan contra el esquema antes de entregarlos al LLM. El backend valida correspondencia entre UUID, evidencia y ejecución.
- El envelope MCP y los errores de transporte siguen el SDK/transporte que se seleccione. Los objetos siguientes son el contenido estructurado de aplicación.

### Errores de aplicación

```json
{
  "code": "upstream_unavailable",
  "message": "No se pudo consultar el historial del usuario.",
  "retryable": true,
  "correlation_id": "00000000-0000-4000-8000-000000000001"
}
```

`code` usa un catálogo acotado: `invalid_input`, `unauthenticated`, `forbidden`, `not_found`, `ambiguous_user`, `upstream_unavailable`, `timeout`, `rate_limited`, `invalid_upstream_response`, `insufficient_evidence`, `proposal_expired`, `proposal_cancelled`, `state_conflict` y `execution_unknown`. `message` no expone URLs internas, credenciales ni detalles de transporte. `retryable` nunca autoriza repetir una sanción sin consultar primero su operación idempotente.

La búsqueda por handle se resuelve con la API de usuarios existente antes de usar las tools de moderación. Una cuenta ambigua requiere selección humana y luego se trabaja con su UUID; el modelo no elige un UUID por semejanza textual.

## get_services_health

**Origen:** API interna bajo demanda de admin, reutilizando su módulo de sondeo.

**Entrada:** `{}`. Los destinos son los seis servicios configurados en backend; el llamador no entrega URLs.

**Salida:** `{ checked_at: datetime, services: ServiceHealth[] }`.

| ServiceHealth | Tipo y significado |
|---|---|
| `service` | `auth-service`, `posts-service`, `social-service`, `media-service`, `admin-service` o `api-gateway`. |
| `state` | `up`, `unavailable` o `unknown`. |
| `http_status` | Entero HTTP o `null` si no se recibió respuesta. |
| `latency_ms` | Entero mayor o igual a cero; duración observada del intento. |
| `checked_at` | `datetime` de la observación por servicio. |
| `reason` | `null`, `timeout`, `unreachable`, `http_error` o `invalid_response`. |

Se devuelve un resultado por cada destino, incluso si algunos fallan. Un fallo total de la API interna es un error de aplicación. La observación no se transforma en diagnóstico de causa ni en disponibilidad histórica.

## get_user_posts

**Origen:** endpoint administrativo interno de posts, pendiente de implementar; la evidencia se registra mediante API de admin.

**Entrada:** `{ user_id: uuid, cursor?: cursor, limit?: integer }`. `limit` debe ser positivo y no superar el máximo del backend.

**Salida:** `{ user_id: uuid, evidence_id: uuid, fetched_at: datetime, items: PostEvidence[], next_cursor: cursor, coverage: object }`.

| PostEvidence | Tipo y significado |
|---|---|
| `post_id` | UUID verificable en posts. |
| `author_id` | UUID; debe coincidir con `user_id`. |
| `text` | Texto obtenido del servicio, con longitud acotada. |
| `created_at` | `datetime` de creación. |

`coverage` declara `returned_count: integer`, `has_more: boolean` y `visibility_policy_version: string`. El backend registra además los filtros aplicados y cualquier omisión/truncamiento. Una página no acredita haber revisado todas las publicaciones del usuario. La inclusión de posts protegidos o eliminados depende de la política administrativa pendiente de IA-01.

`evidence_id` identifica el snapshot persistido de esa página, asociado al usuario y a la ejecución. El agente referencia ese ID en evaluaciones posteriores.

## get_user_history

**Origen:** API de antecedentes de admin, reutilizando auditoría y registros de sanciones.

**Entrada:** `{ user_id: uuid, cursor?: cursor, limit?: integer }`.

**Salida:** `{ user_id: uuid, evidence_id: uuid, fetched_at: datetime, availability: string, items: HistoryEntry[], next_cursor: cursor, coverage: object }`.

| HistoryEntry | Tipo y significado |
|---|---|
| `record_id` | UUID de un registro verificable. |
| `type` | `warning`, `suspension`, `block` o `unblock`. |
| `reason` | Motivo registrado. |
| `occurred_at` | `datetime` de la acción. |
| `expires_at` | `datetime` o `null`; aplica cuando el registro tiene vencimiento. |

`availability` es `available`, `partial` o `unavailable`. `coverage` declara `from: datetime|null`, `to: datetime`, `has_more: boolean` y `limitations: string[]`. Un resultado completo sin antecedentes devuelve `available` con `items: []`; una fuente no disponible lo declara explícitamente. El backend no convierte un fallo en un historial limpio.

Los antecedentes son evidencia histórica. La autorización de una sanción vuelve a consultar el estado actual de la cuenta y sus restricciones; no se deduce ese estado únicamente de esta lista.

## evaluate_with_jev

**Origen:** adaptador HTTPS a TypeSafe Jev. Se registra la evaluación mediante API de admin.

**Entrada:** `{ user_id: uuid, post_evidence_ids: uuid[], history_evidence_id: uuid|null, policy_version: string }`.

El backend carga snapshots existentes, comprueba usuario, permisos y ejecución, aplica la política vigente permitida y limita el contexto enviado. Las instrucciones de la política y los umbrales se gestionan en backend; no se reciben como texto libre elegido por el modelo.

**Salida:** `{ evaluation_id: uuid, user_id: uuid, model_version: string, policy_version: string, evaluated_at: datetime, evidence_ids: uuid[], outcome: string, findings: Finding[], limitations: string[] }`.

| Finding | Tipo y significado |
|---|---|
| `category` | Identificador de categoría de la política versionada. |
| `post_ids` | UUIDs de posts presentes en los snapshots evaluados. |
| `score` | Número entre 0 y 1, o `null` si el contrato real no lo entrega. |
| `confidence` | Número entre 0 y 1, o `null` si no está disponible. |

`outcome` es `no_violation_detected`, `review_required` o `violation_detected`. Describe la evaluación y no autoriza una sanción. El adaptador normaliza la respuesta real de Jev tras la prueba de IA-01, sin inventar campos ni puntuaciones que el proveedor no entregue. Las categorías y umbrales necesitan evaluación con contenido en español. El texto explicativo del agente cita los hallazgos y posts verificables.

## propose_sanction

**Origen y persistencia:** admin-service.

**Entrada:** `{ user_id: uuid, sanction_type: string, duration_seconds: integer|null, reason: string, evidence_ids: uuid[], evaluation_id: uuid|null }`.

`sanction_type` es `warning`, `suspension` o `block`. Una suspensión requiere duración positiva dentro del rango configurado; advertencia y bloqueo usan `null`. Una solicitud humana directa puede no tener evaluación de Jev, pero debe cumplir la política de evidencia y las reglas determinísticas de admin. Falta de evidencia suficiente no habilita la ejecución de una sanción.

**Salida:** `{ proposal_id: uuid, version: integer, user_id: uuid, user_label: string, sanction_type: string, duration_seconds: integer|null, reason: string, evidence_ids: uuid[], evaluation_id: uuid|null, policy_version: string, status: "pending", expires_at: datetime }`.

El backend agrega autor y conversación desde el contexto autenticado y guarda la propuesta canónica. Los datos sensibles quedan inmutables. Cambiarlos crea otra propuesta y requiere una confirmación nueva. Esta tool solo registra la propuesta: no altera el acceso del usuario.

## execute_sanction

**Origen:** flujo confiable de backend -> MCP -> API de sanciones de admin -> auth cuando corresponde.

**Entrada del contenido de aplicación:** `{ proposal_id: uuid, version: integer }`.

La autorización de confirmación se transporta aparte, emitida por admin tras la petición autenticada del modal, vinculada a propuesta/versión, confirmante, acción canónica, operación y vencimiento. Nunca es un argumento que pueda inventar o modificar el LLM. El ciclo libre del modelo no tiene permiso para aprobar ni ejecutar por sí mismo.

**Salida:** `{ proposal_id: uuid, operation_id: uuid, user_id: uuid, status: string, executed_at: datetime|null, audit_reference: uuid }`.

`status` es `succeeded`, `failed` o `unknown`. `audit_reference` identifica el registro durable del intento; un estado desconocido mantiene el seguimiento de la operación sin afirmar que el efecto ocurrió. Admin define cómo consultar su desenlace por `operation_id`. La herramienta no acepta otros valores de usuario, acción, motivo o duración.

La autorización habilita una única operación idempotente. Reenviar la misma operación devuelve su resultado registrado o indica que está pendiente de resolución. Una propuesta cancelada, expirada o no aprobada se rechaza. Ante timeout con desenlace incierto se consulta primero el resultado del servicio que aplica el efecto.

## Contrato HTTP con el portal

Las rutas concretas se fijan al implementar IA-03, IA-09 e IA-10. El comportamiento acordado es:

| Operación | Contrato |
|---|---|
| Enviar mensaje | Cookie administrativa vigente y CSRF; respuesta rápida `202` con `{ run_id: uuid, status: "pending" }`. |
| Consultar ejecución | Acceso autorizado a la conversación; `{ run_id: uuid, status: string, result: object|null, error: object|null }`. |
| Consultar propuesta | Devuelve su versión y contenido canónico para renderizar el modal. |
| Confirmar propuesta | Sesión y rol vigentes, CSRF, `proposal_id` y `version`; crea la autorización de una operación exacta. |
| Cancelar propuesta | Sesión autorizada y CSRF; pasa a `cancelled` sin modificar la cuenta. |

Estados de ejecución: `pending`, `running`, `completed`, `failed`, `interrupted`. El resultado completado contiene `message: string`, `evidence_ids: uuid[]` y `proposal_ids: uuid[]`. El frontend renderiza el contenido de forma segura, conserva referencias verificables y no inicia inferencia al consultar progreso.

Estados de propuesta: `pending`, `approved`, `executing`, `succeeded`, `failed`, `unknown`, `cancelled`, `expired`. Las transiciones se validan en backend. Los estados `executing` y `unknown` exigen consulta de la misma operación antes de volver a intentar el efecto; no vuelven a `pending` automáticamente.
