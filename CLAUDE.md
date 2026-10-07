# Claude Code — Kafka

Este repositorio contiene los esquemas de eventos (`events/`), los topics (`topics/`) y el despliegue de Kafka (`deploy/`).

Antes de cambiar un evento:

1. identificar el productor y los consumidores;
2. clasificar compatibilidad;
3. evitar breaking changes silenciosos (versión nueva del evento en paralelo);
4. mantener `topics/topics.yaml` alineado con `events/`;
5. documentar versión e impacto.

No incluir lógica de negocio.
