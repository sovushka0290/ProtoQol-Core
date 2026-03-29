import json
import hashlib
from solana.rpc.async_api import AsyncClient
from solana.rpc.commitment import Confirmed
from anchorpy import Idl, Program, Provider, Wallet
from config import RPC_URL, MASTER_BIY, PROTOQOL_PROGRAM_ID, IDL_PATH, log

ANCHOR_PROGRAM = None

async def init_anchor_program():
    global ANCHOR_PROGRAM
    try:
        with open(IDL_PATH, "r") as f:
            idl_dict = json.load(f)
        idl = Idl.from_json(idl_dict)
        client = AsyncClient(RPC_URL, commitment=Confirmed)
        wallet = Wallet(MASTER_BIY)
        provider = Provider(client, wallet)
        ANCHOR_PROGRAM = Program(idl, PROTOQOL_PROGRAM_ID, provider)
        log.info("[ANCHOR_NODE] ✓ ProtoQol Core Smart Contract Loaded.")
    except Exception as e:
        log.warning(f"[ANCHOR_NODE] Anchor IDL not ready yet. Deploy/Build in progress? ({e})")

async def check_biy_balance():
    pubkey = MASTER_BIY.pubkey()
    log.info(f"[BIY_ORACLE] Authority Address: {pubkey}")
    try:
        async with AsyncClient(RPC_URL) as client:
            balance = await client.get_balance(pubkey)
            sol = balance.value / 10**9
            log.info(f"[BIY_ORACLE] Sol Balance: {sol:.4f} SOL")
            if sol < 0.05:
                log.warning("[BIY_ORACLE] Critical Low Energy! Requesting Airdrop...")
                try:
                    await client.request_airdrop(pubkey, 1_000_000_000)
                except Exception as e:
                    log.warning(f"[BIY_ORACLE] Airdrop Error: {e}")
    except Exception as e:
        log.warning(f"[BIY_ORACLE] Network unavaible: {e}")

def get_nomad_wallet(user_id: str):
    seed = hashlib.sha256(user_id.encode()).digest()
    from solders.keypair import Keypair
    return Keypair.from_seed(seed)
