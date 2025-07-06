# main.py
import os
import json
import uuid
from pathlib import Path
import csv
import sys
import time
from typing import Optional, Dict, List

# Import untuk PDF
from jinja2 import Environment, FileSystemLoader, select_autoescape
from weasyprint import HTML

from agents import AnalystAgent, BuilderAgent

# --- KONFIGURASI ---
DB_DIR = Path("db")
PRODUCTS_DIR = Path("products")
SIGNALS_DB_PATH = DB_DIR / "signals.json"
PRODUCTS_DB_PATH = DB_DIR / "products.json"

# --- FUNGSI UTILITAS ---
def ensure_setup():
    """Memastikan folder dan file DB yang dibutuhkan ada."""
    DB_DIR.mkdir(exist_ok=True)
    PRODUCTS_DIR.mkdir(exist_ok=True)
    Path("templates").mkdir(exist_ok=True)
    if not SIGNALS_DB_PATH.exists():
        SIGNALS_DB_PATH.write_text("[]", encoding="utf-8")
    if not PRODUCTS_DB_PATH.exists():
        PRODUCTS_DB_PATH.write_text("[]", encoding="utf-8")

def load_db(path: Path):
    """Membaca data dari file JSON."""
    if not path.exists() or path.stat().st_size == 0:
        return []
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"⚠️  Peringatan: File {path.name} korup, menganggap sebagai list kosong.")
        return []

def save_db(path: Path, data):
    """Menyimpan data ke file JSON."""
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def clear_screen():
    """Membersihkan layar terminal."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Menampilkan header aplikasi."""
    clear_screen()
    print("=" * 70)
    print("                    🚀 AUTOPRENEUR v1.0 🚀")
    print("         AI-Powered Digital Product Generator for UMKM")
    print("=" * 70)
    print()

def print_menu(title: str, options: List[str], back_option: bool = True):
    """Menampilkan menu dengan format yang konsisten."""
    print(f"\n📋 {title}")
    print("-" * 50)
    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")
    if back_option:
        print(f"{len(options) + 1}. ⬅️  Kembali")
    print("-" * 50)

def get_choice(max_choice: int, has_back: bool = True) -> Optional[int]:
    """Mendapatkan pilihan dari user dengan validasi."""
    actual_max = max_choice + 1 if has_back else max_choice
    while True:
        try:
            choice = input("\n✏️  Masukkan pilihan Anda: ").strip()
            if not choice:
                continue
            choice_num = int(choice)
            if 1 <= choice_num <= actual_max:
                return choice_num
            else:
                print(f"❌ Pilihan harus antara 1-{actual_max}")
        except ValueError:
            print("❌ Masukkan angka yang valid")

def pause():
    """Pause sebelum melanjutkan."""
    input("\n📌 Tekan Enter untuk melanjutkan...")

# --- FUNGSI BARU UNTUK PDF ---
def write_pdf(product_folder: Path, assets: dict) -> Path:
    """Render template Jinja2 menjadi file PDF menggunakan WeasyPrint."""
    print("📄 Merender file PDF...")
    env = Environment(
        loader=FileSystemLoader("templates"),
        autoescape=select_autoescape(["html"])
    )
    template = env.get_template("umkm_productivity/caption_bank.html")
    html_content = template.render(**assets)
    
    pdf_path = product_folder / "panduan_konten.pdf"
    HTML(string=html_content).write_pdf(pdf_path)
    print(f"✅ File PDF disimpan di: {pdf_path}")
    return pdf_path

