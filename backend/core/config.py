import os
import hashlib
import logging
from dotenv import load_dotenv
from solders.keypair import Keypair
from solders.pubkey import Pubkey

# Modular Boot Sequence for Monorepo
load_dotenv(os.path.join(os.path.dirname(__file__), "../../.env"))

# ═══════════════════════════════════════════════════════════════
# ENGINE CONFIGURATION (ProtoQol Enterprise)
# ═══════════════════════════════════════════════════════════════

VERSION = "3.8.5-ENT"
SIMULATION_MODE = False
ENGINE_NAME = "ProtoQol Decentralized Integrity Engine"

# Persistence Settings (Path tailored for Monorepo structure)
DB_PATH = os.path.join(os.path.dirname(__file__), "../db/protoqol_mvp.db")
DB_WAL_MODE = True
DB_TIMEOUT = 30.0

# ═══════════════════════════════════════════════════════════════
# LOGGING SYSTEM
# ═══════════════════════════════════════════════════════════════
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s][%(name)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
log = logging.getLogger("PROTOCOL_ENGINE")

# ═══════════════════════════════════════════════════════════════
# SOLANA BLOCKCHAIN ADAPTER
# ═══════════════════════════════════════════════════════════════
RPC_URL = os.getenv("RPC_URL", "https://api.devnet.solana.com")
PROTOCOL_PROGRAM_ID = Pubkey.from_string("EdrjHLN9K9eogJ5Pui8WYJRAghdN4knAdAoDcZesAirc")

# PDA Master Authority Key Generation
MASTER_AUTHORITY_SEED = os.getenv("MASTER_AUTHORITY_SECRET", "protoqol_master_engine_authority_2026")
authority_seed_bytes = hashlib.sha256(MASTER_AUTHORITY_SEED.encode()).digest()
MASTER_AUTHORITY_KEY = Keypair.from_seed(authority_seed_bytes)

# ═══════════════════════════════════════════════════════════════
# MULTI-AGENT AI CONSENSUS POOL
# ═══════════════════════════════════════════════════════════════

class KeyManager:
    def __init__(self):
        self.raw_keys = os.getenv("GEMINI_API_KEYS", "")
        self.pool = [k.strip() for k in self.raw_keys.split(",") if k.strip()]
        self._index = 0
        
    def get_key(self) -> str | None:
        if not self.pool: return os.getenv("GEMINI_API_KEY")
        key = self.pool[self._index % len(self.pool)]
        self._index += 1
        return key

ai_keys = KeyManager()

def get_next_engine_api_key():
    return ai_keys.get_key()

AI_TIMEOUT = 30.0

# ═══════════════════════════════════════════════════════════════
# CAMPAIGN REGISTRY
# ═══════════════════════════════════════════════════════════════
SERVICE_STATIC_CAMPAIGNS = {
    "elders_aktobe": {
        "client": "Ak-Niyet Foundation",
        "requirements": "Delivery for senior citizens. Photo/desc required.",
        "status": "active",
        "impact_weight": 1.2,
    },
    "eco_asar": {
        "client": "Aqtobe IT-Hub",
        "requirements": "Cleaning public spaces. Desc/Video proof required.",
        "status": "active",
        "impact_weight": 1.0,
    }
}
