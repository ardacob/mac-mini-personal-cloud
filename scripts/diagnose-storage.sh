#!/usr/bin/env bash
set -euo pipefail
SSD_PATH="${1:-${SSD_PATH:-}}"
if [[ -z "$SSD_PATH" ]]; then
  echo "Kullanım: $0 '/Volumes/SSD ADI'" >&2
  exit 1
fi

echo "== diskutil =="
diskutil info "$SSD_PATH" | grep -E "Device Node|File System|Type \(Bundle\)|Media Read-Only|Volume Read-Only|Writable" || true

echo
echo "== host write test =="
TEST="$SSD_PATH/.cloud-write-test-$$"
if touch "$TEST" 2>/dev/null; then
  rm -f "$TEST"
  echo "OK: Host SSD'ye yazabiliyor."
else
  echo "HATA: Host SSD'ye yazamıyor."
  exit 2
fi
