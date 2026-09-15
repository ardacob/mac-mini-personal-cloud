#!/usr/bin/env bash
set -euo pipefail
FILE="${1:-}"
CONTAINER="${2:-filebrowser}"
if [[ -z "$FILE" || ! -f "$FILE" ]]; then
  echo "Kullanım: $0 '/Volumes/SSD/Cloud/IMG_0001.HEIC' [container]" >&2
  exit 1
fi
case "${FILE,,}" in
  *.heic|*.heif) ;;
  *) echo "UYARI: Dosya HEIC/HEIF görünmüyor: $FILE" ;;
esac

touch "$FILE"
"$(dirname "$0")/clear-heic-cache.sh" "$CONTAINER"
echo "Yeniden preview üretimi için dosya mtime güncellendi: $FILE"
