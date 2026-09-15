# 08 — NAStool Türkçe arayüz patch'i

NAStool'un resmi Türkçe UI seçeneği yoktur. Bu kurulumda iki farklı yaklaşım denendi.

## Riskli yaklaşım: kaynakta global metin değiştirme

Template/static kaynaklarında çok geniş `str.replace()` işlemleri yapmak ilk bakışta hızlı görünür. Fakat tek karakterli Çince eşleşmeler uygulama içindeki JS/Python literal stringlerini de etkileyebilir.

Örneğin karışık çıktılar oluşabilir:

```text
EvetHayır
Yok法
Günlük中心Adres
```

Bu yöntem önerilmez.

## Daha güvenli yaklaşım: DOM çevirisi

Bu repodaki `nastool/nastool_tr_dom_installer.py` script'i görünür DOM metinlerini tarayıcı render ettikten sonra çevirir. Uygulamanın backend iş mantığındaki stringleri toplu şekilde değiştirmez.

Kurulum:

```bash
docker exec -i nas-tools python3 - < nastool/nastool_tr_dom_installer.py
docker restart nas-tools
```

Sonra browser'da hard refresh: `Cmd + Shift + R`.

## Container recreate sonrası kalıcılık

Container içine yazılan `/nas-tools/web` değişiklikleri container recreate edilince kaybolabilir. Çalışan halini host'a çıkarın:

```bash
rm -rf web-tr
docker cp nas-tools:/nas-tools/web ./web-tr
```

`web-tr/` bu repoda `.gitignore` ile dışarıda tutulur; upstream uygulama ağacını repoya kopyalamıyoruz.

Kendi lokal compose'unuzda isterseniz `./web-tr:/nas-tools/web` bind mount'u kullanabilirsiniz.

## Yedek

Patch öncesi:

```bash
./scripts/backup-nastool-web.sh
```

Bir çeviri değişikliği ekranı bozarsa önce son çalışan web ağacına dönün. Küçük, geri alınabilir yamalar daha güvenlidir.
