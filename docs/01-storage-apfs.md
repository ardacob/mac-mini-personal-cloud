# 01 — SSD hazırlığı: NTFS'ten APFS'e

## Belirti

File Browser dosyaları görebiliyor ancak:

- dosya silemiyor,
- klasör oluşturamıyor,
- upload başarısız oluyor.

Önce host tarafında yazma durumunu kontrol edin:

```bash
diskutil info "/Volumes/Crucial T500" | grep -E "File System|Type \(Bundle\)|Read-Only|Writable"
```

Gerçek kurulumda ilk sonuç şuydu:

```text
File System Personality: NTFS
Type (Bundle): ntfs
Media Read-Only: No
Volume Read-Only: Yes (read-only mount flag set)
```

Bu sonuçta sorun Docker veya File Browser kullanıcısı değildir: host işletim sistemi diski read-only bağlamıştır.

## Hangi format?

Mac mini'ye sürekli bağlı kalacak disk için bu rehberde **APFS** kullanıldı.

Windows ve macOS arasında fiziksel olarak sık taşımanız gerekiyorsa exFAT daha uygun olabilir. APFS seçimi bu rehberin “Mac'e sürekli bağlı kişisel bulut diski” senaryosuna göredir.

## Disk Utility ile formatlama

> **UYARI:** Formatlama diskteki tüm verileri siler. Önce yedek alın.

1. Disk Utility açın.
2. View → Show All Devices.
3. Yanlış diski seçmediğinizden emin olun.
4. Harici SSD'nin fiziksel aygıtını seçin.
5. Erase.
6. Name: istediğiniz ad (ör. `Crucial T500`).
7. Format: `APFS`.
8. Scheme: `GUID Partition Map`.

Bittiğinde:

```bash
diskutil info "/Volumes/Crucial T500" | grep -E "File System|Read-Only"
```

Beklenen:

```text
Volume Read-Only: No
```

## Basit yazma testi

```bash
touch "/Volumes/Crucial T500/test-host.txt"
mkdir "/Volumes/Crucial T500/test-host-folder"
rm -f "/Volumes/Crucial T500/test-host.txt"
rmdir "/Volumes/Crucial T500/test-host-folder"
```

Host testi başarısızsa Docker'a geçmeden önce disk sorununu çözün.
