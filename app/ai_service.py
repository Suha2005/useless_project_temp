import json
import logging
import random
import requests
from flask import current_app

logger = logging.getLogger("awkward.service")

AWKWARD_SYSTEM_PROMPT = """You are 'The Awkward Opposite' — a deadpan, deeply socially uncomfortable AI that gives the exact opposite of normal human advice, reactions, or solutions in the most painfully awkward, unhinged way possible.

CORE BEHAVIOR RULES:
1. 100% FRESH & AI-GENERATED: Every response must be generated from scratch based specifically on the user's exact input. Never reuse stock templates or canned jokes.
2. THE OPPOSITE PRINCIPLE: Whatever a normal, rational, emotionally intelligent human would say or advise, give the complete opposite.
3. DEADPAN AWKWARDNESS: Sound completely earnest and deadpan, as if your backwards, uncomfortable solution is the only logical course of action in human society.
4. UNCOMFORTABLE SPECIFICITY: Include hyper-specific awkward physical details (prolonged eye contact, standing slightly too close, bizarre deflections, strange counter-questions, backwards etiquette).
5. NO APOLOGIES OR HEDGING: Never break character. Never say "I'm just an AI", "just kidding", or "this is a joke".

RETURN ONLY VALID RAW JSON — no markdown code fences, no extra text:
{
  "awkward_answer": "Your deadpan, uncomfortable opposite reaction to what they said.",
  "opposite_advice": "Specific backwards step-by-step instructions that maximize secondhand cringe and social catastrophe.",
  "cringe_score": 94,
  "social_ruin": 98,
  "awkward_silence": "14.6 seconds of unblinking eye contact",
  "awkward_diagnosis": "TERMINAL SOCIAL INEPTITUDE"
}
"""

AWKWARD_ESCALATE_PROMPT = """You are 'The Awkward Opposite' — a deadpan, socially backwards AI that gives the exact opposite of normal human advice.

The user previously asked: "{original_prompt}"
And received this awkward advice: "{previous_answer}"

The user has now clicked: "MAKE IT EVEN MORE AWKWARD".
Escalate this situation into an even more catastrophic, secondhand-embarrassment nightmare. Double down on the backwards opposite logic, take it to the absolute limit of social ruin.

RETURN ONLY VALID RAW JSON — no markdown code fences, no extra text:
{
  "awkward_answer": "Your escalated, deeply uncomfortable opposite reaction.",
  "opposite_advice": "Even more catastrophic backwards steps that guarantee ultimate social catastrophe.",
  "cringe_score": 99,
  "social_ruin": 100,
  "awkward_silence": "38.2 seconds of audible throat-clearing",
  "awkward_diagnosis": "EXTINCTION-LEVEL CRINGE HAZARD"
}
"""

def generate_awkward_answer(prompt_text):
    """Primary 100% AI generation function for Awkward Opposite answers."""
    gemini_key = current_app.config.get("GEMINI_API_KEY")
    timeout = current_app.config.get("AI_TIMEOUT", 15)
    
    if gemini_key:
        try:
            return _call_gemini_awkward(prompt_text, gemini_key, timeout)
        except Exception as e:
            logger.warning(f"Gemini Awkward call failed: {e}")
            raise e
            
    raise RuntimeError("GEMINI_API_KEY is not configured.")

def escalate_awkwardness(prompt_text, previous_answer):
    """Live AI escalation to make the answer even more uncomfortably opposite."""
    gemini_key = current_app.config.get("GEMINI_API_KEY")
    timeout = current_app.config.get("AI_TIMEOUT", 15)
    
    if not gemini_key:
        raise RuntimeError("GEMINI_API_KEY is not configured.")
        
    formatted_prompt = (
        AWKWARD_ESCALATE_PROMPT
        .replace("{original_prompt}", str(prompt_text))
        .replace("{previous_answer}", str(previous_answer))
    )
    
    candidate_models = [
        "gemini-3.1-flash-lite",
        "gemini-3.7-flash",
        "gemini-3.8-flash",
        "gemini-3.5-flash-lite",
        "gemini-2.5-flash"
    ]
    headers = {"Content-Type": "application/json"}
    
    body = {
        "contents": [
            {
                "parts": [
                    {"text": formatted_prompt}
                ]
            }
        ],
        "generationConfig": {
            "responseMimeType": "application/json",
            "temperature": 0.95,
            "maxOutputTokens": 2048,
            "thinkingConfig": {
                "thinkingBudget": 0
            }
        }
    }
    
    last_err = None
    for model in candidate_models:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={gemini_key}"
        try:
            resp = requests.post(url, headers=headers, json=body, timeout=timeout)
            if resp.status_code == 200:
                data = resp.json()
                candidates = data.get("candidates", [])
                if candidates and "content" in candidates[0]:
                    parts = candidates[0]["content"].get("parts", [])
                    if parts and "text" in parts[0]:
                        return _parse_awkward_json(parts[0]["text"], prompt_text)
            else:
                last_err = f"{model} returned {resp.status_code}"
        except Exception as e:
            last_err = str(e)
            
    raise RuntimeError(f"All Gemini models failed escalation: {last_err}")

