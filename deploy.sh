#!/usr/bin/env bash
set -euo pipefail

PUERTO="${PUERTO:-8000}"
BASE="http://localhost:${PUERTO}"

cd "$(dirname "$0")"

echo "[1/3] Construyendo imágenes..."
docker compose build

echo "[2/3] Arrancando servicios..."
docker compose up -d

echo "[3/3] Esperando a que ${BASE}/healthz responda 200..."
for intento in $(seq 1 30); do
    if curl -sf "${BASE}/healthz" > /dev/null; then
        echo "Despliegue correcto tras ${intento} intento(s)."
        docker compose ps
        exit 0
    fi
    sleep 2
done

echo "ERROR: la aplicación no respondió en 60 s" >&2
docker compose ps >&2
docker compose logs --tail=20 >&2
exit 1