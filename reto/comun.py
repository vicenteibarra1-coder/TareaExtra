"""
comun.py — lógica compartida del reto "Operación Red Fantasma".
Deriva las flags de cada estudiante a partir de su RUT, de forma determinista.
El MISMO archivo lo usan los servicios (en los contenedores) y el corrector
del profesor (revisar.py), así que las flags siempre coinciden.
"""
import hashlib
import os

# Semilla del reto. El profesor puede cambiarla por curso/semestre con la
# variable de entorno RETO_SECRET, pero debe usar la MISMA al corregir.
SECRET = os.environ.get("RETO_SECRET", "red-fantasma-2026-EIT-UDP")

# Etapas (cada una produce una flag distinta).
ETAPAS = ("mitm", "oraculo", "forja")


def normalizar_rut(rut: str) -> str:
    """Quita puntos, guiones y espacios y pasa a minúscula, para que el RUT
    del estudiante y el del profesor coincidan sin importar el formato."""
    if not rut:
        return ""
    return (rut.strip().lower()
            .replace(".", "").replace("-", "").replace(" ", ""))


def flag(rut: str, etapa: str) -> str:
    """Flag determinista para (rut, etapa). Formato: FLAG{12 hex}."""
    r = normalizar_rut(rut)
    h = hashlib.sha256(f"{r}|{etapa}|{SECRET}".encode()).hexdigest()[:12]
    return "FLAG{" + h + "}"
