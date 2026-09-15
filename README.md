# Mac mini Personal Cloud

Mac mini + harici M.2 SSD + Docker + File Browser + Tailscale + NAStool ile kişisel bulut ve medya depolama sistemi.

Bu repo gerçek bir kurulum sırasında yaşanan sorunları, yanlış denemeleri, teşhis adımlarını ve çalışan çözümleri Türkçe olarak belgeler. Hedef; iPhone'dan ev dışındayken Mac mini'ye bağlı SSD'ye dosya yüklemek/indirmek, HEIC fotoğraflarını düzgün önizlemek ve aynı diski NAStool tarafında medya depolaması olarak kullanmaktır.

> Test ortamı: Apple Silicon Mac mini + harici 1 TB NVMe SSD. Donanım markası zorunlu değildir; disk adı ve yollar sizde farklı olabilir.

## Mimari

```text
iPhone / iPad
    │
    │ Tailscale özel ağı
    ▼
Mac mini
    ├── Docker Desktop
    │   ├── File Browser :8080  ───► Harici SSD
    │   └── NAStool      :3000  ───► Harici SSD
    │
    └── APFS SSD
        ├── Cloud/
        ├── Downloads/
        └── Media/
            ├── Filmler/
            └── Diziler/
```

File Browser ve NAStool aynı fiziksel SSD'yi farklı container yollarından görür. Dosyalar iki kez kopyalanmaz.

## Güvenlik

- File Browser ve NAStool portlarını router üzerinden doğrudan genel internete açmayın.
- Uzak erişim için bu rehber Tailscale kullanır.
- `.env`, uygulama veritabanları, API anahtarları ve gerçek özel ağ adreslerini GitHub'a eklemeyin.
- NAStool upstream projesi arşivlenmiştir; legacy yazılım olarak değerlendirin.

## 1. SSD'yi hazırlama

Önce bağlı diskleri görün:

```bash
ls /Volumes
```

Diskin dosya sistemini ve yazılabilirliğini kontrol edin:

```bash
diskutil info "/Volumes/Crucial T500" | grep -E "File System|Type \(Bundle\)|Read-Only|Writable"
```

Gerçek kurulumda ilk disk NTFS idi ve macOS tarafından read-only mount edildi:

```text
File System Personality: NTFS
Volume Read-Only: Yes
```

Bu durumda File Browser dosyaları okuyabilir ama silemez, klasör oluşturamaz veya upload yapamaz. Mac'e sürekli bağlı disk için APFS'e geçildi. Formatlama tüm verileri siler; önce yedek alın.

Ayrıntı: [docs/01-storage-apfs.md](docs/01-storage-apfs.md)

## 2. Repo hazırlığı

```bash
git clone https://github.com/sykenix/mac-mini-personal-cloud.git
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

Klasörleri oluşturun:

```bash
./scripts/create-storage-folders.sh "/Volumes/Crucial T500"
```

Beklenen yapı:

```text
Crucial T500/
├── Cloud/
├── Downloads/
└── Media/
    ├── Filmler/
    └── Diziler/
```

## 3. Docker servislerini başlatma

```bash
docker compose up -d
```

Kontrol:

```bash
docker ps --format 'table {{.Names}}\t{{.Image}}\t{{.Ports}}'
```

Yerel adresler:

- File Browser: `http://localhost:8080`
- NAStool: `http://localhost:3000`

İlk girişlerden sonra yönetici parolalarını değiştirin.

Docker Desktop ve bind mount ayrıntıları: [docs/02-docker-desktop.md](docs/02-docker-desktop.md)

## 4. File Browser ve HEIC desteği

Bu rehber FFmpeg içeren `gtstef/filebrowser` image'ını kullanır. HEIC preview desteği `filebrowser/config.yaml` içinde açıkça etkinleştirilir:

```yaml
integrations:
  media:
    ffmpegPath: "ffmpeg"
    convert:
      imagePreview:
        heic: true
        jpeg: true
```

Ayrıntı: [docs/04-filebrowser.md](docs/04-filebrowser.md)

## 5. iPhone'dan uzaktan erişim

Mac ve iPhone'a Tailscale kurup aynı tailnet'e bağlanın. Önce File Browser'ın yerel ağda çalıştığını doğrulayın. Daha sonra iPhone'da Wi‑Fi'yi kapatıp hücresel veri üzerinden Tailscale bağlantısını test edin.

Router port-forward kullanmadan erişim yaklaşımı ve opsiyonel iOS Files/SMB notları: [docs/05-tailscale-ios.md](docs/05-tailscale-ios.md)

## 6. HEIC siyah / yarım / siyah-beyaz görünüyorsa

Kurulum sırasında bazı iPhone HEIC dosyaları bozuk preview üretiyordu. Teşhis sırası şöyleydi:

