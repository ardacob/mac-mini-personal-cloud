# Contributing / Katkıda Bulunma

[English](#english) • [Türkçe](#türkçe)

## English

This guide grew out of a real-world setup and troubleshooting process. Contributions are very welcome.

- Clearly describe any hardware, macOS, Docker, File Browser, Tailscale, or NAStool differences that may affect the result.
- Do not submit passwords, API keys, real Tailscale IP addresses, private network details, or personal screenshots containing sensitive information.
- For troubleshooting contributions, prefer the format: **symptom → test → finding → solution**.
- For HEIC-related issues, include the File Browser version, FFmpeg version, and the HTTP status returned by the preview endpoint whenever possible.
- Keep fixes reproducible: include the exact command, configuration change, or log line that confirmed the solution.
- Avoid destructive steps unless they are clearly marked and include a backup or rollback note.
- Submit major behavior changes as a separate pull request so they can be reviewed independently.

### Pull requests

Before opening a pull request:

1. Make sure no secrets, personal files, or private addresses are included.
2. Keep the change focused on one problem or improvement.
3. Update the relevant documentation if the setup steps or expected behavior change.
4. Test commands and configuration examples when possible.
5. Explain what was changed, why it was changed, and how it was verified.

Thanks for helping make the guide more accurate and useful for other Mac mini and self-hosting users.

---

## Türkçe

Bu rehber gerçek bir kurulum ve sorun giderme sürecinden doğdu. Katkılar memnuniyetle kabul edilir.

- Sonucu etkileyebilecek donanım, macOS, Docker, File Browser, Tailscale veya NAStool farklarını açıkça belirtin.
- Şifre, API anahtarı, gerçek Tailscale IP adresi, özel ağ bilgisi veya hassas veri içeren kişisel ekran görüntüsü göndermeyin.
- Sorun giderme katkılarında şu formatı tercih edin: **belirti → test → bulgu → çözüm**.
- HEIC ile ilgili sorunlarda mümkünse File Browser sürümünü, FFmpeg sürümünü ve preview endpoint'inin döndürdüğü HTTP durum kodunu ekleyin.
- Çözümleri tekrar üretilebilir tutun: çözümü doğrulayan tam komutu, yapılandırma değişikliğini veya log satırını ekleyin.
- Yıkıcı işlemlerden kaçının; gerekiyorsa işlemi açıkça işaretleyin ve yedekleme veya geri dönüş notu ekleyin.
- Büyük davranış değişikliklerini ayrı bir pull request olarak gönderin; böylece bağımsız olarak incelenebilir.

### Pull request'ler

Bir pull request açmadan önce:

1. Secret, kişisel dosya veya özel ağ adresi bulunmadığından emin olun.
2. Değişikliği tek bir sorun veya iyileştirme etrafında tutun.
3. Kurulum adımları veya beklenen davranış değişiyorsa ilgili dokümantasyonu güncelleyin.
4. Mümkünse komutları ve yapılandırma örneklerini test edin.
5. Neyin değiştiğini, neden değiştiğini ve nasıl doğrulandığını açıklayın.

Rehberin diğer Mac mini ve self-hosting kullanıcıları için daha doğru ve kullanışlı hale gelmesine katkı sağladığınız için teşekkürler.