# --- FUNGSI MENU ---
def menu_scan_topic():
    """Menu untuk scan topik bisnis."""
    print_header()
    print("🔍 SCAN TOPIK BISNIS BARU")
    print("=" * 70)
    print("\nMasukkan topik bisnis yang ingin Anda riset.")
    print("Contoh topik yang bagus:")
    print("  • ide konten media sosial untuk UMKM kuliner")
    print("  • template invoice untuk bisnis online")
    print("  • kalender konten ramadan untuk toko muslim")
    print("  • hashtag strategy untuk jualan di Shopee")
    print("  • SOP untuk restoran padang")
    print("\nKetik 'batal' untuk kembali ke menu utama.")
    print("-" * 70)
    
    topic = input("\n📝 Masukkan topik: ").strip()
    
    if topic.lower() == 'batal':
        return
    
    if not topic:
        print("❌ Topik tidak boleh kosong!")
        pause()
        return
    
    print(f"\n🔄 Sedang menganalisis: '{topic}'")
    print("⏳ Proses ini membutuhkan waktu 30-60 detik...")
    
    try:
        analyst = AnalystAgent()
        report_text = analyst.research_topic(topic)
        score = analyst.score_idea(report_text)
        signal_id = str(uuid.uuid4())[:8]
        report_file = DB_DIR / f"report_{signal_id}.md"
        report_file.write_text(report_text, encoding="utf-8")
        
        new_signal = {
            "id": signal_id,
            "topic": topic,
            "score": score,
            "status": "new",
            "report_file": str(report_file)
        }
        
        signals = load_db(SIGNALS_DB_PATH)
        signals.append(new_signal)
        save_db(SIGNALS_DB_PATH, signals)
        
        print("\n" + "=" * 70)
        print("✅ ANALISIS SELESAI!")
        print("=" * 70)
        print(f"📊 ID Signal    : {signal_id}")
        print(f"💡 Topik        : {topic}")
        print(f"⭐ Skor Bisnis  : {score}/100")
        print(f"📄 Laporan      : {report_file}")
        print("=" * 70)
        
        if score >= 80:
            print("🎯 Skor SANGAT BAGUS! Topik ini memiliki potensi bisnis tinggi.")
        elif score >= 60:
            print("👍 Skor BAGUS. Topik ini layak untuk dikembangkan.")
        else:
            print("🤔 Skor SEDANG. Pertimbangkan untuk riset topik lain.")
            
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
    
    pause()

def menu_generate_product():
    """Menu untuk generate produk."""
    print_header()
    signals = load_db(SIGNALS_DB_PATH)
    new_signals = [s for s in signals if s['status'] == 'new']
    
    if not new_signals:
        print("⚠️  TIDAK ADA SIGNAL BARU")
        print("=" * 70)
        print("Anda perlu melakukan scan topik terlebih dahulu.")
        print("Kembali ke menu utama dan pilih 'Scan Topik Bisnis Baru'.")
        pause()
        return
    
    print("🎯 GENERATE PRODUK DIGITAL")
    print("=" * 70)
    print("\nSignal yang tersedia untuk di-generate:")
    print("-" * 70)
    print(f"{'No':<4} {'Topik':<40} {'Skor':<10} {'ID':<10}")
    print("-" * 70)
    
    for i, signal in enumerate(new_signals, 1):
        topic_short = signal['topic'][:37] + "..." if len(signal['topic']) > 40 else signal['topic']
        print(f"{i:<4} {topic_short:<40} {signal['score']:<10} {signal['id']:<10}")
    
    print("-" * 70)
    print(f"\n📊 Total signal baru: {len(new_signals)}")
    
    # Pilih signal
    print("\nPilih signal yang ingin di-generate:")
    print("1. Otomatis (pilih skor tertinggi)")
    print("2. Pilih manual")
    print("3. Batal")
    
    choice = get_choice(3, has_back=False)
    
    if choice == 3:
        return
    
    if choice == 1:
        selected_signal = max(new_signals, key=lambda s: s['score'])
    else:
        print(f"\nMasukkan nomor signal (1-{len(new_signals)}): ", end="")
        signal_choice = get_choice(len(new_signals), has_back=False)
        if not signal_choice:
            return
        selected_signal = new_signals[signal_choice - 1]
    
    print(f"\n🔥 Memproses: '{selected_signal['topic']}'")
    print(f"⭐ Skor: {selected_signal['score']}")
    print("\n⏳ Generating produk digital...")
    print("🤖 AI sedang membuat konten...")
    
    try:
        builder = BuilderAgent()
        assets = builder.generate_product_assets(selected_signal['topic'], "caption_bank")
        
        if not assets:
            print("❌ Gagal membuat aset produk.")
            pause()
            return
        
        product_id = f"prod_{uuid.uuid4().hex[:12]}"
        product_folder = PRODUCTS_DIR / product_id
        product_folder.mkdir()
        
        # 1. Simpan file CSV
        csv_path = product_folder / "caption_bank.csv"
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['day', 'text'])
            writer.writeheader()
            writer.writerows(assets['captions'])
        
        # 2. Simpan file PDF
        pdf_path = write_pdf(product_folder, assets)
        
        # 3. Update database
        new_product = {
            "id": product_id,
            "signal_id": selected_signal['id'],
            "name": assets['name'],
            "description": assets['description'],
            "files": {
                "csv": str(csv_path),
                "pdf": str(pdf_path)
            }
        }
        
        products = load_db(PRODUCTS_DB_PATH)
        products.append(new_product)
        save_db(PRODUCTS_DB_PATH, products)
        
        # Update status signal
        for s in signals:
            if s['id'] == selected_signal['id']:
                s['status'] = 'generated'
        save_db(SIGNALS_DB_PATH, signals)
        
        print("\n" + "=" * 70)
        print("🎉 PRODUK BERHASIL DIBUAT!")
        print("=" * 70)
        print(f"📦 ID Produk    : {product_id}")
        print(f"📌 Nama         : {assets['name']}")
        print(f"📝 Deskripsi    : {assets['description'][:60]}...")
        print(f"\n📂 File tersimpan di: {product_folder}")
        print(f"   • Caption Bank (CSV): {csv_path.name}")
        print(f"   • Panduan (PDF)     : {pdf_path.name}")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
    
    pause()

