# Contratos de eventos Kafka

Fuente de verdad de los eventos compartidos entre microservicios. Cada evento tiene además su topic en [`topics/topics.yaml`](../topics/topics.yaml).

Cada evento debe documentar:

- nombre;
- versión;
- productor;
- consumidores;
- esquema;
- campos obligatorios y opcionales;
- semántica;
- compatibilidad;
- idempotencia cuando aplique.

El sobre común debe mantenerse alineado con SDD y DD.

## Convenciones

- **Archivo:** `<eventType>.v<versión>.json`, JSON Schema draft-07 (lo valida el CI con AJV).
- **Sobre común** (DD, sección 8.2.1): `eventId`, `eventType`, `eventVersion`, `occurredAt`, `correlationId`, `tenantId`, `producer` y `data`. Cada esquema lo repite completo para que se valide de forma independiente.
- **Topic:** uno por tipo de evento, con el mismo nombre que `eventType`.
- **Clave del mensaje:** el identificador del agregado (por ejemplo `serviceRequestId`), para conservar el orden por entidad.
- **Publicación:** con Transactional Outbox (ADR-007); `eventId` es el `id` de `outbox_events`.
- **Consumo:** idempotente por `eventId` (`processed_events`, RN-EV1).
- **Compatibilidad:** agregar un campo opcional es compatible; quitar o renombrar un campo, o volverlo obligatorio, es un cambio incompatible y exige una versión nueva del evento (`v2`) publicada en paralelo mientras los consumidores migran.

## Catálogo

|Evento|Versión|Productor|Consumidores|Esquema|
|---|---|---|---|---|
|`service-request.created`|1|ServiceRequest|Matching, Communication|[service-request.created.v1.json](service-request.created.v1.json)|
|`catalog.category-changed`|1|Catalog|ServiceRequest, Matching|[catalog.category-changed.v1.json](catalog.category-changed.v1.json)|
|`technician.registered`|1|Identity|Matching, Communication|[technician.registered.v1.json](technician.registered.v1.json)|
|`technician.verification-changed`|1|Identity|Matching, Communication|[technician.verification-changed.v1.json](technician.verification-changed.v1.json)|
|`matching.offer-created`|1|Matching|Communication|[matching.offer-created.v1.json](matching.offer-created.v1.json)|
|`matching.technician-assigned`|1|Matching|ServiceRequest, Communication|[matching.technician-assigned.v1.json](matching.technician-assigned.v1.json)|
|`matching.no-technician-available`|1|Matching|ServiceRequest, Communication|[matching.no-technician-available.v1.json](matching.no-technician-available.v1.json)|
|`matching.search-resumed`|1|Matching|ServiceRequest, Communication|[matching.search-resumed.v1.json](matching.search-resumed.v1.json)|
|`service-request.status-changed`|1|ServiceRequest|Communication|[service-request.status-changed.v1.json](service-request.status-changed.v1.json)|

Los eventos del técnico (`technician.*`) alimentan la réplica de Matching (P-01) y siguen el ADR-017: llevan el estado completo de la proyección y `updatedAt` como versión, y el consumidor descarta los cambios con un `updatedAt` más antiguo que el que ya tiene. Como son dos topics, el orden entre ellos no está garantizado: `technician.verification-changed` trae también `specialtyId` para que Matching pueda crear la fila aunque todavía no haya procesado `technician.registered`.

`service-request.status-changed` lo publica ServiceRequest cada vez que aplica un cambio de estado, en la misma transacción (Outbox), y no lo publica si descarta el evento que lo habría causado (SCRUM-466). Así el aviso en tiempo real refleja la fuente de verdad: antes Communication avisaba a partir de los eventos de Matching y, si ServiceRequest descartaba uno por viejo (ADR-017), el aviso salía igual. La creación no lo publica: el aviso de `buscando_tecnico` sigue saliendo de `service-request.created`.
