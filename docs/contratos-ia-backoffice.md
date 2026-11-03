# Contratos del asistente de backoffice

Esquemas propuestos para el [ADR-0015](adr-0015.md) y [IA-01 / #63](https://github.com/tds-g6-2s2026/udesa-x-project/issues/63). Deben revisarse antes de implementar IA-02 a IA-13. Los nombres de campos son parte de esta propuesta, no APIs ya desplegadas.

El catálogo MCP tiene cinco tools: `get_services_health`, `get_user_posts`, `get_user_history`, `evaluate_with_jev` y `propose_sanction`. La confirmación y ejecución se realizan directamente por la API de admin, sin tool `execute_sanction` ni dependencia de una ejecución activa del chat.

## Convenciones comunes

- `uuid`: identificador UUID; `datetime`: RFC 3339 en UTC; `cursor`: string opaco o `null`.
- Los campos indicados son obligatorios salvo que se marque `?`. `null` expresa ausencia conocida y no equivale a una lista vacía ni a cero.
- Los objetos de entrada rechazan campos desconocidos. Strings, páginas, pasos, tokens y tiempos tienen máximos configurados por backend y documentados antes de implementar; el llamador no puede ampliarlos.
- Cada llamada tiene contexto autenticado de administrador, conversación, ejecución, permisos y expiración. Ese contexto llega por el canal confiable, separado de los argumentos de la tool.
- Las credenciales de agente/MCP no autorizan confirmaciones ni escrituras de estado de cuenta o caso. Auth exige identidad exclusiva de admin en sus rutas sensibles; la recepción de denuncias admite solo al productor social autorizado. Estas comprobaciones incluyen las rutas heredadas y son condición previa para incorporar los nuevos servicios con acceso a APIs internas.
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

**Entrada:** `{}`. Los destinos son los seis `/healthcheck` configurados en backend, reutilizando el monitor actual; el llamador no entrega URLs.

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

**Origen:** API de antecedentes de admin, reutilizando auditoría, registros de sanciones y el módulo `reports` existente; estado de revisión desde auth.

**Entrada:** `{ user_id: uuid, cursor?: cursor, limit?: integer }`.

**Salida:** `{ user_id: uuid, evidence_id: uuid, fetched_at: datetime, availability: string, items: HistoryEntry[], next_cursor: cursor, account_state: object, reports: object, coverage: object }`.

| HistoryEntry | Tipo y significado |
|---|---|
| `record_id` | UUID de un registro verificable. |
| `type` | `warning`, `suspension`, `block`, `unblock`, `review_started`, `review_ended`, `reports_resolved` o `reports_dismissed`. |
| `reason` | Motivo registrado. |
| `occurred_at` | `datetime` de la acción. |
| `expires_at` | `datetime` o `null`; aplica cuando el registro tiene vencimiento. |

`availability` es `available`, `partial` o `unavailable`. `coverage` declara `from: datetime|null`, `to: datetime`, `has_more: boolean` y `limitations: string[]`. Un resultado completo sin antecedentes devuelve `available` con `items: []`; una fuente no disponible lo declara explícitamente. El backend no convierte un fallo en un historial limpio.

`account_state` contiene `availability: string`, `status: string|null`, `under_review: boolean|null` y `checked_at: datetime|null`. Un estado de revisión es una restricción preventiva y no demuestra una infracción. Fuente inaccesible implica valores desconocidos, no `under_review: false`.

`reports` contiene `availability: string`, `items: ReportEvidence[]`, `next_cursor: cursor`, `pending_count: integer|null`, `case_snapshot_id: uuid|null` y `case_version: integer|null`. Cada `ReportEvidence` contiene `report_id: uuid`, `reason: string`, `status: "pendiente"|"resuelta"|"descartada"`, `reported_at: datetime` y `closed_at: datetime|null`. La cobertura registra también si hay más páginas; una lista truncada no representa todo el caso. No se envía a los modelos la identidad de denunciantes cuando no es necesaria para evaluar.

El snapshot identifica el conjunto exacto y versionado de denuncias contempladas. Como hoy el módulo agrupa casos por usuario y no tiene ID de caso propio, esta es una extensión del contrato de lectura de admin. Una página incompleta no habilita resolver todo un caso: el backend debe obtener y registrar su alcance completo antes de emitir el snapshot resoluble, o devolver snapshot `null`. La API de confirmación vuelve a validar sus IDs y versión; no confía en el resumen que genere el agente.

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

**Entrada:** `{ user_id: uuid, sanction_type: string, duration_seconds: integer|null, reason: string, evidence_ids: uuid[], evaluation_id: uuid|null, case_snapshot_id: uuid|null, case_version: integer|null, case_disposition: "keep_open"|"resolve" }`.

`sanction_type` es `warning`, `suspension` o `block`. Una suspensión requiere duración positiva dentro del rango configurado; advertencia y bloqueo usan `null`. Una solicitud humana directa puede no tener evaluación de Jev, pero debe cumplir la política de evidencia y las reglas determinísticas de admin. Falta de evidencia suficiente no habilita la ejecución de una sanción.

**Salida:** `{ proposal_id: uuid, version: integer, user_id: uuid, user_label: string, sanction_type: string, duration_seconds: integer|null, reason: string, evidence_ids: uuid[], evaluation_id: uuid|null, policy_version: string, case_snapshot_id: uuid|null, case_version: integer|null, case_disposition: "keep_open"|"resolve", status: "pending", expires_at: datetime }`.

El backend agrega autor y conversación desde el contexto autenticado y guarda la propuesta canónica. Los datos sensibles quedan inmutables. Cambiarlos crea otra propuesta y requiere una confirmación nueva. Esta tool solo registra la propuesta: no altera el acceso del usuario.

Un snapshot debe pertenecer al mismo usuario y su alcance se muestra en el modal. `resolve` exige snapshot y versión válidos; sin snapshot solo se admite `keep_open`. El modelo puede proponer una disposición, pero únicamente la selección explícita y confirmación humana del modal la autoriza. Si hay un caso pendiente y la sanción es independiente, el portal informa que el caso seguirá abierto. Cambiar la disposición o el snapshot requiere otra versión de propuesta y otra confirmación.

## Confirmación y ejecución administrativa (fuera de MCP)

**Recorrido:** portal -> gateway -> API de admin -> servicio de dominio de admin -> auth cuando corresponde. Agente, MCP, Bedrock y Jev no participan en este recorrido y no reciben sus credenciales.

**Entrada de confirmación:** `{ proposal_id: uuid, version: integer, case_disposition: "keep_open"|"resolve" }`, con cookie administrativa vigente y CSRF. La disposición debe coincidir con la propuesta canónica, no modifica su alcance; un cambio requiere nueva propuesta. No se exige `run_id` activo.

Admin verifica sesión y rol actuales, pertenencia, propuesta/versión, expiración, estado de cuenta, evidencia y snapshot del caso. Registra aprobación, confirmante, acción canónica e identificador de operación con exclusión de concurrencia y ejecuta mediante su propia lógica. La autorización permanece en backend; no se emite al agente/MCP. Un snapshot desactualizado produce `state_conflict` antes de sancionar y exige nueva revisión y confirmación.

**Salida:** `{ proposal_id: uuid, operation_id: uuid, user_id: uuid, status: string, sanction_status: string, case_status: string, audit_status: string, executed_at: datetime|null, audit_reference: uuid }`.

`status` es `executing`, `succeeded`, `partial`, `failed` o `unknown`. `sanction_status` es `pending`, `applied`, `failed` o `unknown`; `case_status` es `kept_open`, `pending`, `resolved`, `conflict` o `unknown`; `audit_status` es `pending` o `recorded`. `audit_reference` identifica el registro durable del intento. Una sanción aplicada con cierre de caso o auditoría todavía pendiente se informa como `partial`, sin afirmar un éxito completo. Si no se puede persistir la intención, no se inicia el efecto.

El portal consulta el desenlace por `operation_id` mediante admin y puede reintentar explícitamente la misma operación con sesión válida. No vuelve a pedir una decisión al modelo ni exige que agente/MCP estén disponibles. El estado `executing` puede responder `202`; las consultas de estado no aplican efectos ni lanzan IA. No se reciben nuevos valores de usuario, acción, motivo, duración o snapshot al reintentar.

La autorización habilita una única operación idempotente. Reenviar la misma operación devuelve su resultado registrado o indica que está pendiente de resolución. Una confirmación inicial de una propuesta cancelada, expirada o no aprobada se rechaza. Una operación ya aprobada y comenzada conserva su identificador para consultar/reconciliar su desenlace aunque después venza la propuesta; eso no autoriza una sanción nueva ni permite modificarla. Ante timeout con desenlace incierto se consulta primero el resultado del servicio que aplica el efecto.

Después de comprobar el efecto en auth, si se confirmó `resolve`, admin resuelve únicamente los `report_id` del snapshot confirmado y audita en su transacción local. Con `keep_open` conserva las denuncias pendientes y registra esa decisión. Denuncias nuevas o ajenas al alcance confirmado no se resuelven. Ante carrera posterior a la confirmación se mantiene su estado y se reconcilia la restricción de revisión que corresponda. El flujo reutiliza las reglas del módulo `reports`, extendiendo sus escrituras actuales por usuario para admitir el conjunto versionado.

Resolver no levanta bloqueos ni suspensiones. Una advertencia no libera revisión por sí sola. El bloqueo actual limpia la revisión en auth, por lo que la implementación debe preservar/recalcular restricciones de casos pendientes al desbloquear o vencer suspensiones. Estas reglas se verifican junto con los fallos entre auth y la transacción de cierre/auditoría.

## Contrato HTTP con el portal

Las rutas concretas se fijan al implementar IA-03, IA-09 e IA-10. El comportamiento acordado es:

| Operación | Contrato |
|---|---|
| Enviar mensaje | Cookie administrativa vigente y CSRF; respuesta rápida `202` con `{ run_id: uuid, status: "pending" }`. |
| Consultar ejecución | Acceso autorizado a la conversación; `{ run_id: uuid, status: string, result: object|null, error: object|null }`. |
| Consultar propuesta | Devuelve versión, contenido canónico y alcance/disposición de denuncias para renderizar el modal. |
| Confirmar propuesta | Sesión y rol vigentes, CSRF, `proposal_id`, `version` y disposición coincidente; admin registra y ejecuta directamente la operación exacta. |
| Consultar operación de sanción | Consulta de lectura por `operation_id`, con acceso autorizado; devuelve estados de sanción, caso y auditoría sin llamar a IA. |
| Reintentar operación de sanción | Petición humana autenticada con CSRF; consulta el efecto y completa solo pasos pendientes de la operación idempotente. |
| Cancelar propuesta | Sesión autorizada y CSRF; pasa a `cancelled` sin modificar la cuenta. |

Estados de ejecución: `pending`, `running`, `completed`, `failed`, `interrupted`. El resultado completado contiene `message: string`, `evidence_ids: uuid[]` y `proposal_ids: uuid[]`. El frontend renderiza el contenido de forma segura, conserva referencias verificables y no inicia inferencia al consultar progreso.

Estados de propuesta: `pending`, `approved`, `executing`, `succeeded`, `partial`, `failed`, `unknown`, `cancelled`, `expired`. Las transiciones se validan en backend. Los estados `executing`, `partial` y `unknown` exigen consulta de la misma operación antes de volver a intentar el efecto; no vuelven a `pending` automáticamente.

## Validaciones obligatorias de esta revisión

- Auth rechaza llamadas sensibles anónimas y credenciales de agente/MCP; admite admin autorizado. Las rutas heredadas y las escrituras indirectas por recepción de denuncias no permiten eludir esa frontera.
- Con agente/MCP detenidos, una propuesta persistida y vigente puede confirmarse y ejecutarse desde admin; el polling del chat no participa.
- Un caso cambiado antes de confirmar se rechaza; dos confirmaciones concurrentes no duplican la sanción. Una denuncia recibida después no se cierra con el snapshot anterior.
- Si auth aplica la sanción y falla la resolución o auditoría, la operación informa resultado parcial y el reintento completa solo lo pendiente, sin sancionar otra vez ni liberar restricciones ajenas.
