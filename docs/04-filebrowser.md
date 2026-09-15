# 04 — File Browser Quantum kurulumu

Bu rehber FFmpeg içeren `gtstef/filebrowser` ana image'ını kullanır.

## Neden bu image?

HEIC önizlemesi için File Browser'ın media integration özelliği ve FFmpeg gerekir. Ana image media desteğini içerir.

## Config

Önce:

```bash
cp filebrowser/config.example.yaml filebrowser/config.yaml
mkdir -p filebrowser/data
```

Önemli bölüm:

```yaml
integrations:
  media:
    ffmpegPath: "ffmpeg"
    convert:
      imagePreview:
        heic: true
        jpeg: true
```

Upstream varsayılan config'te HEIC preview kapalıdır; açıkça `heic: true` yapıyoruz.

## Persistent database

```yaml
server:
  database: "/home/filebrowser/data/database.db"
```

ve compose'da host'tan `/home/filebrowser/data` dizinine bind mount kullanın. Bu sayede container yeniden oluşturulsa bile File Browser verisi host'ta kalır.

## SSD mount

SSD kökü container içinde `/srv` olarak görünür.

## İlk giriş

İlk girişten sonra yönetici hesabının parolasını değiştirin ve gerçek kimlik bilgilerini repoya eklemeyin.

## Test

```bash
docker compose up -d filebrowser
```

Tarayıcıdan `http://localhost:8080` adresini açın. Ardından dosya oluşturma, silme ve HEIC önizleme işlemlerini doğrulayın.
