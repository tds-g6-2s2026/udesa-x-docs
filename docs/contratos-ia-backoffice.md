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

MCP ejecuta la evaluación mediante Bedrock Converse. Admin prepara y guarda la evaluación por API. El nombre histórico `evaluate_with_jev` se conserva por compatibilidad, según la decisión de IA-06 del 16 de noviembre de 2026.

**Entrada:** `{ user_id: uuid, post_evidence_ids: uuid[], history_evidence_id: uuid|null, policy_version: string }`.

El backend carga snapshots existentes, comprueba usuario, permisos y ejecución, aplica la política vigente permitida y limita el contexto enviado. Las instrucciones de la política y los umbrales se gestionan en backend; no se reciben como texto libre elegido por el modelo.

**Salida:** `{ evaluation_id: uuid, user_id: uuid, model_version: string, policy_version: string, evaluated_at: datetime, evidence_ids: uuid[], outcome: string, findings: Finding[], limitations: string[] }`.

| Finding | Tipo y significado |
|---|---|
| `category` | Identificador de categoría de la política versionada. |
| `post_ids` | UUIDs de posts presentes en los snapshots evaluados. |
| `score` | Número entre 0 y 1, o `null` si el contrato real no lo entrega. |
| `confidence` | Número entre 0 y 1, o `null` si no está disponible. |

`outcome` admite `no_violation_detected`, `review_required` o `violation_detected`. Es un resultado consultivo que conserva referencias verificadas. `score` y `confidence` se guardan en `null` porque la salida elegida es categórica. La política actual `moderation-es-v2` define `spam`, `acoso`, `contenido_inapropiado` y `suplantacion`. La ejecución real inicial del corpus ficticio en español produjo doce respuestas válidas y nueve coincidencias con las expectativas, con tres desacuerdos registrados para revisión. La clasificación y los desacuerdos requieren revisión humana.

### Preparación, inferencia y persistencia de IA-06

| Llamada | Parámetros y autorización |
|---|---|
| MCP → `POST /internal/ai/runs/{id}/evaluations/prepare` en Admin | Entrada de la tool y `allow_inference` opcional, con valor predeterminado `true` por compatibilidad. JWT `aud=admin-service`, `sub=udesa-mcp`, scope `evaluations:prepare`, ligado a administrador, conversación y ejecución. |
| MCP → Bedrock `Converse` | Política versionada, lista de `{post_id,text}` y JSON Schema. Credenciales temporales AWS del servicio MCP, región y application inference profile configurados. |
| MCP → `POST /internal/ai/runs/{id}/evaluations/complete` en Admin | `evaluation_id`, perfil en `model_version`, decisiones, marca de contexto incompleto, error tipado, tokens disponibles, duración e intentos. JWT con `evaluations:complete`. |
| Navegador → `GET /admin/ai/evaluations/{id}` | Sesión administrativa del propietario. Resultado y metadatos persistidos. El gateway agrega el prefijo `/api`. |
| Navegador → `GET /admin/ai/runs/{id}/evaluations` | Misma autorización. Lista acotada por ejecución. El polling conserva la expiración de sesión existente. |

Admin exige una ejecución activa y selección humana del usuario, autorización de la tool persistida y snapshots del mismo usuario y ejecución. Admite hasta veinte snapshots de publicaciones y un snapshot opcional de antecedentes como procedencia. El contexto externo incluye hasta veinte posts únicos, mil caracteres por post y doce mil caracteres totales. El historial y los datos administrativos quedan guardados en Admin. Texto vacío, versiones de un mismo post con contenido diferente o recortes se marcan como contexto incompleto. Una muestra sin texto disponible produce `insufficient_evidence`.

El modelo devuelve `{decisions:[{post_id,verdict,categories}],context_incomplete}`. `verdict` admite `clear`, `violation` o `uncertain`. Admin comprueba cobertura exacta, UUIDs únicos y categorías conocidas. `clear` requiere categorías vacías y `violation` requiere al menos una. `uncertain`, suplantación, contexto incompleto y errores del proveedor producen `review_required`. Solo las categorías con `violation` generan hallazgos. Una respuesta inválida se registra como fallo del evaluador y deriva a revisión humana.

