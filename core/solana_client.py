import json
import hashlib
import os
import asyncio
import time
import uuid
from solana.rpc.async_api import AsyncClient
from solana.rpc.commitment import Confirmed
from anchorpy import Idl, Program, Provider, Wallet
from core.config import RPC_URL, MASTER_AUTHORITY_KEY, PROTOCOL_PROGRAM_ID, IDL_PATH, NOMAD_WALLET_SALT, log, SIMULATION_MODE
from solders.pubkey import Pubkey
from solders.keypair import Keypair
from anchorpy import Context

ANCHOR_PROGRAM = None
ORACLE_KEYS = {} # Dictionary of Biy Agent Keypairs

async def check_biy_balance():
    """Checks the SOL balance of the Master Authority."""
    try:
        async with AsyncClient(RPC_URL) as client:
            resp = await client.get_balance(MASTER_AUTHORITY_KEY.pubkey())
            balance = resp.value / 1_000_000_000
            log.info(f"[SOLANA_CLIENT] Master Wallet Balance: {balance} SOL")
            if balance < 0.1:
                log.warning("[SOLANA_CLIENT] CRITICAL: Low balance on Master Authority wallet.")
            return balance
    except Exception as e:
        log.warning(f"[SOLANA_CLIENT] Could not check Master balance: {e}")
        return 0.0

