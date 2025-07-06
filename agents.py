# agents.py
import os
import json
import uuid
from datetime import datetime, timedelta
import random
from openai import OpenAI
from pathlib import Path

# Inisialisasi client OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class AnalystAgent:
    """Agent untuk menganalisis topik dan mendeteksi sinyal pasar."""
    
    def research_topic(self, topic: str) -> str:
        """Melakukan riset mendalam pada sebuah topik menggunakan web search."""
        system_prompt = (
            "You are an elite market research analyst focused on Indonesian digital products market. "
            "Analyze the given topic for business potential, demand signals, competition, and monetization opportunities. "
            "Produce a comprehensive report with data points, market size estimates, and actionable insights."
        )
        
        print(f"🕵️  AnalystAgent: Researching '{topic}'...")
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Research Indonesian market potential for: {topic}"}
            ],
            temperature=0.7
        )
        report_content = resp.choices[0].message.content
        print("✅  AnalystAgent: Research complete.")
        return report_content

    def score_idea(self, report_content: str) -> int:
        """Memberi skor pada ide berdasarkan laporan riset."""
        print("⚖️  AnalystAgent: Scoring business idea...")
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a Venture Capitalist evaluating Indonesian digital product ideas. Based on the research report, score the business potential from 0 to 100. Consider: market demand (40%), competition level (20%), monetization potential (20%), and ease of automation (20%). Return ONLY the number."},
                {"role": "user", "content": report_content},
            ],
            temperature=0
        )
        try:
            score = int(resp.choices[0].message.content.strip())
            print(f"✅  AnalystAgent: Score given: {score}")
            return score
        except (ValueError, TypeError):
            return 50


