# 📚 Manhwa, Manhua & Manga Scraper Pro

Aplikasi web scraper serbaguna yang dirancang khusus untuk mempermudah pengunduhan chapter dari berbagai situs manhwa, manhua, dan manga. Aplikasi ini mengkombinasikan kekuatan backend Python (Flask) dengan frontend interaktif yang melakukan pengemasan ZIP langsung di browser!

**Link Repositori:** [https://github.com/rekhzzz/manhwa-manhua-manga-scraper-by-rekhzz-samasta](https://github.com/rekhzzz/manhwa-manhua-manga-scraper-by-rekhzz-samasta)
**Website Aplikasi (Siap Pakai):** [https://my-manhwa-scraper.vercel.app/](https://my-manhwa-scraper.vercel.app/)

## ✨ Fitur Utama (Web Structure)

Aplikasi ini dibagi menjadi 3 tab utama di antarmuka web, masing-masing dengan kegunaan spesifik:

### 1. 🤖 Auto Scraper
- Cukup masukkan URL chapter dan kode HTML halaman tersebut.
- Sistem akan mengekstrak semua link gambar secara otomatis (termasuk *lazy-loaded images*).
- Gambar diunduh dan dikemas menjadi file **.zip** secara *real-time* langsung di browser kamu (menggunakan `JSZip`).
- Mendukung proxy internal (`/proxy_image`) untuk menghindari blokir CORS atau *Hotlink Protection* dari target situs.

### 2. 🚀 Bypass Injector (Pusat Senjata Bypass)
Beberapa situs memiliki proteksi anti-bot tingkat tinggi yang sulit ditembus server biasa. Fitur ini menyediakan *script* JavaScript siap pakai untuk di-*inject* langsung ke *Console Browser* di situs target:
- **Mode 1 (V3 Direct Download):** Script cepat yang otomatis mencomot semua gambar di halaman yang sedang kamu buka dan langsung mendownloadnya sebagai file ZIP.
- **Mode 2 (V5 Link Extractor):** Script paling ampuh untuk ekstrak URL murni jika Mode V3 terkena *CORS error*. Ekstrak URL, copy, lalu paste di fitur *Link Sorter*.

### 3. 📋 Link Sorter
Sering dapat daftar link gambar yang urutannya berantakan?
- Paste kode HTML atau daftar link murni ke sini.
- **Smart Numerical Sorting:** Fitur ini dapat mendeteksi nomor halaman di dalam nama file gambar dan mengurutkannya secara otomatis dengan benar (misalnya `001.jpg`, `002.jpg`, dst).
- Download hasil yang sudah rapi langsung sebagai file **.zip** atau simpan daftarnya dalam format `.txt`.

## 🛠️ Persyaratan Sistem

- Python 3.8 atau versi yang lebih baru.
- Browser modern (Chrome/Edge/Firefox) untuk menjalankan UI dan JSZip.

## 📦 Instalasi & Cara Menjalankan

1. **Clone repositori ini:**
   ```bash
   git clone https://github.com/rekhzzz/manhwa-manhua-manga-scraper-by-rekhzz-samasta.git
   cd manhwa-manhua-manga-scraper-by-rekhzz-samasta
   ```

2. **Install dependensi Python:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Jalankan Aplikasi:**
   ```bash
   python app.py
   ```
   *Atau klik dua kali pada `Jalankan_Scraper.bat` jika menggunakan Windows.*

4. Aplikasi akan otomatis membuka browser di alamat `http://127.0.0.1:8000`.

## 📁 Struktur Proyek Utama

- `app.py`: Backend server (Flask) yang menangani proxy gambar dan bypass Cloudflare.
- `scraper.py`: Mode CLI alternatif untuk eksekusi via terminal murni.
- `templates/index.html`: Struktur utama Web UI (menampung logika JSZip, Auto Scraper, Injector, Sorter).
- `static/style.css`: Desain UI keren dengan efek Glassmorphism.

## ⚠️ Disclaimer

Alat ini dibuat semata-mata untuk tujuan edukasi, penanganan DOM, dan *network proxying*. Pengguna bertanggung jawab penuh atas segala aktivitas unduhan. Mohon hormati pembuat dan *publisher* resmi dari komik tersebut.

---
Dibuat dengan ❤️ oleh Rekhzz Samasta.🦵🔥
