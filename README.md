<p align="center">
  <img src="https://raw.githubusercontent.com/ardacob/mac-mini-personal-cloud/main/assets/banner-v2.svg" alt="Lunoud — Your Mac mini. Your cloud." width="100%">
</p>

<p align="center">
  <strong>Türkçe</strong> • <a href="README_EN.md">English</a>
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

**Lunoud**, Mac mini + harici NVMe SSD + Docker + File Browser + Tailscale + NAStool kullanarak kendi kişisel bulutunuzu ve medya depolama sisteminizi kurmanıza yardımcı olan projedir.

Dosyalarınız kendi donanımınızda kalır. iPhone/iPad üzerinden uzaktan erişebilir, aynı fiziksel SSD'yi dosya alanı ve medya depolaması olarak kullanabilir, HEIC önizleme ve macOS/APFS gibi gerçek kurulum sorunlarının belgelenmiş çözümlerinden yararlanabilirsiniz.

Bu repo yalnızca çalışan son ayarları değil; gerçek kurulum sırasında yaşanan sorunları, yanlış denemeleri, teşhis adımlarını ve geri dönüş yöntemlerini de belgeler.

## Öne çıkanlar

- Mac mini üzerinde kişisel bulut
- iPhone/iPad’den hücresel internet üzerinden güvenli uzak dosya erişimi
- File Browser ile yükleme, indirme, klasör oluşturma ve silme
- Tailscale ile router portu açmadan özel ağ erişimi
- Harici NVMe SSD üzerinde merkezi depolama
- Tek fiziksel SSD’yi File Browser ve NAStool ile ortak kullanma
- iPhone HEIC önizleme sorunları için test ve düzeltme akışı
- macOS NTFS read-only teşhisi ve APFS’e geçiş rehberi
- NAStool için daha güvenli DOM tabanlı Türkçe arayüz yaklaşımı
- yedekleme, rollback ve troubleshooting dokümantasyonu

> Test ortamı: Apple Silicon Mac mini + harici 1 TB NVMe SSD. Donanım markası zorunlu değildir; disk adı, yollar ve portlar sizde farklı olabilir.

## Mimari

<p align="center">
  <img src="assets/architecture.svg" alt="Lunoud mimarisi" width="95%">
</p>

File Browser ve NAStool aynı fiziksel SSD’yi farklı container yollarından görür. Dosyalar iki kez kopyalanmaz.

## Hızlı başlangıç

> Repo adı GitHub üzerinde henüz değiştirilmediği için clone adresi şimdilik mevcut adını kullanır.

```bash
git clone https://github.com/ardacob/mac-mini-personal-cloud.git
cd mac-mini-personal-cloud
cp .env.example .env
cp filebrowser/config.example.yaml filebrowser/config.yaml
mkdir -p filebrowser/data
chmod +x scripts/*.sh
```

`.env` içindeki SSD yolunu kendi sisteminize göre düzenleyin:

```dotenv
SSD_PATH=/Volumes/Crucial T500
NASTOOL_PORT=3000
FILEBROWSER_PORT=8080
TZ=Europe/Istanbul
```

Klasörleri oluşturun ve servisleri başlatın:

```bash
./scripts/create-storage-folders.sh "/Volumes/Crucial T500"
docker compose up -d
```

Kontrol:

```bash
docker ps --format 'table {{.Names}}\t{{.Image}}\t{{.Ports}}'
```

Yerel adresler:

- File Browser: `http://localhost:8080`
- NAStool: `http://localhost:3000`

İlk girişten sonra yönetici parolalarını mutlaka değiştirin.

## Depolama

Gerçek kurulumda ilk disk NTFS idi ve macOS tarafından read-only mount edildi. Bu durumda File Browser okuyabilir ancak klasör oluşturamaz, dosya silemez veya upload yapamaz. Mac’e sürekli bağlı disk için APFS tercih edildi.

Ayrıntı: [docs/01-storage-apfs.md](docs/01-storage-apfs.md)

## File Browser ve HEIC

Bu rehber FFmpeg içeren `gtstef/filebrowser` image’ını kullanır. HEIC preview desteği `filebrowser/config.yaml` içinde etkinleştirilir.

HEIC önizlemelerinde siyah, yarım veya siyah-beyaz sonuç alıyorsanız ayrıntılı teşhis akışı için: [docs/06-heic-preview-fix.md](docs/06-heic-preview-fix.md)

## Uzaktan erişim

Mac ve iPhone’a Tailscale kurup aynı tailnet’e bağlanın. Böylece File Browser portunu router’dan genel internete açmadan Lunoud depolamanıza erişebilirsiniz.

Ayrıntı: [docs/05-tailscale-ios.md](docs/05-tailscale-ios.md)

## NAStool

NAStool aynı SSD’yi container içinde `/media` olarak görür. Kurulum ve legacy proje notları: [docs/03-nastool.md](docs/03-nastool.md)

Türkçe arayüz yaklaşımı: [docs/08-nastool-turkish-ui.md](docs/08-nastool-turkish-ui.md)

## Güvenlik

- File Browser ve NAStool portlarını router üzerinden doğrudan genel internete açmayın.
- Uzak erişim için Tailscale kullanın.
- `.env`, uygulama veritabanları, API anahtarları, özel ağ adresleri ve parolaları GitHub’a eklemeyin.
- NAStool upstream projesi arşivlenmiştir; legacy yazılım olarak değerlendirin.

Bkz. [SECURITY.md](SECURITY.md).

## Yedekleme ve sorun giderme

Çalışan sistemi değiştirmeden önce geri dönüş noktası oluşturun. Özellikle compose, NAStool config, File Browser data ve patched NAStool web ağacını yedekleyin.

- [Yedek ve geri dönüş](docs/07-backup-restore.md)
- [Troubleshooting](docs/09-troubleshooting.md)
- [Kurulumdan çıkarılan dersler](docs/10-lessons-learned.md)

## Dokümantasyon

| Dosya | Konu |
|---|---|
| [01-storage-apfs.md](docs/01-storage-apfs.md) | SSD, NTFS ve APFS |
| [02-docker-desktop.md](docs/02-docker-desktop.md) | Docker Desktop ve mount’lar |
| [03-nastool.md](docs/03-nastool.md) | NAStool kurulumu |
| [04-filebrowser.md](docs/04-filebrowser.md) | File Browser kurulumu |
| [05-tailscale-ios.md](docs/05-tailscale-ios.md) | iPhone / Tailscale uzak erişim |
| [06-heic-preview-fix.md](docs/06-heic-preview-fix.md) | HEIC preview teşhisi ve çözümü |
| [07-backup-restore.md](docs/07-backup-restore.md) | Yedek ve geri dönüş |
| [08-nastool-turkish-ui.md](docs/08-nastool-turkish-ui.md) | Türkçe NAStool arayüzü |
| [09-troubleshooting.md](docs/09-troubleshooting.md) | Sorun giderme |
| [10-lessons-learned.md](docs/10-lessons-learned.md) | Kurulumdan çıkarılan dersler |

## Kaynaklar

- NAStool: https://github.com/NAStool/nas-tools
- File Browser Quantum: https://github.com/gtsteffaniak/filebrowser
- Tailscale: https://tailscale.com/
- Docker Desktop: https://docs.docker.com/desktop/
- FFmpeg: https://ffmpeg.org/

## Lisans

Bu repo içindeki özgün rehber ve yardımcı scriptler [MIT License](LICENSE) ile yayımlanır. Üçüncü taraf projelerin kendi lisansları geçerlidir; bkz. [THIRD_PARTY.md](THIRD_PARTY.md).