def menu_view_signals():
    """Menu untuk melihat daftar signal."""
    print_header()
    print("📊 DAFTAR SIGNAL RISET")
    print("=" * 70)
    
    signals = load_db(SIGNALS_DB_PATH)
    
    if not signals:
        print("📭 Belum ada signal yang tersimpan.")
        print("\nMulai dengan scan topik bisnis baru!")
        pause()
        return
    
    # Kelompokkan berdasarkan status
    new_signals = [s for s in signals if s['status'] == 'new']
    generated_signals = [s for s in signals if s['status'] == 'generated']
    
    if new_signals:
        print("\n🆕 SIGNAL BARU (Belum di-generate):")
        print("-" * 70)
        print(f"{'ID':<10} {'Topik':<35} {'Skor':<10} {'Report':<15}")
        print("-" * 70)
        for signal in new_signals:
            topic_short = signal['topic'][:32] + "..." if len(signal['topic']) > 35 else signal['topic']
            report_name = Path(signal['report_file']).name
            print(f"{signal['id']:<10} {topic_short:<35} {signal['score']:<10} {report_name:<15}")
    
    if generated_signals:
        print(f"\n✅ SIGNAL SUDAH DI-GENERATE ({len(generated_signals)} produk):")
        print("-" * 70)
        print(f"{'ID':<10} {'Topik':<35} {'Skor':<10} {'Report':<15}")
        print("-" * 70)
        for signal in generated_signals:
            topic_short = signal['topic'][:32] + "..." if len(signal['topic']) > 35 else signal['topic']
            report_name = Path(signal['report_file']).name
            print(f"{signal['id']:<10} {topic_short:<35} {signal['score']:<10} {report_name:<15}")
    
    print("-" * 70)
    print(f"\n📈 Total signal: {len(signals)} | Baru: {len(new_signals)} | Sudah di-generate: {len(generated_signals)}")
    
    pause()

def menu_view_products():
    """Menu untuk melihat daftar produk."""
    print_header()
    print("📦 DAFTAR PRODUK DIGITAL")
    print("=" * 70)
    
    products = load_db(PRODUCTS_DB_PATH)
    
    if not products:
        print("📭 Belum ada produk yang dibuat.")
        print("\nGenerate produk dari signal yang tersedia!")
        pause()
        return
    
    print(f"\n🎁 Total {len(products)} produk tersedia:")
    print("-" * 70)
    
    for i, product in enumerate(products, 1):
        print(f"\n{i}. {product['name']}")
        print(f"   📌 ID: {product['id']}")
        print(f"   📝 {product['description'][:70]}...")
        print(f"   📂 Lokasi: products/{product['id']}/")
        
        if 'files' in product:
            print("   📎 Files:")
            for file_type, file_path in product['files'].items():
                print(f"      • {file_type.upper()}: {Path(file_path).name}")
    
    print("-" * 70)
    
    # Opsi untuk membuka folder
    print("\n📂 Ingin membuka folder produk?")
    print("1. Ya, buka Windows Explorer")
    print("2. Tidak, kembali ke menu")
    
    choice = get_choice(2, has_back=False)
    
    if choice == 1 and products:
        try:
            # Buka folder products di Windows Explorer
            os.startfile(str(PRODUCTS_DIR.absolute()))
            print("✅ Folder produk telah dibuka!")
        except:
            print(f"📂 Lokasi folder: {PRODUCTS_DIR.absolute()}")
    
    pause()

