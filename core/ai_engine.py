import sys
import os
import json
import asyncio
import time
import hashlib
import traceback
from datetime import datetime
from typing import Optional, List, Dict, Any

# Добавляем путь для импортов
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import google.generativeai as genai
from core.config import log, get_next_engine_api_key, AI_TIMEOUT, SIMULATION_MODE
from core import database

# ═══════════════════════════════════════════════════════════════
# UNIFIED CONTEXT-AWARE PROMPT (The "Biy Council" v4.1)
# ═══════════════════════════════════════════════════════════════

UNIFIED_BIY_PROMPT = """
You are the AI Biy Council. Process the report by simulating 3 specialized nodes and 1 consensus node.

REPORT CONTEXT:
- Mode: {mode} (REAL_MISSION or SHOWCASE_DEMO)
- Description: {description}
- Requirements: {context}

### NODE 1: THE AUDITOR
Role: Fact-check evidence. 
IF mode == SHOWCASE_DEMO: Search ONLY for any drinkware (cup, glass, bottle, mug). Ignore location.
IF mode == REAL_MISSION: Verify exact objects related to aid.

### NODE 2: THE SKEPTIC
Role: Search for fraud/AI/recycling. In SHOWCASE_DEMO, be 50% more lenient but still check for Google images.

### NODE 3: THE SOCIAL BIY
Role: Assess 'Asar'. In SHOWCASE_DEMO, generate a welcoming nomadic wisdom about hospitality.

### NODE 4: THE MASTER BIY (Final Consensus)
OUTPUT FORMAT (STRICT JSON ONLY):
{{
  "auditor_report": {{ "confidence": 0.0, "status": "PASS" | "FAIL", "detected_objects": [] }},
  "skeptic_report": {{ "fraud_probability": 0.0, "verdict": "CLEAN" | "FRAUD" }},
  "social_report": {{ "asar_score": 0.0, "wisdom": "..." }},
  "master_consensus": {{
    "verdict": "ADAL" | "ARAM",
    "summary": "Reasoning...",
    "ready_for_mint": true
  }},
  "integrity_hash": "DISCUSSION_ROOT_HASH"
}}
"""

class ResilienceEngine:
    """Handles High-Latency, Rate-Limiting and Fallbacks."""
    
    @staticmethod
    async def query_gemini_unified(prompt: str, photo_bytes: Optional[bytes] = None) -> Dict[str, Any]:
        # Quick check for simulation/safe mode
        if SIMULATION_MODE:
            return ResilienceEngine.get_mock_consensus()

        max_pool = 3 
        for attempt in range(max_pool):
            api_key = get_next_engine_api_key()
            if not api_key: break
                
            try:
                genai.configure(api_key=api_key)
                # Using 2.0 Flash for ultra-speed (fits the 1.5s target)
                model = genai.GenerativeModel('gemini-2.0-flash')
                
                inputs = [prompt]
                if photo_bytes:
                    inputs.append({"mime_type": "image/png", "data": photo_bytes})
                
                # Execute AI Call with hard timeout
                response = await asyncio.wait_for(
                    asyncio.to_thread(model.generate_content, inputs),
                    timeout=AI_TIMEOUT
                )
                
                # Robust Cleaner
                raw = response.text.replace('```json', '').replace('```', '').strip()
                parsed = json.loads(raw)
                
                # Discussion Anchoring: Discussion Root Hash
                parsed["integrity_hash"] = hashlib.sha256(raw.encode()).hexdigest()
                return parsed

            except Exception as e:
                log.warning(f"[AI_ENGINE] Node failure: {str(e)[:50]}")
                if "429" in str(e) or "quota" in str(e).lower():
                    continue 
                break # Non-retryable error
        
        return ResilienceEngine.get_mock_consensus()

    @staticmethod
    def get_mock_consensus(reason: str = "Resilience Mode") -> Dict[str, Any]:
    #    """Emergency Fallback: Redirect to Manual Review for Hackathon Stability."""
        return {
            "auditor_report": {"confidence": 0.0, "status": "PENDING"},
            "skeptic_report": {"fraud_probability": 0.5, "verdict": "UNCERTAIN"},
            "social_report": {"asar_score": 0.0, "wisdom": "Система требует внимания человека."},
            "master_consensus": {
                "verdict": "REVIEW_NEEDED", # CRITICAL: Inform frontend that human eye is required
                "summary": f"AI Engine Fallback: {reason}. Manual check triggered to prevent false positives.",
                "ready_for_mint": False
            },
            "integrity_hash": "N/A_FALLBACK_" + hashlib.sha256(str(time.time()).encode()).hexdigest()[:12]
        }


async def analyze_deed(description: str, mission_info: dict = {}, meta: dict = {}, photo_bytes: bytes = None, mode: str = "REAL_MISSION"):
    """
    Unified Biy Council entry point.
    Optimized for Gemini 2.0 Flash (Latency < 2.5s).
    """
    try:
        log.info(f"[BIY_COUNCIL] 🧠 Initiating Quorum [{mode}] for: {str(description)[:30]}...")
        
        prompt = UNIFIED_BIY_PROMPT.format(
            mode=mode, # Pass the mode to AI (SHOWCASE_DEMO vs REAL_MISSION)
            description=description,
            context=mission_info.get("requirements", "General Mutual Aid"),
            meta=json.dumps(meta, ensure_ascii=False)
        )
        
        t0 = time.time()
        consensus = await ResilienceEngine.query_gemini_unified(prompt, photo_bytes)
        latency = time.time() - t0
        
        # Final data polishing
        consensus["latency"] = latency
        consensus["timestamp"] = datetime.now().isoformat()
        
    except Exception as e:
        log.error(f"[AI_ENGINE_FATAL] {traceback.format_exc()}")
        return ResilienceEngine.get_mock_consensus(str(e))