Las reglas que deciden revisión humana se guardan en `policy.review` con los campos `context_incomplete`, `uncertain`, `categories` y `provider_error_outcome`. `moderation-es-v2` exige estas reglas explícitas. La versión v1 conserva sus reglas históricas para solicitudes y contextos existentes. El backend usa la política guardada al calcular el resultado.

Los textos de posts son datos no confiables. Las instrucciones incrustadas pueden causar falsos negativos con un esquema válido. La validación verifica referencias y estructura, mientras el administrador revisa la interpretación y conserva la decisión. Las credenciales de sanción son exclusivas de Admin y Auth. Agente, MCP y Bedrock tienen funciones consultivas y permisos de evaluación acotados.

Admin persiste la entrada canónica, el contexto, el perfil, deadlines y el resultado inmutable mediante la migración Goose 15. El mismo conjunto de referencias y política dentro de una ejecución produce una única evaluación. Una repetición devuelve el resultado guardado o el estado en curso. Cada ejecución admite dos evaluaciones. MCP reserva capacidad antes de la preparación. Si está saturado, consulta con `allow_inference=false`. Admin devuelve un resultado existente o el estado en curso, y responde `rate_limited` para una entrada nueva sin crear una fila ni consumir presupuesto. Una finalización idéntica devuelve el resultado existente y una finalización diferente produce `409`. El borrado por retención de la conversación elimina estas evaluaciones junto con sus ejecuciones.

El deadline de evaluación es veinte segundos, acotado por el deadline de la ejecución. MCP reserva tres segundos para el callback y limita la espera de inferencia a quince segundos, la salida a 2048 tokens y la concurrencia a dos llamadas por instancia por defecto. El SDK realiza un intento y permite un segundo solo ante `ThrottlingException`. Los timeouts conservan revisión humana. Las tareas SDK que continúan tras el timeout mantienen ocupado su cupo hasta terminar. Admin recupera deadlines vencidos al mantener o consultar las ejecuciones. Una fila con entrada o contexto corrupto se completa con revisión humana y `invalid_upstream_response`, conservando el mantenimiento y las consultas de las demás filas. El agente dispone de hasta treinta segundos para esta tool.

`model_version` identifica el application inference profile configurado. La trazabilidad adicional conserva versión de política, decisiones validadas, error, uso de tokens disponible e intentos. Cero intentos representa ausencia de una invocación confirmada, por ejemplo al vencer la espera mientras el thread del SDK sigue en curso. La medición de calidad se realiza con el corpus y comando de `udesa-mcp/devtools/evaluate_spanish.py`. Los reportes de ese comando deben acompañar la revisión de la política y del perfil. La opción `--batch-20` ejecuta veinte posts en una llamada y registra tokens, duración, decisiones y validez del contrato. Existe una prueba SDK con respuestas ficticias para ese tamaño. El smoke real de veinte sigue pendiente porque la sesión AWS local venció. Debe ejecutarse y revisarse antes de habilitar la flag, junto con los tres desacuerdos del corpus inicial v1.

## propose_sanction

**Origen y persistencia:** admin-service.

**Entrada:** `{ user_id: uuid, sanction_type: string, duration_seconds: integer|null, reason: string, evidence_ids: uuid[], evaluation_id: uuid|null, case_snapshot_id: uuid|null, case_version: integer|null, case_disposition: "keep_open"|"resolve" }`.

`sanction_type` es `warning`, `suspension` o `block`. Una suspensión requiere duración positiva dentro del rango configurado y las otras acciones usan `null`. Una solicitud humana directa puede tener `evaluation_id=null` y debe cumplir la política de evidencia y las reglas determinísticas de Admin.

