<p align="center">
  <img src="https://raw.githubusercontent.com/ardacob/mac-mini-personal-cloud/main/assets/banner-v2.svg" alt="Lunoud — Your Mac mini. Your cloud." width="100%">
</p>

<p align="center">
  <a href="README.md">Türkçe</a> • <strong>English</strong>
</p>

<p align="center">
  <img alt="macOS" src="https://img.shields.io/badge/platform-macOS-111827?logo=apple&logoColor=white">
  <img alt="Docker" src="https://img.shields.io/badge/docker-compose-2563EB?logo=docker&logoColor=white">
  <img alt="iOS" src="https://img.shields.io/badge/client-iPhone%20%2F%20iPad-111827?logo=apple&logoColor=white">
  <img alt="License" src="https://img.shields.io/github/license/ardacob/mac-mini-personal-cloud">
  <img alt="Release" src="https://img.shields.io/badge/release-v1.0.0-16A34A">
</p>

# Lunoud

> **Your Mac mini. Your cloud.**

**Lunoud** turns a Mac mini and an external NVMe SSD into a lightweight personal cloud and media storage system using Docker, File Browser, Tailscale and NAStool.

Your files stay on your own hardware. You can access them remotely from iPhone/iPad, share the same physical SSD between file storage and media services, and follow documented fixes for real-world macOS, APFS and HEIC preview issues.

This repository documents both the final working setup and the failures, diagnostics and rollback steps discovered during a real installation.

## Highlights

- Personal cloud running on a Mac mini
- Secure remote file access from iPhone/iPad over cellular networks
- Upload, download, folder creation and deletion with File Browser
- Private remote access through Tailscale without exposing router ports
- External NVMe SSD as the central storage layer
- One physical SSD shared by File Browser and NAStool
- HEIC preview troubleshooting and fixes
- macOS NTFS read-only diagnosis and APFS migration guidance
- Safer DOM-based Turkish UI approach for NAStool
- Backup, rollback and troubleshooting documentation

> Tested on an Apple Silicon Mac mini with an external 1 TB NVMe SSD. Storage brands are not important; paths, device names and ports may differ on other systems.

## Architecture

<p align="center">
  <img src="assets/architecture.svg" alt="Lunoud architecture" width="95%">
</p>

File Browser and NAStool access the same physical SSD through different container mount paths. Files are not duplicated.

## Quick start

> The GitHub repository itself has not been renamed yet, so the clone URL still uses the current repository name.

```bash
git clone https://github.com/ardacob/mac-mini-personal-cloud.git
cd mac-mini-personal-cloud
cp .env.example .env
cp filebrowser/config.example.yaml filebrowser/config.yaml
mkdir -p filebrowser/data
chmod +x scripts/*.sh
```

Edit the SSD path in `.env`:

```dotenv
SSD_PATH=/Volumes/Crucial T500
NASTOOL_PORT=3000
FILEBROWSER_PORT=8080
TZ=Europe/Istanbul
```

Create the storage folders and start the services:

```bash
./scripts/create-storage-folders.sh "/Volumes/Crucial T500"
docker compose up -d
```

Verify:

```bash
docker ps --format 'table {{.Names}}\t{{.Image}}\t{{.Ports}}'
```

Local addresses:

- File Browser: `http://localhost:8080`
- NAStool: `http://localhost:3000`

Change all default/admin passwords after the first login.

## Storage

During the real setup, the SSD was initially NTFS and macOS mounted it read-only. In that state File Browser can read files but cannot delete files, create folders or upload data. APFS was used instead for a disk that stays attached to the Mac.

Detailed guide: [docs/01-storage-apfs.md](docs/01-storage-apfs.md)

## File Browser and HEIC

The guide uses `gtstef/filebrowser`, which includes FFmpeg in the main image. HEIC preview support is enabled in `filebrowser/config.yaml`.

For black, partially rendered or monochrome HEIC previews, see: [docs/06-heic-preview-fix.md](docs/06-heic-preview-fix.md)

## Remote access

Install Tailscale on both the Mac and the iPhone and sign in to the same tailnet. This gives you access to Lunoud storage without exposing File Browser directly to the public Internet.

Detailed guide: [docs/05-tailscale-ios.md](docs/05-tailscale-ios.md)

## NAStool

NAStool mounts the same SSD inside the container as `/media`.

- Setup and legacy-project notes: [docs/03-nastool.md](docs/03-nastool.md)
- Optional Turkish UI approach: [docs/08-nastool-turkish-ui.md](docs/08-nastool-turkish-ui.md)

## Security

- Do not expose File Browser or NAStool ports directly through router port forwarding.
- Use Tailscale for private remote access.
- Never commit `.env`, application databases, API keys, passwords or real private-network addresses.
- NAStool is an archived upstream project and should be treated as legacy software.

See [SECURITY.md](SECURITY.md).

## Backup and troubleshooting

Before changing a working setup, create a rollback point. In particular, back up compose files, NAStool config, File Browser data and any patched NAStool web tree.

- [Backup and restore](docs/07-backup-restore.md)
- [Troubleshooting](docs/09-troubleshooting.md)
- [Lessons learned](docs/10-lessons-learned.md)

## Documentation

| File | Topic |
|---|---|
| [01-storage-apfs.md](docs/01-storage-apfs.md) | SSD, NTFS and APFS |
| [02-docker-desktop.md](docs/02-docker-desktop.md) | Docker Desktop and mounts |
| [03-nastool.md](docs/03-nastool.md) | NAStool setup |
| [04-filebrowser.md](docs/04-filebrowser.md) | File Browser setup |
| [05-tailscale-ios.md](docs/05-tailscale-ios.md) | iPhone / Tailscale remote access |
| [06-heic-preview-fix.md](docs/06-heic-preview-fix.md) | HEIC preview diagnostics and fixes |
| [07-backup-restore.md](docs/07-backup-restore.md) | Backup and rollback |
| [08-nastool-turkish-ui.md](docs/08-nastool-turkish-ui.md) | Turkish NAStool UI |
| [09-troubleshooting.md](docs/09-troubleshooting.md) | Troubleshooting |
| [10-lessons-learned.md](docs/10-lessons-learned.md) | Lessons learned |

## Upstream projects

- NAStool: https://github.com/NAStool/nas-tools
- File Browser Quantum: https://github.com/gtsteffaniak/filebrowser
- Tailscale: https://tailscale.com/
- Docker Desktop: https://docs.docker.com/desktop/
- FFmpeg: https://ffmpeg.org/

## License

Original documentation and helper scripts in this repository are released under the [MIT License](LICENSE). Third-party projects keep their own licenses; see [THIRD_PARTY.md](THIRD_PARTY.md).
