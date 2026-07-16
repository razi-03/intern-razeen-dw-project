"""
🔍 GEMINI API KEY DIAGNOSTIC
Tests if your API key is valid and properly formatted
"""

import os
from pathlib import Path
from dotenv import load_dotenv

print("\n" + "="*80)
print("🔍 GEMINI API KEY DIAGNOSTIC")
print("="*80)

# Load .env
env_path = Path('.env')
if not env_path.exists():
    print("\n❌ ERROR: .env file not found!")
    print("   Create .env in your project folder with:")
    print("   GEMINI_API_KEY=your-api-key-here")
    exit(1)

print("\n✅ Found .env file")

# Read raw content
print("\n📄 Reading .env file...")
with open(env_path, 'r') as f:
    content = f.read()
    print(f"   Content: {content[:50]}...")

# Load with dotenv
load_dotenv(env_path)
api_key = os.getenv('GEMINI_API_KEY')

if not api_key:
    print("\n❌ ERROR: GEMINI_API_KEY not set in .env!")
    print("   Make sure .env contains: GEMINI_API_KEY=your-key")
    exit(1)

print(f"\n✅ API Key loaded from .env")

# Validate format
print(f"\n📋 API Key Analysis:")
print(f"   Length: {len(api_key)} characters")
print(f"   First 10 chars: {api_key[:10]}")
print(f"   Last 10 chars: {api_key[-10:]}")
print(f"   Contains dash (-): {'-' in api_key}")
print(f"   Contains underscore (_): {'_' in api_key}")
print(f"   All alphanumeric + dash/underscore: {all(c.isalnum() or c in '-_' for c in api_key)}")

# Check for common issues
print(f"\n🔎 Checking for common issues:")

issues = []

if len(api_key) < 20:
    issues.append("❌ Key is too short (should be 30+ characters)")

if api_key.startswith('sk-'):
    issues.append("⚠️  Key starts with 'sk-' (old format?)")

if api_key.startswith('AIza'):
    issues.append("⚠️  Key starts with 'AIza' (different Google service?)")

if ' ' in api_key:
    issues.append("❌ Key contains spaces (REMOVE THEM!)")

if api_key != api_key.strip():
    issues.append("❌ Key has leading/trailing whitespace (TRIM IT!)")

if not all(c.isalnum() or c in '-_' for c in api_key):
    issues.append("❌ Key contains invalid characters")

if issues:
    print("\n⚠️  ISSUES FOUND:")
    for issue in issues:
        print(f"   {issue}")
else:
    print("   ✅ Key format looks valid")

# Test with google.genai
print(f"\n🧪 Testing API connectivity...")
try:
    import google.genai as genai
    print(f"   ✅ google.genai imported")
    
    client = genai.Client(api_key=api_key)
    print(f"   ✅ Client created with your key")
    
    print(f"\n   🚀 Attempting simple API call...")
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents="Say 'works' if you can read this."
    )
    print(f"   ✅ API CALL SUCCESSFUL!")
    print(f"   Response: {response.text[:50]}")
    
except Exception as e:
    print(f"   ❌ API Error: {type(e).__name__}")
    print(f"   Message: {str(e)[:200]}")

print(f"\n" + "="*80)
print("DIAGNOSIS COMPLETE")
print("="*80)

print(f"""
NEXT STEPS:

If you see "API CALL SUCCESSFUL" above:
  ✅ Your key is valid! Categorizer should work.
  
If you see "API Error":
  ❌ Your API key is invalid. Get a new one:
  
  1. Go to: https://ai.google.dev/
  2. Click "Get API Key" button
  3. Create new API key
  4. Copy the ENTIRE key (it's long!)
  5. Replace the key in .env file
  6. Run this diagnostic again

KEY REQUIREMENTS:
  • Minimum length: 30+ characters
  • Only contains: letters, numbers, dashes, underscores
  • No spaces or special characters
  • From https://ai.google.dev/ (NOT from Google Cloud)
  • Fresh/not expired
""")
