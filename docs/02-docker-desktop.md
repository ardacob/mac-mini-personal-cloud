# 02 — Docker Desktop ve harici SSD bind mount

Docker Desktop on macOS, host klasörlerini Linux container'lara bind mount eder.

## Harici SSD yolu

```bash
ls /Volumes
```

Örnek host yolu:

```text
/Volumes/Crucial T500
```

Yolda boşluk olduğu için shell komutlarında çift tırnak kullanın.

## Docker Desktop file sharing

Modern Docker Desktop sürümlerinde `/Volumes` varsayılan paylaşılan alanlardan biridir; ancak `Mounts denied` görürseniz:

1. Docker Desktop → Settings.
2. Resources → File sharing.
3. SSD'yi veya `/Volumes` altındaki ilgili klasörü ekleyin.
4. Apply / Restart.

## Docker'ın SSD'ye yazabildiğini test etme

Servis başladıktan sonra:

```bash
docker exec filebrowser sh -lc 'touch /srv/docker-write-test.txt && rm /srv/docker-write-test.txt'
```

`Permission denied` alırsanız şu sırayla kontrol edin:

1. `diskutil info` ile `Volume Read-Only`.
2. Docker Desktop File Sharing.
3. Container mount yolu.
4. Source'un `readOnly: false` olması.

## YAML'ı Terminal'e doğrudan yapıştırmayın

Şu içerik bir shell komutu değildir:

```yaml
services:
  filebrowser:
    image: ...
```

Bunu doğrudan zsh'e yapıştırırsanız:

```text
zsh: command not found: services:
```

alırsınız. YAML bir `compose.yaml` veya `config.yaml` dosyasına yazılmalıdır.
