#!/usr/bin/env bash
# verificar_entorno.sh — comprueba que tu mini-red quedó bien levantada y que
# tu estación de ataque tiene todo lo necesario para las 3 misiones.
# NO resuelve ninguna misión: solo revisa que el entorno esté listo.
# Úsalo desde la carpeta 'reto/':   bash verificar_entorno.sh

ok()  { echo -e "  [ OK ] $1"; }
bad() { echo -e "  [ NO ] $1"; FALLOS=$((FALLOS+1)); }
FALLOS=0

echo "=================================================================="
echo "  Verificando el entorno del reto..."
echo "=================================================================="

# 1) Los 4 contenedores arriba
ARRIBA=$(docker compose ps --services --filter "status=running" 2>/dev/null | sort | tr '\n' ' ')
for svc in atacante cliente oraculo servidor; do
  if echo "$ARRIBA" | grep -qw "$svc"; then ok "contenedor '$svc' corriendo"
  else bad "contenedor '$svc' NO está corriendo  (revisa 'docker compose up -d --build')"; fi
done

# 2) Conectividad desde el atacante hacia los demás
for ip in 172.28.0.10 172.28.0.20 172.28.0.30; do
  if docker exec atacante ping -c1 -W2 "$ip" >/dev/null 2>&1; then ok "el atacante alcanza a $ip"
  else bad "el atacante NO alcanza a $ip"; fi
done

# 3) Herramientas dentro del atacante
docker exec atacante python3 -c "import scapy" >/dev/null 2>&1 \
  && ok "Scapy disponible en el atacante" || bad "falta Scapy en el atacante"
docker exec atacante sh -c "command -v tcpdump" >/dev/null 2>&1 \
  && ok "tcpdump disponible en el atacante" || bad "falta tcpdump en el atacante"

# 4) Capacidades de red (ARP spoofing necesita raw sockets e ip_forward)
docker exec atacante python3 -c "import socket; socket.socket(socket.AF_PACKET, socket.SOCK_RAW, 0).close()" >/dev/null 2>&1 \
  && ok "raw sockets (NET_RAW) funcionan" || bad "raw sockets bloqueados (revisa cap_add NET_RAW)"
FWD=$(docker exec atacante cat /proc/sys/net/ipv4/ip_forward 2>/dev/null | tr -d '[:space:]')
[ "$FWD" = "1" ] && ok "ip_forward activado (reenvío listo)" || bad "ip_forward en '$FWD' (deberia ser 1)"

echo "------------------------------------------------------------------"
if [ "$FALLOS" -eq 0 ]; then
  echo "  TODO OK. Tu entorno está listo para las 3 misiones."
else
  echo "  Hay $FALLOS punto(s) con problema. Revisa arriba antes de seguir."
fi
echo "=================================================================="
