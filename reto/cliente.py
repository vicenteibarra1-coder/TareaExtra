"""
cliente.py — Estación de telemetría (contenedor 'cliente', 172.28.0.20).

Cada 4 segundos envía un GET al servidor con su token en la cabecera X-Token,
EN CLARO. Como cliente y servidor están en el mismo bridge, su tráfico unicast
no llega al atacante salvo que éste haga un MITM (ARP spoofing). Ese token es
la FLAG 1.
"""
import os
import time
import urllib.request

from comun import flag

RUT = os.environ.get("ESTUDIANTE", "")
TOKEN = flag(RUT, "mitm")
SERVIDOR = os.environ.get("SERVIDOR", "http://servidor:8080")


def latido():
    req = urllib.request.Request(SERVIDOR + "/telemetria",
                                 headers={"X-Token": TOKEN})
    with urllib.request.urlopen(req, timeout=3) as r:
        r.read()


if __name__ == "__main__":
    print("[cliente] enviando telemetria cada 4 s hacia", SERVIDOR, flush=True)
    while True:
        try:
            latido()
        except Exception as e:
            print("[cliente] reintentando:", e, flush=True)
        time.sleep(4)
