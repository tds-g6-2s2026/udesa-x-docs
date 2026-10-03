# Registro de decisiones de arquitectura

Cada archivo registra una decisión con su contexto, la decisión tomada, las alternativas y sus consecuencias (formato Michael Nygard).

| Número | Decisión | Fecha | Estado |
|---|---|---|---|
| {doc}`ADR-0001 <adr-0001>` | Microservicios por contexto acotado, no por épica | 2026-08-11 | Aceptada |
| {doc}`ADR-0002 <adr-0002>` | Una base de datos por servicio, sin claves foráneas entre servicios | 2026-08-19 | Aceptada |
| {doc}`ADR-0003 <adr-0003>` | PostgreSQL como fuente de verdad y Redis para datos que vencen | 2026-08-13 | Aceptada |
| {doc}`ADR-0004 <adr-0004>` | Python con FastAPI y SQLAlchemy 2.0 sincrónico | 2026-08-11 | Aceptada |
| {doc}`ADR-0005 <adr-0005>` | admin-service escrito en Go | 2026-09-17 | Aceptada |
| {doc}`ADR-0006 <adr-0006>` | Sesiones con JWT firmado y revocable | 2026-08-16 | Aceptada |
| {doc}`ADR-0007 <adr-0007>` | API gateway propio con verificación central del token | 2026-09-14 | Aceptada |
| {doc}`ADR-0008 <adr-0008>` | La base garantiza unicidad, idempotencia y contadores | 2026-08-13 | Aceptada |
| {doc}`ADR-0009 <adr-0009>` | Paginación por cursor en las listas | 2026-08-31 | Aceptada |
| {doc}`ADR-0010 <adr-0010>` | Comunicación sincrónica entre servicios, en lote y con falla cerrada | 2026-09-10 | Aceptada |
| {doc}`ADR-0011 <adr-0011>` | Baja lógica de usuarios y posts | 2026-08-18 | Aceptada |
| {doc}`ADR-0012 <adr-0012>` | Despliegue en el cluster EKS compartido de la cátedra | 2026-10-02 | Aceptada |
| {doc}`ADR-0013 <adr-0013>` | Testing con dependencias inyectadas, base real y mínimo de cobertura | 2026-09-04 | Aceptada |
| {doc}`ADR-0014 <adr-0014>` | App mobile con Expo, TanStack Query y Zustand | 2026-08-25 | Aceptada |

```{toctree}
:maxdepth: 1
:hidden:
:caption: ADRs

adr-0001
adr-0002
adr-0003
adr-0004
adr-0005
adr-0006
adr-0007
adr-0008
adr-0009
adr-0010
adr-0011
adr-0012
adr-0013
adr-0014
```
