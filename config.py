import os
import hashlib
import logging
from dotenv import load_dotenv
from solders.keypair import Keypair
from solders.pubkey import Pubkey

load_dotenv()

# Logger
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
log = logging.getLogger("protoqol")

# Solana Config
RPC_URL = os.getenv("RPC_URL", "https://api.devnet.solana.com")
PROTOQOL_PROGRAM_ID = Pubkey.from_string("Fg6PaFpoGXkYsidMpWTK6W2BeZ7FEfcYkg476zPFsLnS")
IDL_PATH = os.path.join(os.path.dirname(__file__), "protoqol_core/target/idl/protoqol_core.json")

# Master Biy Oracle
MASTER_BIY_SEED = os.getenv("MASTER_BIY_SECRET", "protoqol_master_authority_fallback_seed_2026")
master_seed_bytes = hashlib.sha256(MASTER_BIY_SEED.encode()).digest()
MASTER_BIY = Keypair.from_seed(master_seed_bytes)

# AI-Oracle Consensus Engines
RAW_KEYS = os.getenv("GEMINI_API_KEYS", os.getenv("GEMINI_API_KEY", ""))
GEMINI_API_KEYS = [k.strip() for k in RAW_KEYS.split(",") if k.strip()]

KEY_INDEX = 0

def get_next_gemini_key():
    global KEY_INDEX
    if not GEMINI_API_KEYS:
        return None
    key = GEMINI_API_KEYS[KEY_INDEX % len(GEMINI_API_KEYS)]
    KEY_INDEX += 1
    return key

# Auth
VALID_API_KEYS = {"PQ_DEV_TEST_2026", "AKTOBE_HUB_AUTHORITY", "PQ_LIVE_DEMO_SECRET"}

# Mission DB (Static for pitch)
ACTIVE_MISSIONS = {
    "elders_aktobe": {
        "client": "Ak-Niyet Foundation",
        "foundation_id": "AK_NIYET",
        "theme_accent": "#FFD700",
        "requirements": "Доставка помощи пожилым людям. Требуется описание места и перечня оказанной помощи.",
        "status": "active",
        "impact_weight": 1.2,
    },
    "eco_asar": {
        "client": "Aqtobe IT-Hub",
        "foundation_id": "AQTOBE_HUB",
        "theme_accent": "#64FFDA",
        "requirements": "Уборка парков или общественных пространств. Требуется описание объема выполненной работы.",
        "status": "active",
        "impact_weight": 1.0,
    },
    "it_mentorship": {
        "client": "Qol-Dau IT",
        "foundation_id": "QOL_DAU",
        "theme_accent": "#B388FF",
        "requirements": "Бесплатное обучение детей цифровой грамотности. Укажите количество учеников и тему.",
        "status": "active",
        "impact_weight": 1.5,
    },
}
