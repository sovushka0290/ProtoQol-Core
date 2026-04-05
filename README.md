# 🛡️ ProtoQol: Autonomous AI Integrity Engine on Solana

<div align="center">
  
  ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
  ![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
  ![Solana](https://img.shields.io/badge/Solana-9945FF?style=for-the-badge&logo=solana&logoColor=white)
  ![Gemini](https://img.shields.io/badge/Gemini_2.0-8E75B2?style=for-the-badge&logo=googlegemini&logoColor=white)
  ![Anchor](https://img.shields.io/badge/Anchor_Framework-00C2FF?style=for-the-badge)

  [🌐 ProtoQol Ecosystem Hub (Live Demo)](https://protoqol.vercel.app/hub.html)

  <h3>Case 2: AI + Blockchain — Autonomous Smart Contracts</h3>
  
  <p><b>ProtoQol</b> is a decentralized integrity engine where an AI multi-agent swarm (the "Biy Council") autonomously verifies ESG and social impact claims, reaches consensus, and executes on-chain actions — escrow release, oracle voting, and Soulbound Token minting — without human intervention.</p>

  [🚀 Live Bot](https://t.me/qaiyrym_bot) • [📹 Demo Video](https://youtu.be/WfGhMsGE2M8) • [🔍 View Program on Solana Explorer](https://explorer.solana.com/address/EdrjHLN9K9eogJ5Pui8WYJRAghdN4knAdAoDcZesAirc?cluster=devnet)
  
  > **Note:** Backend runs locally. See [Quick Start](#-quick-start) to launch in 60 seconds.
</div>

---

## 🎯 Problem Statement

**ESG fraud (greenwashing) is a $540B problem.** Companies and individuals fabricate social impact reports to gain reputation, grants, and regulatory benefits. Traditional verification relies on:
- Manual auditors (slow, expensive, biased)
- Static smart contracts that can't evaluate qualitative evidence (photos, descriptions)
- Centralized decision-making with no transparency

**ProtoQol solves this** by making AI the autonomous oracle that drives on-chain state changes.

### Why existing approaches fail

| Approach | Limitation | ProtoQol |
|----------|-----------|----------|
| Manual audit firms | Slow (weeks), expensive ($5k+), subjective | AI Council: **<3 seconds**, $0.001/verification |
| Static smart contracts | Cannot evaluate text, photos, or intent | Gemini 2.0 Flash with multimodal input |
| Centralized AI (GPT wrappers) | No transparency, no on-chain proof | Every decision SHA-256 anchored on Solana |
| Self-reported ESG scores | Easily fabricated, no verification | Multi-agent adversarial consensus (Skeptic vs Auditor) |

---

## 🌍 QAIYRYM Ecosystem: The First Client of the ProtoQol Protocol

> **Note:** The project is submitted to the hackathon under the name **QAIYRYM**, with ProtoQol serving as its foundational Integrity Layer. **QAIYRYM is the ecosystem and user interface**, while **ProtoQol is the technology driving it under the hood**.

**QAIYRYM (from Kazakh "Қайырым" — virtue/charity)** is a decentralized Telegram-based platform that unites volunteers, charitable foundations, and ESG-driven businesses into a single trusted environment. ProtoQol acts as the incorruptible, autonomous judge within this space.

### 🦸‍♂️ For Volunteers (Nomads)

* **Web2 Ease, Web3 Power:** Users interact via a familiar Telegram Mini-App. No wallet setup is required — the system automatically generates deterministic **Shadow Solana accounts** based on their Telegram IDs.
* **Guaranteed Rewards:** Upon completing a mission (e.g., delivering groceries to the elderly), volunteers upload a photo report **enriched with geolocation and timestamps**. If ProtoQol issues an `ADAL` (Truth) verdict, a Solana smart contract autonomously releases SOL rewards from escrow and mints an **Integrity Soulbound Token (SBT)**, building the user's verifiable social impact profile.
* **Transparent Growth:** Each confirmed `ADAL` verdict increases the volunteer's "Aura" — a dynamic on-chain reputation score. Higher Aura levels unlock more complex and highly-rewarded missions.

### 🏢 For Businesses & Foundations (B2B / ESG Sponsors)

* **Fraud Protection:** Organizations can fund local initiatives by depositing assets into Program Derived Accounts (PDAs). Funds are released **only** after cross-verification by the "AI Biy Council," including geolocation analysis, temporal validation, and multimodal photo audit.
* **Transparent ESG Reporting:** Zero greenwashing. Businesses receive a mathematically proven audit trail (anchored via SHA-256 hashes on Solana) to showcase to regulators, shareholders, or investors.
* **Real-time Webhooks:** The system dispatches automated notifications to a business endpoint upon every consensus event, providing full transaction metadata for seamless integration.

### 🤲 For Society (The Culture of "Asar")

* The platform restores faith in philanthropy. ProtoQol’s multi-layered fraud detection filters out:
  - 📷 **Stock photos** — via Gemini Vision visual analysis
  - 🤖 **AI-generations** — via neural network artifact recognition
  - ♻️ **Recycled reports** — via hash-based uniqueness checks
  - 📍 **Fake locations** — via geolocation cross-validation with mission zones
* This ensures that aid reaches real people in the physical world.

### 📊 QAIYRYM Economics: Traditional Approach vs Web3 (ROI)

How QAIYRYM fundamentally disrupts the economics of charitable campaigns (demonstrated on a local foundation case study distributing 500 food aid packages):

| Metric | Traditional Foundation (Without QAIYRYM) | QAIYRYM Ecosystem | Improvement / Savings |
| :--- | :--- | :--- | :--- |
| **Verification Cost** | Manual auditor/manager salaries (~$1,500) | AI Oracle API usage (~$1.5 for the entire pool) | **99.9% Budget Savings** |
| **Verification Time** | 2-3 weeks (manual calls, paper audits) | < 3 seconds per report | **Instant Consensus** |
| **Fraud Rate** | 15-20% average (fake signatures, duplicates) | ~0% (vision fraud detection, geolocation) | **100% Target Allocation** |
| **Volunteer Reward** | Paper certificates (easily forged) | Immutable SBT on Solana | **Verifiable Social Lift** |

**Bottom Line:** A single foundation saves up to $1,500 per campaign, redirecting those funds from bureaucracy to actual aid.

### What We Are Presenting

We are delivering more than just a protocol — we are showcasing a **fully functional end-to-end product**:

| Layer | Component | Technology |
|------|-----------|------------|
| **Frontend** | Telegram Mini-App (Volunteers) + Enterprise Dashboard (Business) | HTML/CSS/JS + Telegram Web App API |
| **AI Layer** | ProtoQol Multi-Agent Swarm ("The Biy Council") | Gemini 2.0 Flash (4 specialized nodes) |
| **Blockchain** | Smart contracts for voting, escrow, and SBT minting | Solana Devnet, Anchor Framework |

---

## 💰 Business Model & Revenue

ProtoQol targets the **$540B ESG compliance market**. The protocol operates as **"Stripe for Social Impact Verification"** — B2B clients pay per-verification through our API.

| Segment | Use Case | Revenue Model |
|---------|----------|---------------|
| **NGOs & Foundations** | Verify that donated funds actually reached beneficiaries | Per-verification fee via API |
| **Corporate CSR Departments** | Prove ESG compliance to shareholders without greenwashing risk | Monthly subscription (tiered plans) |
| **Government Agencies** | Validate grant-funded social projects at scale | Enterprise license + SLA |
| **ESG Investment Funds** | Verify impact data before allocating capital | Per-report + dashboard access |

### Business Integration (B2B SDK)

ProtoQol is not just an application — it is **infrastructure for trustless verification**. Any organization with an existing CSR reporting system can integrate ProtoQol as an independent external audit layer by connecting to our API:

```bash
# One API call = Full AI Council audit + On-chain settlement
curl -X POST https://protoqol.org/api/v1/etch_deed \
  -H "X-API-Key: YOUR_B2B_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Delivered 50kg of food supplies to rural school in Aktobe region",
    "nomad_id": "volunteer_042",
    "mission_id": "elders_aktobe",
    "source": "Partner_CSR_System"
  }'
```

**Response (< 3 seconds):**
```json
{
  "status": "crystalizing",
  "verdict": "ADAL",
  "integrity_hash": "a7f3b2e1c9d04f68",
  "impact_points": 87,
  "wisdom": "Қайырымдылық — жүректен шығады.",
  "ai_dialogue": [
    {"node": "AUDITOR", "verdict": "ADAL", "confidence": 0.92},
    {"node": "SKEPTIC", "verdict": "ADAL", "fraud_probability": 0.04},
    {"node": "SOCIAL_BIY", "verdict": "ADAL", "asar_score": 0.87}
  ]
}
```

Companies get: **AI-powered ESG verification**, **on-chain immutable proof**, **webhook notifications** on consensus, and a **real-time dashboard** (`/api/v1/dashboard/stats`) — all without building any blockchain infrastructure themselves.

### 🏢 Enterprise Use Cases: How ProtoQol Saves Millions

ProtoQol is more than a smart contract — it is a **Trust-as-a-Service (TaaS)** infrastructure solving global B2B pain points.

#### Case 1: International Grant Distribution (UN, USAID)
* **Problem:** Up to 30% of global grant funds are lost to intermediaries and local corruption before reaching the final stage.
* **ProtoQol Solution:** Grants are locked in Solana PDA escrows. Funds are released *only* after the AI Biy Council verifies real-world proof-of-work (e.g., photo + GPS validation of a newly built well or school).
* **Impact:** 100% cryptographic transparency. Zero possibility of bribing an automated auditor.

#### Case 2: Corporate ESG Audit (Anti-Greenwashing)
* **Problem:** Corporations claim to plant 10,000 trees to offset carbon, but investors demand independent audits costing tens of thousands of dollars to prove it.
* **ProtoQol Solution:** The company integrates the `/api/v1/etch_deed` endpoint. Field workers submit photos of planted trees via their app. ProtoQol autonomously verifies the uniqueness of each sapling, filters duplicates, and writes an immutable hash record to Solana.
* **Impact:** Corporations benefit from instant, publicly verifiable audits at near-zero cost, fully eliminating greenwashing reputation risks.

---

## 🏛️ Architecture: AI → Decision → On-Chain Action

```mermaid
graph TD
    User(("Volunteer / NGO")) -->|"Submit Report + Photo"| Gateway["FastAPI Integrity Gateway"]
    Gateway -->|"Multimodal Input"| Council["🧠 Neural Biy Council"]

    Council --> A1["⚔️ The Auditor\nFact-checks evidence"]
    Council --> A2["🔍 The Skeptic\nDetects fraud patterns"]
    Council --> A3["🤝 The Social Biy\nEvaluates sincerity"]
    Council --> A4["⚖️ Master Biy\nFinal consensus"]

    A4 -->|"ADAL ✅"| Chain["Solana Devnet"]
    A4 -->|"ARAM ❌"| Reject["Record Locally"]

    Chain --> P1["propose_deed\nEscrow funds in PDA"]
    P1 --> P2["vote_deed × 3\nOracle consensus"]
    P2 --> P3["Auto-resolve\nRelease escrow to volunteer"]
    P2 --> P4["mint_integrity_sbt\nSoulbound Token"]

    P4 --> Mirror["🔍 Public Audit Mirror\nSHA-256 anchored"]
```

### The Autonomous Pipeline

| Step | Component | What happens |
|------|-----------|-------------|
| 1️⃣ | **User** | Submits impact report + photo via Telegram Mini App |
| 2️⃣ | **AI Council** | 4-agent swarm (Gemini 2.0 Flash) analyzes evidence |
| 3️⃣ | **Verdict** | AI decides `ADAL` (truthful) or `ARAM` (fraudulent) |
| 4️⃣ | **propose_deed** | Anchor smart contract creates PDA, escrows SOL reward |
| 5️⃣ | **vote_deed ×3** | AI oracle agents vote on-chain → auto-resolve at quorum |
| 6️⃣ | **mint_sbt** | Soulbound Integrity Token minted to volunteer (non-transferable) |
| 7️⃣ | **Audit Mirror** | Full AI dialogue anchored via SHA-256 hash, publicly verifiable |

> **Key insight:** Steps 3→7 happen **autonomously** — no human in the loop.

---

## ⛓️ Smart Contract (Anchor / Rust)

**Program ID:** [`EdrjHLN9K9eogJ5Pui8WYJRAghdN4knAdAoDcZesAirc`](https://explorer.solana.com/address/EdrjHLN9K9eogJ5Pui8WYJRAghdN4knAdAoDcZesAirc?cluster=devnet)  
**Network:** Solana Devnet  
**Status:** ✅ Pre-deployed — no Rust/Anchor toolchain needed to run the demo

### Instructions

| Instruction | Purpose | State Change |
|------------|---------|-------------|
| `initialize_protocol` | Bootstrap protocol stats PDA | Creates `ProtocolStats` account |
| `add_oracle` | Register AI agent as on-chain oracle | Creates `OracleRegistry` PDA |
| `propose_deed` | Create deed + escrow SOL reward | Creates `DeedRecord` PDA, transfers lamports |
| `vote_deed` | Oracle casts ADAL/ARAM vote | Increments vote counters, auto-resolves at 3 votes |

### On-Chain Accounts

```rust
pub struct DeedRecord {
    pub nomad: Pubkey,          // Volunteer
    pub proposer: Pubkey,       // Foundation/B2B client
    pub mission_id: String,     // Campaign identifier
    pub reward_amount: u64,     // Escrowed SOL
    pub evidence_hash: String,  // SHA-256 of AI discussion
    pub votes_adal: u8,         // Positive votes
    pub votes_aram: u8,         // Negative votes
    pub resolved: bool,         // Auto-set at 3 votes
    pub timestamp: i64,         // On-chain clock
}
```

### Security Constraints
- Oracle voting requires `oracle_registry.is_active == true` (PDA-verified)
- Protocol admin is hardcoded to a specific Pubkey (zero-trust)
- Deed accounts are PDA-derived from `[b"deed", deed_id]` — collision-resistant

---

## 🧠 AI Multi-Agent System ("Council of Biys")

The "Biy Council" is inspired by the Kazakh steppe tradition of **Zheti Zhargy** (Seven Laws), where a council of wise men (Biys) would deliberate and reach consensus on matters of justice.

| Agent | Role | What it actually checks |
|-------|------|------------------------|
| ⚔️ **The Auditor** | Fact-checker | Multimodal photo analysis: object detection, geolocation cross-validation (`lat/lon` vs mission zone), timestamp freshness, and EXIF metadata consistency |
| 🔍 **The Skeptic** | Fraud detector | Reverse-image search patterns, AI-generated image artifacts (GAN fingerprints), recycled report detection via hash deduplication, and prompt injection attempts |
| 🤝 **The Social Biy** | Impact evaluator | Assesses "Asar" (communal spirit), calculates weighted social impact score based on mission difficulty and cultural context |
| ⚖️ **Master Biy** | Consensus judge | Aggregates all 3 node outputs. Only a unanimous or 2/3 majority vote triggers an `ADAL` on-chain settlement |

### Technical Details
- **Model:** Gemini 2.0 Flash (optimized for speed — target <2.5s response)
- **Multimodal input:** Text descriptions + photo evidence (base64 PNG) + geolocation metadata (`lat`, `lon`) + timestamps
- **Mode switching:** `REAL_MISSION` (strict — full fraud detection) vs `SHOWCASE_DEMO` (lenient for live demos)
- **Integrity anchor:** SHA-256 hash of the raw AI response = `integrity_hash`
- **API key rotation:** Round-robin pool across multiple Gemini keys to prevent 429 rate limits
- **Resilience:** Hard timeout (30s) + automatic fallback to `REVIEW_NEEDED` (never fakes a positive verdict)

---

## 🔒 Anti-Fraud: How QAIYRYM Makes Cheating Impossible

Fraud prevention is not an afterthought — it is **baked into every layer** of the protocol. Here is how each type of fraud is neutralized:

### 📍 Geolocation & Timestamp Verification

Every mission report carries metadata: `lat`, `lon`, and `timestamp`. The AI Auditor cross-validates this against the mission's expected geographic zone. A report claiming aid delivery in Aktobe but geotagged in Almaty will trigger an automatic `ARAM` (reject).

```python
# Metadata passed to the Biy Council for every verification
meta = {"lat": 50.2839, "lon": 57.1670, "timestamp": "2026-04-05T10:30:00Z"}
ai_res = await ai_engine.analyze_deed(description, mission_info, meta=meta, photo_bytes=photo)
```

### 📷 Multimodal Photo Forensics (Gemini Vision)

Photos aren't just stored — they are **analyzed pixel by pixel** by Gemini 2.0 Flash:

| Check | How it works | Example |
|-------|-------------|----------|
| **Object detection** | AI verifies the described objects actually appear in the photo | "Delivered food" → must detect food/packages in image |
| **Stock photo detection** | The Skeptic searches for visual patterns typical of stock photography | Professional lighting, watermarks, perfect composition → `FRAUD` |
| **AI-generated image detection** | Checks for GAN artifacts, unnatural textures, and deepfake patterns | DALL-E/Midjourney outputs → `FRAUD` |
| **Photo recycling** | SHA-256 hash of photo bytes compared against previous submissions | Same photo used twice → `ARAM` |

### ⏰ Temporal Integrity

- Reports are timestamped at submission and cross-checked against mission active periods
- The `integrity_hash` includes the timestamp, making retroactive tampering detectable
- Stale reports (submitted days after the claimed action) receive lower confidence scores

### 🛡️ Multi-Agent Adversarial Design

The key architectural insight: **The Skeptic and The Auditor are adversaries by design.** The Skeptic's entire purpose is to find flaws in the evidence that The Auditor might accept. This creates a natural checks-and-balances system where no single AI agent can unilaterally approve a fraudulent claim.

```
Auditor says PASS + Skeptic says FRAUD → Master Biy investigates deeper → likely ARAM
Auditor says PASS + Skeptic says CLEAN → Master Biy approves → ADAL
All 3 agents say FRAUD → Instant ARAM, no appeal
```

---

## 📡 Live On-Chain Proof

> **End-to-end example:** AI decision → smart contract state change → SBT mint

```
Input:   "Delivered food to 3 elderly residents in Aktobe"
AI:      ADAL (auditor: PASS, skeptic: CLEAN, asar: 0.87)
Deed TX: propose_deed → vote_deed ×2 → DeedRecord.resolved = true
SBT:     mint_integrity_sbt → 1 token, authority revoked (soulbound)
```

**Verify on-chain (real transactions from the ProtoQol Engine):**
- [🔍 View Deployed Program on Solana Explorer ↗](https://explorer.solana.com/address/EdrjHLN9K9eogJ5Pui8WYJRAghdN4knAdAoDcZesAirc?cluster=devnet)
- [📝 View Deed Proposed TX ↗](https://solscan.io/tx/4DuZMAkH1FTueetgB4AExC5hLFnsPf7jTjJWYNRkVPfzcyqCukcohXpod3XncKJJrwFubsp1upAzHB3udqfxNdit?cluster=devnet)
- [🗳️ View AI Biy Oracle Vote TX ↗](https://solscan.io/tx/3atA1kXGLSE41M2V5QHzYfAaqPL9X3uP9Bgm6kjxfAxrqzxsuJ5WcGUPMtwfuPxwgoCXm9AYnvzfaMvXkNioYwZX?cluster=devnet)

---

## 🏦 Impact Tokenomics & Dynamic Reputation

### Soulbound Integrity Token (SBT)

After a positive `ADAL` verdict, the system **autonomously mints** a Soulbound Token:

1. **SPL Token Mint** with 0 decimals (NFT)
2. **Associated Token Account** created for the volunteer
3. **Exactly 1 token** minted
4. **Mint authority revoked** → no more can ever be created
5. Token is permanently bound to the volunteer's wallet

This creates an **immutable, on-chain proof of verified social impact**.

### 🌟 The "Aura" Score — Dynamic Reputation

Each confirmed `ADAL` verdict does more than release tokens — it updates the volunteer's **dynamic on-chain reputation**. We call it the "Aura":

> Every verified deed accumulates into a living, public reputation score anchored in the blockchain. The higher the volunteer's "Aura" level, the more complex and highly rewarded missions become available to them. A volunteer with 50+ verified SBTs is a fundamentally different entity in the eyes of the protocol than one with 2.

This creates a **provable meritocracy**: your social capital is not a self-reported number, it is a cryptographically verified track record.

### Impact Incentives — Why Everyone Wins

ProtoQol is structurally designed so that every participant benefits from honest behavior:

| Stakeholder | Incentive | Mechanism |
|-------------|-----------|-----------|
| **Volunteer** | SOL rewards + an immutable SBT portfolio that universities and employers can verify | `mint_integrity_sbt` → permanent on-chain CV |
| **Sponsor / NGO** | 1000x reduction in verification cost, 0% greenwashing risk | `etch_deed` API → AI audit < $0.001 |
| **Society** | Trustless, transparent proof that aid reached its destination | Public Audit Mirror + SHA-256 on Solana |

The SBT profile becomes the volunteer's **Social Lift passport** — a bridge from physical-world good deeds to digital-world opportunities.

---

## 🚀 V2 Architecture: 100% Zero-Trust & Cryptographic Proof of Impact

While the current version anchors the final decision hash in Solana, **V2 scales this to a billion-dollar enterprise B2B verification infrastructure**. To achieve absolute verifiability, we are implementing a deterministic Hash Chain stored on IPFS/Arweave.

Instead of writing just the final report, V2 uses a cryptographic waterfall:

```javascript
evidence_hash  = SHA256(photo_bytes + description + timestamp)
ai_hash        = SHA256(ai_raw_response)
consensus_hash = SHA256(evidence_hash + ai_hash + verdict + mission_id)
```

**The Mechanics:**
1. **Solana Layer:** We only write the `consensus_hash` and the `IPFS_CID` to the blockchain (saving gas).
2. **IPFS/Arweave Layer:** We store the raw JSON mapping containing all evidence bytes, "Biy Council" deliberation logs, and AI signatures.
3. **The Business Value:** Any external B2B sponsor, NGO, or independent auditor can pull the JSON from IPFS, locally recalculate the hashes, and compare them against the immutable `consensus_hash` in Solana. 

This mathematical proof guarantees that **the evidence was not tampered with before reaching the AI**, and **the AI's verdict was not manipulated by intermediate backend layers**. It is a mathematically proven, 100% trustless audit trail. See [AI-SPEC.md](./AI-SPEC.md) for deeper implementation details.

---

## 🗄️ Account Abstraction (Shadow Wallets)

Users interact via Telegram — they never see Solana keypairs:

```python
def get_nomad_wallet(user_id: str):
    seed = SHA256(f"{user_id}::{WALLET_SALT}")
    return Keypair.from_seed(seed)
```

Each Telegram user gets a **deterministic**, invisible Solana wallet. Gas is sponsored by the protocol's Master Authority.

---

## 🔌 B2B API Reference

ProtoQol exposes a full REST API for enterprise integration. Authentication is via `X-API-Key` header with tiered subscription plans (Free / Pro / Enterprise).

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/v1/etch_deed` | `POST` | Submit a deed for AI verification + on-chain settlement |
| `/api/v1/verify_mission` | `POST` | Universal verification (JSON + multipart with photos) |
| `/api/v1/dashboard/stats` | `GET` | Client-specific impact metrics & recent activity |
| `/api/v1/gateway/missions` | `GET` | List all active campaigns/missions |
| `/api/v1/engine/health` | `GET` | Engine status, node list, and aggregate metrics |
| `/api/v1/sbt/check/{user_id}` | `GET` | Check SBT existence for a specific volunteer |
| `/audit/{integrity_hash}` | `GET` | Public Audit Mirror — full AI discussion transparency page |
| `/api/v1/inquiry` | `POST` | B2B lead capture for enterprise partnerships |

**Webhook support:** B2B clients can register a `webhook_url` per campaign. ProtoQol fires a POST notification on every `CONSENSUS_REACHED` event with deed ID, verdict, and transaction hash.

---

## 🚀 Quick Start

> **Prerequisites:** Python 3.10+ and a Gemini API key. That's it.  
> The Anchor smart contract is **pre-deployed on Devnet** — you don't need Rust, Anchor CLI, or Solana tools.

### 1. Clone & Configure
```bash
git clone <repo-url>
cd ProtoQol
cp .env.example .env
# Add your GEMINI_API_KEY to .env (required)
# BOT_TOKEN is optional — only needed for Telegram bot
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Launch Backend
```bash
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 4. Test the Pipeline
```bash
curl -X POST http://localhost:8000/api/v1/verify_mission \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Delivered groceries to elderly woman in Aktobe.",
    "user_id": "test_nomad_001",
    "mission_id": "elders_aktobe",
    "mode": "REAL_MISSION"
  }'
```

### 5. Verify On-Chain
Open the `integrity_hash` from the response and visit:
```
http://localhost:8000/audit/<integrity_hash>
```
This opens the **Public Audit Mirror** — a full cyberpunk-styled log of the AI Council deliberation.

> 💡 **For Judges & Reviewers**  
> The backend engine runs locally for this showcase. To test the full user experience immediately without setup, try our live Telegram Mini App:  
> 🚀 **Public Demo:** [t.me/qaiyrym_bot](https://t.me/qaiyrym_bot)  
> 🌐 **Ecosystem Hub:** [protoqol.vercel.app/hub.html](https://protoqol.vercel.app/hub.html)

---

## 📁 Project Structure

```
ProtoQol/
├── main.py                    # FastAPI Integrity Gateway (entry point)
├── core/
│   ├── ai_engine.py           # Unified Biy Council (Gemini 2.0 Flash)
│   ├── solana_client.py       # Anchor RPC + SBT Minting + Shadow Wallets
│   ├── database.py            # SQLite WAL persistence layer
│   ├── config.py              # Engine configuration + API key rotation
│   ├── auth.py                # B2B API key authentication + credit quota
│   ├── guardian.py            # Rate limiting (IP-based)
│   ├── exceptions.py          # Custom error hierarchy
│   ├── event_monitor.py       # Autonomous on-chain event listener
│   └── webhooks.py            # B2B webhook dispatcher
├── routes/
│   ├── oracle.py              # Protocol verification + on-chain voting
│   ├── gateway.py             # B2B enterprise API gateway
│   └── health.py              # System health endpoints
├── protoqol_core/             # Anchor smart contract (Rust)
│   └── programs/protoqol_core/src/lib.rs
├── dashboard.html             # Enterprise Command Center UI
├── index.html                 # Landing page (Nomad Cyberpunk theme)
├── AI-SPEC.md                 # V2 cryptographic specification
├── requirements.txt           # Python dependencies
└── .env.example               # Environment template
```

---

## 🛡️ Security & Trust Model

- **API keys injected via `.env`** — Gemini keys, bot tokens, and wallet salts are never committed to the repo
- **B2B authentication** — `X-API-Key` header with credit-based quotas (402 Payment Required on exhaustion)
- **Deterministic wallets** — SHA-256 derived from Telegram ID + salt, no key files stored
- **On-chain authorization** — Oracle voting requires PDA-verified `is_active == true`
- **Integrity anchoring** — Every AI decision is SHA-256 hashed before on-chain settlement
- **No PII on-chain** — Only hashes and Pubkeys are stored on the public ledger
- **Rate limiting** — IP-based in-memory limiter protects AI/Solana budget during demos
- **Fail-safe AI** — On timeout/failure, verdict falls back to `REVIEW_NEEDED` (never fakes a positive)

---

## 📊 Evaluation Criteria Mapping

| Criteria | Points | How ProtoQol addresses it |
|----------|--------|--------------------------|
| **Product & Idea** | 20 | Solves real $540B greenwashing problem with cultural "Asar" narrative |
| **Technical Implementation** | 25 | Working MVP: FastAPI + 4-agent AI + Anchor smart contract + SBT minting |
| **Use of Solana** | 15 | PDA escrow, oracle voting, auto-resolution, SBT mint, on-chain explorer links |
| **Innovation** | 15 | First "Ethics as a Service" protocol with nomadic AI consensus metaphor |
| **UX & Product Thinking** | 10 | Telegram Mini App + Account Abstraction = zero-friction onboarding |
| **Demo & Presentation** | 10 | Showcase Mode, Public Audit Mirror, real-time enterprise dashboard |
| **Completeness & Documentation** | 5 | This README, AI-SPEC.md, inline code docs, .env.example |

---

> "I realized that trustless verification in philanthropy is only achievable through the total removal of human bias. ProtoQol is my attempt to replace subjective belief with autonomous, on-chain certainty."  
> — **Alikhan Bakhtybay, Solo Founder**

<div align="center">
  <p><i>"The truth doesn't need to be loud, it just needs to be on the blockchain."</i></p>
  <br>
  <p align="center">
    <b>Built for Decentrathon — National Solana Hackathon 2026</b><br>
    <i>Case 2: AI + Blockchain — Autonomous Smart Contracts</i><br>
    © 2026 Alikhan Bakhtybay. Licensed under the <a href="./LICENSE">MIT License</a>.
  </p>
  <p>Solo Founder • 17 years old • Aktobe, Kazakhstan 🇰🇿</p>
</div>

┬┴┬┴┤( ͡° ͜ʖ├┬┴┬┴ Спасибо что дочитали!
