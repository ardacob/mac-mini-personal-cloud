# 03 — NAStool kurulumu

> NAStool upstream projesi 2023'te arşivlendi ve artık bakım almıyor. Bu rehber mevcut/legacy bir kurulumu belgelemek amacıyla NAStool kullanır.

## Compose servisi

Ana `compose.yaml` dosyasında NAStool servisine kalıcı `./config:/config` ve harici SSD için `${SSD_PATH}:/media` mount'u verilir.

Başlatın:

```bash
docker compose up -d nas-tools
```

Web UI:

```text
http://localhost:3000
```

İlk girişte upstream dokümantasyonundaki başlangıç hesabını kullanıp parolayı hemen değiştirin.

## Disk yolu neden `/media`?

Host örneği:

```text
/Volumes/Crucial T500
```

Container:

```text
/media
```

Örneğin:

```text
Host:      /Volumes/Crucial T500/Media/Filmler
NAStool:   /media/Media/Filmler
```

Aynı storage kökünü tek mount olarak vermek klasör mantığı açısından daha sağlıklıdır.

## TMDB ve diğer ayarlar

NAStool ilk kurulumda TMDB API Key gibi ayarlar isteyebilir. API anahtarlarını `.env`, GitHub veya ekran görüntülerine koymayın.

## Dış erişim

NAStool'u router üzerinden doğrudan internete açmayın. Bu rehber özel ağ üzerinden erişim yaklaşımını tercih eder.
