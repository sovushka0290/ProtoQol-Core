import json
import asyncio
import google.generativeai as genai
from config import log, get_next_gemini_key

async def query_agent(node_name: str, prompt: str, description: str, mission_info: dict, fallback_verdict: str) -> dict:
    key = get_next_gemini_key()
    if not key:
        log.warning(f"[{node_name}] No API Key found. Running simulation.")
        import random
        v = "ADAL" if random.random() > 0.4 or node_name != "ORACLE_NODE_2" else "ARAM"
        w = "Честное дело — светлое будущее." if v == "ADAL" else "Слова без дела мертвы."
        return {"verdict": v, "wisdom": w, "impact_score": 0.75 if v == "ADAL" else 0.1}

    # Configure on each request to support key rotation
    genai.configure(api_key=key)
    model = genai.GenerativeModel('gemini-2.0-flash')
    
    user_prompt = f"Миссия: {mission_info['requirements']}\nЗаявка пользователя: {description}"
    try:
        response = await asyncio.to_thread(
            model.generate_content,
            [prompt, user_prompt],
            generation_config=genai.GenerationConfig(temperature=0.3, max_output_tokens=300)
        )
        raw = response.text.replace('```json', '').replace('```', '').strip()
        
        # [HARDENING] Strict JSON parsing with fallback
        try:
            result = json.loads(raw)
        except json.JSONDecodeError:
            log.warning(f"[{node_name}] JSON Decode Error. Using Safe Fallback.")
            result = {"verdict": "ARAM", "wisdom": "Broken Signal", "impact_score": 0.0, "reasoning": "AI Node returned malformed payload."}
            
        result.setdefault("verdict", fallback_verdict)
        log.info(f"[{node_name}] Validation complete. Status: {result['verdict']}")
        return result
    except Exception as e:
        log.error(f"[{node_name}] Execution Link Failed: {e}")
        return {"verdict": "ARAM", "wisdom": "Система молчит", "impact_score": 0.0, "reasoning": "Network or API failure."}

async def query_agent_with_timeout(node_name: str, prompt: str, description: str, mission_info: dict, fallback: str) -> dict:
    try:
        return await asyncio.wait_for(query_agent(node_name, prompt, description, mission_info, fallback), timeout=10.0)
    except asyncio.TimeoutError:
        log.warning(f"[{node_name}] TimeoutError (10s exceeded). Degrading gracefully.")
        return {"verdict": fallback, "wisdom": "Оракул спит", "impact_score": 0.1, "reasoning": "Timeout"}
    except Exception as e:
        log.error(f"[{node_name}] Unexpected Error: {e}")
        return {"verdict": fallback, "wisdom": "Системный сбой", "impact_score": 0.1, "reasoning": "Error"}

async def analyze_deed(description: str, mission_info: dict) -> dict:
    auditor_prompt = "Ты — Агент 1 (Аудитор). Твоя цель — оценить практическую пользу дела. Отвечай строго в JSON: {\"verdict\": \"ADAL\"/\"ARAM\", \"impact_score\": 0.0-1.0, \"reasoning\": \"...\"}"
    skeptic_prompt = "Ты — Агент 2 (Скептик). Твоя цель — найти фальшь и нестыковки. Будь строгим. Отвечай строго в JSON: {\"verdict\": \"ADAL\"/\"ARAM\", \"impact_score\": 0.0-1.0, \"reasoning\": \"...\"}"
    compliance_prompt = "Ты — Агент 3 (Комплаенс). Соответствует ли дело правилам миссии? Отвечай строго в JSON: {\"verdict\": \"ADAL\"/\"ARAM\", \"impact_score\": 0.0-1.0, \"reasoning\": \"...\"}"

    tasks = [
        query_agent_with_timeout("ORACLE_NODE_1", auditor_prompt, description, mission_info, "ADAL"),
        query_agent_with_timeout("ORACLE_NODE_2", skeptic_prompt, description, mission_info, "ARAM"),
        query_agent_with_timeout("ORACLE_NODE_3", compliance_prompt, description, mission_info, "ADAL")
    ]
    
    results = await asyncio.gather(*tasks, return_exceptions=True)
    clean_results = [r if not isinstance(r, Exception) else {"verdict": "ARAM", "impact_score": 0.0} for r in results]

    validator_prompt = f"""Ты — Валидатор (Master Biy). 
Отчеты 3-х независимых ИИ-агентов (Аудитор, Скептик, Комплаенс): 
{json.dumps(clean_results, ensure_ascii=False)}

Задача:
1. Вынести итоговый verdict. Если хотя бы 2 из 3 агентов сказали "ADAL", то "ADAL". Иначе "ARAM".
2. Вывести средний impact_score.
3. Дать мудрость (wisdom) — казахскую пословицу.
4. Вывести общее reasoning.

Отвечай СТРОГО в JSON без разметки:
{{"verdict": "ADAL", "impact_score": 0.85, "wisdom": "...", "reasoning": "..."}}"""

    final_res = await query_agent_with_timeout("ORACLE_VALIDATOR", validator_prompt, description, mission_info, "ADAL")
    
    final_res.setdefault("verdict", "ADAL")
    final_res.setdefault("impact_score", 0.7)
    final_res.setdefault("wisdom", "Правда сильнее камня.")
    final_res.setdefault("reasoning", "Consensus reached.")
    final_res["impact_score"] = max(0.0, min(1.0, float(final_res["impact_score"])))

    log.info(f"[CONSENSUS] Final Verdict: {final_res['verdict']} | Score: {final_res['impact_score']:.2f}")
    return final_res
