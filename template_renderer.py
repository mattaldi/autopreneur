# template_renderer.py

from jinja2 import Environment, FileSystemLoader, select_autoescape
from weasyprint import HTML
from pathlib import Path
import json
from typing import Dict, Any, List

class TemplateRenderer:
    """Centralized template rendering system for all product types."""
    
    def __init__(self, template_dir: str = "templates"):
        self.env = Environment(
            loader=FileSystemLoader(template_dir),
            autoescape=select_autoescape(["html"]),
            trim_blocks=True,
            lstrip_blocks=True
        )
        
        # Register custom filters
        self.env.filters['number_format'] = self.number_format
        self.env.filters['currency_format'] = self.currency_format
        
    def number_format(self, value: float) -> str:
        """Format numbers with thousand separators."""
        try:
            return "{:,.0f}".format(value).replace(",", ".")
        except:
            return str(value)
    
    def currency_format(self, value: float) -> str:
        """Format currency in Indonesian Rupiah."""
        try:
            return f"Rp {self.number_format(value)}"
        except:
            return f"Rp {value}"
    
    def render_product(self, product_type: str, data: Dict[str, Any], output_folder: Path) -> Dict[str, Path]:
        """Render product based on type and return paths to generated files."""
        
        template_map = {
            # UMKM Productivity Suite
            "content_calendar": "umkm_productivity/content_calendar.html",
            "caption_bank": "umkm_productivity/caption_bank.html",
            "invoice_macro": "umkm_productivity/invoice_macro.html",
            
            # Shopee Toolkit
            "keyword_tracker": "shopee_toolkit/keyword_tracker.html",
            "hashtag_clusterer": "shopee_toolkit/hashtag_clusterer.html",
            "copy_swipes": "shopee_toolkit/copy_swipes.html",
            
            # Canva Assets
            "batik_patterns": "canva_assets/batik_patterns.html",
            "brand_kit": "canva_assets/brand_kit.html",
            "capcut_templates": "canva_assets/capcut_templates.html",
            
            # Finance Pack
            "pajak_calculator": "finance_pack/pajak_calculator.html",
            "cash_flow": "finance_pack/cash_flow.html",
            "sop_templates": "finance_pack/sop_templates.html",
            
            # Seasonal
            "ramadan_calendar": "seasonal/ramadan_calendar.html",
            "wedding_planner": "seasonal/wedding_planner.html",
            "yearend_planner": "seasonal/yearend_planner.html",
        }
        
        if product_type not in template_map:
            raise ValueError(f"No template found for product type: {product_type}")
        
        # Get template
        template = self.env.get_template(template_map[product_type])
        
        # Render HTML
        html_content = template.render(**data)
        
        # Create output paths
        output_folder.mkdir(parents=True, exist_ok=True)
        pdf_path = output_folder / f"{product_type}.pdf"
        html_path = output_folder / f"{product_type}.html"
        json_path = output_folder / f"{product_type}_data.json"
        
        # Generate PDF
        try:
            HTML(string=html_content).write_pdf(pdf_path)
            print(f"✅ PDF generated: {pdf_path}")
        except Exception as e:
            print(f"⚠️ PDF generation failed: {e}")
            pdf_path = None
        
        # Save HTML for preview
        html_path.write_text(html_content, encoding="utf-8")
        print(f"✅ HTML saved: {html_path}")
        
        # Save JSON data
        json_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"✅ JSON data saved: {json_path}")
        
        return {
            "pdf": pdf_path,
            "html": html_path,
            "json": json_path
        }
    
    def render_suite(self, suite_type: str, suite_data: Dict[str, Dict[str, Any]], output_folder: Path) -> Dict[str, Dict[str, Path]]:
        """Render complete product suite."""
        
        suite_results = {}
        suite_folder = output_folder / suite_type
        suite_folder.mkdir(parents=True, exist_ok=True)
        
        for product_type, product_data in suite_data.items():
            print(f"\n📄 Rendering {product_type}...")
            product_folder = suite_folder / product_type
            
            try:
                files = self.render_product(product_type, product_data, product_folder)
                suite_results[product_type] = files
            except Exception as e:
                print(f"❌ Error rendering {product_type}: {e}")
                suite_results[product_type] = None
        
        # Create suite manifest
        manifest = {
            "suite_type": suite_type,
            "products": list(suite_data.keys()),
            "files": {k: {ftype: str(fpath) for ftype, fpath in v.items() if fpath} 
                     for k, v in suite_results.items() if v}
        }
        
        manifest_path = suite_folder / "manifest.json"
        manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
        print(f"\n✅ Suite manifest saved: {manifest_path}")
        
        return suite_results
    
    def get_available_templates(self) -> Dict[str, List[str]]:
        """Get list of available templates organized by suite."""
        
        return {
            "umkm_productivity": ["content_calendar", "caption_bank", "invoice_macro"],
            "shopee_toolkit": ["keyword_tracker", "hashtag_clusterer", "copy_swipes"],
            "canva_assets": ["batik_patterns", "brand_kit", "capcut_templates"],
            "finance_pack": ["pajak_calculator", "cash_flow", "sop_templates"],
            "seasonal": ["ramadan_calendar", "wedding_planner", "yearend_planner"]
        }
    
    def validate_template_data(self, product_type: str, data: Dict[str, Any]) -> List[str]:
        """Validate required fields for each template type."""
        
        required_fields = {
            "content_calendar": ["name", "description", "month", "year", "calendar_weeks"],
            "caption_bank": ["name", "description", "captions"],
            "invoice_macro": ["name", "description", "invoices"],
            "keyword_tracker": ["name", "description", "report_date", "shop_name", "keywords", "recommendations"],
            "hashtag_clusterer": ["name", "description", "clusters", "usage_guide", "monthly_calendar"],
            "copy_swipes": ["name", "description", "categories", "swipe_sections", "usage_tips"],
            "batik_patterns": ["name", "description", "patterns", "usage_examples", "license_terms"],
            "brand_kit": ["name", "description", "logos", "colors", "fonts", "templates", "guidelines"],
            "capcut_templates": ["name", "description", "categories", "templates", "tutorial_steps"],
            "pajak_calculator": ["name", "description", "sample_data", "tax_rules", "tax_tips", "tax_deadlines"],
            "cash_flow": ["name", "description", "summary", "transactions", "income_categories", "expense_categories", "projections"],
            "sop_templates": ["name", "description", "sop_categories", "sop_documents", "version", "last_updated"],
            "ramadan_calendar": ["name", "description", "location", "current_date", "prayer_times", "calendar_days", "content_categories", "popular_hashtags", "special_days"],
            "wedding_planner": ["name", "description", "couple_names", "wedding_date", "total_budget", "budget_items", "timeline", "vendors", "guest_stats", "guest_list", "todo_columns", "important_notes"],
            "yearend_planner": ["name", "description", "year", "achievements", "goal_categories", "monthly_breakdown", "habits", "visions", "reflection_prompts"]
        }
        
        if product_type not in required_fields:
            return [f"Unknown product type: {product_type}"]
        
        missing_fields = []
        for field in required_fields[product_type]:
            if field not in data:
                missing_fields.append(f"Missing required field: {field}")
        
        return missing_fields