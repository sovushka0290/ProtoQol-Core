# ProtoQol: AI & Cryptographic Specification (V2)

## 1. The Core Philosophy
ProtoQol evaluates unstructured, qualitative real-world data (photos, natural language, geolocation) and outputs deterministic, quantitative, and immutable on-chain state changes. To achieve absolute trust, the AI evaluation process itself must be cryptographically verifiable.

## 2. Multi-Agent Biy Council Architecture
Our Gemini 2.0 Flash integration utilizes a specialized "Agent-Validator" Swarm (The Council of Biys):

- **The Auditor:** Extracts objects, classifies actions, and matches text against image metadata.
- **The Skeptic (Adversarial Node):** Analyzes the exact same input through a negative lens. Looks for deepfakes, recycled images, and LLM-generated prompt injections.
- **The Social Biy:** Normalizes the impact score against ESG KPIs and contextual cultural data ("Asar").
- **Master Consensus:** Aggregates the 3 node outputs. Only a unanimous or 2/3 majority vote triggers an `ADAL` on-chain settlement.

## 3. Cryptographic Hash Chain (V2 Implementation)
To prevent "Backend-in-the-Middle" attacks where a malicious server alters the AI's response before it reaches Solana, V2 implements a cryptographic Hash Chain.

### 3.1. Formula
```javascript
// 1. Anchor the input
evidence_hash = SHA256(photo_bytes + description + timestamp + geo_sig)

// 2. Anchor the AI's output
ai_hash = SHA256(biy_council_raw_json)

// 3. Create the final Integrity Anchor
consensus_hash = SHA256(evidence_hash + ai_hash + verdict + mission_id)
```

### 3.2. Data Availability Layer (IPFS/Arweave)
Solana block space is expensive. Therefore, the actual payloads (the `photo_bytes` and `biy_council_raw_json`) are stored on IPFS.

We write to the Solana PDA:
`[ consensus_hash (32 bytes), IPFS_CID (59 bytes) ]`

### 3.3. Independent Auditability (Zero-Trust)
B2B clients (ESG Funds, Governments) do not need to trust ProtoQol.
They can run an open-source verification script that:
1. Queries the Solana PDA to get the `IPFS_CID` and `consensus_hash`.
2. Downloads the raw evidence payload from IPFS.
3. Re-runs the `SHA256` hashing protocol locally.
4. Asserts that the computed hash perfectly matches the Solana records.

This provides **mathematical proof of impact**.
