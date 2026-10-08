# Despliegue de Kafka

Despliegue de Apache Kafka (un nodo en modo KRaft, ADR-006 y R10) y Kafka UI en producción (VM6) y QA (VM7), y creación de los topics de `topics/topics.yaml` (ADR-022). Se trasladó desde `quickpatch-infrastructure` (SCRUM-338).

|Archivo|Contenido|
|---|---|
|`deploy-kafka.yml`|Playbook: escribe el Compose, levanta Kafka y Kafka UI, espera al broker y crea los topics que falten.|
|`compose.yml.j2`|Compose de Kafka y Kafka UI. Las imágenes, la retención y el heap salen del inventario.|

## Cómo se ejecuta

El playbook usa el inventario y el vault de `infrastructure/ansible` del repositorio `quickpatch`, que trae este repositorio como submódulo en `apps/kafka`. Desde `infrastructure/ansible`:

```bash
./ap playbooks/deploy-kafka.yml            # producción y QA
./ap playbooks/deploy-kafka.yml -l qa      # solo QA (VM7)
```

`playbooks/deploy-kafka.yml` de `infrastructure/ansible` importa este archivo. Se aplica la versión de este repositorio que fija el submódulo, igual que los contratos (ADR-021).

## Topics

Cada topic de `topics/topics.yaml` se crea con sus particiones, su factor de replicación y `retention.ms` = `retentionHours`. Los topics se crean solo si no existen (`--if-not-exists`), porque Kafka tiene desactivada la creación automática (`KAFKA_AUTO_CREATE_TOPICS_ENABLE=false`). Un cambio de particiones o de retención en un topic que ya existe no se aplica solo: se hace a mano con `kafka-topics.sh --alter` o `kafka-configs.sh` y se registra en `topics.yaml`.
