# 10 — Kurulum günlüğü: ne denendi, ne işe yaradı?

Bu bölüm yalnızca sonucu değil, teşhis mantığını da belgelemek için yazıldı.

## 1. Compose YAML → zsh

İlk hata compose içeriğinin Terminal'e komut gibi yapıştırılmasıydı. `services:` ve `image:` gibi YAML anahtarları shell komutu değildir.

**Ders:** Önce bloğun shell mi, YAML mı, JSON mu olduğunu ayırın.

## 2. SSD File Browser'da read-only

İlk şüphe container UID/GID oldu. Fakat `diskutil info` host diskin NTFS ve read-only bağlı olduğunu gösterdi.

**Ders:** Önce host storage katmanını test edin; sonra Docker izinlerine geçin.

## 3. APFS sonrası yazma

SSD APFS formatlandıktan sonra `Volume Read-Only: No` görüldü. Klasör oluşturma ve silme çalıştı.

## 4. HEIC: decoder mı cache mi?

Bazı HEIC'ler siyah veya yarım görünüyordu. Manuel FFmpeg ve macOS `sips` dönüşümleri düzgün çıktı. Aynı HEIC yeni isimle kopyalandığında preview da düzgün oldu. Eski preview isteği `304`, yeni kopya ise `200` dönüyordu.

**Sonuç:** Asıl sorun stale preview/cache idi.

## 5. `numImageProcessors: 1`

Image processor sayısını 1'e düşürmek tek başına sorunu çözmedi.

**Ders:** Sonuç vermeyen bir değişikliği kök neden sanmayın.

## 6. Latest → beta image

Beta image da tek başına problemi çözmedi. Sürüm değiştirmekten çok log ve A/B testi belirleyici oldu.

## 7. NAStool Türkçe çeviri

Geniş global source replace karışık stringler üretti. DOM-only yaklaşım daha güvenli çıktı.

## 8. Çalışan yapıyı fazla temizleme girişimi

Birden fazla çeviri script'ini tek yapıya indirme girişimi UI'yı bozdu; yedekten geri dönüldü.

**Ders:** Önce çalışan snapshot alın, sonra küçük ve geri alınabilir değişiklikler yapın.

## 9. Test container → ana container

Yeni File Browser önce ayrı test portunda doğrulandı, sonra ana sisteme geçirildi.

**Ders:** Çalışan sistemi doğrudan değiştirmek yerine test ortamı kullanın.
