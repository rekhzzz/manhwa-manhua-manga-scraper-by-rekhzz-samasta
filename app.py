import os
import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import urlparse
import urllib.request
from flask import Flask, render_template, request, Response, jsonify, send_from_directory
import threading
import webbrowser
import socket
from PIL import Image
import io
import urllib3
import re
import ssl
import cloudscraper

# Disable insecure request warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = Flask(__name__)

# Create a cloudscraper instance
scraper = cloudscraper.create_scraper(
    browser={
        'browser': 'chrome',
        'platform': 'windows',
        'desktop': True
    }
)

# Konfigurasi Dasar
# Vercel menggunakan /tmp untuk penyimpanan sementara
if os.environ.get('VERCEL') or os.path.exists('/tmp'):
    DOWNLOAD_BASE_DIR = os.path.join(tempfile.gettempdir(), 'scraper_downloads') if 'tempfile' in globals() else '/tmp/scraper_downloads'
else:
    DOWNLOAD_BASE_DIR = 'downloads'

if not os.path.exists(DOWNLOAD_BASE_DIR):
    try:
        os.makedirs(DOWNLOAD_BASE_DIR, exist_ok=True)
    except:
        pass

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

def get_image_url(tag):
    attributes = ['data-src', 'data-lazy-src', 'data-original', 'data-srcset', 'src', 'data-actualsrc']
    for attr in attributes:
        url = tag.get(attr)
        if url:
            if attr == 'data-srcset':
                url = url.split(',')[0].split(' ')[0]
            url = "".join(url.split())
            if url.startswith('//'):
                url = 'https:' + url
            if url.startswith('http') and not any(ext in url.lower() for ext in ['.ico', '.gif', 'logo', 'avatar']):
                return url
    return None

def get_folder_name_from_url(url):
    try:
        path = urlparse(url).path.strip('/')
        parts = path.split('/')
        if len(parts) >= 2:
            return os.path.join(parts[-2], parts[-1])
        elif len(parts) == 1:
            return parts[0]
    except:
        pass
    return 'chapter_images'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def scrape():
    data = request.json
    html_content = data.get('html_content', '')
    referer_url = data.get('referer_url', '').strip()

    if not html_content or not referer_url:
        return jsonify({"error": "HTML dan URL wajib diisi"}), 400

    image_urls = []
    soup = BeautifulSoup(html_content, 'html.parser')
    img_tags = soup.find_all('img')
    
    for tag in img_tags:
        url = get_image_url(tag)
        if url and url not in image_urls:
            image_urls.append(url)
    
    if not image_urls:
        urls_found = re.findall(r'https?://[^\s<>"]+|//[^\s<>"]+', html_content)
        for url in urls_found:
            url = url.strip()
            if url.startswith('//'): url = 'https:' + url
            if any(ext in url.lower() for ext in ['.jpg', '.jpeg', '.png', '.webp', '.avif']):
                if url not in image_urls: image_urls.append(url)
    
    if not image_urls:
        return jsonify({"error": "Tidak ada gambar ditemukan"}), 404

    folder_name = get_folder_name_from_url(referer_url)
    return jsonify({"image_urls": image_urls, "folder_name": folder_name})

@app.route('/proxy_image')
def proxy_image():
    url = request.args.get('url')
    referer = request.args.get('referer')
    if not url: return "Missing URL", 400

    url = "".join(url.split())
    
    headers = {
        'Referer': referer if referer else url,
        'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9,id;q=0.8',
    }

    try:
        response = scraper.get(url, headers=headers, timeout=25)
        if response.status_code == 200:
            return Response(response.content, mimetype=response.headers.get('Content-Type', 'image/jpeg'))
    except:
        pass

    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/121.0.0.0 Safari/537.36', 'Referer': referer if referer else url})
        with urllib.request.urlopen(req, context=ctx, timeout=20) as response:
            return Response(response.read(), mimetype='image/jpeg')
    except Exception as e:
        return str(e), 500

@app.route('/download/<path:filename>')
def download_file(filename):
    return send_from_directory(DOWNLOAD_BASE_DIR, filename, as_attachment=True)

if __name__ == '__main__':
    # Only run this if we are local (not on Vercel)
    if not os.environ.get('VERCEL'):
        local_ip = get_local_ip()
        print(f"\nMANHWA SCRAPER PRO AKTIF! URL: http://{local_ip}:8000\n")
        
        def open_browser():
            time.sleep(1.5)
            webbrowser.open("http://127.0.0.1:8000")
            
        threading.Thread(target=open_browser).start()
        app.run(host='0.0.0.0', port=8000, debug=False)
    else:
        app.run()