class BuilderAgent:
    """Enhanced agent untuk membuat berbagai jenis produk digital."""
    
    def generate_product_suite(self, suite_type: str, topic: str):
        """Generate complete product suite."""
        
        suites = {
            "umkm_productivity": {
                "products": ["content_calendar", "caption_bank", "invoice_macro"],
                "bundle_price": 199000
            },
            "shopee_toolkit": {
                "products": ["keyword_tracker", "hashtag_clusterer", "copy_swipes"],
                "bundle_price": 149000
            },
            "canva_assets": {
                "products": ["batik_patterns", "brand_kit", "capcut_templates"],
                "bundle_price": 149000
            },
            "finance_pack": {
                "products": ["pajak_calculator", "cash_flow", "sop_templates"],
                "bundle_price": 249000
            },
            "seasonal": {
                "products": ["ramadan_calendar", "wedding_planner", "yearend_planner"],
                "bundle_price": 99000
            }
        }
        
        if suite_type not in suites:
            raise ValueError(f"Unknown suite type: {suite_type}")
        
        suite_config = suites[suite_type]
        results = {}
        
        for product_type in suite_config["products"]:
            print(f"🔨 Generating {product_type}...")
            results[product_type] = self.generate_product_assets(topic, product_type)
        
        return results, suite_config

    def generate_product_assets(self, topic: str, product_type: str):
        """Route to specific generator based on product type."""
        
        generators = {
            # UMKM Productivity Suite
            "content_calendar": self._generate_content_calendar,
            "caption_bank": self._generate_caption_bank,
            "invoice_macro": self._generate_invoice_macro,
            
            # Shopee Toolkit  
            "keyword_tracker": self._generate_keyword_tracker,
            "hashtag_clusterer": self._generate_hashtag_clusterer,
            "copy_swipes": self._generate_copy_swipes,
            
            # Canva Assets
            "batik_patterns": self._generate_batik_patterns,
            "brand_kit": self._generate_brand_kit,
            "capcut_templates": self._generate_capcut_templates,
            
            # Finance Pack
            "pajak_calculator": self._generate_pajak_calculator,
            "cash_flow": self._generate_cash_flow,
            "sop_templates": self._generate_sop_templates,
            
            # Seasonal
            "ramadan_calendar": self._generate_ramadan_calendar,
            "wedding_planner": self._generate_wedding_planner,
            "yearend_planner": self._generate_yearend_planner,
        }
        
        if product_type not in generators:
            raise ValueError(f"Unknown product type: {product_type}")
            
        return generators[product_type](topic)

    # ============== UMKM PRODUCTIVITY SUITE ==============
    
    def _generate_content_calendar(self, topic: str):
        """Generate 30-day content calendar."""
        
        system_prompt = """
        You are a social media strategist for Indonesian UMKM.
        Create a comprehensive 30-day content calendar.
        
        Return JSON with:
        - name: catchy product name in Indonesian
        - description: compelling description
        - month: target month name
        - year: 2025
        - calendar_weeks: array of 4 week objects, each containing:
          - week_number: 1-4
          - theme: weekly theme
          - days: array of 7 days with:
            - date: "Senin, 1 Jan"
            - content_type: "Educational" / "Promotional" / "Engagement" / "Behind the Scene"
            - idea: specific post idea in Indonesian (50-100 chars)
            - best_time: optimal posting time like "19:00"
          - hashtags: array of 10 relevant Indonesian hashtags
        """
        
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Create content calendar for: {topic}"}
            ],
            response_format={"type": "json_object"},
            temperature=0.8
        )
        
        return json.loads(resp.choices[0].message.content)

    def _generate_caption_bank(self, topic: str):
        """Generate caption bank with 30 captions."""
        
        system_prompt = """
        You are a social media copywriting expert for Indonesian market.
        Create 30 engaging social media captions.
        
        Return JSON with:
        - name: catchy product name
        - description: product description
        - captions: array of 30 objects with:
          - day: number 1-30
          - text: caption text in Indonesian (100-200 chars)
          - hashtags: array of 5 relevant hashtags
        
        Mix educational (40%), promotional (30%), engagement (20%), and storytelling (10%) content.
        Use conversational Indonesian with occasional English terms where natural.
        """
        
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Create caption bank for: {topic}"}
            ],
            response_format={"type": "json_object"},
            temperature=0.8
        )
        
        return json.loads(resp.choices[0].message.content)

    def _generate_invoice_macro(self, topic: str):
        """Generate invoice templates with macro calculations."""
        
        system_prompt = """
        Create professional invoice templates for Indonesian businesses.
        Include proper tax calculations (PPN 11%), payment terms, and bank details.
        
        Return JSON with:
        - name: product name
        - description: product description
        - invoices: array of 3 sample invoices with:
          - company_name, company_address, company_phone
          - number: "INV/2025/001" format
          - date: current date
          - due_date: 14 days later
          - client_name, client_address, client_phone
          - bank_name: use major Indonesian banks
          - account_number, account_name
          - items: array of 3-5 items with:
            - description: service/product description
            - quantity: number
            - price: realistic price in IDR
            - total: quantity * price
          - subtotal: sum of all items
          - tax: 11% of subtotal
          - total: subtotal + tax
          - notes: payment instructions in Indonesian
        """
        
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Create invoice templates for business type: {topic}"}
            ],
            response_format={"type": "json_object"},
            temperature=0.7
        )
        
        return json.loads(resp.choices[0].message.content)

    # ============== SHOPEE TOOLKIT ==============
    
    def _generate_keyword_tracker(self, topic: str):
        """Generate keyword tracking report."""
        
        system_prompt = """
        Create a Shopee keyword ranking report for Indonesian sellers.
        Analyze keywords relevant to the given topic.
        
        Return JSON with:
        - name: product name
        - description: product description
        - report_date: today's date
        - shop_name: sample shop name related to topic
        - keywords: array of 50 keywords with:
          - keyword: Indonesian keyword
          - search_volume: realistic monthly searches (100-50000)
          - competition: "Low" / "Medium" / "High"
          - current_position: 1-100 or "Not Ranked"
          - previous_position: position last month
          - change: position change (-50 to +50)
          - cpc_estimate: cost per click in IDR (500-5000)
          - recommended_action: actionable advice in Indonesian
        - summary: executive summary in Indonesian
        - recommendations: array of 5 strategic recommendations
        """
        
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Create keyword report for Shopee seller in: {topic}"}
            ],
            response_format={"type": "json_object"},
            temperature=0.7
        )
        
        return json.loads(resp.choices[0].message.content)

    def _generate_hashtag_clusterer(self, topic: str):
        """Generate clustered hashtags for maximum reach."""
        
        system_prompt = """
        Create hashtag clusters for Indonesian social media marketing.
        Group hashtags by competition level and relevance.
        
        Return JSON with:
        - name: product name  
        - description: product description
        - clusters: array of 5 clusters:
          - cluster_name: "High Competition" / "Medium Competition" / "Low Competition" / "Branded" / "Community"
          - hashtags: array of 20 hashtags with:
            - tag: hashtag with # symbol
            - posts_count: estimated post count
            - engagement_rate: percentage like "3.5"
            - best_time: optimal posting time
        - usage_guide: strategy guide in Indonesian
        - monthly_calendar: object with days as keys, cluster recommendations as values
        """
        
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Create hashtag clusters for: {topic}"}
            ],
            response_format={"type": "json_object"},
            temperature=0.7
        )
        
        return json.loads(resp.choices[0].message.content)

    def _generate_copy_swipes(self, topic: str):
        """Generate copywriting swipe file."""
        
        system_prompt = """
        Create a comprehensive copywriting swipe file for Indonesian businesses.
        Include various copy types and proven formulas.
        
        Return JSON with:
        - name: product name
        - description: product description
        - categories: array of category names
        - swipe_sections: array of sections with:
          - name: section name
          - swipes: array of 10 swipes with:
            - title: swipe title
            - type: "Headline" / "Body Copy" / "CTA" / "Hook"
            - content: the actual copy in Indonesian
            - conversion_rate: estimated rate (2-15)
            - click_rate: estimated CTR (1-8)
            - best_for: ideal use case
        - usage_tips: array of 5 tips with:
          - title: tip title
          - content: tip description in Indonesian
        """
        
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Create copy swipes for: {topic}"}
            ],
            response_format={"type": "json_object"},
            temperature=0.8
        )
        
        return json.loads(resp.choices[0].message.content)

    # ============== CANVA ASSETS ==============
    
    def _generate_batik_patterns(self, topic: str):
        """Generate batik pattern collection."""
        
        system_prompt = """
        Create a digital batik pattern collection inspired by Indonesian heritage.
        Design patterns suitable for Canva and digital design.
        
        Return JSON with:
        - name: product name
        - description: product description
        - patterns: array of 40 patterns with:
          - name: pattern name (Indonesian batik motif)
          - region: Indonesian region of origin
          - preview_url: placeholder URL
          - format: "PNG" / "SVG"
          - resolution: "300 DPI"
          - seamless: "Yes" / "No"
          - colors: array of 4-5 hex color codes
        - usage_examples: array of 6 examples with:
          - icon: emoji icon
          - title: use case title
          - description: how to use
        - license_terms: licensing information in Indonesian
        """
        
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Create batik pattern collection for: {topic}"}
            ],
            response_format={"type": "json_object"},
            temperature=0.8
        )
        
        return json.loads(resp.choices[0].message.content)

    def _generate_brand_kit(self, topic: str):
        """Generate complete brand kit."""
        
        system_prompt = """
        Create a comprehensive brand kit for Indonesian businesses.
        Include all essential brand elements.
        
        Return JSON with:
        - name: product name
        - description: product description
        - logos: array of 4 logo variants with:
          - name: variant name
          - preview: placeholder text
          - background: hex color
          - usage: when to use
        - colors: array of 6 brand colors with:
          - name: color name
          - hex: hex code
          - rgb: RGB values
          - cmyk: CMYK values
        - fonts: array of 3 fonts with:
          - name: font name
          - family: font family
          - category: "Heading" / "Body" / "Accent"
          - sample_text: Indonesian sample text
          - sample_size: font size
          - weights: array of available weights
        - templates: array of 12 Canva templates with:
          - name: template name
          - icon: emoji
          - dimensions: size like "1080x1080"
          - format: "Instagram Post" / "Story" / etc
        - guidelines: array of 5 brand guidelines with:
          - icon: emoji
          - title: guideline title
          - description: guideline details
          - dos: array of 3 do's
          - donts: array of 3 don'ts
        """
        
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Create brand kit for: {topic}"}
            ],
            response_format={"type": "json_object"},
            temperature=0.7
        )
        
        return json.loads(resp.choices[0].message.content)

    def _generate_capcut_templates(self, topic: str):
        """Generate CapCut video templates."""
        
        system_prompt = """
        Create CapCut video templates for Indonesian content creators.
        Focus on viral formats and trending styles.
        
        Return JSON with:
        - name: product name
        - description: product description
        - categories: array of category names
        - templates: array of 20 templates with:
          - name: template name
          - icon: emoji
          - duration: seconds (15/30/60)
          - music_type: "Upbeat" / "Chill" / "Dramatic" / "Trendy"
          - ratio: "9:16" / "1:1" / "16:9"
          - tags: array of 3 tags
          - features: array of 3 key features
        - tutorial_steps: array of 6 steps with:
          - title: step title
          - description: how to do it in Indonesian
        """
        
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Create CapCut templates for: {topic}"}
            ],
            response_format={"type": "json_object"},
            temperature=0.8
        )
        
        return json.loads(resp.choices[0].message.content)

    # ============== FINANCE PACK ==============
    
    def _generate_pajak_calculator(self, topic: str):
        """Generate tax calculator for UMKM."""
        
        system_prompt = """
        Create a comprehensive tax calculator for Indonesian UMKM.
        Include PPh Final and PPN calculations.
        
        Return JSON with:
        - name: product name
        - description: product description
        - location: "Jakarta" or other city
        - current_date: today's date
        - sample_data: object with:
          - monthly_revenue: realistic amount
          - annual_revenue: monthly * 12
          - tax_rate: 0.5 (for PPh Final)
          - monthly_tax: calculated tax
          - annual_tax: calculated annual tax
          - dpp: sample amount for PPN
          - ppn: 11% of dpp
          - total_with_ppn: dpp + ppn
        - tax_rules: array of 5 rules with:
          - criteria: rule description
          - rate: tax rate
          - notes: additional notes
        - tax_tips: array of 8 tax saving tips in Indonesian
        - tax_deadlines: array of 12 monthly deadlines with:
          - date: deadline date
          - description: what's due
        """
        
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Create tax calculator for UMKM in: {topic}"}
            ],
            response_format={"type": "json_object"},
            temperature=0.7
        )
        
        return json.loads(resp.choices[0].message.content)

    def _generate_cash_flow(self, topic: str):
        """Generate cash flow tracker."""
        
        system_prompt = """
        Create a comprehensive cash flow management system for Indonesian businesses.
        Include realistic transaction data and projections.
        
        Return JSON with:
        - name: product name
        - description: product description
        - summary: object with:
          - total_income: realistic monthly income
          - total_expense: realistic expenses
          - balance: income - expense
          - income_change: percentage change
          - expense_change: percentage change
          - balance_change: percentage change
          - runway_months: months of runway
          - burn_rate: monthly burn rate
        - transactions: array of 20 transactions with:
          - date: transaction date
          - description: transaction description in Indonesian
          - category: category name
          - type: "income" / "expense"
          - amount: transaction amount
          - balance: running balance
        - income_categories: array of 5 categories with:
          - name: category name
          - amount: total amount
          - percentage: percentage of total
          - color: hex color
        - expense_categories: array of 7 categories with:
          - name: category name
          - amount: total amount
          - percentage: percentage of total
          - color: hex color
        - projections: array of 6 monthly projections with:
          - month: month name
          - value: projected cash flow
        """
        
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Create cash flow tracker for: {topic}"}
            ],
            response_format={"type": "json_object"},
            temperature=0.7
        )
        
        return json.loads(resp.choices[0].message.content)

    def _generate_sop_templates(self, topic: str):
        """Generate SOP templates."""
        
        system_prompt = """
        Create comprehensive SOP templates for Indonesian businesses.
        Include step-by-step procedures and forms.
        
        Return JSON with:
        - name: product name
        - description: product description
        - version: "1.0"
        - last_updated: today's date
        - sop_categories: array of 6 categories with:
          - icon: emoji
          - name: category name
        - sop_documents: array of 3 SOPs with:
          - title: SOP title
          - effective_date: date
          - responsible: person responsible
          - revision: revision number
          - purpose: SOP purpose in Indonesian
          - scope: SOP scope
          - steps: array of 5-7 steps with:
            - title: step title
            - description: detailed description
            - checklist: array of 3-4 checklist items
          - form_template: object with:
            - title: form title
            - fields: array of 5 fields with label and placeholder
          - warnings: array of 2 warnings
          - tips: array of 3 tips
          - approval_flow: array of 3 approval steps with:
            - role: approver role
            - action: what they do
        """
        
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Create SOP templates for: {topic}"}
            ],
            response_format={"type": "json_object"},
            temperature=0.7
        )
        
        return json.loads(resp.choices[0].message.content)

    # ============== SEASONAL ==============
    
    def _generate_ramadan_calendar(self, topic: str):
        """Generate Ramadan content calendar."""
        
        system_prompt = """
        Create a comprehensive Ramadan calendar for Indonesian Muslims.
        Include prayer times, content ideas, and special days.
        
        Return JSON with:
        - name: product name
        - description: product description
        - location: "Jakarta" or other Indonesian city
        - current_date: formatted date
        - month_name: "Ramadan"
        - year: 2025
        - hijri_month: Hijri month name
        - hijri_year: Hijri year
        - weekdays: array of 7 weekday names in Indonesian
        - prayer_times: array of 5 prayers with:
          - name: prayer name
          - time: time like "04:30"
        - calendar_days: array of 30 days with:
          - number: day number
          - hijri: Hijri date
          - is_today: boolean
          - event: special event if any
        - content_categories: array of 4 categories with:
          - icon: emoji
          - title: category title
          - ideas: array of 5 content ideas
        - popular_hashtags: array of 20 Ramadan hashtags
        - special_days: array of special days with:
          - date: date
          - name: day name
          - description: significance
        """
        
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Create Ramadan calendar for: {topic}"}
            ],
            response_format={"type": "json_object"},
            temperature=0.7
        )
        
        return json.loads(resp.choices[0].message.content)

    def _generate_wedding_planner(self, topic: str):
        """Generate wedding planner."""
        
        system_prompt = """
        Create a comprehensive wedding planner for Indonesian couples.
        Include budget, timeline, vendors, and guest management.
        
        Return JSON with:
        - name: product name
        - description: product description
        - couple_names: "Andi & Siti"
        - wedding_date: date 6 months from now
        - total_budget: realistic Indonesian wedding budget
        - budget_items: array of 8 budget categories with:
          - category: category name
          - amount: allocated amount
          - percentage: percentage of total
        - timeline: array of 6 milestones with:
          - date: milestone date
          - title: milestone title
          - tasks: array of 3-4 tasks
        - vendors: array of 8 vendors with:
          - icon: emoji
          - name: vendor type
          - status: "booked" / "pending" / "searching"
          - status_text: status in Indonesian
          - description: vendor description
          - budget: allocated budget
          - phone: sample phone
          - location: location
        - guest_stats: object with:
          - total: total guests
          - confirmed: confirmed guests
          - pending: pending
          - tables: number of tables
        - guest_list: array of 10 sample guests with:
          - name: guest name
          - relation: relationship
          - pax: number of people
          - rsvp: "yes" / "no" / "pending"
          - rsvp_text: RSVP in Indonesian
          - table: table number
          - notes: any notes
        - todo_columns: array of 3 columns with:
          - title: column title
          - items: array of 5 todo items
        - important_notes: array of 3 notes with:
          - title: note title
          - content: note content
        """
        
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Create wedding planner for: {topic}"}
            ],
            response_format={"type": "json_object"},
            temperature=0.7
        )
        
        return json.loads(resp.choices[0].message.content)

    def _generate_yearend_planner(self, topic: str):
        """Generate year-end planner."""
        
        system_prompt = """
        Create a comprehensive year-end planner for Indonesian professionals.
        Include reflection, goals, and monthly planning.
        
        Return JSON with:
        - name: product name
        - description: product description
        - year: 2025
        - achievements: array of 6 achievements with:
          - icon: emoji
          - title: achievement title
          - description: achievement description
          - metric: key metric or number
        - goal_categories: array of 4 categories with:
          - icon: emoji
          - name: category name
          - goals: array of 5 goals with:
            - text: goal description
            - priority: "High" / "Medium" / "Low"
        - monthly_breakdown: array of 12 months with:
          - name: month name
          - focus: monthly focus area
          - tasks: array of 3 key tasks
        - habits: array of 6 habits with:
          - icon: emoji
          - name: habit name
          - frequency: daily/weekly/monthly
          - progress: percentage (0-100)
          - streak: current streak days
        - visions: array of 6 vision items with:
          - icon: emoji
          - title: vision title
          - description: vision description
        - reflection_prompts: array of 4 prompts with:
          - question: reflection question
          - placeholder: sample answer or guidance
        """
        
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Create year-end planner for: {topic}"}
            ],
            response_format={"type": "json_object"},
            temperature=0.7
        )
        
        return json.loads(resp.choices[0].message.content)