import json
import hashlib
import os
import asyncio
import time
import uuid
from solana.rpc.async_api import AsyncClient
from solana.rpc.commitment import Confirmed
from anchorpy import Idl, Program, Provider, Wallet
from solders.pubkey import Pubkey
from solders.keypair import Keypair
from anchorpy import Context

# Enterprise Modular Imports
from core.config import RPC_URL, MASTER_AUTHORITY_KEY, PROTOCOL_PROGRAM_ID, NOMAD_WALLET_SALT, log, SIMULATION_MODE

ANCHOR_PROGRAM = None
ORACLE_KEYS = {} # Dictionary of Biy Agent Keypairs

async def check_biy_balance():
    try:
        async with AsyncClient(RPC_URL) as client:
            resp = await client.get_balance(MASTER_AUTHORITY_KEY.pubkey())
            balance = resp.value / 1_000_000_000
            log.info(f"[SOLANA_CLIENT] Master Wallet Balance: {balance} SOL")
            return balance
    except Exception as e:
        log.warning(f"[SOLANA_CLIENT] Could not check Master balance: {e}")
        return 0.0

async def init_anchor_program():
    global ANCHOR_PROGRAM, ORACLE_KEYS
    try:
        # VIRTUAL IDL: Protocol Definition for Decentralized Audits
        v_idl = {
            "name": "protoqol_core",
            "version": "0.1.0",
            "instructions": [
                {
                    "name": "propose_deed",
                    "accounts": [
                        {"name": "deed", "isMut": True, "isSigner": False},
                        {"name": "nomad", "isMut": False, "isSigner": False},
                        {"name": "proposer", "isMut": True, "isSigner": True},
                        {"name": "system_program", "isMut": False, "isSigner": False}
                    ],
                    "args": [
                        {"name": "deed_id", "type": "string"},
                        {"name": "mission_id", "type": "string"},
                        {"name": "evidence_hash", "type": "string"},
                        {"name": "reward_amount", "type": "u64"}
                    ]
                },
                {
                    "name": "vote_deed",
                    "accounts": [
                        {"name": "deed", "isMut": True, "isSigner": False},
                        {"name": "nomad", "isMut": True, "isSigner": False},
                        {"name": "proposer", "isMut": True, "isSigner": False},
                        {"name": "oracle", "isMut": True, "isSigner": True},
                        {"name": "oracle_registry", "isMut": False, "isSigner": False},
                        {"name": "system_program", "isMut": False, "isSigner": False}
                    ],
                    "args": [
                        {"name": "deed_id", "type": "string"},
                        {"name": "verdict_adal", "type": "bool"}
                    ]
                }
            ],
            "accounts": []
        }
        
        idl = Idl.from_json(json.dumps(v_idl))
        client = AsyncClient(RPC_URL, commitment=Confirmed, timeout=35.0)
        wallet = Wallet(MASTER_AUTHORITY_KEY)
        provider = Provider(client, wallet)
        ANCHOR_PROGRAM = Program(idl, PROTOCOL_PROGRAM_ID, provider)
        
        # Deterministic Biy Oracles Initialization
        for agent in ["AUDITOR", "SKEPTIC", "SOCIAL_BIY"]:
            seed = hashlib.sha256(f"BIY_{agent}_{NOMAD_WALLET_SALT}".encode()).digest()
            ORACLE_KEYS[agent] = Keypair.from_seed(seed)
            log.info(f"[ORACLE_LOAD] node::{agent} ready: {ORACLE_KEYS[agent].pubkey()}")

        log.info("[BLOCKCHAIN_ADAPTER] ✓ ProtoQol Enterprise Protocol Stack ready.")
    except Exception as e:
        log.warning(f"[SOLANA_CLIENT_FATAL] Initialization failure: {e}")

async def propose_deed_on_chain(deed_id, nomad_pubkey, proposer_kp, mission_id, evidence_hash, reward_amount):
    if SIMULATION_MODE: return f"SIM_PROPOSE_{uuid.uuid4().hex[:8]}"

    global ANCHOR_PROGRAM
    if not ANCHOR_PROGRAM: await init_anchor_program()

    deed_pda, _ = Pubkey.find_program_address(
        [b"deed", str(deed_id).encode("utf-8")],
        PROTOCOL_PROGRAM_ID
    )

    try:
        tx = await ANCHOR_PROGRAM.rpc["propose_deed"](
            str(deed_id), str(mission_id), str(evidence_hash), int(reward_amount),
            ctx=Context(
                accounts={
                    "deed": deed_pda,
                    "nomad": nomad_pubkey,
                    "proposer": proposer_kp.pubkey(),
                    "system_program": Pubkey.from_string("11111111111111111111111111111111"),
                },
                signers=[proposer_kp]
            )
        )
        log.info(f"[SOLANA_CLIENT] TX Proposed: {tx}")
        return str(tx)
    except Exception as e:
        log.error(f"[SOLANA_CLIENT] TX Error: {e}")
        raise e

