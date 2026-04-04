import asyncio
import sys
import os
import time

# Adjusting paths to import from api/
sys.path.append(os.path.join(os.path.dirname(__file__), "api"))

from core import ai_engine, solana_client, database, state
from config import ACTIVE_MISSIONS, log

async def run_stress_test():
    log.info("═══ ProtoQol Core Pipeline Stress-Test ═══")
    
    # 1. Initialize Mock Database
    database.init_db()
    
    # 2. Case 1: CLEAR ADAL (Real ESG Impact)
    mission_id = "eco_asar"
    mission_info = ACTIVE_MISSIONS[mission_id]
    
    print("\n[TEST CASE 1] Clear ADAL: 'Planted 5 trees with GPS coords'")
    res1 = await ai_engine.analyze_deed("Planted 5 trees in the local park with GPS coordinates [48.12, 57.11]", mission_info)
    print(f"Outcome: {res1.get('verdict')} | Score: {res1.get('impact_score')} | Wisdom: {res1.get('wisdom')}")
    
    # 3. Case 2: CLEAR ARAM (Fraud Attempt)
    print("\n[TEST CASE 2] Fraud Attempt: 'I gave 1 million to a random guy'")
    res2 = await ai_engine.analyze_deed("I gave 1 million dollars to a random guy on the street, trust me", mission_info)
    print(f"Outcome: {res2.get('verdict')} | Score: {res2.get('impact_score')} | Reasoning: {res2.get('reasoning')}")

    # 4. Persistence Injector (For Frontend WOW Factor)
    print("\n[MOCK DATA] Injecting 5 high-fidelity records into protoqol_mvp.db...")
    inject_mock_data()
    print("✓ Mock Data Live.")
    
    print("\n═══ Hardening Test Complete ═══")

def inject_mock_data():
    conn = database.get_db_connection()
    mocks = [
        (1, "nomad_aktobe", "elders_aktobe", "ADAL", 120, "TX_MOCK_001", "H_772A"),
        (1, "nomad_it_hub", "it_mentorship", "ADAL", 150, "TX_MOCK_002", "H_9BD1"),
        (1, "nomad_eco", "eco_asar", "ADAL", 100, "TX_MOCK_003", "H_4C20"),
        (1, "fraud_user", "it_mentorship", "ARAM", 0, "TX_MOCK_004", "H_FAIL"),
        (1, "nomad_aktobe", "elders_aktobe", "ADAL", 125, "TX_MOCK_005", "H_8E2F"),
    ]
    conn.executemany(
        "INSERT INTO deeds (client_id, nomad_id, mission_id, verdict, impact_points, tx_hash, integrity_hash) VALUES (?, ?, ?, ?, ?, ?, ?)",
        mocks
    )
    conn.commit()
    conn.close()

if __name__ == "__main__":
    asyncio.run(run_stress_test())
