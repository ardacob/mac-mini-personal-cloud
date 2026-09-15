# Changelog

All notable changes to this project are documented here.

## [1.0.0] - 2026-09-15

### Added
- Complete Mac mini personal cloud walkthrough using Docker, File Browser, Tailscale and NAStool.
- External APFS SSD layout for `Cloud`, `Downloads` and `Media`.
- iPhone/iPad remote upload and download workflow over Tailscale.
- HEIC preview troubleshooting based on a real cache failure scenario.
- FFmpeg and macOS `sips` comparison steps for validating HEIC files.
- File Browser cache cleanup and preview refresh helper scripts.
- Docker/SSD diagnostic and stack verification scripts.
- NAStool setup notes and legacy/upstream warnings.
- Optional Turkish DOM-based NAStool UI translator.
- Backup, rollback, security and troubleshooting documentation.
- Turkish and English README files.
- Project banner, logo, architecture diagram and privacy-safe File Browser UI mock.

### Fixed / documented
- macOS mounting NTFS as read-only for this use case.
- YAML accidentally pasted into zsh as shell commands.
- Docker bind-mount write issues caused by a read-only host volume.
- HEIC thumbnails showing black, partial or monochrome previews because stale preview data was reused.
- `docker logs -f` making Terminal appear frozen until `Ctrl+C`.
- Risks of aggressive global source-string replacement in NAStool.

### Security
- No real passwords, API keys, private Tailscale addresses or application databases are committed.
- Remote access guidance avoids directly exposing File Browser or NAStool ports to the public Internet.
