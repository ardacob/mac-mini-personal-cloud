# 06 — HEIC siyah / yarım / siyah-beyaz önizleme problemi

Bu bölüm, decoder ile cache sorununu birbirinden ayırmak için kullandığımız teşhis akışını belgeler.

## Belirti

Bazı HEIC dosyaları düzgün görünürken bazıları siyah, yarım veya siyah-beyaz thumbnail üretebilir.

## 1. FFmpeg sürümünü kontrol et

```bash
docker exec filebrowser sh -lc 'which ffmpeg && ffmpeg -version | head -3'
```

## 2. Problemli HEIC'i manuel dönüştür

```bash
docker exec filebrowser ffmpeg -y \
  -i "/srv/Cloud/IMG_0030.HEIC" \
  -frames:v 1 \
  "/srv/Cloud/ffmpeg-0030.jpg"
```

JPEG düzgünse decoder en azından bu dosyayı doğru okuyabiliyor.

## 3. macOS decoder ile karşılaştır

```bash
sips -s format jpeg \
  "/Volumes/Crucial T500/Cloud/IMG_0030.HEIC" \
  --out "/Volumes/Crucial T500/Cloud/mac-test.jpg"
```

Hem FFmpeg hem `sips` düzgünse, orijinal HEIC bozuk değildir.

## 4. File Browser logunu izle

Geçici olarak config'te media debug açılabilir. Ardından:

```bash
docker logs -f filebrowser
```

Canlı log takibinden çıkmak için `Ctrl + C` kullanın.

## 5. 304 vs 200 testi

Gerçek kurulumda eski bozuk preview istekleri `304 Not Modified`, yeni isimli kopyalar ise `200 OK` dönüyordu. Yeni isimli kopyalar düzgün görünüyordu. Bu, stale preview/client cache ihtimalini doğruladı.

## 6. Yeni isimli kopya testi

```bash
cp "/Volumes/Crucial T500/Cloud/IMG_0029.HEIC" \
   "/Volumes/Crucial T500/Cloud/IMG_0029_TEST.HEIC"
```

`_TEST` dosyası düzgün görünüyorsa cache şüphesi güçlenir.

## 7. Cache temizleme

```bash
./scripts/clear-heic-cache.sh
```

Script yalnızca File Browser preview/cache dosyalarını temizler; SSD'deki kullanıcı fotoğraflarını silmez.

## 8. Belirli dosyayı yeniden üretmeye zorlama

```bash
./scripts/refresh-heic-preview.sh "/Volumes/Crucial T500/Cloud/IMG_0029.HEIC"
```

## 9. Tarayıcı tarafı

Son olarak hard refresh (`Cmd + Shift + R`), gerekirse gizli pencere veya site verisi temizleme ile client cache'i de eleyin.

## Neyi yapmadık?

- HEIC dosyalarını otomatik JPEG'e çevirmedik.
- Orijinalleri değiştirmedik.
- iPhone'un fotoğraf formatını kapatmadık.

Orijinal HEIC dosyaları SSD'de aynen kaldı.
