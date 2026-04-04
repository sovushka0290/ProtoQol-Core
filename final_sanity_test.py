import requests
import json
import time

# ⚙️ CONFIGURATION
API_URL = "http://localhost:8000/api/v1/verify_mission"
MOCK_PHOTO = "https://images.unsplash.com/photo-1516738901171-ec347895f510?q=80&w=1000&auto=format&fit=crop" # A glass of water

def run_trial_audit():
    print("🚀 [TRIAL] Starting Interactive Showcase Audit (Cup Mission)...")
    
    payload = {
        "user_id": "JUDGE_777",
        "mission_id": "DEMO_CASE_01",
        "description": "Сдаю отчет: вот стакан воды на моем столе во время презентации.",
        "mode": "SHOWCASE_DEMO",
        "requirements": "Verify the presence of drinkware (cup/glass)."
    }
    
    try:
        # Simulate multipart form (even with mock photo URL for now)
        files = {
            "metadata": (None, json.dumps(payload))
        }
        
        t0 = time.time()
        response = requests.post(API_URL, files=files, timeout=15)
        latency = time.time() - t0
        
        if response.status_code == 200:
            res = response.json()
            print(f"✅ [RESULT] Verdict: {res.get('verdict')}")
            print(f"✨ [WISDOM] {res.get('wisdom')}")
            print(f"📊 [LATENCY] {latency:.2f}s")
            print(f"🔗 [AUDIT_LINK] Check here: http://localhost:8000/audit/{res.get('integrity_hash')}")
        else:
            print(f"❌ [ERROR] API Status {response.status_code}: {response.text}")
            
    except Exception as e:
        print(f"❌ [FATAL] Test failed: {e}")

if __name__ == "__main__":
    run_trial_audit()
