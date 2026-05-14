import os
import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import urlparse
from PIL import Image
import io

# Konfigurasi
INPUT_FILE = 'input.html'

def get_image_url(tag):
    """
    Ekstrak URL dari tag img dengan mengecek berbagai atribut lazy-load.
    """
    attributes = ['data-src', 'data-lazy-src', 'data-original', 'data-srcset', 'src']
    
    for attr in attributes:
        url = tag.get(attr)
        if url:
            if attr == 'data-srcset':
                url = url.split(',')[0].split(' ')[0]
            
            url = url.strip()
            if url.startswith('//'):
                url = 'https:' + url
            
            if url.startswith('http') and not any(ext in url.lower() for ext in ['.ico', '.gif', 'logo', 'avatar']):
                return url
    return None

def get_folder_name_from_url(url):
    """
    Mengekstrak nama manga dan chapter dari URL untuk jadi nama folder.
    """
    try:
        path = urlparse(url).path.strip('/')
        parts = path.split('/')
        # Biasanya manhwa sites punya struktur /manga/judul/chapter/
        if len(parts) >= 2:
            # Menggabungkan nama manga dan chapter (misal: go-deok-chuns-food-truck/chapter-26)
            return os.path.join(parts[-2], parts[-1])
        elif len(parts) == 1:
            return parts[0]
    except:
        pass
    return 'chapter_images'

def download_images():
    print("=== Manhwa Image Scraper (Auto-Folder) ===")
    
    # Input Referer dari user
    referer_url = input("[?] Masukkan URL Halaman Chapter (contoh: https://kunmanga.com/.../): ").strip()
    
    if not referer_url:
        print("[!] URL wajib diisi agar bisa menentukan folder dan melewati proteksi!")
        return

    # Tentukan folder berdasarkan URL
    folder_name = get_folder_name_from_url(referer_url)
    current_download_dir = os.path.join('downloads', folder_name)

    if not os.path.exists(current_download_dir):
        os.makedirs(current_download_dir)
        print(f"[*] Folder dibuat: {current_download_dir}")
    else:
        print(f"[*] Menggunakan folder yang sudah ada: {current_download_dir}")
    
    if not os.path.exists(INPUT_FILE):
        print(f"[!] File {INPUT_FILE} tidak ditemukan.")
        return

    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, 'html.parser')
    img_tags = soup.find_all('img')

    image_urls = []
    for tag in img_tags:
        url = get_image_url(tag)
        if url and url not in image_urls:
            image_urls.append(url)

    if not image_urls:
        print("[!] Tidak ada gambar ditemukan di input.html.")
        return

    print(f"[*] Menemukan {len(image_urls)} gambar. Memulai pengunduhan...")

    # Header yang lebih lengkap untuk melewati proteksi
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9,id;q=0.8',
        'Referer': referer_url,
        'Connection': 'keep-alive',
    }

    session = requests.Session()

    for i, url in enumerate(image_urls, 1):
        path = urlparse(url).path.lower()
        original_ext = '.jpg'
        if path.endswith('.png'): original_ext = '.png'
        elif path.endswith('.webp'): original_ext = '.webp'
        elif path.endswith('.jpeg'): original_ext = '.jpeg'

        # Jika webp, kita akan ubah jadi jpg
        save_ext = '.jpg' if original_ext == '.webp' else original_ext
        filename = f"{i:03d}{save_ext}"
        filepath = os.path.join(current_download_dir, filename)

        try:
            print(f"[{i}/{len(image_urls)}] Mengunduh: {filename}...", end='\r')
            response = session.get(url, headers=headers, timeout=20)
            response.raise_for_status()

            # Gunakan Pillow untuk mendeteksi format asli dari konten
            img_data = io.BytesIO(response.content)
            try:
                img = Image.open(img_data)
                real_format = img.format.upper() if img.format else ""
            except:
                real_format = ""

            # Daftar format yang ingin kita ubah ke JPG (WebP, AVIF, dll)
            target_conversion_formats = ['WEBP', 'AVIF']

            if real_format in target_conversion_formats:
                # Konversi ke JPG
                if img.mode in ("RGBA", "P", "LA"):
                    # Buat background hitam untuk gambar transparan
                    background = Image.new("RGB", img.size, (0, 0, 0))
                    if img.mode == "RGBA":
                        background.paste(img, mask=img.split()[3])
                    elif img.mode == "LA":
                        background.paste(img, mask=img.split()[1])
                    else:
                        background.paste(img)
                    img = background
                elif img.mode != "RGB":
                    img = img.convert("RGB")
                
                # Pastikan ekstensi file adalah .jpg
                if not filepath.lower().endswith('.jpg'):
                    filepath = os.path.splitext(filepath)[0] + '.jpg'
                    
                img.save(filepath, "JPEG", quality=95)
            else:
                # Jika bukan WebP/AVIF, simpan apa adanya (JPG asli atau PNG)
                with open(filepath, 'wb') as f:
                    f.write(response.content)
            
            time.sleep(0.3)
        except Exception as e:
            print(f"\n[!] Gagal mengunduh {url}: {e}")

    print(f"\n[+] Selesai! Cek folder: {current_download_dir}")

if __name__ == "__main__":
    download_images()