def menu_view_report():
    """Menu untuk melihat detail report."""
    print_header()
    print("📄 LIHAT DETAIL REPORT RISET")
    print("=" * 70)
    
    signals = load_db(SIGNALS_DB_PATH)
    
    if not signals:
        print("📭 Belum ada signal yang tersimpan.")
        pause()
        return
    
    print("\nPilih report yang ingin dilihat:")
    print("-" * 70)
    
    for i, signal in enumerate(signals, 1):
        status_icon = "🆕" if signal['status'] == 'new' else "✅"
        print(f"{i}. {status_icon} {signal['topic'][:50]} (Skor: {signal['score']})")
    
    print(f"{len(signals) + 1}. ⬅️  Kembali")
    
    choice = get_choice(len(signals), has_back=True)
    
    if choice == len(signals) + 1:
        return
    
    selected_signal = signals[choice - 1]
    report_path = Path(selected_signal['report_file'])
    
    if report_path.exists():
        print_header()
        print(f"📄 REPORT: {selected_signal['topic']}")
        print(f"⭐ Skor: {selected_signal['score']}/100")
        print("=" * 70)
        
        report_content = report_path.read_text(encoding='utf-8')
        
        # Tampilkan report dengan pagination
        lines = report_content.split('\n')
        page_size = 20
        
        for i in range(0, len(lines), page_size):
            for line in lines[i:i+page_size]:
                print(line)
            
            if i + page_size < len(lines):
                input("\n--- Tekan Enter untuk lanjut membaca ---")
                print()
    else:
        print("❌ File report tidak ditemukan!")
    
    pause()

def menu_help():
    """Menu bantuan dan panduan."""
    print_header()
    print("❓ BANTUAN & PANDUAN")
    print("=" * 70)
    
    help_topics = [
        "Cara Menggunakan Autopreneur",
        "Jenis-jenis Produk Digital",
        "Tips Memilih Topik yang Bagus",
        "Estimasi Biaya & API Usage",
        "Troubleshooting",
        "Tentang Autopreneur"
    ]
    
    print_menu("Pilih topik bantuan:", help_topics)
    
    choice = get_choice(len(help_topics))
    
    if choice == len(help_topics) + 1:
        return
    
    print_header()
    
    if choice == 1:
        print("📚 CARA MENGGUNAKAN AUTOPRENEUR")
        print("=" * 70)
        print("\n🔄 Workflow Dasar:")
        print("1. SCAN TOPIK: Riset ide bisnis dengan AI")
        print("2. LIHAT SIGNAL: Cek skor dan pilih yang terbaik")
        print("3. GENERATE PRODUK: Buat produk digital dari signal")
        print("4. AKSES FILE: Produk tersimpan di folder 'products'")
        print("\n💡 Tips:")
        print("• Scan beberapa topik untuk membandingkan skor")
        print("• Pilih topik dengan skor >70 untuk hasil terbaik")
        print("• Setiap produk berisi PDF panduan + data CSV")
        
    elif choice == 2:
        print("📦 JENIS-JENIS PRODUK DIGITAL")
        print("=" * 70)
        print("\n1. UMKM Productivity Suite:")
        print("   • Content Calendar: Kalender konten 30 hari")
        print("   • Caption Bank: 30 caption siap pakai")
        print("   • Invoice Macro: Template invoice otomatis")
        print("\n2. Shopee Toolkit:")
        print("   • Keyword Tracker: Laporan SEO kata kunci")
        print("   • Hashtag Clusterer: Strategi hashtag")
        print("   • Copy Swipes: Template copywriting")
        print("\n3. Canva Assets:")
        print("   • Batik Patterns: 40 pola batik digital")
        print("   • Brand Kit: Paket branding lengkap")
        print("   • CapCut Templates: Template video viral")
        
    elif choice == 3:
        print("💡 TIPS MEMILIH TOPIK YANG BAGUS")
        print("=" * 70)
        print("\n✅ Topik yang BAGUS:")
        print("• Spesifik: 'konten untuk toko kue tradisional'")
        print("• Ada target: 'untuk ibu-ibu PKK'")
        print("• Platform jelas: 'Instagram Stories UMKM'")
        print("• Lokal: 'promosi warung makan Padang'")
        print("\n❌ Hindari topik yang:")
        print("• Terlalu umum: 'ide bisnis'")
        print("• Tidak jelas: 'konten sosmed'")
        print("• Tanpa konteks: 'template'")
        
    elif choice == 4:
        print("💰 ESTIMASI BIAYA & API USAGE")
        print("=" * 70)
        print("\n📊 Perkiraan biaya OpenAI API:")
        print("• Scan topik: ~$0.02-0.05 per scan")
        print("• Generate produk: ~$0.05-0.10 per produk")
        print("• Total per produk: ~$0.07-0.15")
        print("\n💡 Tips hemat:")
        print("• Scan topik yang sudah jelas")
        print("• Generate hanya signal skor tinggi")
        print("• Monitor usage di dashboard OpenAI")
        
    elif choice == 5:
        print("🔧 TROUBLESHOOTING")
        print("=" * 70)
        print("\n❌ Error 'API Key Invalid':")
        print("• Cek file .env di folder root")
        print("• Pastikan API key benar (sk-...)")
        print("• Tidak ada spasi atau tanda kutip")
        print("\n❌ Error 'Rate Limit':")
        print("• Tunggu beberapa menit")
        print("• Upgrade plan OpenAI jika perlu")
        print("\n❌ PDF tidak terbuat:")
        print("• Install wkhtmltopdf")
        print("• Restart terminal")
        print("• Cek dengan: wkhtmltopdf --version")
        
    elif choice == 6:
        print("📖 TENTANG AUTOPRENEUR")
        print("=" * 70)
        print("\n🚀 Autopreneur v1.0")
        print("AI-Powered Digital Product Generator")
        print("\n👨‍💻 Dibuat untuk:")
        print("• Entrepreneur Indonesia")
        print("• UMKM yang ingin go digital")
        print("• Content creator")
        print("• Online seller")
        print("\n💡 Powered by:")
        print("• OpenAI GPT-4o Mini")
        print("• Python")
        print("• ❤️ untuk UMKM Indonesia")
    
    pause()

