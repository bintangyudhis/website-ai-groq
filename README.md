# website-ai-groq

Aplikasi web chat AI berbasis Flask yang terhubung ke API Groq. Pengunjung dapat bertukar pesan dengan model bahasa dari Groq melalui halaman chat yang sederhana. Seluruh riwayat percakapan dikirim pada setiap permintaan, jadi asisten dapat menanggapi lanjutan dari obrolan yang sama selama sesi berlangsung.

## Fitur

- Halaman chat dengan daftar pesan, kolom ketik, dan tombol kirim
- Indikator mengetik saat menunggu jawaban dari Groq
- Riwayat percakapan dipertahankan selama sesi halaman dibuka
- Tombol percakapan baru untuk mengosongkan obrolan dan mulai dari awal
- Pemanggilan Groq API melalui endpoint chat completions yang kompatibel dengan OpenAI
- Model dapat diganti lewat variabel lingkungan GROQ_MODEL, bawaan llama-3.3-70b-versatile
- Pesan pemberitahuan yang ramah bila kunci API belum diatur, tanpa menampilkan galat mentah
- Tampilan responsif untuk layar kecil dan besar

## Teknologi

- Python 3.10 atau lebih baru
- Flask 3.1
- Requests untuk memanggil Groq API
- HTML, CSS, dan JavaScript murni tanpa CDN
- Groq API dengan model llama-3.3-70b-versatile sebagai bawaan

## Cara Instalasi

Prasyarat:

- Python 3.10 atau lebih baru
- pip
- Kunci API Groq

Langkah instalasi:

1. Clone repositori ini lalu masuk ke folder proyek.

   ```bash
   git clone https://github.com/bintangyudhis/website-ai-groq.git
   cd website-ai-groq
   ```

2. Buat dan aktifkan lingkungan virtual.

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

   Di Windows, aktifkan dengan perintah `venv\Scripts\activate`.

3. Pasang dependensi.

   ```bash
   pip install -r requirements.txt
   ```

4. Salin berkas contoh konfigurasi menjadi .env lalu isi kunci API Anda.

   ```bash
   cp .env.example .env
   ```

   Isi variabel GROQ_API_KEY di dalam berkas .env dengan kunci Anda. Variabel GROQ_MODEL boleh diganti bila ingin memakai model Groq lain, dan PORT boleh diubah bila port bawaan 5000 sedang terpakai.

### Mendapatkan kunci API Groq

1. Buka https://console.groq.com lalu masuk atau daftar akun.
2. Buka halaman API Keys di https://console.groq.com/keys.
3. Buat kunci baru, salin nilainya, lalu tempel ke variabel GROQ_API_KEY pada berkas .env.

Jangan pernah membagikan kunci API Anda atau menulisnya langsung di dalam kode.

## Cara Menjalankan

```bash
python main.py
```

Aplikasi berjalan di http://localhost:5000. Buka alamat itu di peramban, tulis pesan pada kolom di bagian bawah halaman, lalu tekan Enter atau tombol Kirim.

Bila kunci API belum diatur, aplikasi tetap berjalan dan menampilkan pemberitahuan bahwa kunci belum diisi. Isi berkas .env terlebih dahulu agar asisten dapat menjawab.

Menjalankan dengan Docker:

```bash
docker build -t website-ai-groq .
docker run -p 5000:5000 -e GROQ_API_KEY=isi_kunci_anda website-ai-groq
```

## Tangkapan Layar

![Tangkapan layar halaman chat](docs/screenshot.png)

## Lisensi

Proyek ini memakai lisensi MIT. Lihat berkas [LICENSE](LICENSE).
