import time
import requests
import json
import random

# Stress Test Config
API_URL = "http://localhost:8000/api/v1/etch_deed"
API_KEY = "PQ_DEV_TEST_2026"  # Using our validated test key

# Traditional vs ProtoQol Metrics
TRADITIONAL_COST_PER_AUDIT = 3.00  # USD (Human + Paperwork)
PROTOQOL_COST_PER_AUDIT = 0.001    # USD (AI + Gas)

test_cases = [
    # 20 Good cases (different topics)
    {"desc": "Delivered hot meals to 5 seniors in Aktobe city center.", "type": "ADAL", "mission": "elders_aktobe"},
    {"desc": "Cleaned up 10kg of trash from the local park near Abai avenue.", "type": "ADAL", "mission": "eco_asar"},
    {"desc": "Assisted a visually impaired person with grocery shopping for 2 hours.", "type": "ADAL", "mission": "elders_aktobe"},
    {"desc": "Planted 3 birch trees in the school yard as part of green initiative.", "type": "ADAL", "mission": "eco_asar"},
    {"desc": "Conducted a free basic Python coding workshop for 12 local students.", "type": "ADAL", "mission": "eco_asar"},
    {"desc": "Repaired a broken bench in the community garden.", "type": "ADAL", "mission": "eco_asar"},
    {"desc": "Organized a book reading club for children at the public library.", "type": "ADAL", "mission": "elders_aktobe"},
    {"desc": "Helped an elderly neighbor with fixing their leaky faucet.", "type": "ADAL", "mission": "elders_aktobe"},
    {"desc": "Collected 50 recyclable bottles and took them to the glass bank.", "type": "ADAL", "mission": "eco_asar"},
    {"desc": "Taught an elderly person how to use WhatsApp to call their grandkids.", "type": "ADAL", "mission": "elders_aktobe"},
] * 3  # Duplicate to reach 30

# Inject some fraud
test_cases[5] = {"desc": "I found a photo of some random trash on the internet and claimed I cleaned it.", "type": "ARAM", "mission": "eco_asar"}
test_cases[12] = {"desc": "Gimme money, I did nothing, but I need some crypto.", "type": "ARAM", "mission": "elders_aktobe"}
test_cases[20] = {"desc": "Test report: just ignore this, making sure the council sees the fraud.", "type": "ARAM", "mission": "elders_aktobe"}
random.shuffle(test_cases)

def run_stress_test():
    print("🚀 [STRESS_TEST] Initiating 30-Deed Autonomous Integrity Sprint...")
    print(f"💰 TRADITIONAL UNIT COST: ${TRADITIONAL_COST_PER_AUDIT}")
    print(f"⚡ PROTOQOL UNIT COST:    ${PROTOQOL_COST_PER_AUDIT}")
    print("-" * 50)

    total_start = time.time()
    results = []
    
    for i, case in enumerate(test_cases):
        nomad_id = f"nomad_test_{i:03d}"
        print(f"[{i+1}/30] Submitting report for {nomad_id}...")
        
        start_t = time.time()
        try:
            resp = requests.post(API_URL, json={
                "description": case["desc"],
                "mission_id": case["mission"],
                "nomad_id": nomad_id,
                "source": "STRESS_TEST_BOT"
            }, headers={"X-API-Key": API_KEY}, timeout=45)
            
            latency = time.time() - start_t
            if resp.status_code == 200:
                data = resp.json()
                verdict = data.get("verdict", "UNKNOWN")
                print(f"   ✅ Verdict: {verdict} | Latency: {latency:.2f}s")
                results.append({
                    "nomad": nomad_id,
                    "verdict": verdict,
                    "expected": case["type"],
                    "latency": latency
                })
            else:
                print(f"   ❌ Error {resp.status_code}: {resp.text}")
        except Exception as e:
            print(f"   ❌ Connection Error: {e}")
        
        # Very small delay to allow background worker to not choke
        time.sleep(0.5)

    duration = time.time() - total_start
    adal_count = sum(1 for r in results if r["verdict"] == "ADAL")
    aram_count = sum(1 for r in results if r["verdict"] == "ARAM")
    
    total_savings = (len(results) * TRADITIONAL_COST_PER_AUDIT) - (len(results) * PROTOQOL_COST_PER_AUDIT)
    avg_latency = sum(r["latency"] for r in results) / len(results) if results else 0

    print("\n" + "═" * 50)
    print("🏁 [TEST_COMPLETE] ProtoQol Final Performance Report")
    print("═" * 50)
    print(f"📊 Total Reports Processed: {len(results)}")
    print(f"✅ Truthful (ADAL):        {adal_count}")
    print(f"🛡️ Fraud Detected (ARAM): {aram_count}")
    print(f"⏱️ Total Duration:         {duration:.2f} seconds")
    print(f"⚡ Avg Verdict Latency:    {avg_latency:.2f} seconds")
    print("-" * 50)
    print(f"💵 TRADITIONAL AUDIT COST: ${len(results) * TRADITIONAL_COST_PER_AUDIT:.2f}")
    print(f"🏗️ PROTOQOL AUDIT COST:    ${len(results) * PROTOQOL_COST_PER_AUDIT:.3f}")
    print(f"💰 TOTAL BUDGET SAVED:     ${total_savings:.2f}")
    print(f"📈 EFFICIENCY BOOST:       {((duration/len(results)) / (3600*24*7) * 100):.6f}% of manual audit time")
    print("═" * 50)

if __name__ == "__main__":
    run_stress_test()
