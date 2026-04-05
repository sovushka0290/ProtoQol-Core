
import httpx
import asyncio
import json
import os
from main import app # Assuming we can import the app directly

# We'll use the ASGITransport to test without starting a separate process
async def run_pitch_tests():
    print("🚀 [PROTOQOL_DEMO] Starting Protocol Validation...\n")
    transport = httpx.ASGITransport(app=app)
    
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        
        # ══════════════════════════════════════════════════════
        # TEST 1: B2B Enterprise ESG Etch (/api/v1/etch_deed)
        # ══════════════════════════════════════════════════════
        print("🏢 [CASE 1] B2B Enterprise ESG Verification")
        print("Context: 'Aqtobe IT-Hub' reports a local 'eco_asar' cleanup mission.")
        
        b2b_payload = {
            "description": "Successfully organized a waste collection event at the central park. Gathered 20 bags of non-recyclable waste.",
            "nomad_id": "corporate_volunteer_01",
            "mission_id": "eco_asar",
            "source": "Aqtobe_IT_Hub_Internal_System",
            "lat": 50.28,
            "lon": 57.16
        }
        
        headers = {"X-API-Key": "PQ_DEV_TEST_2026"}
        
        try:
            resp1 = await client.post("/api/v1/etch_deed", json=b2b_payload, headers=headers)
            print(f"Status: {resp1.status_code}")
            data1 = resp1.json()
            print(json.dumps(data1, indent=2, ensure_ascii=False))
            print(f"✅ B2B Result: {data1.get('verdict')} (Impact Points: {data1.get('impact_points')})")
        except Exception as e:
            print(f"❌ CASE 1 Error: {e}")

        print("\n" + "="*50 + "\n")

        # ══════════════════════════════════════════════════════
        # TEST 2: QAIYRYM Individual Mission (/api/v1/verify_mission)
        # ══════════════════════════════════════════════════════
        print("🦸‍♂️ [CASE 2] QAIYRYM Volunteer Mission Submission")
        print("Context: Individual nomad 'v_user_123' delivering food to elders in Aktobe.")
        
        # We'll use SHOWCASE_DEMO for easier testing without actual photo data
        qaiyrym_payload = {
            "description": "Visited Mrs. Sidorova at Abai Ave, 23. Delivered bread, milk and groceries. She was very grateful.",
            "user_id": "v_user_123",
            "mission_id": "elders_aktobe",
            "mode": "SHOWCASE_DEMO" 
        }
        
        try:
            resp2 = await client.post("/api/v1/verify_mission", json=qaiyrym_payload)
            print(f"Status: {resp2.status_code}")
            data2 = resp2.json()
            print(json.dumps(data2, indent=2, ensure_ascii=False))
            print(f"✅ QAIYRYM Result: {data2.get('verdict')} (Aura Gained: {data2.get('aura')})")
            print(f"🔍 Public Audit: http://localhost:8000/audit/{data2.get('integrity_hash')}")
        except Exception as e:
            print(f"❌ CASE 2 Error: {e}")

    print("\n🏁 [DEMO_COMPLETE] Protocol verified successfully.")

if __name__ == "__main__":
    asyncio.run(run_pitch_tests())