**Salida:** `{ proposal_id: uuid, version: integer, user_id: uuid, user_label: string, sanction_type: string, duration_seconds: integer|null, reason: string, evidence_ids: uuid[], evaluation_id: uuid|null, policy_version: string, proposal_policy_version: string, case_snapshot_id: uuid|null, case_version: integer|null, case_disposition: "keep_open"|"resolve", status: "pending"|"cancelled"|"expired", expires_at: datetime }`.

El backend agrega autor y conversación desde el contexto autenticado y guarda la propuesta canónica. Los datos sensibles quedan inmutables. Cambiarlos crea otra propuesta y requiere una confirmación nueva. Esta tool solo registra la propuesta: no altera el acceso del usuario.

Un snapshot debe pertenecer al mismo usuario y su alcance se muestra en el modal. `resolve` exige snapshot y versión válidos; sin snapshot solo se admite `keep_open`. El modelo puede proponer una disposición, pero únicamente la selección explícita y confirmación humana del modal la autoriza. Si hay un caso pendiente y la sanción es independiente, el portal informa que el caso seguirá abierto. Cambiar la disposición o el snapshot requiere otra versión de propuesta y otra confirmación.

## Confirmación y ejecución administrativa (fuera de MCP)

El recorrido de ejecución es portal → gateway → API de Admin → servicio de dominio de Admin → Auth cuando corresponde. Admin conserva las credenciales de ejecución y la autorización humana.

**Entrada de confirmación:** `{ proposal_id: uuid, version: integer, case_disposition: "keep_open"|"resolve" }`, con cookie administrativa vigente y CSRF. La disposición debe coincidir con la propuesta canónica, no modifica su alcance; un cambio requiere nueva propuesta. No se exige `run_id` activo.

Admin verifica sesión y rol actuales, pertenencia, propuesta/versión, expiración, estado de cuenta, evidencia y snapshot del caso. Registra aprobación, confirmante, acción canónica e identificador de operación con exclusión de concurrencia y ejecuta mediante su propia lógica. La autorización permanece en backend; no se emite al agente/MCP. Un snapshot desactualizado produce `state_conflict` antes de sancionar y exige nueva revisión y confirmación.

**Salida:** `{ proposal_id: uuid, operation_id: uuid, user_id: uuid, status: string, sanction_status: string, case_status: string, audit_status: string, executed_at: datetime|null, audit_reference: uuid }`.

`status` es `executing`, `succeeded`, `partial`, `failed` o `unknown`. `sanction_status` es `pending`, `applied`, `failed` o `unknown`; `case_status` es `kept_open`, `pending`, `resolved`, `conflict` o `unknown`; `audit_status` es `pending` o `recorded`. `audit_reference` identifica el registro durable del intento. Una sanción aplicada con cierre de caso o auditoría todavía pendiente se informa como `partial`, sin afirmar un éxito completo. Si no se puede persistir la intención, no se inicia el efecto.

El portal consulta el desenlace por `operation_id` mediante admin y puede reintentar explícitamente la misma operación con sesión válida. No vuelve a pedir una decisión al modelo ni exige que agente/MCP estén disponibles. El estado `executing` puede responder `202`; las consultas de estado no aplican efectos ni lanzan IA. No se reciben nuevos valores de usuario, acción, motivo, duración o snapshot al reintentar.

La autorización habilita una única operación idempotente. Reenviar la misma operación devuelve su resultado registrado o indica que está pendiente de resolución. Una confirmación inicial de una propuesta cancelada, expirada o no aprobada se rechaza. Una operación ya aprobada y comenzada conserva su identificador para consultar/reconciliar su desenlace aunque después venza la propuesta; eso no autoriza una sanción nueva ni permite modificarla. Ante timeout con desenlace incierto se consulta primero el resultado del servicio que aplica el efecto.

