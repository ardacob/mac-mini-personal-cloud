#!/usr/bin/env bash
set -euo pipefail
CONTAINER="${1:-filebrowser}"
echo "File Browser preview cache temizleniyor: $CONTAINER"
docker exec "$CONTAINER" sh -lc '
  rm -rf /home/filebrowser/tmp/heic/* \
         /home/filebrowser/tmp/thumbnails/* \
         /home/filebrowser/tmp/diskcache/* 2>/dev/null || true
'
docker restart "$CONTAINER" >/dev/null
echo "Tamam. Tarayıcıda hard refresh yapın: Cmd + Shift + R"
