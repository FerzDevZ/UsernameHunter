# UsernameHunter

[![Python](https://img.shields.io/badge/python-3.8%2B-blue?logo=python)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Contributors](https://img.shields.io/github/contributors/FerzDevZ/UsernameHunter)](https://github.com/FerzDevZ/UsernameHunter/graphs/contributors)
[![Issues](https://img.shields.io/github/issues/FerzDevZ/UsernameHunter)](https://github.com/FerzDevZ/UsernameHunter/issues)
[![Stars](https://img.shields.io/github/stars/FerzDevZ/UsernameHunter?style=social)](https://github.com/FerzDevZ/UsernameHunter)
[![Build Status](https://img.shields.io/github/actions/workflow/status/FerzDevZ/UsernameHunter/python-app.yml?branch=main)](https://github.com/FerzDevZ/UsernameHunter/actions)
[![Streamlit App](https://img.shields.io/badge/Live%20Demo-Streamlit-ff4b4b?logo=streamlit&logoColor=white)](https://usernamehunter.streamlit.app/)

> **UsernameHunter** — Advanced & Modern Username Checker for 200+ Social Media & Viral Sites (Global & Indonesia) 🚀

---

## 🌐 Live Demo

Coba langsung versi web UsernameHunter (tanpa install, gratis!):

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://usernamehunter.streamlit.app/)

[https://usernamehunter.streamlit.app/](https://usernamehunter.streamlit.app/)

---

## 📝 Deskripsi Singkat

UsernameHunter adalah tools open-source untuk cek ketersediaan username di ratusan platform sosial media, marketplace, dan situs viral secara paralel, cepat, dan modern. Mendukung multi-username, plugin, proxy, filter hasil, progress bar, output warna, statistik, chart, logging, wizard interaktif, ekspor hasil ke berbagai format, serta GUI web modern.

---

## ✨ Fitur Utama
- **Cek username** di ratusan platform (global, Indonesia, viral)
- **Multi-username & multi-platform search**
- **Pencarian paralel** (ThreadPoolExecutor)
- **Validasi username otomatis & per platform**
- **Proxy otomatis & retry**
- **Plugin system** (folder plugins/ & custom JSON)
- **Export hasil:** JSON, CSV, TXT, Markdown (.md), HTML (.html), PDF (.pdf)
- **Filter hasil:** hanya ditemukan/tidak ditemukan/gagal
- **Progress bar multi-level** (tqdm & rich.progress)
- **Output warna** (rich, emoji, multi-level)
- **Mode silent & logfile**
- **Riwayat pencarian** (history.jsonl)
- **Statistik hasil & chart** (pie/bar, auto-save PNG)
- **Wizard interaktif** (stub, roadmap)
- **Logging detail** (Python logging)
- **Dokumentasi CLI bilingual, FAQ, tips**
- **Auto-create config** (YAML/JSON)
- **Multi-language CLI & output** (id/en)
- **GUI/Web Interface** (Streamlit, dark mode, monitor, generator, tab, export, chart, dsb)

---

## ⚙️ Cara Kerja
1. User memasukkan username atau file daftar username.
2. Tools melakukan validasi & pencarian paralel ke semua platform.
3. Hasil difilter, divisualisasikan, dan bisa diexport ke berbagai format.
4. Riwayat dan statistik otomatis tersimpan.
5. (Opsional) Notifikasi, monitoring, dan integrasi automation.

---

## 🏗️ Arsitektur Modular

```
app/
├── uh.py                # Main CLI & entrypoint
├── platforms.py         # Daftar platform utama
├── proxy/               # Manajemen proxy
├── validation/          # Validasi username
├── plugins_mod/         # Loader plugin
├── exporter/            # Export hasil
├── search/              # Core search, filter, statistik, riwayat
├── plugins/             # Contoh plugin platform
├── config.json          # Config default
├── history.jsonl        # Riwayat pencarian
├── hasil_chart.png      # Output chart
├── gui/                 # Streamlit & Tkinter GUI
```

---

## 🖥️ GUI/Web Interface (Streamlit)

- Multi-bahasa (Indonesia & English)
- Input username manual & upload file .txt
- Pilih platform (multi-select)
- Advanced options: timeout, max workers, proxy, custom platforms, plugin dir
- Filter hasil (all, only found, only not found, show failed)
- Export hasil ke berbagai format: JSON, CSV, TXT, Markdown, HTML, PDF
- Statistik hasil & chart pie/bar interaktif
- Riwayat pencarian (history.jsonl, download)
- Download hasil & chart langsung dari web
- Tampilan hasil warna, badge status, link langsung ke profil
- Tips, FAQ, dokumentasi singkat di sidebar
- Wizard interaktif (roadmap)
- Notifikasi hasil (toast/success/error)
- Auto-create & load config (upload/download)
- **Dark mode, monitor/auto-refresh, username generator, tab UX**

---

## 🚀 Cara Instalasi & Menjalankan

1. **Clone repository:**
   ```bash
   git clone https://github.com/FerzDevZ/UsernameHunter.git
   cd UsernameHunter/app
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   # Untuk fitur chart: pip install matplotlib
   # Untuk config YAML: pip install pyyaml
   # Untuk output warna: pip install rich
   # Untuk progress bar: pip install tqdm
   # Untuk export Excel: pip install pandas openpyxl
   # Untuk plugin/ekstensi: pip install requests colorama
   ```
3. **Jalankan CLI:**
   ```bash
   python3 uh.py johndoe
   python3 uh.py johndoe janedoe --only-found
   python3 uh.py --username-file daftar.txt --output hasil.json
   python3 uh.py --list-platforms
   python3 uh.py --chart
   ```
4. **Jalankan GUI (Streamlit):**
   ```bash
   python3 uh.py --gui
   # atau langsung
   streamlit run gui/streamlit_app.py
   ```

---

## 📊 Contoh Output & Visualisasi

- Output CLI warna, emoji, badge status, link langsung ke profil
- Export hasil ke JSON, CSV, TXT, Markdown, HTML, PDF
- Statistik summary & chart pie/bar (matplotlib)
- Riwayat pencarian (history.jsonl)
- GUI: hasil interaktif, download, chart, tab, dark mode, dsb

---

## 💡 Tips & Best Practice
- Gunakan `--progress` untuk progress bar modern
- Gunakan `--plugin-dir` untuk menambah platform custom
- Gunakan `--proxy-file` untuk menghindari rate limit/blokir
- Simpan hasil ke file (`--output`) untuk analisis lebih lanjut
- Gunakan `--logfile` dan `--loglevel` untuk debugging/monitoring
- Manfaatkan `--chart` untuk visualisasi hasil
- Gunakan `--config` untuk workflow otomatis
- Cek FAQ, tips, dan troubleshooting jika ada error dependency

---

## ❓ FAQ & Troubleshooting

- **Bagaimana export ke Excel?**
  - Gunakan `--output hasil.xlsx` (fitur segera hadir, sementara gunakan .csv)
- **Bagaimana menambah platform baru?**
  - Tambahkan di custom JSON atau folder plugins.
- **Bagaimana agar hasil hanya ke file, tidak ke layar?**
  - Gunakan `--silent --logfile hasil.log`
- **Bagaimana monitoring otomatis?**
  - Jalankan dengan cron/scheduler dan gunakan `--logfile`.
- **Bagaimana deploy GUI ke internet?**
  - Deploy ke [Streamlit Cloud](https://streamlit.io/cloud) (lihat panduan di bawah).
- **matplotlib error:**
  - Install: `pip install matplotlib`
  - Jika warning headless, chart otomatis disimpan ke PNG
- **pyyaml error:**
  - Install: `pip install pyyaml`
- **rich/tqdm error:**
  - Install: `pip install rich tqdm`
- **Export Excel error:**
  - Install: `pip install pandas openpyxl`

---

## 🌐 Cara Deploy GUI ke Streamlit Cloud

1. Push project ke GitHub (pastikan `app/gui/streamlit_app.py` dan `requirements.txt` ada).
2. Daftar/login di https://streamlit.io/cloud
3. Klik **New app**, pilih repo, branch, dan file utama: `app/gui/streamlit_app.py`
4. Klik **Deploy** dan tunggu build selesai.
5. Akses aplikasi di URL yang diberikan.

> **Tips:**
> - Pastikan semua dependency sudah di `requirements.txt`.
> - File hasil export/history di cloud hanya sementara.
> - Untuk private repo, hubungkan GitHub dan izinkan akses.

---

## 💡 Tips Agar Scraping Lebih Sukses & Minim Error

- Gunakan **proxy premium** (bukan gratisan/cloud) dan aktifkan rotasi proxy otomatis.
- Aktifkan **random User-Agent** di setiap request.
- Tambahkan **delay/jitter acak** antar request (misal 1-3 detik).
- Jika sering rate limit/captcha, aktifkan mode **headless browser** (Selenium/Playwright) dan integrasi anti-captcha API.
- Gunakan **timeout & retry** yang cukup (misal timeout 10 detik, retry 2-3x).
- Jalankan tools di **VPS/PC lokal** (bukan cloud gratisan) untuk hasil maksimal.
- Simpan log error detail untuk troubleshooting.
- Update daftar platform secara berkala.
- Untuk scraping masif, gunakan mode **silent/log only** dan monitoring otomatis (cron/scheduler).

---

## 🏆 Kontribusi & Komunitas
- Join komunitas [ferztap](https://github.com/ferztap) untuk diskusi, plugin, dan update fitur.
- Submit issue, pull request, atau ide fitur baru di GitHub.
- Lihat [Wiki](https://github.com/FerzDevZ/UsernameHunter/wiki) untuk dokumentasi lanjutan.

---

## 📄 Lisensi

MIT License © [FerzDevZ](https://github.com/FerzDevZ) & [ferztap](https://github.com/ferztap)
