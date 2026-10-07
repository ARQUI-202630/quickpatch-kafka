# AGENTS — Kafka

- `events/`: esquemas JSON de los eventos (fuente de verdad).
- `topics/topics.yaml`: un topic por eventType.
- `deploy/`: despliegue de Kafka (DevOps).
- Todo cambio identifica productor y consumidores, y clasifica compatibilidad.
- Breaking changes requieren una versión nueva del evento.
- No incluir lógica de negocio.
