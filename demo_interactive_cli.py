# Demo Script untuk Autopreneur Interactive CLI

print("""
DEMO: Cara Menggunakan Autopreneur v1.0
========================================

Sekarang Autopreneur menggunakan menu interaktif yang mudah digunakan!
Tidak perlu lagi mengingat command yang rumit.

CARA MENJALANKAN:
----------------
python main.py

TAMPILAN MENU UTAMA:
-------------------
======================================================================
                    🚀 AUTOPRENEUR v1.0 🚀
         AI-Powered Digital Product Generator for UMKM
======================================================================

📊 Status: 2 Signal | 1 Baru | 1 Produk

📋 MENU UTAMA
--------------------------------------------------
1. 🔍 Scan Topik Bisnis Baru
2. 🎯 Generate Produk Digital
3. 📋 Lihat Daftar Signal
4. 📦 Lihat Daftar Produk
5. 📄 Lihat Detail Report
6. ❓ Bantuan & Panduan
7. 🚪 Keluar
--------------------------------------------------

✏️  Masukkan pilihan Anda: _

WORKFLOW SEDERHANA:
------------------
1. Pilih menu 1 untuk scan topik bisnis
   - Masukkan ide bisnis Anda
   - Tunggu 30-60 detik untuk analisis
   - Dapatkan skor 0-100

2. Pilih menu 2 untuk generate produk
   - Lihat signal yang tersedia
   - Pilih otomatis (skor tertinggi) atau manual
   - Tunggu proses generate
   - Produk siap!

3. Pilih menu 4 untuk lihat produk
   - Lihat semua produk yang sudah dibuat
   - Buka folder produk langsung

FITUR BARU:
-----------
✅ Menu interaktif yang user-friendly
✅ Validasi input otomatis
✅ Status tracking real-time
✅ Bantuan terintegrasi
✅ Navigasi yang jelas (termasuk tombol kembali)
✅ Error handling yang lebih baik
✅ Bisa buka folder produk langsung dari menu

TIPS:
-----
• Gunakan angka 1-7 untuk memilih menu
• Ketik 'batal' untuk membatalkan operasi
• Tekan Ctrl+C untuk keluar darurat
• Backup folder 'db' dan 'products' secara berkala

Selamat mencoba! 🚀
""")

# Contoh input/output untuk dokumentasi
example_session = """
CONTOH SESI LENGKAP:
===================

> python main.py

[Menu Utama muncul]

✏️  Masukkan pilihan Anda: 1

🔍 SCAN TOPIK BISNIS BARU
==================================================================
Masukkan topik bisnis yang ingin Anda riset.
Contoh topik yang bagus:
  • ide konten media sosial untuk UMKM kuliner
  • template invoice untuk bisnis online
  • kalender konten ramadan untuk toko muslim

📝 Masukkan topik: ide konten untuk toko fashion muslim

🔄 Sedang menganalisis: 'ide konten untuk toko fashion muslim'
⏳ Proses ini membutuhkan waktu 30-60 detik...

======================================================================
✅ ANALISIS SELESAI!
======================================================================
📊 ID Signal    : abc12345
💡 Topik        : ide konten untuk toko fashion muslim
⭐ Skor Bisnis  : 92/100
📄 Laporan      : db\\report_abc12345.md
======================================================================
🎯 Skor SANGAT BAGUS! Topik ini memiliki potensi bisnis tinggi.

📌 Tekan Enter untuk melanjutkan...

[Kembali ke Menu Utama]

✏️  Masukkan pilihan Anda: 2

🎯 GENERATE PRODUK DIGITAL
======================================================================
Signal yang tersedia untuk di-generate:
----------------------------------------------------------------------
No   Topik                                    Skor       ID        
----------------------------------------------------------------------
1    ide konten untuk toko fashion muslim     92         abc12345  
----------------------------------------------------------------------

📊 Total signal baru: 1

Pilih signal yang ingin di-generate:
1. Otomatis (pilih skor tertinggi)
2. Pilih manual
3. Batal

✏️  Masukkan pilihan Anda: 1

🔥 Memproses: 'ide konten untuk toko fashion muslim'
⭐ Skor: 92

⏳ Generating produk digital...
🤖 AI sedang membuat konten...

======================================================================
🎉 PRODUK BERHASIL DIBUAT!
======================================================================
📦 ID Produk    : prod_xyz789abc123
📌 Nama         : FashionMuslimah Content Creator Pack
📝 Deskripsi    : Paket lengkap konten media sosial untuk toko fashion...

📂 File tersimpan di: products\\prod_xyz789abc123
   • Caption Bank (CSV): caption_bank.csv
   • Panduan (PDF)     : panduan_konten.pdf
======================================================================

📌 Tekan Enter untuk melanjutkan...
"""

print(example_session)
