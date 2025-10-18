"""
Simple script to test usage tracking API endpoints
"""
import httpx
import time

BASE_URL = "http://localhost:8000"

def test_usage_endpoints():
    """Test the usage tracking endpoints"""
    
    print("🧪 Testing Usage Tracking Endpoints\n")
    print("=" * 60)
    
    # Test 1: Get global usage
    print("\n1. Testing Global Usage Endpoint...")
    try:
        response = httpx.get(f"{BASE_URL}/api/usage/global/summary", timeout=5.0)
        if response.status_code == 200:
            data = response.json()
            print("✅ Global Usage:")
            print(f"   Whisper: {data['usage']['whisper']['minutes']} minutes - {data['usage']['whisper']['cost']}")
            print(f"   GPT: {data['usage']['gpt']['total_tokens']} tokens - {data['usage']['gpt']['cost']}")
            print(f"   TTS: {data['usage']['tts']['characters']} chars - {data['usage']['tts']['cost']}")
            print(f"   TOTAL COST: {data['usage']['total_cost']}")
        else:
            print(f"❌ Failed with status {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 2: Check account balance
    print("\n2. Testing Account Balance Endpoint...")
    try:
        response = httpx.get(f"{BASE_URL}/api/account/balance", timeout=5.0)
        if response.status_code == 200:
            data = response.json()
            if data.get('available'):
                print("✅ Balance info available!")
                print(f"   {data}")
            else:
                print("ℹ️  Balance check not available with this API key")
                print(f"   Note: {data.get('note', 'N/A')}")
        else:
            print(f"⚠️  Status {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 3: List available scenarios (to get a session)
    print("\n3. Testing with Active Session...")
    print("   Start a conversation in the app, then we can track that session's usage")
    
    print("\n" + "=" * 60)
    print("\n✨ Usage Tracking Features Added:")
    print("   • Live cost tracking during conversation")
    print("   • Per-session usage breakdown")
    print("   • Global usage across all sessions")
    print("   • Detailed API cost estimates")
    print("\n📊 Open the app and check the metrics display!")
    print("   You'll see 'API Cost: $X.XX' updating in real-time\n")

if __name__ == "__main__":
    print("\n🚀 Make sure the server is running: python run.py")
    print("   Then run this script to test usage tracking\n")
    
    input("Press Enter when server is ready...")
    
    try:
        test_usage_endpoints()
    except httpx.ConnectError:
        print("\n❌ Could not connect to server!")
        print("   Make sure it's running with: python run.py")