Después de comprobar el efecto en auth, si se confirmó `resolve`, admin resuelve únicamente los `report_id` del snapshot confirmado y audita en su transacción local. Con `keep_open` conserva las denuncias pendientes y registra esa decisión. Denuncias nuevas o ajenas al alcance confirmado no se resuelven. Ante carrera posterior a la confirmación se mantiene su estado y se reconcilia la restricción de revisión que corresponda. El flujo reutiliza las reglas del módulo `reports`, extendiendo sus escrituras actuales por usuario para admitir el conjunto versionado.

Resolver no levanta bloqueos ni suspensiones. Una advertencia no libera revisión por sí sola. IA-08 conserva la revisión en auth al bloquear y sincroniza su versión según las denuncias pendientes al desbloquear o cerrar casos. Estas reglas se verifican junto con los fallos entre auth y la transacción de cierre/auditoría.

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


## Adición IA-08 · Resultado de operaciones de sanción

El backend de Auth registra por `operation_id` usuario, actor, acción, motivo, duración y resultado. Sus APIs son `POST /internal/users/{id}/sanctions` y `GET /internal/sanction-operations/{operation_id}`, reservadas a la identidad de moderación de Admin.

El resultado incluye `operation_id`, `user_id`, `actor_id`, `action`, `status`, `created_at`, `applied_at`, `suspended_until` y `error_code`. Estados de efecto: `applied`, `failed`, `sending`, `unknown`, `simulated`; Admin agrega `pending` mientras solo existe la intención. La auditoría se controla por separado. Una operación repetida conserva resultado y fecha de fin; reutilizar su UUID con otro contenido se rechaza.

Suspensión exige `duration_seconds` igual a 3600, 86400, 604800 o 2592000. Advertencia y bloqueo omiten duración. Una suspensión vigente rechaza otra operación nueva. El estado administrativo agrega `suspendido`, fecha de fin y revisión independiente. Las entradas de `get_user_history` agregan `status` opcional para distinguir intenciones y resultados. Las entradas históricas existentes pueden omitirlo.

La advertencia se envía por SMTP al email canónico de Auth. La aceptación de SMTP no demuestra lectura o entrega final. Un resultado incierto no se reenvía automáticamente. El proveedor de logs de desarrollo devuelve `simulated`.

El JWT de Admin→Auth usa una clave RS256 exclusiva de moderación y audiencia `auth-service:moderation`, con actor, usuario, operación, permiso exacto, `iat`, `exp` de hasta 60 segundos y `jti`. La recepción Social→Admin exige una credencial independiente. Las confirmaciones públicas y propuestas permanecen en IA-09/10.


## Recuperación y despliegue coordinado de IA-08

El listado administrativo de denuncias incluye `sync_pending=true` cuando falta completar
la sincronización de revisión en Auth. El caso permanece visible aunque ya se haya guardado
el cierre de sus denuncias. `POST /admin/reports/{id}/retry` exige sesión administrativa y CSRF,
y completa la operación y versión pendientes. El resultado del panel se actualiza al consultar
nuevamente el listado.

La activación del despliegue se controla con `MODERATION_ROLLOUT_ENABLED=true` en Auth,
Admin y Social. Preparar antes los Secrets de GitHub `MODERATION_PRIVATE_KEY_PEM_B64` en Admin,
`MODERATION_PUBLIC_KEY_PEM_B64` en Auth y `REPORTS_SERVICE_TOKEN` en Admin y Social. Los pipelines
renderizan y montan las claves durante el rollout coordinado de IA-12 y validan la configuración
antes de publicar imágenes. El valor inicial vacío deja el despliegue pendiente.


## APIs implementadas de IA-09

| Método y ruta en Admin | Contrato |
|---|---|
| `POST /internal/ai/runs/{id}/proposals` | Entrada de `propose_sanction`, JWT de MCP con `proposals:create`, ligado a administrador, conversación, ejecución y usuario seleccionado. |
| `GET /admin/ai/proposals/{id}` | Documento canónico y estado actual, con sesión del propietario. |
| `GET /admin/ai/runs/{id}/proposals` | Propuestas persistidas de la ejecución, incluyendo runs fallidos. |
| `POST /admin/ai/proposals/{id}/cancel` | Cuerpo `{}`, sesión vigente y CSRF. Cancelación idempotente. |

