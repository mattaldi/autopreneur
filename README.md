# Autopreneur

🚀 AI-powered digital product generator for Indonesian entrepreneurs - automatically create high-quality digital products to sell online.

![Python](https://img.shields.io/badge/python-v3.10+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

## 🌟 Overview

Autopreneur is an AI-driven tool that helps Indonesian entrepreneurs (especially UMKM - Usaha Mikro, Kecil, dan Menengah) identify business opportunities and automatically generate professional digital products. From social media content calendars to tax calculators, Autopreneur leverages GPT-4 to create ready-to-sell digital products in minutes.

### 🎯 Key Features

- **Market Research**: AI-powered topic analysis with business potential scoring (0-100)
- **Automated Generation**: Creates complete digital products with PDF guides and supporting files
- **Multiple Product Types**: 15+ product templates across 5 categories
- **Indonesian Market Focus**: Tailored for Indonesian business culture and regulations
- **Professional Output**: Generates polished PDFs and structured data files
- **Interactive CLI**: User-friendly menu system - no technical commands needed!

## 📋 Table of Contents
1. [Quick Start](#-quick-start)
2. [Installation](#-installation)
3. [Product Categories](#-product-categories)
4. [Using Autopreneur](#-using-autopreneur)
5. [Usage Examples](#-usage-examples)
6. [Architecture](#-architecture)
7. [Configuration](#-configuration)
8. [Troubleshooting](#-troubleshooting)
9. [Best Practices](#-best-practices)
10. [Contributing](#-contributing)

## 🚀 Quick Start

### Basic Workflow
1. **Research a topic** → Creates market signal with score (0-100)
2. **Generate product** → Converts best signal to digital product
3. **Access files** → Find generated PDFs and data in `products/` folder

### Your First Product in 3 Minutes
```bash
# Start the program
python main.py

# Then follow the interactive menu:
# 1. Choose "Scan Topik Bisnis Baru" 
# 2. Enter your business topic
# 3. Choose "Generate Produk Digital"
# 4. Select the signal to generate
# 5. Your product is ready!
```

**Generated files location:**
```
products/prod_xxxxxxxxxxxx/
├── caption_bank.csv       # Structured data
├── panduan_konten.pdf     # Professional PDF guide
└── metadata.json          # Product information
```

## 🛠 Installation

### Prerequisites
- Python 3.10 or higher
- OpenAI API key
- wkhtmltopdf (for PDF generation)
- Windows/Linux/Mac OS

### Step 1: Clone the Repository
```bash
cd C:\code
git clone https://github.com/yourusername/autopreneur.git
cd autopreneur
```

### Step 2: Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On Mac/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure OpenAI API Key
Create a `.env` file in the project root:
```env
OPENAI_API_KEY=your-openai-api-key-here
```

**Important**: Never share your API key publicly!

### Step 5: Install wkhtmltopdf
Download and install wkhtmltopdf from: https://wkhtmltopdf.org/downloads.html

On Windows, add it to your PATH or install using:
```bash
# Using Chocolatey
choco install wkhtmltopdf

# Or download installer from website
```

## 📦 Product Categories

### 1. UMKM Productivity Suite
- **Content Calendar** (`content_calendar`): 30-day social media planning calendar with weekly themes, daily post ideas, optimal posting times
- **Caption Bank** (`caption_bank`): 30 ready-to-use social media captions with hashtags, mix of educational (40%), promotional (30%), engagement (20%), storytelling (10%)
- **Invoice Macro** (`invoice_macro`): Professional invoice templates with automatic PPN 11% calculations, payment terms, bank details

### 2. Shopee Toolkit
- **Keyword Tracker** (`keyword_tracker`): SEO keyword ranking reports with search volume, competition analysis, position tracking
- **Hashtag Clusterer** (`hashtag_clusterer`): Organized hashtag strategies by competition level, engagement rates, monthly calendar
- **Copy Swipes** (`copy_swipes`): High-converting copywriting templates for headlines, body copy, CTAs with conversion estimates

### 3. Canva Assets
- **Batik Patterns** (`batik_patterns`): 40 digital Indonesian batik patterns with regional variations, high-resolution formats
- **Brand Kit** (`brand_kit`): Complete branding package with logo variants, color palettes, font recommendations, 12 Canva templates
- **CapCut Templates** (`capcut_templates`): 20 video editing templates for viral formats, multiple durations (15/30/60s)

### 4. Finance Pack
- **Pajak Calculator** (`pajak_calculator`): Indonesian UMKM tax calculator for PPh Final (0.5%) and PPN (11%), tax saving tips
- **Cash Flow** (`cash_flow`): Income/expense tracking with category breakdowns, monthly projections, visual summaries
- **SOP Templates** (`sop_templates`): 3 comprehensive SOP documents with step-by-step procedures, forms, approval workflows

### 5. Seasonal Products
- **Ramadan Calendar** (`ramadan_calendar`): 30-day Ramadan planner with prayer times, content ideas, special days, hashtags
- **Wedding Planner** (`wedding_planner`): Complete wedding planning system with budget tracker, timeline, vendor management, guest list
- **Year-end Planner** (`yearend_planner`): Annual reflection tools with achievements, goals by category, monthly breakdown, habit tracking

## 📋 Using Autopreneur

### Starting the Program
```bash
python main.py
```

You'll see an interactive menu like this:

```
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
```

### Menu Options Explained

#### 1️⃣ **Scan Topik Bisnis Baru**
Research and analyze a business topic.
- Enter your business idea in Indonesian
- AI will research the market potential
- Receive a score from 0-100
- Creates a "signal" for later use

**Example topics:**
- "ide konten media sosial untuk UMKM kuliner"
- "template invoice untuk bisnis online"
- "kalender konten ramadan untuk toko muslim"
- "hashtag strategy untuk jualan di Shopee"
- "SOP untuk restoran padang"

#### 2️⃣ **Generate Produk Digital**
Create a digital product from your signals.
- View all available signals
- Choose automatic (highest score) or manual selection
- AI generates complete product package
- Creates PDF guide + CSV data file

#### 3️⃣ **Lihat Daftar Signal**
View all your market research signals.
- See new signals (not yet generated)
- See completed signals (already generated)
- Check scores and topics

#### 4️⃣ **Lihat Daftar Produk**
View all generated products.
- See product names and descriptions
- Check file locations
- Option to open product folder directly

#### 5️⃣ **Lihat Detail Report**
Read full market research reports.
- Select any signal to view detailed analysis
- Paginated view for easy reading

#### 6️⃣ **Bantuan & Panduan**
Access help and guidelines.
- How to use Autopreneur
- Product types available
- Tips for choosing topics
- Cost estimates
- Troubleshooting

## 📚 Usage Examples

### Example 1: Complete Workflow

```
1. Start program: python main.py

2. Choose option 1 (Scan Topik Bisnis Baru)
   Enter: "ide konten untuk toko fashion muslim"
   Result: Signal created with score 92/100

3. Choose option 2 (Generate Produk Digital)
   Select: Automatic (highest score)
   Result: Product generated successfully

4. Choose option 4 (Lihat Daftar Produk)
   Find your product location
   Open folder to access files
```

### Example 2: Research Multiple Topics

```
1. Scan first topic:
   - Choose option 1
   - Enter: "template story Instagram untuk UMKM"
   - Get score: 78/100

2. Scan second topic:
   - Choose option 1 again
   - Enter: "kalender promosi untuk warung makan"
   - Get score: 65/100

3. Scan third topic:
   - Choose option 1 again
   - Enter: "hashtag strategy untuk jualan online"
   - Get score: 88/100

4. View all signals:
   - Choose option 3
   - See all topics with scores

5. Generate best product:
   - Choose option 2
   - Select automatic (chooses 88/100 score)
```

### Example 3: Reading Research Reports

```
1. Choose option 5 (Lihat Detail Report)
2. Select signal number to read
3. Read paginated report
4. Press Enter to continue reading
5. Return to main menu when done
```

## 🏗 Architecture

```
autopreneur/
├── main.py                 # Interactive CLI interface
├── agents.py               # AI agents (Analyst & Builder)
├── template_renderer.py    # PDF generation system
├── requirements.txt        # Python dependencies
├── .env                   # API keys (create this)
├── db/                    # Database files
│   ├── signals.json       # Market research signals
│   ├── products.json      # Product records
│   └── report_*.md        # Research reports
├── products/              # Generated products
│   └── prod_*/           # Individual products
├── templates/            # HTML templates for PDFs
│   ├── umkm_productivity/
│   ├── shopee_toolkit/
│   ├── canva_assets/
│   ├── finance_pack/
│   └── seasonal/
└── venv/                 # Virtual environment
```

### Key Components

1. **Interactive CLI** (`main.py`)
   - User-friendly menu system
   - Input validation
   - Clear navigation
   - Status tracking

2. **AnalystAgent** (`agents.py`)
   - Researches topics using GPT-4
   - Scores business potential (0-100)
   - Generates market reports

3. **BuilderAgent** (`agents.py`)
   - Creates product content
   - Supports 15+ product types
   - Generates structured data

4. **TemplateRenderer** (`template_renderer.py`)
   - Renders HTML templates
   - Generates PDF files
   - Handles multiple formats

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
OPENAI_API_KEY=sk-your-openai-api-key-here
```

### Adding New Product Types

1. **Add generator method in `agents.py`:**
```python
def _generate_your_product(self, topic: str):
    system_prompt = """
    Your custom prompt here...
    Return JSON with required fields
    """
    
    resp = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Create product for: {topic}"}
        ],
        response_format={"type": "json_object"},
        temperature=0.8
    )
    
    return json.loads(resp.choices[0].message.content)
```

2. **Create HTML template in `templates/category/your_product.html`**

3. **Update template mapping in `template_renderer.py`:**
```python
template_map = {
    # ... existing mappings ...
    "your_product": "category/your_product.html",
}
```

### Template Customization

Modify HTML templates in the `templates/` directory:

```html
<!-- templates/umkm_productivity/caption_bank.html -->
<style>
    /* Customize colors, fonts, layout */
    h1 { 
        color: #your-brand-color;
        font-family: 'Your Font', sans-serif;
    }
</style>
```

## 🐛 Troubleshooting

### Common Issues and Solutions

#### 1. OpenAI API Errors
**Error**: `ERROR: OpenAI API Key tidak ditemukan!`
- **Solution**: Create `.env` file with your API key
- Format: `OPENAI_API_KEY=sk-...`
- No quotes or extra spaces

**Error**: `openai.error.RateLimitError`
- **Solution**: You've exceeded API limits
- Wait a few minutes or upgrade your OpenAI plan
- Consider adding delays between operations

#### 2. PDF Generation Fails
**Error**: `OSError: No wkhtmltopdf executable found`
- **Solution**: Install wkhtmltopdf and add to PATH
- Restart terminal after installation
- Verify: `wkhtmltopdf --version`

#### 3. No New Signals to Process
**Message**: "Tidak ada signal baru untuk diproses"
- **Solution**: Use option 1 to scan topics first
- Check option 3 to see signal status
- Ensure signals haven't been generated already

#### 4. Import Errors
**Error**: `ModuleNotFoundError`
- **Solution**: Activate virtual environment
- Run `pip install -r requirements.txt`
- Check Python version (must be 3.10+)

#### 5. Menu Navigation Issues
- Use numbers (1-7) to select options
- Press Enter after your choice
- Type 'batal' to cancel operations
- Use Ctrl+C to emergency exit

## 💡 Best Practices

### 1. Topic Selection
- **Be specific**: "ide konten untuk toko kue tradisional" > "ide konten"
- **Include target audience**: "untuk ibu-ibu PKK"
- **Mention platform**: "untuk Instagram Stories"
- **Use Indonesian context**: Reference local culture/events

### 2. API Usage & Cost Management
- Monitor your OpenAI usage dashboard
- Each scan costs approximately $0.02-0.05
- Each generate costs approximately $0.05-0.10
- Consider daily/monthly budgets
- Scan multiple topics before generating

### 3. Product Quality
- Review generated content before selling
- Customize templates for your brand
- Add your logo and contact info to PDFs
- Test products with sample customers

### 4. File Organization
- Regularly backup `db/` and `products/` folders
- Archive old products monthly
- Keep your `.env` file secure
- Use version control (git) for custom templates

### 5. Workflow Optimization
- Scan 3-5 topics before generating
- Generate products from scores >70
- Use manual selection for specific needs
- Read reports to understand market insights

## 🎨 Example Output

### Caption Bank Sample
```csv
day,text
1,Selalu ada cerita unik di setiap resep yang kami sajikan. Sudah mencoba favorit kami bulan ini? 🍴✨ #KulinerLokal #UMKM
2,Bingung mau makan apa hari ini? Coba deh menu baru kami, garantikan ketagihan! 🌟 #CicipiRasa #UMKMKuliner
3,Kami percaya, kualitas terbaik berasal dari bahan-bahan lokal. Dukung petani lokal dengan mencicipi menu kami! 🌾🍽 #DukungLokal
```

### Generated Files Structure
```
products/prod_ee0ebcbcfeb8/
├── caption_bank.csv       # 30 captions with hashtags
├── panduan_konten.pdf     # Professional usage guide
└── metadata.json          # Product information
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Development Guidelines

1. **Code Standards**
   - Write code in English
   - Add Indonesian comments where helpful
   - Follow PEP 8 style guidelines
   - Add type hints where possible

2. **Testing**
   - Test new product types thoroughly
   - Verify PDF generation works
   - Check Indonesian language quality
   - Test menu navigation flow

3. **Documentation**
   - Update README for new features
   - Document new product types
   - Include example outputs
   - Update help menu in main.py

### How to Contribute

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with ❤️ for Indonesian entrepreneurs
- Powered by OpenAI GPT-4
- Inspired by the vibrant Indonesian UMKM community
- Special thanks to all contributors

## 📞 Support

For questions and support:
- **Issues**: Create an issue on GitHub
- **Email**: [your-email@example.com]
- **Documentation**: Check this README first
- **Community**: Join our Discord server

---

**Note**: This project requires an active OpenAI API key. Usage will incur costs based on OpenAI's pricing. Always monitor your usage to avoid unexpected charges.

**Tips for Success**:
1. Start small - test with one topic before scaling
2. Review all generated content for quality
3. Customize outputs to match your brand
4. Track which products sell best
5. Stay updated with Indonesian market trends

*Happy selling! 🚀*
