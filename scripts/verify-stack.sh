#!/usr/bin/env bash
set -euo pipefail

echo "== Containers =="
docker ps --format 'table {{.Names}}\t{{.Image}}\t{{.Ports}}'

echo
echo "== NAStool =="
if docker inspect nas-tools >/dev/null 2>&1; then
  docker inspect nas-tools --format 'Image={{.Config.Image}} Status={{.State.Status}}'
else
  echo "nas-tools bulunamadı"
fi

echo
echo "== File Browser =="
if docker inspect filebrowser >/dev/null 2>&1; then
  docker inspect filebrowser --format 'Image={{.Config.Image}} Status={{.State.Status}}'
  docker exec filebrowser sh -lc 'echo -n "ffmpeg: "; ffmpeg -version 2>/dev/null | head -1 || echo missing'
else
  echo "filebrowser bulunamadı"
fi
