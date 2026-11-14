"""
oraculo.py — Oráculo binario (contenedor 'oraculo', 172.28.0.30:9999/udp).

Solo responde a datagramas UDP cuyo payload empieza con el "magic" de 4 bytes
0xDEADBEEF seguido del RUT del estudiante (bytes ASCII, ya normalizado:
sin puntos ni guion). A una petición bien formada responde con la FLAG 2.

No basta con 'nc' o un echo: hay que CONSTRUIR el paquete byte a byte
(Scapy o un socket en Python), que es justo lo que practicaron en el curso.
"""
import os
import socket

from comun import flag, normalizar_rut

RUT = normalizar_rut(os.environ.get("ESTUDIANTE", ""))
FLAG_ORACULO = flag(RUT, "oraculo")
MAGIC = b"\xde\xad\xbe\xef"


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(("0.0.0.0", 9999))
    print("[oraculo] escuchando UDP en 0.0.0.0:9999", flush=True)
    while True:
        datos, origen = s.recvfrom(2048)
        if datos.startswith(MAGIC) and datos[4:].decode(errors="ignore").strip() == RUT:
            s.sendto((FLAG_ORACULO + "\n").encode(), origen)
        else:
            ayuda = (b"formato invalido. payload = 0xDEADBEEF + tu_rut "
                     b"(sin puntos ni guion) en ASCII\n")
            s.sendto(ayuda, origen)


if __name__ == "__main__":
    main()
