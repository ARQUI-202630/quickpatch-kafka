"""Verifica que topics/topics.yaml y events/ estén alineados.

- Cada topic apunta a un esquema que existe y cuyo eventType es el nombre del topic.
- Cada esquema de events/ tiene su topic declarado.
"""
import json
import pathlib
import sys

import yaml

root = pathlib.Path(__file__).resolve().parent.parent
topics = yaml.safe_load((root / "topics" / "topics.yaml").read_text(encoding="utf-8"))["topics"]
errores = []
declarados = set()

for t in topics:
    for campo in ("name", "schema", "producer", "consumers", "partitions", "replicationFactor"):
        if campo not in t:
            errores.append(f"topic {t.get('name', '?')}: falta '{campo}'")
    esquema = root / t.get("schema", "")
    if not esquema.is_file():
        errores.append(f"topic {t['name']}: no existe el esquema {t.get('schema')}")
        continue
    declarados.add(esquema.resolve())
    tipo = json.loads(esquema.read_text(encoding="utf-8"))["properties"]["eventType"].get("const")
    if tipo != t["name"]:
        errores.append(f"topic {t['name']}: el esquema declara eventType '{tipo}'")

for esquema in sorted((root / "events").glob("*.json")):
    if esquema.resolve() not in declarados:
        errores.append(f"{esquema.relative_to(root)}: no tiene topic en topics/topics.yaml")

for e in errores:
    print(f"::error::{e}")
print(f"{len(topics)} topics revisados, {len(errores)} errores.")
sys.exit(1 if errores else 0)
