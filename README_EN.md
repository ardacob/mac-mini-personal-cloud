<p align="center">
  <img src="assets/banner.svg" alt="Mac mini Personal Cloud" width="100%">
</p>

<p align="center">
  <a href="README.md">Türkçe</a> • <strong>English</strong>
</p>

<p align="center">
  <img alt="macOS" src="https://img.shields.io/badge/platform-macOS-111827?logo=apple&logoColor=white">
  <img alt="Docker" src="https://img.shields.io/badge/docker-compose-2563EB?logo=docker&logoColor=white">
  <img alt="iOS" src="https://img.shields.io/badge/client-iPhone%20%2F%20iPad-111827?logo=apple&logoColor=white">
  <img alt="License" src="https://img.shields.io/github/license/sykenix/mac-mini-personal-cloud">
  <img alt="Release" src="https://img.shields.io/badge/release-v1.0.0-16A34A">
</p>

# Mac mini Personal Cloud

Turn a Mac mini and an external NVMe SSD into a lightweight personal cloud and media storage system using Docker, File Browser, Tailscale and NAStool.

This repository is based on a real installation and documents not only the final working setup, but also the failures, diagnostics and fixes that were needed along the way. The main goals are:

- upload and download files from an iPhone while away from home;
- keep the external SSD as the single physical storage location;
- browse and preview iPhone HEIC photos correctly;
- use the same SSD for NAStool media storage;
- avoid exposing File Browser or NAStool directly to the public Internet.

> Tested on an Apple Silicon Mac mini with an external 1 TB NVMe SSD. The SSD brand is not important; paths and device names will vary on other systems.

## Architecture

<p align="center">
  <img src="assets/architecture.svg" alt="Architecture diagram" width="95%">
</p>

File Browser and NAStool see the same physical SSD through different container mount paths. Files are not duplicated.

## Security model

- Do not expose File Browser or NAStool ports directly through router port forwarding.
- This guide uses Tailscale for private remote access.
- Never commit `.env`, application databases, API keys, passwords or real private-network addresses.
- NAStool is an archived upstream project and should be treated as legacy software.

## 1. Prepare the SSD

List mounted volumes:

```bash
ls /Volumes
```

Check the file system and whether the volume is writable:

```bash
diskutil info "/Volumes/Crucial T500" | grep -E "File System|Type \(Bundle\)|Read-Only|Writable"
```

During the real setup, the SSD was initially NTFS and macOS mounted it read-only:

```text
File System Personality: NTFS
Volume Read-Only: Yes
```

In that state File Browser can read files, but it cannot delete files, create folders or upload data. For a disk that stays attached to a Mac, APFS was used instead. Formatting erases the disk, so back up your data first.

Detailed guide: [docs/01-storage-apfs.md](docs/01-storage-apfs.md)

## 2. Clone and configure

```bash
git clone https://github.com/sykenix/mac-mini-personal-cloud.git
cd mac-mini-personal-cloud
cp .env.example .env
cp filebrowser/config.example.yaml filebrowser/config.yaml
mkdir -p filebrowser/data
chmod +x scripts/*.sh
```

Edit the SSD path in `.env` for your system:

```dotenv
SSD_PATH=/Volumes/Crucial T500
NASTOOL_PORT=3000
FILEBROWSER_PORT=8080
TZ=Europe/Istanbul
```

Create the storage folders:

```bash
./scripts/create-storage-folders.sh "/Volumes/Crucial T500"
```

Expected layout:

```text
Crucial T500/
├── Cloud/
├── Downloads/
└── Media/
    ├── Filmler/
    └── Diziler/
```

## 3. Start the Docker services

```bash
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

Docker Desktop and bind-mount notes: [docs/02-docker-desktop.md](docs/02-docker-desktop.md)

## 4. File Browser and HEIC support

The guide uses `gtstef/filebrowser`, which includes FFmpeg in the main image. HEIC preview support is explicitly enabled in `filebrowser/config.yaml`:

```yaml
integrations:
  media:
    ffmpegPath: "ffmpeg"
    convert:
      imagePreview:
        heic: true
        jpeg: true
