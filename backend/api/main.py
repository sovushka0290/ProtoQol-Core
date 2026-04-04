import os
import io
import json
import random
import time
from datetime import datetime
from typing import Optional, List, Dict, Any

from fastapi import FastAPI, HTTPException, Request, File, UploadFile, Form, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

# ═══════════════════════════════════════════════════════════════
# ENTERPRISE MONOREPO BOOTSTRAP
# ═══════════════════════════════════════════════════════════════

try:
    from core.config import log, ENGINE_NAME, VERSION, MASTER_AUTHORITY_KEY, SIMULATION_MODE
    from core import solana_client, ai_engine
    from db import database
except ImportError:
    # Fallback for direct execution
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    from core.config import log, ENGINE_NAME, VERSION, MASTER_AUTHORITY_KEY, SIMULATION_MODE
    from core import solana_client, ai_engine
    from db import database

app = FastAPI(
    title="ProtoQol Integrity Engine",
    version=VERSION,
    description="🚀 Universal Verification Protocol for ESG & Social Integrity."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ═══════════════════════════════════════════════════════════════
# ASYNC SETTLEMENT WORKERS
# ═══════════════════════════════════════════════════════════════

async def anchor_integrity_task(user_id: str, mission_id: str, integrity_hash: str, verdict: str):
    """Anchors the AI decision to Solana Devnet in the background."""
    try:
        nomad_kp = solana_client.get_nomad_wallet(str(user_id))
        log.info(f"[SOLANA_BACKBONE] ⛓️ Anchoring for {user_id} ({nomad_kp.pubkey()[:8]}...)")
        
        if verdict == "ADAL" and not SIMULATION_MODE:
            tx_sig = await solana_client.propose_deed_on_chain(
                deed_id=f"HACK_{mission_id}_{user_id}",
                nomad_pubkey=nomad_kp.pubkey(),
                proposer_kp=MASTER_AUTHORITY_KEY,
                mission_id=mission_id,
                evidence_hash=integrity_hash,
                reward_amount=10000000 
            )
            database.update_deed_status(integrity_hash, str(tx_sig), "finalized")

            for agent in ["AUDITOR", "SKEPTIC"]:
                await solana_client.vote_deed_on_chain(
                    deed_id=f"HACK_{mission_id}_{user_id}",
                    oracle_agent_name=agent,
                    verdict_adal=True,
                    nomad_pubkey=nomad_kp.pubkey(),
                    proposer_pubkey=MASTER_AUTHORITY_KEY.pubkey()
                )
            log.info(f"[SOLANA_BACKBONE] ✅ Discussion Anchored & SBT Minted.")
    except Exception as e:
        log.error(f"[SOLANA_BACKBONE] ❌ Anchorage Failure: {e}")

# ═══════════════════════════════════════════════════════════════
# B2B INQUIRY HUB
# ═══════════════════════════════════════════════════════════════

class InquirySubmission(BaseModel):
    name: str = Field(..., min_length=1)
    email: str = Field(..., min_length=5)
    message: str = Field(..., min_length=1)

@app.post("/api/v1/inquiry", tags=["B2B_Integrity"])
async def process_b2b_inquiry(data: InquirySubmission):
    log.warning(f"🚀 [B2B_LEAD] New Inquiry from {data.email} ({data.name})")
    return {
        "status": "success",
        "message": "Enquiry Secured",
        "tx_hash": f"PROTO_INQ_{random.randint(1000, 9999)}_x{random.randint(10, 99)}f777",
        "timestamp": datetime.now().isoformat()
    }

# ═══════════════════════════════════════════════════════════════
# OMNIVOROUS API GATEWAY
# ═══════════════════════════════════════════════════════════════

@app.post("/api/v1/verify_mission", response_class=JSONResponse, tags=["Impact_Verification"])
async def verify_mission(
    request: Request,
    background_tasks: BackgroundTasks,
    photo: Optional[UploadFile] = File(None),
    metadata: Optional[str] = Form(None)
):
    try:
        content_type = request.headers.get("content-type", "")
        if "multipart" in content_type:
            payload = json.loads(metadata) if metadata else {}
        else:
            payload = await request.json()

        log.info(f"[GATEWAY] 📥 Processing Audit for User: {payload.get('user_id')}")
        
        photo_bytes = await photo.read() if photo else None

        analysis = await ai_engine.analyze_deed(
            description=payload.get("description", "Mission report via AI Proxy."),
            mission_info=payload,
            meta=payload,
            photo_bytes=photo_bytes,
            mode=payload.get("mode", "REAL_MISSION")
        )

        master = analysis.get("master_consensus", {})
        database.save_deed({
            "wallet_address": payload.get("user_id"),
            "user_id": payload.get("user_id"),
            "mission_id": payload.get("mission_id"),
            "verdict": master.get("verdict", "ARAM"),
            "impact_score": analysis.get("impact_score", 0.0),
            "tx_hash": "Pending...",
            "integrity_hash": analysis.get("integrity_hash", "0x0"),
            "ai_dialogue": analysis.get("consensus_logs", {}),
            "wisdom": analysis.get("wisdom", "В единстве — правда.")
        }, payload)

        background_tasks.add_task(
            anchor_integrity_task, 
            payload.get("user_id"), 
            payload.get("mission_id"), 
            analysis.get("integrity_hash"), 
            master.get("verdict")
        )

        return {
            "status": "success",
            "verdict": master.get("verdict", "ARAM"),
            "wisdom": analysis.get("wisdom", "В единстве — правда."),
            "integrity_hash": analysis.get("integrity_hash"),
            "latency": f"{analysis.get('latency', 0):.2f}s",
            "audit_trail": "Solana Anchorage Initiated"
        }
    except Exception as e:
        log.critical(f"[CRITICAL_BACKEND] Resilience Triggered: {e}")
        return {"status": "warning", "verdict": "REVIEW_NEEDED", "wisdom": "Система в режиме защиты."}

@app.on_event("startup")
async def startup_event():
    database.init_db()
    await solana_client.check_biy_balance()
    log.info(f"🚀 {ENGINE_NAME} v{VERSION} OPERATIONAL")

@app.get("/audit/{integrity_hash}", tags=["Transparency"])
async def public_audit_mirror(integrity_hash: str):
    """The Public Glass Box: Cyberpunk Transparency Mirror."""
    deed = database.get_deed_by_hash(integrity_hash)
    if not deed: raise HTTPException(status_code=404, detail="Audit Link Invalid.")
    
    dialog = json.loads(deed.get('ai_dialogue', '{}'))
    if isinstance(dialog, str): dialog = json.loads(dialog)

    html_content = f"""
    <html>
    <head>
        <title>ProtoQol Audit: {integrity_hash[:8]}</title>
        <style>
            body {{ background: #050510; color: #00FFCC; font-family: 'Courier New', monospace; padding: 20px; }}
            .terminal {{ background: rgba(0,255,200,0.05); border: 2px solid #00FFCC; padding: 25px; border-radius: 12px; box-shadow: 0 0 20px #00FFCC33; max-width: 800px; margin: auto; }}
            .header {{ border-bottom: 2px solid #00FFCC; margin-bottom: 20px; padding-bottom: 10px; font-weight: 900; }}
            .node {{ margin-bottom: 15px; border-left: 2px solid #00FFCC; padding-left: 15px; opacity: 0.8; }}
            .verdict {{ font-size: 2.5em; text-align: center; margin: 30px 0; border: 4px solid #00FFCC; border-radius: 8px; text-transform: uppercase; }}
            .adal {{ color: #00FFCC; box-shadow: 0 0 30px #00FFCC66; }}
            .aram {{ border-color: #FF5555; color: #FF5555; }}
            .wisdom {{ font-style: italic; color: #FFD700; text-align: center; margin-top: 10px; }}
        </style>
    </head>
    <body>
        <div class="terminal">
            <div class="header">PROTO[Q]OL // INTEGRITY MIRROR v{VERSION}</div>
            <div style="opacity: 0.7;">ROOT_HASH: {integrity_hash}</div>
            <div class="verdict {'adal' if deed['verdict'] == 'ADAL' else 'aram'}">{deed['verdict']}</div>
            <div class="wisdom">"{deed.get('wisdom', 'В единстве — правда.')}"</div>
            <h4 style="margin-top: 40px;">◆ DECRYPTED COUNCIL DIALOGUE:</h4>
            {''.join([f'<div class="node"><b>[{k.upper()}]:</b> {v}</div>' for k,v in dialog.items() if v])}
        </div>
    </body>
    </html>
    """
    return StreamingResponse(io.BytesIO(html_content.encode()), media_type="text/html")

@app.get("/")
async def read_index():
    # Attempt to serve from frontend directory
    frontend_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "frontend/index.html")
    if os.path.exists(frontend_path):
        return FileResponse(frontend_path)
    return {"status": "ProtoQol API Active", "frontend": "Not Linked"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
