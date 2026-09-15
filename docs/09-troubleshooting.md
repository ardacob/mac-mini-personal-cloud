# 09 — Troubleshooting

## `zsh: command not found: services:`

Neden: YAML içeriği Terminal komutu olarak çalıştırılmıştır.

Çözüm: İçeriği `compose.yaml` dosyasına yazın; YAML bloklarını doğrudan zsh'e yapıştırmayın.

## File Browser dosya silemiyor / klasör oluşturamıyor

Önce host diskin yazılabilir olduğundan emin olun:

```bash
diskutil info "/Volumes/Crucial T500" | grep -E "File System|Read-Only"
```

`Volume Read-Only: Yes` ise sorun Docker'dan önce host filesystem katmanındadır.

## `Mounts denied`

Docker Desktop ayarlarında SSD yolunun file sharing kapsamında olduğundan emin olun.

## `port is already allocated`

```bash
docker ps --format 'table {{.Names}}\t{{.Ports}}'
```

Aynı portu kullanan eski test container'ı olup olmadığını kontrol edin.

## `docker logs -f` sonrası Terminal komut almıyor

`-f` canlı log takibidir. Çıkmak için `Ctrl + C` kullanın.

## HEIC preview siyah / yarım

[06-heic-preview-fix.md](06-heic-preview-fix.md) akışını izleyin. Özellikle manuel FFmpeg testi, macOS `sips` karşılaştırması, `_TEST` kopyası ve `200` / `304` preview farkı önemlidir.

## NAStool Türkçe patch sonrası UI bozuldu

Global source replacement yaptıysanız yedeğe dönün. DOM tabanlı patch'i tercih edin.

## SSD Docker'da görünmüyor

Disk mount adının değişmediğini ve compose içindeki host yolunun güncel olduğunu kontrol edin.

## iPhone uzaktan bağlanmıyor

Mac ve iPhone tarafında Tailscale bağlantısını, Mac'in uyku durumunu ve ilgili Docker container'ın çalıştığını kontrol edin. Hücresel veri ile test etmek gerçek uzak erişimi doğrulamanın en kolay yollarından biridir.