```

More details: [docs/04-filebrowser.md](docs/04-filebrowser.md)

## 5. Remote access from iPhone

Install Tailscale on both the Mac and the iPhone and sign in to the same tailnet. First verify File Browser locally. Then disable Wi‑Fi on the iPhone and test over cellular data through Tailscale.

This gives remote access without opening router ports to the public Internet.

Detailed iOS/Tailscale notes: [docs/05-tailscale-ios.md](docs/05-tailscale-ios.md)

## 6. Fix black, half-rendered or monochrome HEIC previews

Some iPhone HEIC files produced black, partially rendered or black-and-white thumbnails in File Browser even though the original files were valid.

The diagnostic process was:

1. Convert the same HEIC manually with FFmpeg inside the container.
2. Convert the same HEIC with macOS `sips`.
3. If both JPEG outputs are correct, the original HEIC and decoder are probably fine.
4. Copy the HEIC to a new filename such as `_TEST.HEIC`.
5. Compare File Browser preview requests in the logs.
6. If the old file returns `304` while the renamed copy returns `200` and looks correct, stale preview/cache is strongly indicated.
7. Clear File Browser's preview cache and hard-refresh the browser.

FFmpeg test:

```bash
docker exec filebrowser ffmpeg -y \
  -i "/srv/Cloud/IMG_0030.HEIC" \
  -frames:v 1 \
  "/srv/Cloud/ffmpeg-0030.jpg"
```

macOS comparison:

```bash
sips -s format jpeg \
  "/Volumes/Crucial T500/Cloud/IMG_0030.HEIC" \
  --out "/Volumes/Crucial T500/Cloud/mac-test.jpg"
```

Clear the preview cache:

```bash
./scripts/clear-heic-cache.sh
```

Force a preview refresh for a specific HEIC:

```bash
./scripts/refresh-heic-preview.sh "/Volumes/Crucial T500/Cloud/IMG_0030.HEIC"
```

Full troubleshooting flow: [docs/06-heic-preview-fix.md](docs/06-heic-preview-fix.md)

## 7. NAStool

NAStool mounts the same SSD inside the container as `/media`.

Example:

```text
Host:    /Volumes/Crucial T500/Media/Filmler
NAStool: /media/Media/Filmler
```

NAStool setup and legacy-project notes: [docs/03-nastool.md](docs/03-nastool.md)

## 8. Optional Turkish UI patch for NAStool

Large global source-code string replacements were found to be risky because short Chinese strings can also exist in application logic. That approach caused mixed-language strings and could break behavior.

The repository therefore includes a safer DOM-based installer that translates visible UI text after rendering:

```bash
docker exec -i nas-tools python3 - < nastool/nastool_tr_dom_installer.py
docker restart nas-tools
```

Then perform a browser hard refresh.

Details: [docs/08-nastool-turkish-ui.md](docs/08-nastool-turkish-ui.md)

## 9. Backup and rollback

Before changing a working setup, create a rollback point. In particular, back up:

- `compose.yaml`;
- NAStool configuration;
- File Browser data/configuration;
- any patched NAStool web tree.

Guide: [docs/07-backup-restore.md](docs/07-backup-restore.md)

## 10. Real-world problems documented in this repo

The setup includes troubleshooting for:

- pasting YAML directly into zsh;
- NTFS being mounted read-only by macOS;
- Docker bind-mount permissions;
- stale HEIC preview caches;
- `docker logs -f` making Terminal look frozen;
- over-aggressive source translation breaking NAStool UI strings;
- rolling back an unnecessary cleanup/refactor of a working system.

See [docs/09-troubleshooting.md](docs/09-troubleshooting.md) and [docs/10-lessons-learned.md](docs/10-lessons-learned.md).

## Helper scripts

```text
scripts/
├── backup-nastool-web.sh
├── clear-heic-cache.sh
├── create-storage-folders.sh
├── diagnose-storage.sh
├── refresh-heic-preview.sh
└── verify-stack.sh
```

Storage diagnostics:

```bash
./scripts/diagnose-storage.sh "/Volumes/Crucial T500"
```

Stack verification:

```bash
./scripts/verify-stack.sh
```

## Upstream projects

- NAStool: https://github.com/NAStool/nas-tools
- File Browser Quantum: https://github.com/gtsteffaniak/filebrowser
- Tailscale: https://tailscale.com/
- Docker Desktop: https://docs.docker.com/desktop/
- FFmpeg: https://ffmpeg.org/

## License

Original documentation and helper scripts in this repository are released under the [MIT License](LICENSE). Third-party projects keep their own licenses; see [THIRD_PARTY.md](THIRD_PARTY.md).
