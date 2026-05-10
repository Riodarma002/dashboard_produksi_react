"""
Test script to verify data refresh functionality
"""
import requests
import json

API_BASE_URL = "http://localhost:8000"

def test_refresh():
    print("\n" + "="*60)
    print("🧪 TESTING DATA REFRESH")
    print("="*60)
    
    # 1. Check health before refresh
    print("\n1️⃣ Checking health before refresh...")
    try:
        response = requests.get(f"{API_BASE_URL}/api/health")
        health = response.json()
        print(f"   Status: {health['status']}")
        print(f"   Cache age: {health.get('cache_age_seconds', 'N/A')} seconds")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return
    
    # 2. Force refresh
    print("\n2️⃣ Forcing data refresh...")
    try:
        response = requests.post(f"{API_BASE_URL}/api/refresh", timeout=30)
        result = response.json()
        print(f"   Status: {result['status']}")
        print(f"   Message: {result['message']}")
        print(f"   Sheets available: {len(result.get('sheets_available', []))}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return
    
    # 3. Check health after refresh
    print("\n3️⃣ Checking health after refresh...")
    try:
        response = requests.get(f"{API_BASE_URL}/api/health")
        health = response.json()
        print(f"   Status: {health['status']}")
        print(f"   Cache age: {health.get('cache_age_seconds', 'N/A')} seconds")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return
    
    # 4. Get chart data for North JO IC
    print("\n4️⃣ Getting chart data for North JO IC...")
    try:
        response = requests.get(f"{API_BASE_URL}/api/charts/hourly?pit=North JO IC")
        chart_data = response.json()
        hours = [d['hour'] for d in chart_data['data']]
        print(f"   Hours with data: {', '.join(hours)}")
        print(f"   Total hours: {len(hours)}")
        
        # Show last 5 hours
        print(f"\n   Last 5 hours:")
        for d in chart_data['data'][-5:]:
            print(f"      {d['hour']}: OB={d['ob']}, CH={d['ch']}, Rain={d['rain']}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return
    
    print("\n" + "="*60)
    print("✅ TEST COMPLETE")
    print("="*60 + "\n")

if __name__ == "__main__":
    test_refresh()
