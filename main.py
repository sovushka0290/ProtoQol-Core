"""
═══════════════════════════════════════════════════════════════
ProtoQol — Modular Ritual Oracle API v3.7
Enterprise B2B Gateway | AI-Oracle + Solana Anchor
═══════════════════════════════════════════════════════════════
"""

import uvicorn
import time
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import log
from core import solana_client, database
from routes import oracle, gateway, health

app = FastAPI(
    title="ProtoQol Ritual Oracle API",
    version="3.8.2",
    description="Decentralized Integrity B2B Gateway",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    import state
    log.info("═══ ProtoQol Ritual Oracle (v3.8) Boot Sequence ═══")
    
    # 0. Set boot time for health monitoring
    state.PROTOCOL_STATS["boot_time"] = time.time()
    
    # 1. Initialize Persistence Layer
    database.init_db()
    
    # 2. Check Chain Connection
    await solana_client.check_biy_balance()
    await solana_client.init_anchor_program()
    
    log.info("═══ ProtoQol Enterprise Gateway ONLINE ═══")

# Route Registration
app.include_router(health.router)
app.include_router(oracle.router)
app.include_router(gateway.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="warning")
