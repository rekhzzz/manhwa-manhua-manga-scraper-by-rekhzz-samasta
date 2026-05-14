# 📚 Manhwa Image Scraper Pro

Aplikasi web dan CLI canggih untuk melakukan scraping gambar dari berbagai situs baca manhwa/manga/manhua. Dibangun dengan Python (Flask) dan dilengkapi dengan fitur *bypass protection* yang tangguh.

## ✨ Fitur Unggulan

- **🛡️ Bypass Proteksi (Cloudflare & Hotlink):** Menggunakan `cloudscraper` dan proxy internal untuk melewati proteksi anti-bot dan *hotlink protection* dari situs-situs manhwa.
- **🖼️ Auto-Convert Format Gambar:** Otomatis mendeteksi dan mengonversi format web modern seperti `WebP` dan `AVIF` menjadi `JPG`. Gambar transparan (seperti format RGBA/LA) otomatis diberi latar belakang hitam agar gambar tidak rusak.
- **📂 Auto-Folder Management:** Pintar! Aplikasi akan otomatis membuat folder dengan nama manga dan chapter berdasarkan URL aslinya (contoh: `/downloads/judul-manga/chapter-1`).
- **🚀 Dual Mode (Web UI & CLI):**
  - **Web UI (`app.py`):** Antarmuka pengguna yang modern dan interaktif. Server otomatis membuka browser lokal saat dijalankan. Mendukung *proxying* gambar secara real-time.
  - **CLI Mode (`scraper.py`):** Eksekusi cepat melalui terminal dengan membaca *source* dari `input.html`.
- **⚡ Lazy-Load Support:** Mampu mengekstrak URL gambar sesungguhnya dari atribut seperti `data-src`, `data-lazy-src`, dan `data-srcset` (bukan mengambil gambar placeholder).
- **🌐 Cloud Ready:** Konfigurasi sudah disesuaikan untuk deployment ke layanan serverless seperti **Vercel** (penyesuaian folder `/tmp`).

## 🛠️ Persyaratan Sistem

- Python 3.8 atau versi yang lebih baru.

## 📦 Instalasi

1. **Clone repositori ini:**
   ```bash
   git clone https://github.com/USERNAME_KAMU/my-manhwa-scraper.git
   cd my-manhwa-scraper
   ```
   *(Jangan lupa ubah `USERNAME_KAMU` dengan username GitHub milikmu)*

2. **Install dependensi yang dibutuhkan:**
   ```bash
   pip install -r requirements.txt
   ```
   *Dependensi utama meliputi: Flask, requests, beautifulsoup4, Pillow, cloudscraper.*

## 🚀 Cara Penggunaan

### Mode 1: Menggunakan Web Interface (Rekomendasi)

Jalankan server web lokal dengan perintah:
```bash
python app.py
```
*Atau, kamu bisa cukup klik dua kali pada file `Jalankan_Scraper.bat` (jika menggunakan Windows).*

Server akan berjalan dan otomatis membuka tab baru di browsermu (biasanya di `http://127.0.0.1:8000`). Kamu tinggal mengikuti instruksi di antarmuka web.

### Mode 2: Menggunakan CLI / Terminal

1. Buka halaman chapter manhwa di browsermu.
2. Lakukan *Inspect Element* atau lihat *Page Source*, lalu salin elemen HTML yang berisi gambar-gambarnya.
3. Tempel (paste) HTML tersebut ke dalam file `input.html`.
4. Jalankan script scraper:
   ```bash
   python scraper.py
   ```
5. Saat diminta di terminal, masukkan URL asal (Referer) dari chapter tersebut.
6. Gambar akan mulai diunduh otomatis ke dalam folder `downloads/judul-manga/chapter-XX`.

## 📁 Struktur Direktori

```text
my-manhwa-scraper/
├── app.py                # File utama untuk menjalankan Web UI (Flask)
├── scraper.py            # File utama untuk mode CLI
├── requirements.txt      # Daftar pustaka Python yang dibutuhkan
├── input.html            # File input HTML untuk mode CLI
├── vercel.json           # Konfigurasi deployment untuk Vercel
├── Jalankan_Scraper.bat  # Script cepat untuk menjalankan server (Windows)
├── downloads/            # Direktori hasil unduhan gambar (otomatis dibuat)
├── static/               # File statis web (CSS, JS, dll)
└── templates/            # File template HTML untuk Web UI (index.html)
```

## ⚠️ Disclaimer

Alat ini dibuat semata-mata untuk tujuan edukasi (web scraping, manipulasi gambar dengan Python, dan manajemen network/HTTP). Pengguna bertanggung jawab penuh atas penggunaan alat ini. Mohon gunakan dengan bijak dan selalu hormati hak cipta dari pembuat/pemilik karya.

## 🤝 Kontribusi

Kontribusi untuk pengembangan proyek ini selalu terbuka! Silakan lakukan *Fork*, buat *Branch* baru untuk fiturmu, dan kirimkan *Pull Request*.

---
Dibuat dengan ❤️ untuk kemudahan membaca secara offline.
