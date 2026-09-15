# 05 — iPhone'dan Tailscale ile uzaktan erişim

Amaç, File Browser'ı genel internete doğrudan açmadan iPhone veya iPad'den erişmektir.

## Kurulum

1. Mac'e Tailscale kurun ve hesabınıza giriş yapın.
2. iPhone/iPad'e Tailscale kurun ve aynı tailnet'e giriş yapın.
3. iOS'un VPN profil iznine izin verin.
4. File Browser'ı önce yerel ağda doğrulayın.
5. Daha sonra Wi‑Fi'yi kapatıp hücresel veri üzerinden Tailscale bağlantısını test edin.

## Neden port yönlendirme yok?

Bu rehberde File Browser ve NAStool servisleri router üzerinden genel internete yayınlanmaz. Tailscale, cihazları özel bir ağda birleştirerek uzaktan erişim sağlar.

## iOS Files + SMB

İsterseniz Mac'te File Sharing özelliğini açıp yalnızca paylaşmak istediğiniz SSD klasörünü SMB ile sunabilirsiniz. iPhone'daki Files uygulamasından `Connect to Server` seçeneği ile Mac'e bağlanabilirsiniz.

## MagicDNS

MagicDNS kullanıyorsanız sayısal Tailscale IP yerine cihaz adını kullanabilirsiniz. İlk teşhis sırasında sayısal adres daha kolay olabilir.

> Gerçek Tailscale IP'nizi veya kimlik doğrulama anahtarlarını repoya eklemeyin.
