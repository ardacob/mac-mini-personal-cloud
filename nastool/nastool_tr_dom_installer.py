#!/usr/bin/env python3
from pathlib import Path
import shutil
import sys

WEB = Path('/nas-tools/web')
STATIC_JS = WEB / 'static' / 'js'
TEMPLATES = WEB / 'templates'
TR_JS = STATIC_JS / 'nastool-tr.js'

if not WEB.exists():
    print('HATA: /nas-tools/web bulunamadı.')
    sys.exit(1)

STATIC_JS.mkdir(parents=True, exist_ok=True)

js = r'''(() => {
  'use strict';

  const MAP = {
    '首页':'Ana Sayfa',
    '我的媒体库':'Medya Kütüphanem',
    '媒体库':'Medya Kütüphanesi',
    '媒体管理':'Medya Yönetimi',
    '媒体整理':'Medya Düzenleme',
    '文件管理':'Dosya Yönetimi',
    '下载管理':'İndirme Yönetimi',
    '订阅管理':'Abonelik Yönetimi',
    '站点管理':'Site Yönetimi',
    '系统设置':'Sistem Ayarları',
    '基础设置':'Temel Ayarlar',
    '服务设置':'Servis Ayarları',
    '插件管理':'Eklenti Yönetimi',
    '用户名':'Kullanıcı Adı',
    '密码':'Şifre',
    '登录':'Giriş Yap',
    '保持登录':'Oturumu Açık Tut',
    '电影':'Filmler',
    '电视剧':'Diziler',
    '搜索':'Ara',
    '下载':'İndir',
    '上传':'Yükle',
    '文件':'Dosya',
    '文件夹':'Klasör',
    '目录':'Dizin',
    '路径':'Yol',
    '转移':'Aktar',
    '重命名':'Yeniden Adlandır',
    '刮削':'Scrape',
    '手动识别':'Manuel Tanıma',
    '保存':'Kaydet',
    '确定':'Tamam',
    '取消':'İptal',
    '添加':'Ekle',
    '编辑':'Düzenle',
    '删除':'Sil',
    '刷新':'Yenile',
    '状态':'Durum',
    '时间':'Zaman',
    '来源':'Kaynak',
    '全部':'Tümü',
    '成功':'Başarılı',
    '失败':'Başarısız',
    '未知':'Bilinmiyor',
    '上级目录':'Üst Dizin',
    'TMDB缓存':'TMDB Önbelleği',
    '清理TMDB缓存':'TMDB Önbelleğini Temizle',
    '清理转移缓存':'Aktarma Önbelleğini Temizle',
    '名称识别测试':'Ad Tanıma Testi',
    '媒体信息':'MEDYA BİLGİSİ',
    '文件信息':'DOSYA BİLGİSİ',
    '通用':'Genel',
    '被替换词':'Değiştirilecek Kelime',
    '替换词':'Yeni Kelime',
    '前定位词':'Ön Konumlandırma Kelimesi',
    '后定位词':'Son Konumlandırma Kelimesi',
    '批量管理':'Toplu Yönetim',
    '未配置':'Yapılandırılmamış',
    '媒体库同步':'Medya Kütüphanesini Senkronize Et',
    '媒体服务器连接失败！':'Medya Sunucusu Bağlantısı Başarısız!'
  };

  const SKIP = new Set(['SCRIPT','STYLE','NOSCRIPT','CODE','PRE','TEXTAREA']);
  const ATTRS = ['placeholder','title','aria-label','data-bs-original-title','data-bs-content'];
  const entries = Object.entries(MAP).sort((a,b) => b[0].length - a[0].length);

  function tr(value) {
    if (!value) return value;
    let out = value;
    for (const [from,to] of entries) {
      if (out.includes(from)) out = out.split(from).join(to);
    }
    out = out.replace(/共\s*(\d+)\s*条记录/g, (_,n) => `Toplam ${n} kayıt`);
    out = out.replace(/共\s*(\d+)\s*个\s*(?:文件|Dosya)/g, (_,n) => `Toplam ${n} dosya`);
    return out;
  }

  function process(root=document.body) {
    if (!root) return;
    const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
    const nodes = [];
    while (walker.nextNode()) nodes.push(walker.currentNode);
    for (const node of nodes) {
      const parent = node.parentElement;
      if (!parent || SKIP.has(parent.tagName)) continue;
      const next = tr(node.nodeValue);
      if (next !== node.nodeValue) node.nodeValue = next;
    }
    document.querySelectorAll('*').forEach(el => {
      for (const attr of ATTRS) {
        if (!el.hasAttribute(attr)) continue;
        const old = el.getAttribute(attr);
        const next = tr(old);
        if (next !== old) el.setAttribute(attr, next);
      }
    });
  }

  let scheduled = false;
  const schedule = () => {
    if (scheduled) return;
    scheduled = true;
    requestAnimationFrame(() => {
      scheduled = false;
      process();
    });
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
      process();
      new MutationObserver(schedule).observe(document.body,{subtree:true,childList:true,characterData:true});
    }, {once:true});
  } else {
    process();
    new MutationObserver(schedule).observe(document.body,{subtree:true,childList:true,characterData:true});
  }
})();'''

TR_JS.write_text(js, encoding='utf-8')
tag = '<script src="/static/js/nastool-tr.js?v=1"></script>'

for name in ['navigation.html', 'login.html']:
    path = TEMPLATES / name
    if not path.exists():
        continue
    text = path.read_text(encoding='utf-8', errors='ignore')
    if 'nastool-tr.js' in text:
        continue
    backup = path.with_suffix(path.suffix + '.trbak')
    if not backup.exists():
        shutil.copy2(path, backup)
    if '</body>' in text:
        text = text.replace('</body>', tag + '\n</body>')
    else:
        text += '\n' + tag + '\n'
    path.write_text(text, encoding='utf-8')

print('NAStool Türkçe DOM çeviricisi kuruldu.')
print('Şimdi: docker restart nas-tools')
print('Ardından tarayıcıda hard refresh yapın.')
