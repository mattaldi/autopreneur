# main.py
import argparse
import json
import os
import uuid
from pathlib import Path
import csv

# Impor baru untuk PDF
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
    Path("templates").mkdir(exist_ok=True) # Pastikan folder templates ada
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

# --- FUNGSI BARU UNTUK PDF ---
def write_pdf(product_folder: Path, assets: dict) -> Path:
    """Render template Jinja2 menjadi file PDF menggunakan WeasyPrint."""
    print("📄 Merender file PDF...")
    env = Environment(
        loader=FileSystemLoader("templates"),
        autoescape=select_autoescape(["html"])
    )
    template = env.get_template("caption_bank.html")
    html_content = template.render(**assets)
    
    pdf_path = product_folder / "panduan_konten.pdf"
    HTML(string=html_content).write_pdf(pdf_path)
    print(f"✅ File PDF disimpan di: {pdf_path}")
    return pdf_path

# --- FUNGSI HANDLER PERINTAH ---
def handle_scan(topic: str):
    # (Tidak ada perubahan di sini)
    analyst = AnalystAgent()
    report_text = analyst.research_topic(topic)
    score = analyst.score_idea(report_text)
    signal_id = str(uuid.uuid4())[:8]
    report_file = DB_DIR / f"report_{signal_id}.md"
    report_file.write_text(report_text, encoding="utf-8")
    new_signal = {"id": signal_id, "topic": topic, "score": score, "status": "new", "report_file": str(report_file)}
    signals = load_db(SIGNALS_DB_PATH)
    signals.append(new_signal)
    save_db(SIGNALS_DB_PATH, signals)
    print(f"\n✅ Signal baru disimpan! ID: {signal_id}, Topik: '{topic}', Skor: {score}")

def handle_generate():
    """Membuat produk (CSV & PDF) dari sinyal terbaik."""
    signals = load_db(SIGNALS_DB_PATH)
    new_signals = [s for s in signals if s['status'] == 'new']
    
    if not new_signals:
        print("⚠️ Tidak ada sinyal baru untuk diproses.")
        return

    best_signal = max(new_signals, key=lambda s: s['score'])
    print(f"\n🔥 Memilih sinyal terbaik: '{best_signal['topic']}' (Skor: {best_signal['score']})")

    builder = BuilderAgent()
    assets = builder.generate_product_assets(best_signal['topic'])

    if not assets:
        print("❌ Gagal membuat aset produk.")
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
    print(f"✅ File CSV disimpan di: {csv_path}")

    # 2. Simpan file PDF (INTEGRASI BARU)
    pdf_path = write_pdf(product_folder, assets)

    # 3. Update database produk dengan file CSV dan PDF
    new_product = {
        "id": product_id,
        "signal_id": best_signal['id'],
        "name": assets['name'],
        "description": assets['description'],
        "files": {
            "csv": str(csv_path),
            "pdf": str(pdf_path) # <-- Menambahkan path PDF
        }
    }
    products = load_db(PRODUCTS_DB_PATH)
    products.append(new_product)
    save_db(PRODUCTS_DB_PATH, products)

    # Update status sinyal
    for s in signals:
        if s['id'] == best_signal['id']:
            s['status'] = 'generated'
    save_db(SIGNALS_DB_PATH, signals)

    print(f"\n🎉 Produk baru (CSV + PDF) berhasil dibuat! ID Produk: {product_id}")

def handle_list(what: str):
    # (Tidak ada perubahan di sini)
    if what == "signals": db_path, title = SIGNALS_DB_PATH, "Sinyal Pasar"
    elif what == "products": db_path, title = PRODUCTS_DB_PATH, "Produk"
    else: return
    print(f"\n--- Daftar {title} ---")
    data = load_db(db_path)
    if not data: print("Tidak ada data.")
    for item in data: print(json.dumps(item, indent=2))

# --- TITIK MASUK UTAMA ---
if __name__ == "__main__":
    ensure_setup()
    parser = argparse.ArgumentParser(description="Autopreneur-Lite MVP")
    # (Parser tidak ada perubahan)
    subparsers = parser.add_subparsers(dest="command", required=True)
    scan_parser = subparsers.add_parser("scan", help="Mencari dan menganalisis ide produk baru.")
    scan_parser.add_argument("topic", type=str, help="Topik yang akan di-riset.")
    generate_parser = subparsers.add_parser("generate", help="Membuat produk dari sinyal terbaik.")
    list_parser = subparsers.add_parser("list", help="Menampilkan daftar sinyal atau produk.")
    list_parser.add_argument("what", choices=["signals", "products"], help="Apa yang ingin ditampilkan.")
    args = parser.parse_args()
    if args.command == "scan": handle_scan(args.topic)
    elif args.command == "generate": handle_generate()
    elif args.command == "list": handle_list(args.what)