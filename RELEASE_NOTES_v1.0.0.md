# v1.0.0 — First public release

This is the first public release of **Mac mini Personal Cloud**.

The project documents a complete real-world setup for turning a Mac mini and an external NVMe SSD into a personal cloud and media storage system with:

- Docker Desktop
- File Browser
- Tailscale
- NAStool
- APFS external storage
- iPhone/iPad remote access
- HEIC preview troubleshooting and cache recovery

## Highlights

- End-to-end setup from SSD preparation to remote iPhone access.
- One physical SSD shared safely between File Browser and NAStool through Docker bind mounts.
- Detailed explanation of why NTFS caused read-only behavior on macOS in the tested setup.
- Reproducible HEIC troubleshooting flow using FFmpeg, macOS `sips`, HTTP `200` vs `304` behavior and preview-cache cleanup.
- Helper scripts for storage diagnostics, cache cleanup, folder creation, NAStool backup and stack verification.
- Optional safer DOM-based Turkish translation approach for NAStool.
- Security guidance that avoids publishing passwords, API keys and private Tailscale addresses.
- Turkish and English project landing pages.

## Tested scenario

- Apple Silicon Mac mini
- External NVMe SSD
- macOS + Docker Desktop
- iPhone client over cellular data

Hardware brands are examples only. Adjust SSD names, paths and ports for your own environment.

## Important note

NAStool's upstream repository is archived. Treat it as legacy software and evaluate the security implications before exposing or relying on it long term.

See the full documentation in `README.md` and the `docs/` directory.