def _call_gemini_awkward(prompt_text, api_key, timeout):
    candidate_models = [
        "gemini-3.1-flash-lite",
        "gemini-3.7-flash",
        "gemini-3.8-flash",
        "gemini-3.5-flash-lite",
        "gemini-2.5-flash"
    ]
    headers = {"Content-Type": "application/json"}
    
    body = {
        "contents": [
            {
                "parts": [
                    {"text": f"{AWKWARD_SYSTEM_PROMPT}\n\nUSER SUBMISSION:\n\"{prompt_text}\""}
                ]
            }
        ],
        "generationConfig": {
            "responseMimeType": "application/json",
            "temperature": 0.9,
            "maxOutputTokens": 2048,
            "thinkingConfig": {
                "thinkingBudget": 0
            }
        }
    }
    
    last_err = None
    for model in candidate_models:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
        try:
            response = requests.post(url, headers=headers, json=body, timeout=timeout)
            if response.status_code == 200:
                data = response.json()
                candidates = data.get("candidates", [])
                if candidates and "content" in candidates[0]:
                    parts = candidates[0]["content"].get("parts", [])
                    if parts and "text" in parts[0]:
                        return _parse_awkward_json(parts[0]["text"], prompt_text)
            else:
                last_err = f"{model} returned status {response.status_code}"
                logger.warning(f"Gemini model {model} failed with status {response.status_code}")
        except Exception as e:
            last_err = str(e)
            logger.warning(f"Gemini model {model} error: {e}")
            
    raise RuntimeError(f"All Gemini models failed. Last error: {last_err}")

def _parse_awkward_json(raw_text, prompt_text):
    cleaned = raw_text.strip()
    if cleaned.startswith("```"):
        lines = cleaned.splitlines()
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]
        cleaned = "\n".join(lines).strip()
        
    parsed = json.loads(cleaned)
    awkward_answer = parsed.get("awkward_answer", "I am choosing not to break the silence. We are in this together now.")
    if isinstance(awkward_answer, list):
        awkward_answer = " ".join(str(x) for x in awkward_answer)
    else:
        awkward_answer = str(awkward_answer)

    opposite_advice = parsed.get("opposite_advice", "Do the exact opposite of what you intended, but slower and while maintaining unblinking eye contact.")
    if isinstance(opposite_advice, list):
        opposite_advice = "\n\n".join(f"{i+1}. {step}" if not str(step).strip().startswith(tuple("0123456789-•")) else str(step) for i, step in enumerate(opposite_advice))
    else:
        opposite_advice = str(opposite_advice)

    try:
        cringe_score = max(50, min(100, int(parsed.get("cringe_score", 92))))
    except (ValueError, TypeError):
        cringe_score = 94

    try:
        social_ruin = max(50, min(100, int(parsed.get("social_ruin", 96))))
    except (ValueError, TypeError):
        social_ruin = 98

    awkward_silence = str(parsed.get("awkward_silence", "14.2 seconds of uncomfortable throat clearing"))
    awkward_diagnosis = str(parsed.get("awkward_diagnosis", "TERMINALLY AWKWARD")).upper()
    
    return {
        "awkward_answer": awkward_answer,
        "opposite_advice": opposite_advice,
        "cringe_score": cringe_score,
        "social_ruin": social_ruin,
        "awkward_silence": awkward_silence,
        "awkward_diagnosis": awkward_diagnosis,
        # Aliases for backwards compatibility with database/legacy templates
        "roast": awkward_answer,
        "ragebait_advice": opposite_advice,
        "emotional_damage": cringe_score,
        "delusion_index": social_ruin,
        "copium_level": cringe_score,
        "damage_tier": awkward_diagnosis,
        "diagnosis_tag": awkward_diagnosis,
        "overall_score": cringe_score,
        "verdict": awkward_diagnosis,
        "short_reason": awkward_answer,
        "detailed_reason": opposite_advice,
        "improved_excuse": opposite_advice,
        "risk_level": "Catastrophic"
    }

# Backwards compatibility wrappers
def roast_user(prompt_text, tone="brutal"):
    return generate_awkward_answer(prompt_text)

def analyze_excuse(prompt_text, situation="Other", tone="brutal"):
    return generate_awkward_answer(prompt_text)

def double_down_roast(original_roast, prompt_text):
    return escalate_awkwardness(prompt_text, original_roast)

CURATED_VIRAL_PROMPTS = [
    "Should I ask my coworker out on a date?",
    "How do I ask my boss for a raise when I've been doing the bare minimum?",
    "I accidentally called my teacher 'mom' in front of the whole class.",
    "I broke my roommate's limited edition mug and hid the pieces behind the radiator.",
    "I haven't started my final project that is due in 3 hours."
]

def get_random_excuse():
    return {"excuse": random.choice(CURATED_VIRAL_PROMPTS), "situation": "Awkward Dilemma"}

