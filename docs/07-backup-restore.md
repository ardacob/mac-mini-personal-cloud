# 07 — Yedekleme ve geri dönüş planı

Kurulum sırasında en faydalı alışkanlık: çalışan bir şeyi değiştirmeden önce yedek almak.

## Compose

```bash
cp compose.yaml compose.yaml.backup
```

## NAStool config

```bash
tar -czf "nastool-config-$(date +%Y%m%d-%H%M%S).tar.gz" config
```

## NAStool web arayüzü

Türkçe UI patch gibi container içi değişikliklerden önce:

```bash
./scripts/backup-nastool-web.sh
```

## File Browser database

`filebrowser/data` host'a bind mount edilir. Yedek:

```bash
tar -czf "filebrowser-data-$(date +%Y%m%d-%H%M%S).tar.gz" filebrowser/data
```

## Container image commit hakkında

Gerçek teşhis sürecinde çalışan test container'ını hızlı geri dönüş için lokal image'a commit etmek işe yaradı:

```bash
docker commit filebrowser-heic-test filebrowser-heic-working:local
```

Bu, başka kullanıcılar için taşınabilir bir dağıtım yöntemi değildir. Bu repo resmi image + config ile yeniden üretilebilir kurulum kullanır.

## Geri dönüş prensibi

1. Önce yeni container'ı test portunda çalıştırın.
2. Eski container'ı silmeden durdurun.
3. Yeni yapı doğrulandıktan sonra ana porta geçin.
4. Bir süre eski container'ı yedek adla saklayın.
5. Her şey doğrulanınca temizleyin.