async def vote_deed_on_chain(deed_id, oracle_agent_name, verdict_adal, nomad_pubkey, proposer_pubkey):
    if SIMULATION_MODE: return f"SIM_VOTE_{uuid.uuid4().hex[:8]}"

    global ANCHOR_PROGRAM, ORACLE_KEYS
    oracle_kp = ORACLE_KEYS.get(oracle_agent_name)
    deed_pda, _ = Pubkey.find_program_address([b"deed", str(deed_id).encode("utf-8")], PROTOCOL_PROGRAM_ID)
    oracle_reg_pda, _ = Pubkey.find_program_address([b"oracle", bytes(oracle_kp.pubkey())], PROTOCOL_PROGRAM_ID)

    try:
        tx = await ANCHOR_PROGRAM.rpc["vote_deed"](
            str(deed_id), verdict_adal,
            ctx=Context(
                accounts={
                    "deed": deed_pda,
                    "nomad": nomad_pubkey,
                    "proposer": proposer_pubkey,
                    "oracle": oracle_kp.pubkey(),
                    "oracleRegistry": oracle_reg_pda,
                    "systemProgram": Pubkey.from_string("11111111111111111111111111111111"),
                },
                signers=[oracle_kp]
            )
        )
        return str(tx)
    except Exception as e:
        log.error(f"[SOLANA_CLIENT] Vote failed: {e}")
        raise e

def get_nomad_wallet(user_id: str):
    seed = hashlib.sha256(f"{user_id}::{NOMAD_WALLET_SALT}".encode()).digest()
    return Keypair.from_seed(seed)


# ═══════════════════════════════════════════════════════════════
# SOULBOUND INTEGRITY TOKEN (SBT) — SPL Token Mint
# ═══════════════════════════════════════════════════════════════

TOKEN_PROGRAM_ID = Pubkey.from_string("TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA")
ASSOCIATED_TOKEN_PROGRAM_ID = Pubkey.from_string("ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL")
SYSVAR_RENT = Pubkey.from_string("SysvarRent111111111111111111111111111111111")
SYS_PROGRAM = Pubkey.from_string("11111111111111111111111111111111")


def _find_ata(wallet: Pubkey, mint: Pubkey) -> Pubkey:
    ata, _ = Pubkey.find_program_address(
        [bytes(wallet), bytes(TOKEN_PROGRAM_ID), bytes(mint)],
        ASSOCIATED_TOKEN_PROGRAM_ID,
    )
    return ata


async def mint_integrity_sbt(nomad_user_id: str, integrity_hash: str, verdict: str, mission_id: str = "GLOBAL") -> dict:
    """
    Mints a Soulbound Integrity Token after ADAL consensus:
    1. Create SPL Mint (0 decimals) → 2. Create ATA → 3. Mint 1 → 4. Revoke authority
    """
    if SIMULATION_MODE:
        log.info(f"[SBT_MINT] 🛡️ Simulation: mock SBT for {nomad_user_id}")
        return {"status": "simulated", "tx_hash": f"SIM_SBT_{uuid.uuid4().hex[:12]}"}

    try:
        from solders.instruction import Instruction, AccountMeta
        from solders.transaction import Transaction as SoldersTx
        from solders.message import Message
        import struct

        mint_seed = hashlib.sha256(f"SBT_{integrity_hash}_{mission_id}".encode()).digest()
        mint_kp = Keypair.from_seed(mint_seed)
        nomad_kp = get_nomad_wallet(nomad_user_id)
        authority = MASTER_AUTHORITY_KEY

        async with AsyncClient(RPC_URL, commitment=Confirmed) as client:
            acct = await client.get_account_info(mint_kp.pubkey())
            if acct.value is not None:
                return {"status": "exists", "mint_address": str(mint_kp.pubkey())}

            rent = await client.get_minimum_balance_for_rent_exemption(82)
            ata = _find_ata(nomad_kp.pubkey(), mint_kp.pubkey())

            ixs = [
                Instruction(SYS_PROGRAM, [
                    AccountMeta(authority.pubkey(), True, True),
                    AccountMeta(mint_kp.pubkey(), True, True),
                ], bytes([0,0,0,0]) + struct.pack("<Q", rent.value) + struct.pack("<Q", 82) + bytes(TOKEN_PROGRAM_ID)),

                Instruction(TOKEN_PROGRAM_ID, [
                    AccountMeta(mint_kp.pubkey(), False, True),
                    AccountMeta(SYSVAR_RENT, False, False),
                ], bytes([0,0]) + bytes(authority.pubkey()) + bytes([1]) + bytes(authority.pubkey())),

                Instruction(ASSOCIATED_TOKEN_PROGRAM_ID, [
                    AccountMeta(authority.pubkey(), True, True),
                    AccountMeta(ata, False, True),
                    AccountMeta(nomad_kp.pubkey(), False, False),
                    AccountMeta(mint_kp.pubkey(), False, False),
                    AccountMeta(SYS_PROGRAM, False, False),
                    AccountMeta(TOKEN_PROGRAM_ID, False, False),
                ], bytes([])),

                Instruction(TOKEN_PROGRAM_ID, [
                    AccountMeta(mint_kp.pubkey(), False, True),
                    AccountMeta(ata, False, True),
                    AccountMeta(authority.pubkey(), True, False),
                ], bytes([7]) + struct.pack("<Q", 1)),

                Instruction(TOKEN_PROGRAM_ID, [
                    AccountMeta(mint_kp.pubkey(), False, True),
                    AccountMeta(authority.pubkey(), True, False),
                ], bytes([6, 0, 0])),
            ]

            bh = await client.get_latest_blockhash()
            msg = Message.new_with_blockhash(ixs, authority.pubkey(), bh.value.blockhash)
            tx = SoldersTx.new([authority, mint_kp], msg, bh.value.blockhash)
            result = await client.send_transaction(tx)

            log.info(f"[SBT_MINT] ✅ Minted: {mint_kp.pubkey()} | TX: {result.value}")
            return {"status": "minted", "mint_address": str(mint_kp.pubkey()), "tx_hash": str(result.value)}

    except Exception as e:
        log.error(f"[SBT_MINT] ❌ Failed: {e}")
        return {"status": "failed", "error": str(e)}

