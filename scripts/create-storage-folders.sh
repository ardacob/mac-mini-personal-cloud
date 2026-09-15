#!/usr/bin/env bash
set -euo pipefail
SSD_PATH="${1:-${SSD_PATH:-}}"
if [[ -z "$SSD_PATH" ]]; then
  echo "Kullanım: $0 '/Volumes/SSD ADI'" >&2
  exit 1
fi
if [[ ! -d "$SSD_PATH" ]]; then
  echo "HATA: SSD yolu bulunamadı: $SSD_PATH" >&2
  exit 1
fi
mkdir -p "$SSD_PATH/Cloud" "$SSD_PATH/Downloads" "$SSD_PATH/Media/Filmler" "$SSD_PATH/Media/Diziler"
echo "Hazır: $SSD_PATH"
find "$SSD_PATH" -maxdepth 2 -type d | sort
