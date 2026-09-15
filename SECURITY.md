# Security Policy

**English** • [Türkçe](#türkçe)

This repository is a self-hosting guide and a collection of helper scripts/configuration examples. It does **not** operate a hosted service and it does not receive or store users' credentials.

## Supported versions

Security-related documentation and fixes are maintained for the current `main` branch and the latest release. Older releases may contain outdated commands, images, defaults, or dependency versions.

## Threat model

The setup is intended for a trusted Mac mini/home server and private remote access. The main risks are:

- accidentally exposing File Browser or NAStool to the public Internet;
- weak/default passwords;
- committing API keys, credentials, private addresses, databases, or configuration backups;
- mounting more host storage into a container than necessary;
- relying on old or archived upstream software;
- running stale container images or dependencies;
- sharing logs/screenshots that contain private information.

## Network exposure

Do **not** forward File Browser or NAStool ports from your router/modem to the public Internet.

This guide uses Tailscale for private remote access. Keep in mind that Docker port publishing such as:

```yaml
ports:
  - "8080:80"
```

normally publishes the service on host network interfaces. Tailscale does not by itself mean that the same Docker port is unreachable from your local network. Use appropriate host firewall rules, Tailscale ACLs/grants, trusted LAN settings, or a reverse proxy/Tailscale Serve design if you need stricter isolation.

HTTP access inside a Tailscale tunnel is protected by the encrypted Tailscale connection between peers, but the same HTTP service must **not** be exposed directly to the public Internet.

## Authentication

- Change all default/admin credentials before enabling remote access.
- Use a long, unique password for File Browser and NAStool.
- Do not reuse the same password as your Apple, GitHub, email, or Tailscale account.
- Enable MFA on GitHub, Tailscale, and other supporting accounts where available.
- Remove or disable unused accounts.

## Secrets and private data

Never commit or publish:

- `.env` files containing real values;
- File Browser databases or session/authentication data;
- NAStool `/config` contents;
- TMDB/OpenAI/other API keys;
- Tailscale auth keys or reusable tokens;
- real passwords or recovery codes;
- private IP addresses, MagicDNS names, device IDs, or tailnet identifiers when they are not needed for the example;
- screenshots containing account names, email addresses, tokens, QR codes, personal photos, or private paths;
- logs that contain secrets, cookies, authorization headers, or private URLs.

Use placeholders such as:

```text
100.x.x.x
example.ts.net
YOUR_API_KEY
YOUR_PASSWORD
```

If a secret is accidentally committed, deleting it from the current file is **not enough**. Revoke/rotate the credential first, then remove it from Git history if appropriate.

## Storage and container permissions

A bind mount gives the container access to the mounted host path. Prefer mounting only the directories the service actually needs instead of an entire disk whenever practical.

Before changing permissions or ownership on an external SSD:

- create a backup;
- verify the exact path;
- avoid recursive `chmod`, `chown`, or destructive commands unless required and understood;
- test write access with a disposable file first.

Do not expose Docker's socket (`/var/run/docker.sock`) to these containers unless you explicitly understand and accept the security implications.

## Container images and dependencies

The example Compose file uses upstream container images. Before production use:

- review the upstream project and image source;
- check release notes before upgrading;
- keep Docker Desktop and container images updated;
- consider pinning a tested version or image digest instead of `latest` when reproducibility is more important than automatic updates;
- back up configuration before image upgrades.

### NAStool legacy warning

NAStool's upstream project is archived and should be treated as **legacy software**. It may no longer receive security fixes. Do not expose it directly to the public Internet, and evaluate whether a maintained alternative is more appropriate for long-term use.

The optional Turkish UI patch in this repository changes presentation-layer files only. Back up the original NAStool web tree before applying it, and review changes before using modified files in a sensitive environment.

## Backups

Security also includes recoverability. Keep backups of:

- important SSD data;
- File Browser configuration/data;
- NAStool configuration;
- working Compose/environment files;
- any local UI patches.

A backup that has never been restored in a test is not a verified backup.

## Reporting a vulnerability

If you find a security issue in the original scripts or configuration provided by this repository:

1. **Do not** post active credentials, private addresses, exploit payloads, or sensitive logs in a public issue.
2. Prefer GitHub's private vulnerability reporting / Security Advisory flow if it is available for this repository.
3. If no private reporting channel is available, open a minimal public issue asking for a private contact method **without including vulnerability details**.
4. Include the affected file/version, impact, reproduction conditions, and a safe proof of concept when possible.

For vulnerabilities in Docker, Tailscale, File Browser, NAStool, FFmpeg, macOS, or another upstream dependency, report the issue to the relevant upstream project as well.

## Scope

Configuration mistakes caused by intentionally exposing ports, publishing secrets, disabling authentication, or ignoring documented warnings are not vulnerabilities in this repository itself. Documentation that could reasonably lead users into an unsafe default is still worth reporting and will be treated seriously.

---

# Türkçe

Bu repo bir self-hosting rehberi ile yardımcı script/yapılandırma örnekleri içerir. Herhangi bir barındırılan servis işletmez ve kullanıcıların kimlik bilgilerini almaz veya saklamaz.

## Desteklenen sürümler

Güvenlikle ilgili dokümantasyon ve düzeltmeler güncel `main` branch'i ve en son release için tutulur. Eski sürümlerde artık güncel olmayan komutlar, image'lar, varsayılanlar veya bağımlılık sürümleri bulunabilir.

## Tehdit modeli

Kurulum, güvenilen bir Mac mini/ev sunucusu ve özel uzaktan erişim için tasarlanmıştır. Başlıca riskler şunlardır:

- File Browser veya NAStool'u yanlışlıkla açık internete sunmak;
- zayıf/varsayılan parolalar kullanmak;
- API anahtarı, kimlik bilgisi, özel adres, veritabanı veya config yedeğini repoya göndermek;
- container'a gerekenden daha geniş host depolama erişimi vermek;
- eski veya arşivlenmiş upstream yazılımlara güvenmek;
- eski container image/bağımlılıklarını kullanmak;
- özel bilgi içeren log veya ekran görüntüsü paylaşmak.

## Ağ erişimi

File Browser veya NAStool portlarını modem/router üzerinden doğrudan internete **port forward etmeyin**.

Bu rehber özel uzaktan erişim için Tailscale kullanır. Ancak Docker'daki şu tür bir port yayınının:

```yaml
ports:
  - "8080:80"
```

genellikle servisi host'un ağ arayüzlerinde yayınladığını unutmayın. Tailscale kullanıyor olmanız aynı Docker portunun yerel ağdan otomatik olarak erişilemez olduğu anlamına gelmez. Daha sıkı izolasyon gerekiyorsa host firewall kuralları, Tailscale ACL/grants, güvenilir LAN ayarları veya reverse proxy/Tailscale Serve yaklaşımı kullanın.

Tailscale tüneli içindeki HTTP trafiği eşler arasındaki şifreli Tailscale bağlantısı ile korunur; ancak aynı HTTP servisini doğrudan açık internete sunmayın.

## Kimlik doğrulama

- Uzaktan erişimi açmadan önce tüm varsayılan/admin parolalarını değiştirin.
- File Browser ve NAStool için uzun ve benzersiz parola kullanın.
- Apple, GitHub, e-posta veya Tailscale hesabınızdaki parolayı tekrar kullanmayın.
- Mümkün olan GitHub, Tailscale ve diğer destekleyici hesaplarda MFA açın.
- Kullanılmayan hesapları kaldırın veya devre dışı bırakın.

## Gizli ve özel veriler

Şunları asla commit etmeyin veya yayınlamayın:

- gerçek değerler içeren `.env` dosyaları;
- File Browser veritabanı veya oturum/kimlik doğrulama verileri;
- NAStool `/config` içeriği;
- TMDB/OpenAI/diğer API anahtarları;
- Tailscale auth key veya tekrar kullanılabilir token'lar;
- gerçek parolalar ve kurtarma kodları;
- örnek için gerekli değilse özel IP'ler, MagicDNS adları, cihaz ID'leri veya tailnet bilgileri;
- hesap adı, e-posta, token, QR kod, kişisel fotoğraf veya özel yol içeren ekran görüntüleri;
- secret, cookie, authorization header veya özel URL içeren loglar.

Örneklerde şu tür placeholder'lar kullanın:

```text
100.x.x.x
example.ts.net
YOUR_API_KEY
YOUR_PASSWORD
```

Bir secret yanlışlıkla commit edilirse yalnızca güncel dosyadan silmek **yeterli değildir**. Önce ilgili credential'ı iptal edin/yenileyin; gerekiyorsa daha sonra Git geçmişinden temizleyin.

## Depolama ve container izinleri

Bind mount, container'a bağlanan host yoluna erişim verir. Mümkün olduğunda tüm diski bağlamak yerine servisin gerçekten ihtiyaç duyduğu klasörleri mount edin.

Harici SSD'nin izin veya sahipliğini değiştirmeden önce:

- yedek alın;
- doğru path üzerinde olduğunuzu doğrulayın;
- gerekmiyorsa recursive `chmod`, `chown` veya yıkıcı komutlar kullanmayın;
- önce geçici bir dosya ile yazma testini yapın.

Güvenlik etkilerini açıkça anlamadığınız sürece Docker socket'ini (`/var/run/docker.sock`) bu container'lara bağlamayın.

## Container image'ları ve bağımlılıklar

Örnek Compose dosyası upstream container image'larını kullanır. Kalıcı kullanım öncesinde:

- upstream proje ve image kaynağını inceleyin;
- yükseltme öncesinde release notlarını kontrol edin;
- Docker Desktop ve container image'larını güncel tutun;
- tekrar üretilebilirlik otomatik güncellemeden daha önemliyse `latest` yerine test edilmiş bir sürüm veya image digest sabitlemeyi düşünün;
- image yükseltmelerinden önce config yedeği alın.

### NAStool legacy uyarısı

NAStool'un upstream projesi arşivlenmiştir ve **legacy yazılım** olarak değerlendirilmelidir. Artık güvenlik güncellemesi almıyor olabilir. Doğrudan açık internete sunmayın ve uzun vadede bakımı devam eden bir alternatifin daha uygun olup olmadığını değerlendirin.

Bu repodaki isteğe bağlı Türkçe UI patch'i yalnızca sunum katmanı dosyalarını değiştirir. Uygulamadan önce orijinal NAStool web ağacını yedekleyin ve hassas bir ortamda kullanmadan önce değişiklikleri inceleyin.

## Yedekler

Güvenliğin bir parçası da geri dönebilmektir. Şunların yedeğini tutun:

- önemli SSD verileri;
- File Browser yapılandırma/verileri;
- NAStool yapılandırması;
- çalışan Compose/environment dosyaları;
- yerel UI patch'leri.

Geri yükleme testi yapılmamış bir yedek doğrulanmış sayılmaz.

## Güvenlik açığı bildirimi

Bu repodaki özgün script veya yapılandırmada bir güvenlik problemi bulursanız:

1. Aktif credential, özel adres, exploit payload veya hassas logları public issue'ya **koymayın**.
2. Bu repo için kullanılabiliyorsa GitHub'ın private vulnerability reporting / Security Advisory akışını tercih edin.
3. Özel kanal yoksa güvenlik açığı detaylarını paylaşmadan, özel iletişim yöntemi isteyen minimum bilgilerle public issue açın.
4. Mümkünse etkilenen dosya/sürüm, etki, tekrar üretme koşulları ve güvenli bir proof of concept ekleyin.

Docker, Tailscale, File Browser, NAStool, FFmpeg, macOS veya başka bir upstream bağımlılıktaki güvenlik açığını ilgili upstream projeye de bildirin.

## Kapsam

Portları bilerek internete açmak, secret yayınlamak, kimlik doğrulamayı kapatmak veya dokümante edilmiş uyarıları yok saymak sonucu oluşan yapılandırma hataları bu reponun güvenlik açığı sayılmaz. Buna rağmen kullanıcıyı makul biçimde güvensiz bir varsayılana yönlendirebilecek dokümantasyon hataları bildirilebilir ve ciddiyetle ele alınır.
