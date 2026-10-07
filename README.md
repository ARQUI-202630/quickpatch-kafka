# quickpatch-kafka

Bus de eventos de QUICKPATCH (ADR-006): los **contratos de eventos** (JSON Schema), la **definición de los topics** y el despliegue de Apache Kafka.

Es uno de los 12 repositorios del multirepo (SCRUM-333). Los servicios incluyen este repositorio como submódulo en `contracts/kafka/` para leer los esquemas (`contracts/kafka/events/...`).

## Estructura

```text
events/    Esquemas de los eventos, uno por tipo y versión (fuente de verdad)
topics/    topics.yaml: un topic por eventType, con productor, consumidores y particiones
deploy/    Despliegue de Kafka en producción y QA (SCRUM-338)
scripts/   check-topics.py: el CI verifica que topics y esquemas estén alineados
```

## Convenciones

Detalle y catálogo de eventos en [events/README.md](events/README.md).

- **Sobre común:** `eventId`, `eventType`, `eventVersion`, `occurredAt`, `correlationId`, `tenantId`, `producer` y `data`.
- **Topic:** uno por tipo de evento, con el mismo nombre que `eventType`, creado de forma explícita (no por creación automática).
- **Clave del mensaje:** el identificador del agregado, para conservar el orden por entidad.
- **Publicación** con Outbox y **consumo** idempotente por `eventId` (ADR-007).
- **Compatibilidad:** agregar un campo opcional es compatible; quitar, renombrar o volver obligatorio un campo exige una versión nueva del evento (`v2`) en paralelo.
- **Versión del repositorio:** tags `vMAJOR.MINOR.PATCH`; cada servicio fija una versión en su submódulo.

## Historia

Los esquemas de eventos vivían en `quickpatch-contracts` junto con los contratos REST. Por la retroalimentación del profesor (12 repositorios), pasaron a este repositorio y los REST a `quickpatch-api-gateway`; el historial de cada archivo se conserva.