El gateway agrega `/api` a las rutas administrativas. Las lecturas usan
`Cache-Control: no-store` y conservan la expiración de sesión por inactividad.
La consulta y cancelación operan después de terminar la ejecución del agente.

La respuesta incorpora `proposal_policy_version=sanctions-proposal-v1`. Los
reintentos idénticos devuelven el documento original con su estado actual, incluidos
`cancelled` y `expired`. Una propuesta nueva usa versión 1 y un UUID nuevo. La vigencia
es quince minutos, acotada por la conversación, con hasta cien propuestas por run.

Admin exige al menos un snapshot de publicaciones con texto y verifica referencias
del mismo usuario y ejecución. Si se referencia una evaluación, debe estar completada
y todas sus evidencias deben estar incluidas. Conserva su política de moderación.
El camino humano directo con evaluación nula usa `policy_version=manual-review-v1`.
Las dos variantes conservan la confirmación humana de IA-10 como siguiente paso.

Los snapshots de denuncias contienen el conjunto completo de UUIDs pendientes. La
versión aumenta ante cambios reales del conjunto, y Admin rechaza un snapshot
ajeno o desactualizado al proponer. El contador `pending_count` asociado al snapshot
corresponde a ese conjunto congelado. La página de antecedentes conserva su propia
cobertura limitada. IA-10 volverá a validar el snapshot y la versión al confirmar.

## API de confirmación de IA-10

| Ruta del portal | Pedido y respuesta |
|---|---|
| `POST /api/admin/ai/proposals/{id}/confirm` | `version` y `confirm_case_resolution: true` cuando el alcance aprobado es `resolve`. Devuelve la operación persistida. |
| `GET /api/admin/ai/sanction-operations/{id}` | Devuelve el estado de la operación al administrador que confirmó, sin renovar su sesión. |
| `POST /api/admin/ai/sanction-operations/{id}/retry` | `{}`. Reconcilia el efecto y completa pasos pendientes sobre el mismo identificador. |

Admin valida sesión vigente, rol `moderator` o `superadmin`, CSRF en escrituras, propiedad,
versión, expiración, cuenta, evidencia y snapshot de denuncias. El UUID de la propuesta
identifica la operación y el registro de autorización de un solo uso. El cuerpo de
confirmación solo confirma el documento. Doble clic devuelve el estado guardado.
Una propuesta confirmada incluye `operation_id` en sus consultas.

La operación puede estar `pending`, `unknown`, `failed`, `simulated`, `partial` o
`applied`. `effect_status` muestra el estado registrado para Auth y `pending_steps`
señala qué falta. Las escrituras responden `202` cuando la operación está pendiente, y
`200` cuando devuelven un resultado conocido o incierto. La lectura responde `200` al
devolver el estado disponible. El portal puede mostrar la fecha de vencimiento real de
una suspensión a partir de `suspended_until`. Una advertencia `applied` acredita
aceptación SMTP. Si el envío quedó incierto, el reintento consulta la operación y
conserva ese estado sin reenviar.

Admin conserva confirmación, intentos y resultado de forma correlacionada, incluso
después de la limpieza de la conversación. Ante pérdida de respuesta de Auth, consulta
ese UUID antes de reintentar. Para `resolve`, las denuncias nuevas quedan pendientes y el
cierre autorizado solo modifica los IDs guardados. Con pasos administrativos pendientes
tras un efecto aplicado, Admin devuelve `partial` y ofrece reintento explícito desde el
portal. El frontend y el modal se implementan en IA-11.

El resultado de una ejecución puede incluir `proposal_ids`. El agente los obtiene
de las respuestas de la herramienta. Admin comprueba su pertenencia al run antes
de guardar el resultado. Los resultados anteriores que solo contienen `message`
siguen siendo válidos. El listado por run permite recuperar propuestas si falla la
respuesta del agente después de guardarlas.
