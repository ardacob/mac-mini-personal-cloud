#!/usr/bin/env bash
set -euo pipefail
CONTAINER="${1:-nas-tools}"
DEST="${2:-./backups}"
STAMP="$(date +%Y%m%d-%H%M%S)"
mkdir -p "$DEST"
docker cp "$CONTAINER:/nas-tools/web" "$DEST/nastool-web-$STAMP"
echo "Yedek: $DEST/nastool-web-$STAMP"
