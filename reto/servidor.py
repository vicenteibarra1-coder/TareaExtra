"""
servidor.py — Servicio de telemetría (contenedor 'servidor', 172.28.0.10:8080).

Expone GET /telemetria. Exige la cabecera X-Token con el token secreto del
estudiante (que es la FLAG 1). El 'cliente' se la envía en claro cada pocos
segundos; por eso se puede capturar con un MITM.

Si además llega la cabecera X-Comando: liberar (con el token correcto), el
servidor entrega la FLAG 3. El cliente legítimo NUNCA manda ese comando: el
estudiante debe forjar la petición con el token que capturó.
"""
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from comun import flag

RUT = os.environ.get("ESTUDIANTE", "")
TOKEN = flag(RUT, "mitm")     # FLAG 1 (la que viaja en claro)
FLAG_FORJA = flag(RUT, "forja")  # FLAG 3


class Handler(BaseHTTPRequestHandler):
    # Silenciar el log de acceso para no filtrar tokens por consola.
    def log_message(self, *a):
        return

    def _responder(self, codigo, cuerpo):
        self.send_response(codigo)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(cuerpo.encode())

    def do_GET(self):
        if self.path.split("?")[0] != "/telemetria":
            self._responder(404, "ruta no encontrada\n")
            return
        token = self.headers.get("X-Token", "")
        if token != TOKEN:
            self._responder(401, "token invalido o ausente\n")
            return
        comando = self.headers.get("X-Comando", "")
        if comando == "liberar":
            self._responder(200, FLAG_FORJA + "\n")
        elif comando == "estado":
            self._responder(200, "sistema armado; accion privilegiada: "
                                 "X-Comando: liberar\n")
        elif comando:
            self._responder(200, "comando invalido (validos: estado, liberar)\n")
        else:
            self._responder(200, "telemetria-ok (nivel lectura). Para acciones "
                                 "envia la cabecera X-Comando (prueba: estado)\n")


if __name__ == "__main__":
    srv = ThreadingHTTPServer(("0.0.0.0", 8080), Handler)
    print("[servidor] telemetria escuchando en 0.0.0.0:8080", flush=True)
    srv.serve_forever()
