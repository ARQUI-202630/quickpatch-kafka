"""Rechaza cambios incompatibles en los esquemas de events/ frente a la rama base.

Uso: python scripts/check-compat.py <ref-base>
Incompatible: borrar un esquema, quitar una propiedad, volver obligatorio un campo o cambiar
eventType/eventVersion. Esos cambios exigen un esquema nuevo (vN+1) publicado en paralelo.
"""
import json
import subprocess
import sys


def git(*args):
    return subprocess.run(["git", *args], capture_output=True, text=True, encoding="utf-8")


def walk(old, new, path, errores):
    if not isinstance(old, dict) or not isinstance(new, dict):
        return
    for campo in old.get("properties", {}):
        if campo not in new.get("properties", {}):
            errores.append(f"{path}: se quitó la propiedad '{campo}'")
    nuevos = set(new.get("required", [])) - set(old.get("required", []))
    for campo in sorted(nuevos):
        errores.append(f"{path}: '{campo}' pasó a ser obligatorio")
    for campo, sub in old.get("properties", {}).items():
        if campo in new.get("properties", {}):
            walk(sub, new["properties"][campo], f"{path}.{campo}", errores)


base = sys.argv[1]
errores = []
cambios = git("diff", "--name-status", f"{base}...HEAD", "--", "events/*.json").stdout.splitlines()
for linea in cambios:
    estado, archivo = linea.split("\t")[0], linea.split("\t")[-1]
    if estado.startswith("D"):
        errores.append(f"{archivo}: se eliminó el esquema")
        continue
    anterior = git("show", f"{base}:{archivo}")
    if anterior.returncode != 0:
        print(f"Esquema nuevo: {archivo}")
        continue
    old = json.loads(anterior.stdout)
    with open(archivo, encoding="utf-8") as f:
        new = json.load(f)
    for campo in ("eventType", "eventVersion"):
        if old["properties"][campo] != new["properties"][campo]:
            errores.append(f"{archivo}: cambió {campo}")
    walk(old, new, archivo, errores)
    print(f"Comparado: {archivo}")

for e in errores:
    print(f"::error::{e}")
sys.exit(1 if errores else 0)
