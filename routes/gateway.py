import time
import hashlib
from fastapi import APIRouter, Form, HTTPException, Depends
from solders.pubkey import Pubkey
from anchorpy import Context

from config import ACTIVE_MISSIONS, MASTER_BIY, PROTOQOL_PROGRAM_ID, log
from core import ai_engine, solana_client, state, database, auth

router = APIRouter(prefix="/api/v1", tags=["B2B Gateway"])

@router.post("/etch_deed")
async def enterprise_etch_deed(
    description: str = Form(...),
    nomad_id: str = Form(None),
    mission_id: str = Form(...),
    client: dict = Depends(auth.get_api_key)
):
    """
    Enterprise Standard Endpoint for B2B Clients.
    Automated Multi-Agent AI Consensus + Solana Gasless Settlement.
    """
    if mission_id not in ACTIVE_MISSIONS:
        raise HTTPException(status_code=400, detail="Unknown Mission mandate.")

    mission_info = ACTIVE_MISSIONS[mission_id]
    log.info(f"[B2B_GW] Client: {client['name']} | mission: {mission_id}")

    # 1. AI CONSENSUS
    ai_res = await ai_engine.analyze_deed(description, mission_info)
    verdict = ai_res.get("verdict", "ARAM")
    points = int(float(ai_res.get("impact_score", 0)) * 100) if verdict == "ADAL" else 0

    # 2. INTEGRITY HASH (PQ-Standard v1)
    integrity_hash = hashlib.sha256(f"{description}|{client['name']}|{time.time()}".encode()).hexdigest()[:16]

    # 3. SETTLEMENT
    tx_hash = "SIMULATED_TX"
    user_kp = solana_client.get_nomad_wallet(nomad_id or f"nomad_{time.time()}")
    
    if verdict == "ADAL":
        if solana_client.ANCHOR_PROGRAM:
            try:
                deed_id = f"EQ_{int(time.time()*1000)}"
                nomad_pubkey = user_kp.pubkey()
                deed_pda, _ = Pubkey.find_program_address([b"deed", bytes(nomad_pubkey), deed_id.encode()], PROTOQOL_PROGRAM_ID)
                profile_pda, _ = Pubkey.find_program_address([b"profile", bytes(nomad_pubkey)], PROTOQOL_PROGRAM_ID)

                tx = await solana_client.ANCHOR_PROGRAM.rpc["etch_deed"](
                    nomad_pubkey, deed_id, mission_id, points, verdict, integrity_hash,
                    ctx=Context(accounts={
                        "deed_record": deed_pda, "nomad_profile": profile_pda,
                        "oracle": MASTER_BIY.pubkey(), "system_program": Pubkey.from_string("11111111111111111111111111111111")
                    }, signers=[MASTER_BIY])
                )
                tx_hash = str(tx)
            except Exception as e:
                log.error(f"[GATEWAY_TX] Error: {e}")
                # We still want to log the event in DB as "Attempted/Failed"? 
                # For MVP we simple raise 503
                raise HTTPException(status_code=503, detail="Blockchain sync failed.")

    # 4. DB LOGGING (Persistence)
    conn = database.get_db_connection()
    conn.execute(
        "INSERT INTO deeds (client_id, nomad_id, mission_id, verdict, impact_points, tx_hash, integrity_hash) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (client['id'], nomad_id or "Anonymous", mission_id, verdict, points, tx_hash, integrity_hash)
    )
    conn.commit()
    conn.close()

    return {
        "status": "crystalized" if verdict == "ADAL" else "denied",
        "verdict": verdict,
        "tx_hash": tx_hash,
        "integrity_hash": integrity_hash,
        "impact_points": points,
        "auditor_wisdom": ai_res.get("wisdom", "")
    }

@router.get("/dashboard/stats")
async def get_client_stats(client: dict = Depends(auth.get_api_key)):
    conn = database.get_db_connection()
    stats = conn.execute(
        "SELECT COUNT(*) as total_deeds, SUM(impact_points) as total_points FROM deeds WHERE client_id = ?",
        (client['id'],)
    ).fetchone()
    
    recent = conn.execute(
        "SELECT tx_hash, verdict, impact_points, timestamp FROM deeds WHERE client_id = ? ORDER BY id DESC LIMIT 10",
        (client['id'],)
    ).fetchall()
    
    conn.close()
    
    return {
        "client_name": client['name'],
        "total_impact": stats['total_points'] or 0,
        "total_verifications": stats['total_deeds'] or 0,
        "recent_activity": [dict(r) for r in recent]
    }

@router.post("/dashboard/generate_key")
async def generate_new_api_key(new_client_name: str = Form(...), client: dict = Depends(auth.get_api_key)):
    # Simple internal admin-like check or just allow creation for MVP
    new_key = hashlib.sha256(f"{new_client_name}|{time.time()}".encode()).hexdigest()[:32]
    conn = database.get_db_connection()
    try:
        conn.execute("INSERT INTO clients (name, api_key) VALUES (?, ?)", (new_client_name, new_key))
        conn.commit()
        return {"name": new_client_name, "api_key": new_key}
    except Exception:
        raise HTTPException(status_code=400, detail="Client already exists.")
    finally:
        conn.close()