def main_menu():
    """Menu utama aplikasi."""
    while True:
        print_header()
        
        # Statistik
        signals = load_db(SIGNALS_DB_PATH)
        products = load_db(PRODUCTS_DB_PATH)
        new_signals = len([s for s in signals if s['status'] == 'new'])
        
        print(f"📊 Status: {len(signals)} Signal | {new_signals} Baru | {len(products)} Produk")
        print("=" * 70)
        
        options = [
            "🔍 Scan Topik Bisnis Baru",
            "🎯 Generate Produk Digital",
            "📋 Lihat Daftar Signal",
            "📦 Lihat Daftar Produk",
            "📄 Lihat Detail Report",
            "❓ Bantuan & Panduan",
            "🚪 Keluar"
        ]
        
        print_menu("MENU UTAMA", options, back_option=False)
        
        choice = get_choice(len(options), has_back=False)
        
        if choice == 1:
            menu_scan_topic()
        elif choice == 2:
            menu_generate_product()
        elif choice == 3:
            menu_view_signals()
        elif choice == 4:
            menu_view_products()
        elif choice == 5:
            menu_view_report()
        elif choice == 6:
            menu_help()
        elif choice == 7:
            print_header()
            print("👋 Terima kasih telah menggunakan Autopreneur!")
            print("\n💡 Tips terakhir:")
            print("• Produk Anda tersimpan di folder 'products'")
            print("• Backup folder 'db' dan 'products' secara berkala")
            print("• Jangan lupa review produk sebelum dijual")
            print("\nSemoga sukses dengan bisnis digital Anda! 🚀")
            print("=" * 70)
            break

# --- ENTRY POINT ---
if __name__ == "__main__":
    ensure_setup()
    
    # Cek API key
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ ERROR: OpenAI API Key tidak ditemukan!")
        print("\nPastikan file .env berisi:")
        print("OPENAI_API_KEY=sk-your-key-here")
        print("\nBaca panduan instalasi untuk detail.")
        sys.exit(1)
    
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n\n⚠️  Program dihentikan oleh user.")
        print("Data Anda aman tersimpan. Sampai jumpa! 👋")
    except Exception as e:
        print(f"\n❌ Error tidak terduga: {e}")
        print("Silakan restart program atau hubungi support.")
