import time
import hashlib
from fastapi import APIRouter, Form, HTTPException, Query
from solders.pubkey import Pubkey
from anchorpy import Context

from config import ACTIVE_MISSIONS, VALID_API_KEYS, MASTER_BIY, PROTOQOL_PROGRAM_ID, log
from core import ai_engine, solana_client, state

router = APIRouter(prefix="", tags=["Oracle"])

@router.get("/", tags=["System"])
async def root():
    return {
        "protocol": "ProtoQol_v3",
        "status": "online",
        "oracle_nodes": 4,
        "chain": "Solana Devnet",
        "total_events": len(state.GLOBAL_PULSE),
        "boot_time": state.PROTOCOL_STATS["boot_time"],
    }

@router.get("/protocol_pulse", tags=["Network"])
async def get_pulse(limit: int = Query(5, ge=1, le=20)):
    return sorted(state.GLOBAL_PULSE[-limit:], key=lambda x: x['ts'], reverse=True)

@router.get("/protocol_stats", tags=["Network"])
async def get_stats():
    return state.PROTOCOL_STATS

@router.post("/verify", tags=["Oracle"])
async def ritual_verify(
    description: str = Form(...),
    telegram_id: str = Form("UnknownNomad"),
    mission_id: str = Form(None),
    api_key: str = Form("PQ_DEV_TEST_2026"),
):
    if api_key not in VALID_API_KEYS:
        raise HTTPException(status_code=401, detail="Unauthorized Oracle Access.")

    if not mission_id or mission_id not in ACTIVE_MISSIONS:
        raise HTTPException(status_code=400, detail="Unknown Mission mandate.")

    mission_info = ACTIVE_MISSIONS[mission_id]
    log.info(f"[REQUEST] mission={mission_id}, nomad={telegram_id[:12]}…")

    # 1. AI CONSENSUS
    ai_res = await ai_engine.analyze_deed(description, mission_info)
    verdict = ai_res.get("verdict", "ARAM")
    wisdom = ai_res.get("wisdom", "...")
    raw_score = float(ai_res.get("impact_score", 0))

    weighted_score = raw_score * mission_info.get("impact_weight", 1.0)
    points = int(weighted_score * 100) if verdict == "ADAL" else 0

    # 2. PQ-STANDARD INTEGRITY HASH
    content_payload = f"{description}|{mission_id}|{telegram_id}|{int(time.time())}"
    integrity_hash = hashlib.sha256(content_payload.encode()).hexdigest()[:16]

    # 3. NOMAD SHADOW WALLET
    user_kp = solana_client.get_nomad_wallet(telegram_id)
    tx_hash = "ON_CHAIN_ETCHING_FAILED"

    # 4. ON-CHAIN GASLESS ANCHOR CALL
    if verdict == "ADAL":
        if not solana_client.ANCHOR_PROGRAM:
            log.warning("[ANCHOR_NODE] Target Program disconnected. Emulating finality.")
            tx_hash = f"SIM_ANCHOR_{int(time.time()*100)}"
        else:
            try:
                deed_id = f"D_{int(time.time()*1000)}"
                nomad_pubkey = user_kp.pubkey()

                deed_pda, _ = Pubkey.find_program_address(
                    [b"deed", bytes(nomad_pubkey), deed_id.encode("utf-8")],
                    PROTOQOL_PROGRAM_ID
                )
                profile_pda, _ = Pubkey.find_program_address(
                    [b"profile", bytes(nomad_pubkey)],
                    PROTOQOL_PROGRAM_ID
                )

                log.info(f"[ANCHOR_NODE] Routing transaction. Payer: {MASTER_BIY.pubkey()}")
                
                # Check for the global program object correctly
                tx = await solana_client.ANCHOR_PROGRAM.rpc["etch_deed"](
                    nomad_pubkey,
                    deed_id,
                    mission_id,
                    points,
                    verdict,
                    integrity_hash,
                    ctx=Context(
                        accounts={
                            "deed_record": deed_pda,
                            "nomad_profile": profile_pda,
                            "oracle": MASTER_BIY.pubkey(),
                            "system_program": Pubkey.from_string("11111111111111111111111111111111"),
                        },
                        signers=[MASTER_BIY]
                    )
                )
                tx_hash = str(tx)
                log.info(f"[ANCHOR_TX] Signature: {tx_hash[:24]}...")
                
            except Exception as e:
                log.error(f"[ANCHOR_TX] CRITICAL NETWORK ERROR: {e}")
                raise HTTPException(status_code=503, detail="SOLANA_NETWORK_ERROR")

    # 5. GLOBAL PULSE UPDATE
    new_event = {
        "ts": time.time(),
        "mission_id": mission_id,
        "foundation_id": mission_info['foundation_id'],
        "status": verdict,
        "impact_points": points,
        "wisdom": wisdom,
        "integrity_hash": integrity_hash,
        "tx_hash": tx_hash,
        "wallet_address": str(user_kp.pubkey()),
        "accent": mission_info['theme_accent'],
    }
    state.GLOBAL_PULSE.append(new_event)

    state.PROTOCOL_STATS["total_audits"] += 1
    if verdict == "ADAL":
        state.PROTOCOL_STATS["adal_count"] += 1
        state.PROTOCOL_STATS["total_impact_score"] += raw_score
    else:
        state.PROTOCOL_STATS["aram_count"] += 1

    return new_event
