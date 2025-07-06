# fix_existing_data.py
"""
Script to fix existing data if needed
"""

import json
from pathlib import Path

def check_and_fix_data():
    """Check and fix existing JSON data files"""
    
    # Check signals
    signals_path = Path("db/signals.json")
    if signals_path.exists():
        print("Checking signals.json...")
        try:
            with open(signals_path, 'r', encoding='utf-8') as f:
                signals = json.load(f)
            print(f"✅ Found {len(signals)} signals")
            
            # Check for any issues
            for signal in signals:
                print(f"  - Signal {signal['id']}: {signal['topic'][:30]}... (Score: {signal['score']}, Status: {signal['status']})")
                
        except Exception as e:
            print(f"❌ Error reading signals: {e}")
    
    # Check products
    products_path = Path("db/products.json")
    if products_path.exists():
        print("\nChecking products.json...")
        try:
            with open(products_path, 'r', encoding='utf-8') as f:
                products = json.load(f)
            print(f"✅ Found {len(products)} products")
            
            for product in products:
                print(f"  - Product {product['id']}: {product['name']}")
                
        except Exception as e:
            print(f"❌ Error reading products: {e}")
    
    print("\nData check complete!")

if __name__ == "__main__":
    print("=" * 70)
    print("AUTOPRENEUR - Data Check & Fix Utility")
    print("=" * 70)
    
    check_and_fix_data()
    
    print("\nIf you see any errors above, you may need to:")
    print("1. Check your JSON files for syntax errors")
    print("2. Ensure all required fields are present")
    print("3. Run the main program to regenerate products")
