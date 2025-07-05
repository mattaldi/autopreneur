# agents.py
import os
import json
import uuid
from openai import OpenAI
from pathlib import Path

# Inisialisasi client OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class AnalystAgent:
    """Agent untuk menganalisis topik dan mendeteksi sinyal pasar."""
    
    def research_topic(self, topic: str) -> str:
        """Melakukan riset mendalam pada sebuah topik menggunakan web search."""
        system_prompt = (
            "You are Atlas, an elite research engine. Use web_search to gather real-time data. "
            "Produce a comprehensive Markdown report (~1,500 words) with sections, "
            "bullet points, and citations on the given topic."
        )
        # (Logika dari run_web_research di skrip Anda akan masuk ke sini)
        # ... untuk singkatnya, kita asumsikan ini mengembalikan teks laporan
        
        # Simulasi panggilan API dari skrip Anda
        print(f"🕵️  AnalystAgent: Researching '{topic}'...")
        resp = client.chat.completions.create(
            model="gpt-4-turbo", # atau gpt-4.1-mini jika tersedia
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": topic}
            ],
            # Fungsi web_search akan dipanggil secara otomatis oleh model ini
        )
        report_content = resp.choices[0].message.content
        print("✅  AnalystAgent: Research complete.")
        return report_content

    def score_idea(self, report_content: str) -> int:
        """Memberi skor pada ide berdasarkan laporan riset."""
        print("⚖️  AnalystAgent: Scoring a business idea...")
        resp = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are a Venture Capitalist. Based on the following research report, score the business potential from 0 to 100 for the Indonesian digital product market. Consider demand, competition, and monetization potential. Return ONLY the number."},
                {"role": "user", "content": report_content},
            ],
            temperature=0
        )
        try:
            score = int(resp.choices[0].message.content.strip())
            print(f"✅  AnalystAgent: Score given: {score}")
            return score
        except (ValueError, TypeError):
            return 0


class BuilderAgent:
    """Agent untuk membuat produk digital berdasarkan sebuah ide."""
    
    def generate_product_assets(self, topic: str, product_type: str = "caption_bank"):
        """Menghasilkan aset-aset yang dibutuhkan untuk sebuah produk."""
        if product_type == "caption_bank":
            print(f"🛠️  BuilderAgent: Generating 'AI Caption Bank' for '{topic}'...")
            
            # 1. Hasilkan nama produk dan deskripsi
            product_details_resp = client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[
                    {"role": "system", "content": "You are a creative product marketer. Create a catchy product name and a short, compelling description for an 'AI Caption Bank' product about the given topic for the Indonesian market. Return a JSON object with 'name' and 'description' keys."},
                    {"role": "user", "content": topic}
                ],
                response_format={"type": "json_object"}
            )
            details = json.loads(product_details_resp.choices[0].message.content)

            # 2. Hasilkan 30 caption dalam format JSON
            captions_resp = client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[
                    {"role": "system", "content": "You are a social media expert. Create 30 social media captions in Bahasa Indonesia about the given topic. Provide a mix of educational, engagement, and promotional content. Return a JSON object with a 'captions' key, which is a list of objects, each with 'day' and 'text' keys."},
                    {"role": "user", "content": topic}
                ],
                response_format={"type": "json_object"}
            )
            content = json.loads(captions_resp.choices[0].message.content)
            
            print("✅  BuilderAgent: Assets generated.")
            return {**details, **content}
        return None