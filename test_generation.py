# test_generation.py
"""
Test script to verify caption generation works correctly
"""

import json
from agents import BuilderAgent

def test_caption_generation():
    """Test generating captions to check data structure"""
    print("Testing caption generation...")
    
    builder = BuilderAgent()
    topic = "ide konten untuk kedai kopi"
    
    try:
        # Generate caption bank
        assets = builder.generate_product_assets(topic, "caption_bank")
        
        print("\n✅ Generation successful!")
        print(f"Product name: {assets.get('name', 'N/A')}")
        print(f"Description: {assets.get('description', 'N/A')[:60]}...")
        print(f"Number of captions: {len(assets.get('captions', []))}")
        
        # Check caption structure
        if 'captions' in assets and assets['captions']:
            caption = assets['captions'][0]
            print(f"\nFirst caption structure:")
            print(f"- Day: {caption.get('day', 'N/A')}")
            print(f"- Text: {caption.get('text', 'N/A')[:50]}...")
            print(f"- Hashtags: {caption.get('hashtags', 'N/A')}")
            print(f"- Hashtags type: {type(caption.get('hashtags', None))}")
            
            # Test processing
            if 'hashtags' in caption and caption['hashtags']:
                if isinstance(caption['hashtags'], list):
                    hashtags_str = ' '.join(caption['hashtags'])
                    print(f"- Processed hashtags: {hashtags_str}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error during generation: {e}")
        return False

if __name__ == "__main__":
    print("=" * 70)
    print("AUTOPRENEUR - Caption Generation Test")
    print("=" * 70)
    
    success = test_caption_generation()
    
    if success:
        print("\n✅ Test passed! Caption generation is working correctly.")
        print("\nYou can now use the main program without errors:")
        print("python main.py")
    else:
        print("\n❌ Test failed. Please check the error messages above.")