1. Aynı HEIC'i container içindeki FFmpeg ile manuel JPEG'e çevir.
2. Aynı dosyayı macOS `sips` ile JPEG'e çevir.
3. İki çıktı da düzgünse orijinal HEIC'in bozuk olmadığını doğrula.
4. Aynı HEIC'i `_TEST` gibi yeni bir adla kopyala.
5. File Browser loglarında eski preview isteği ile yeni preview isteğini karşılaştır.
6. Eski istek `304`, yeni kopya `200` dönüyor ve yeni kopya düzgün görünüyorsa stale preview/cache ihtimali güçlenir.
7. File Browser preview cache'ini temizle ve tarayıcıda hard refresh yap.

Manuel FFmpeg testi:

```bash
docker exec filebrowser ffmpeg -y \
  -i "/srv/Cloud/IMG_0030.HEIC" \
  -frames:v 1 \
  "/srv/Cloud/ffmpeg-0030.jpg"
```

macOS karşılaştırması:

```bash
sips -s format jpeg \
  "/Volumes/Crucial T500/Cloud/IMG_0030.HEIC" \
  --out "/Volumes/Crucial T500/Cloud/mac-test.jpg"
```

Cache temizleme:

```bash
./scripts/clear-heic-cache.sh
```

Belirli bir HEIC için yeniden preview üretimini tetikleme:

```bash
./scripts/refresh-heic-preview.sh "/Volumes/Crucial T500/Cloud/IMG_0030.HEIC"
```

Tam teşhis akışı: [docs/06-heic-preview-fix.md](docs/06-heic-preview-fix.md)

## 7. NAStool

NAStool servisi aynı SSD'yi container içinde `/media` olarak görür. Örneğin:

```text
Host:    /Volumes/Crucial T500/Media/Filmler
NAStool: /media/Media/Filmler
```

NAStool kurulumu ve legacy proje notları: [docs/03-nastool.md](docs/03-nastool.md)

## 8. NAStool Türkçe arayüzü

Kaynak dosyalarda geniş global string replacement yapmak riskli çıktı. Tek karakterli Çince eşleşmeler uygulama mantığındaki stringleri de etkileyebiliyor ve karışık metinler oluşturabiliyor.

Bu nedenle repoda görünür DOM metinlerini çeviren daha güvenli bir installer bulunuyor:

```bash
docker exec -i nas-tools python3 - < nastool/nastool_tr_dom_installer.py
docker restart nas-tools
```

Ardından tarayıcıda hard refresh yapın.

Ayrıntı: [docs/08-nastool-turkish-ui.md](docs/08-nastool-turkish-ui.md)

## 9. Yedek ve geri dönüş

Çalışan sistemi değiştirmeden önce snapshot/yedek alın. Özellikle compose, NAStool config, File Browser data ve patched NAStool web ağacı için geri dönüş noktası oluşturun.

Ayrıntı: [docs/07-backup-restore.md](docs/07-backup-restore.md)

## 10. Troubleshooting ve kurulum günlüğü

Yaşanan önemli sorunlar:

- YAML'ın zsh komutu gibi yapıştırılması
- NTFS diskin macOS'ta read-only mount edilmesi
- Docker bind mount izinleri
- HEIC preview cache problemi
- `docker logs -f` komutunun Terminal'i “donmuş” gibi göstermesi
- NAStool global kaynak çevirisinin UI'yı bozması
- Çalışan sistemi temizleme amacıyla yapılan fazla değişikliğin geri alınması

Bkz. [docs/09-troubleshooting.md](docs/09-troubleshooting.md) ve [docs/10-lessons-learned.md](docs/10-lessons-learned.md).

## Yardımcı scriptler

```text
scripts/
├── backup-nastool-web.sh
├── clear-heic-cache.sh
├── create-storage-folders.sh
├── diagnose-storage.sh
├── refresh-heic-preview.sh
└── verify-stack.sh
```

Storage teşhisi:

```bash
./scripts/diagnose-storage.sh "/Volumes/Crucial T500"
```

Stack kontrolü:

```bash
./scripts/verify-stack.sh
```

## Kaynaklar

- NAStool: https://github.com/NAStool/nas-tools
- File Browser Quantum: https://github.com/gtsteffaniak/filebrowser
- Tailscale: https://tailscale.com/
- Docker Desktop: https://docs.docker.com/desktop/
- FFmpeg: https://ffmpeg.org/

## Lisans

Bu repo içindeki özgün rehber ve yardımcı scriptler [MIT License](LICENSE) ile yayımlanır. Üçüncü taraf projelerin kendi lisansları geçerlidir; bkz. [THIRD_PARTY.md](THIRD_PARTY.md).