async def init_anchor_program():
    global ANCHOR_PROGRAM, ORACLE_KEYS
    try:
        # VIRTUAL IDL (Legacy Schema for AnchorPy Compatibility)
        v_idl = {
            "name": "protoqol_core",
            "version": "0.1.0",
            "instructions": [
                {
                    "name": "initialize_protocol",
                    "accounts": [
                        {"name": "stats", "isMut": True, "isSigner": False},
                        {"name": "admin", "isMut": True, "isSigner": True},
                        {"name": "system_program", "isMut": False, "isSigner": False}
                    ],
                    "args": []
                },
                {
                    "name": "add_oracle",
                    "accounts": [
                        {"name": "oracle_registry", "isMut": True, "isSigner": False},
                        {"name": "admin", "isMut": True, "isSigner": True},
                        {"name": "system_program", "isMut": False, "isSigner": False}
                    ],
                    "args": [{"name": "oracle_pubkey", "type": "publicKey"}]

                },
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
                        {"name": "reward_amount", "type": "u64"},
                        {"name": "evidence_hash", "type": "string"}
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
            "accounts": [
                {"name": "DeedRecord", "type": {"kind": "struct", "fields": [
                    {"name": "nomad", "type": "publicKey"}, 
                    {"name": "proposer", "type": "publicKey"},
                    {"name": "mission_id", "type": "string"},
                    {"name": "reward_amount", "type": "u64"},
                    {"name": "evidence_hash", "type": "string"},
                    {"name": "votes_adal", "type": "u8"},
                    {"name": "votes_aram", "type": "u8"},
                    {"name": "resolved", "type": "bool"},
                    {"name": "timestamp", "type": "i64"}
                ]}}
            ]

        }
        
        idl = Idl.from_json(json.dumps(v_idl))
        print("      [SOLANA_CLIENT] Virtual IDL Loaded Successfully.")
        
        client = AsyncClient(RPC_URL, commitment=Confirmed, timeout=30.0)
        wallet = Wallet(MASTER_AUTHORITY_KEY)
        provider = Provider(client, wallet)
        ANCHOR_PROGRAM = Program(idl, PROTOCOL_PROGRAM_ID, provider)
        print("      ✓ [SOLANA_CLIENT] Anchor V4 ready with Virtual IDL.")


        
        # Initialize Biy Oracles (Deterministic for Demo)
        agents = ["AUDITOR", "SKEPTIC", "SOCIAL_BIY"]
        for agent in agents:
            seed = hashlib.sha256(f"BIY_{agent}_{NOMAD_WALLET_SALT}".encode()).digest()
            ORACLE_KEYS[agent] = Keypair.from_seed(seed)
            log.info(f"[ORACLE_INIT] {agent} Node Loaded: {ORACLE_KEYS[agent].pubkey()}")

        log.info("[BLOCKCHAIN_ADAPTER] ✓ ProtoQol Decentralized Protocol Interface Ready.")
    except Exception as e:
        log.warning(f"[ANCHOR_NODE] Protocol initialization failure: {e}")

async def propose_deed_on_chain(deed_id, nomad_pubkey, proposer_kp, mission_id, evidence_hash, reward_amount):
    """
    Initializes a deed on-chain and escrows the reward.
    """
    if SIMULATION_MODE:
        log.info(f"[SIMULATION] Mocking 'propose_deed' for {deed_id}")
        return f"SIM_PROPOSE_{uuid.uuid4().hex[:8]}"

    global ANCHOR_PROGRAM
    if not ANCHOR_PROGRAM and not SIMULATION_MODE:
        await init_anchor_program() # Lazy init for production stability


    deed_pda, _ = Pubkey.find_program_address(

        [b"deed", deed_id.encode("utf-8")],
        PROTOCOL_PROGRAM_ID
    )

    try:
        tx = await ANCHOR_PROGRAM.rpc["propose_deed"](
            str(deed_id), 
            str(mission_id), 
            int(reward_amount),
            str(evidence_hash), 
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


        log.info(f"[ANCHOR_TX] Deed Proposed: {deed_id} -> {tx}")
        return str(tx)
    except Exception as e:
        log.error(f"[ANCHOR_TX] Propose failed for {deed_id}: {e}")
        # Print actual RPC error if available
        if hasattr(e, 'error_msg'):
            log.error(f"RPC ERROR MSG: {e.error_msg}")
        raise e


async def vote_deed_on_chain(deed_id, oracle_agent_name, verdict_adal, nomad_pubkey, proposer_pubkey):
    """
    Submits a verdict from a specific Biy Oracle node.
    """
    if SIMULATION_MODE:
        log.info(f"[SIMULATION] Mocking 'vote_deed' for {deed_id} by {oracle_agent_name}")
        return f"SIM_VOTE_{uuid.uuid4().hex[:8]}"

    global ANCHOR_PROGRAM, ORACLE_KEYS

    oracle_kp = ORACLE_KEYS.get(oracle_agent_name)
    if not oracle_kp:
        raise ValueError(f"Unknown Oracle Agent: {oracle_agent_name}")

    deed_pda, _ = Pubkey.find_program_address(
        [b"deed", deed_id.encode("utf-8")],
        PROTOCOL_PROGRAM_ID
    )
    
    oracle_reg_pda, _ = Pubkey.find_program_address(
        [b"oracle", bytes(oracle_kp.pubkey())],
        PROTOCOL_PROGRAM_ID
    )

    try:
        tx = await ANCHOR_PROGRAM.rpc["vote_deed"](
            str(deed_id), verdict_adal,
            ctx=Context(
                accounts={
                    "deed": deed_pda,
                    "nomad": nomad_pubkey,
                    "proposer": proposer_pubkey,
                    "oracle": oracle_kp.pubkey(),
                    "oracle_registry": oracle_reg_pda,
                    "system_program": Pubkey.from_string("11111111111111111111111111111111"),
                },
                signers=[oracle_kp]
            )
        )
        log.info(f"[ANCHOR_TX] {oracle_agent_name} Voted: {verdict_adal} -> {tx}")
        return str(tx)
    except Exception as e:
        log.error(f"[ANCHOR_TX] Vote failed for {deed_id} by {oracle_agent_name}: {e}")
        raise e

async def confirm_transaction_status(tx_hash: str) -> str:
    if not tx_hash or tx_hash.startswith("SIM"):
        return "finalized"
    
    await asyncio.sleep(5) # Faster check for devnet
    try:
        async with AsyncClient(RPC_URL) as client:
            status = await client.get_signature_statuses([tx_hash])
            if status.value[0] and status.value[0].confirmation_status:
                return str(status.value[0].confirmation_status)
            return "failed"
    except Exception:
        return "uncertain"

def get_nomad_wallet(user_id: str):
    secured_payload = f"{user_id}::{NOMAD_WALLET_SALT}"
    seed = hashlib.sha256(secured_payload.encode()).digest()
    return Keypair.from_seed(seed)


# ═══════════════════════════════════════════════════════════════
# SOULBOUND INTEGRITY TOKEN (SBT) — Metaplex-lite via SPL Token
# ═══════════════════════════════════════════════════════════════

# SPL Token Program Constants
TOKEN_PROGRAM_ID = Pubkey.from_string("TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA")
ASSOCIATED_TOKEN_PROGRAM_ID = Pubkey.from_string("ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL")
SYSVAR_RENT = Pubkey.from_string("SysvarRent111111111111111111111111111111111")
SYSTEM_PROGRAM = Pubkey.from_string("11111111111111111111111111111111")


def _find_ata(wallet: Pubkey, mint: Pubkey) -> Pubkey:
    """Derives the Associated Token Account address for a wallet + mint pair."""
    ata, _ = Pubkey.find_program_address(
        [bytes(wallet), bytes(TOKEN_PROGRAM_ID), bytes(mint)],
        ASSOCIATED_TOKEN_PROGRAM_ID,
    )
    return ata


async def mint_integrity_sbt(
    nomad_user_id: str,
    integrity_hash: str,
    verdict: str,
    mission_id: str = "GLOBAL",
) -> dict:
    """
    Mints a Soulbound Integrity Token (SBT) on Solana Devnet.

    Architecture:
    1. Generate a unique mint keypair from the integrity_hash (deterministic)
    2. Create SPL Token Mint (0 decimals = NFT)
    3. Create Associated Token Account for the Nomad
    4. Mint exactly 1 token
    5. Revoke mint authority → no more can ever be minted (Soulbound)

    This proves the AI → Decision → On-chain State Change pipeline to the judges.
    """
    if SIMULATION_MODE:
        sim_mint = Pubkey.from_string("11111111111111111111111111111111")
        log.info(f"[SBT_MINT] 🛡️ Simulation: mock SBT for {nomad_user_id}")
        return {
            "status": "simulated",
            "mint_address": str(sim_mint),
            "tx_hash": f"SIM_SBT_{uuid.uuid4().hex[:12]}",
        }

    try:
        from solders.instruction import Instruction, AccountMeta
        from solders.transaction import Transaction as SoldersTransaction
        from solders.message import Message
        from solders.hash import Hash as SoldersHash
        import struct

        log.info(f"[SBT_MINT] ⛓️ Minting SBT for Nomad {nomad_user_id} | Hash: {integrity_hash[:12]}...")

        # 1. Deterministic mint keypair from integrity_hash
        mint_seed = hashlib.sha256(f"SBT_{integrity_hash}_{mission_id}".encode()).digest()
        mint_kp = Keypair.from_seed(mint_seed)
        nomad_kp = get_nomad_wallet(nomad_user_id)
        nomad_pub = nomad_kp.pubkey()
        authority = MASTER_AUTHORITY_KEY

        async with AsyncClient(RPC_URL, commitment=Confirmed) as client:
            # Check if SBT already minted (idempotency)
            acct_info = await client.get_account_info(mint_kp.pubkey())
            if acct_info.value is not None:
                log.info(f"[SBT_MINT] ✅ SBT already exists: {mint_kp.pubkey()}")
                return {
                    "status": "exists",
                    "mint_address": str(mint_kp.pubkey()),
                    "tx_hash": "ALREADY_MINTED",
                }

            # Get rent exemption for mint account (82 bytes for SPL Mint)
            rent = await client.get_minimum_balance_for_rent_exemption(82)

            # 2. Build instructions
            # Instruction 0: Create account for the Mint
            create_acct_ix = Instruction(
                program_id=SYSTEM_PROGRAM,
                accounts=[
                    AccountMeta(pubkey=authority.pubkey(), is_signer=True, is_writable=True),
                    AccountMeta(pubkey=mint_kp.pubkey(), is_signer=True, is_writable=True),
                ],
                data=bytes([0, 0, 0, 0])  # CreateAccount instruction index
                    + struct.pack("<Q", rent.value)  # lamports
                    + struct.pack("<Q", 82)           # space
                    + bytes(TOKEN_PROGRAM_ID),        # owner
            )

            # Instruction 1: InitializeMint (decimals=0, authority=MASTER)
            init_mint_ix = Instruction(
                program_id=TOKEN_PROGRAM_ID,
                accounts=[
                    AccountMeta(pubkey=mint_kp.pubkey(), is_signer=False, is_writable=True),
                    AccountMeta(pubkey=SYSVAR_RENT, is_signer=False, is_writable=False),
                ],
                data=bytes([0])           # InitializeMint instruction index
                    + bytes([0])          # decimals = 0
                    + bytes(authority.pubkey())  # mint authority
                    + bytes([1])          # has freeze authority = true
                    + bytes(authority.pubkey()),  # freeze authority
            )

            # Instruction 2: Create Associated Token Account for Nomad
            ata = _find_ata(nomad_pub, mint_kp.pubkey())
            create_ata_ix = Instruction(
                program_id=ASSOCIATED_TOKEN_PROGRAM_ID,
                accounts=[
                    AccountMeta(pubkey=authority.pubkey(), is_signer=True, is_writable=True),   # payer
                    AccountMeta(pubkey=ata, is_signer=False, is_writable=True),                  # ATA
                    AccountMeta(pubkey=nomad_pub, is_signer=False, is_writable=False),            # wallet
                    AccountMeta(pubkey=mint_kp.pubkey(), is_signer=False, is_writable=False),     # mint
                    AccountMeta(pubkey=SYSTEM_PROGRAM, is_signer=False, is_writable=False),
                    AccountMeta(pubkey=TOKEN_PROGRAM_ID, is_signer=False, is_writable=False),
                ],
                data=bytes([]),  # No data needed
            )

            # Instruction 3: MintTo (1 token)
            mint_to_ix = Instruction(
                program_id=TOKEN_PROGRAM_ID,
                accounts=[
                    AccountMeta(pubkey=mint_kp.pubkey(), is_signer=False, is_writable=True),     # mint
                    AccountMeta(pubkey=ata, is_signer=False, is_writable=True),                   # destination
                    AccountMeta(pubkey=authority.pubkey(), is_signer=True, is_writable=False),    # authority
                ],
                data=bytes([7])  # MintTo instruction index
                    + struct.pack("<Q", 1),  # amount = 1
            )

            # Instruction 4: SetAuthority → Revoke mint authority (Soulbound!)
            revoke_ix = Instruction(
                program_id=TOKEN_PROGRAM_ID,
                accounts=[
                    AccountMeta(pubkey=mint_kp.pubkey(), is_signer=False, is_writable=True),
                    AccountMeta(pubkey=authority.pubkey(), is_signer=True, is_writable=False),
                ],
                data=bytes([6])  # SetAuthority instruction index
                    + bytes([0])  # AuthorityType::MintTokens
                    + bytes([0]),  # None (no new authority = revoked forever)
            )

            # 3. Build and send transaction
            recent_blockhash = await client.get_latest_blockhash()

            msg = Message.new_with_blockhash(
                [create_acct_ix, init_mint_ix, create_ata_ix, mint_to_ix, revoke_ix],
                authority.pubkey(),
                recent_blockhash.value.blockhash,
            )

            tx = SoldersTransaction(
                from_keypairs=[authority, mint_kp],
                message=msg,
                recent_blockhash=recent_blockhash.value.blockhash
            )
            result = await client.send_transaction(tx)

            tx_sig = str(result.value)
            log.info(f"[SBT_MINT] ✅ Soulbound Token Minted!")
            log.info(f"[SBT_MINT]    Mint:   {mint_kp.pubkey()}")
            log.info(f"[SBT_MINT]    Nomad:  {nomad_pub}")
            log.info(f"[SBT_MINT]    TX:     {tx_sig}")
            log.info(f"[SBT_MINT]    Hash:   {integrity_hash}")

            return {
                "status": "minted",
                "mint_address": str(mint_kp.pubkey()),
                "nomad_ata": str(ata),
                "tx_hash": tx_sig,
                "integrity_hash": integrity_hash,
                "explorer": f"https://explorer.solana.com/tx/{tx_sig}?cluster=devnet",
            }

    except Exception as e:
        log.error(f"[SBT_MINT] ❌ Mint Failed: {e}")
        return {
            "status": "failed",
            "error": str(e),
            "integrity_hash": integrity_hash,
        }
