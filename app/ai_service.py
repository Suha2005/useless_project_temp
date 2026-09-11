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
    """Primary AI generation function for Awkward Opposite answers with fallback."""
    gemini_key = current_app.config.get("GEMINI_API_KEY")
    timeout = current_app.config.get("AI_TIMEOUT", 15)
    
    if gemini_key:
        try:
            return _call_gemini_awkward(prompt_text, gemini_key, timeout)
        except Exception as e:
            logger.warning(f"Gemini Awkward call failed: {e}. Falling back to heuristic oracle.")
            
    return _generate_fallback_awkward(prompt_text)

def escalate_awkwardness(prompt_text, previous_answer):
    """Live AI escalation to make the answer even more uncomfortably opposite."""
    gemini_key = current_app.config.get("GEMINI_API_KEY")
    timeout = current_app.config.get("AI_TIMEOUT", 15)
    
    if gemini_key:
        formatted_prompt = (
            AWKWARD_ESCALATE_PROMPT
            .replace("{original_prompt}", str(prompt_text))
            .replace("{previous_answer}", str(previous_answer))
        )
        
        candidate_models = [
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
                "maxOutputTokens": 2048
            }
        }
        
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
            except Exception as e:
                logger.warning(f"Gemini escalate model {model} error: {e}")

    return _generate_fallback_escalate(prompt_text, previous_answer)

def _call_gemini_awkward(prompt_text, api_key, timeout):
    candidate_models = [
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

def _generate_fallback_awkward(prompt_text):
    """Contextual heuristic generator that delivers awkward opposite answers when live API is unconfigured."""
    text_lower = prompt_text.lower()
    
    if any(w in text_lower for w in ["ex", "text", "crush", "date", "confess", "relationship"]):
        answer = f"Whatever you do, do not communicate in any conventional human syntax. You should send them a 14-page PDF detailing the geopolitical trade treaties of 1842, followed immediately by 'oops wrong chat' and then delete your entire digital existence for 72 hours."
        plan = "1. Draft an overly formal telegram addressed to their legal guardian.\n2. Arrive at their local supermarket 12 minutes before closing and stare intently at canned garbanzo beans until noticed.\n3. If spoken to, pretend you only speak Esperanto and briskly back away without blinking."
        silence = "21.4 seconds of mutual, unblinking horror"
        diag = "ROMANTIC SABOTAGE EXTRAORDINAIRE"
    elif any(w in text_lower for w in ["boss", "job", "work", "raise", "salary", "interview", "fired"]):
        answer = f"The optimal professional strategy is absolute non-sequitur dominance. Schedule an urgent 1-on-1 meeting at 7:00 AM titled 'STATUS CHECK', sit on the floor instead of a chair, and offer them a lukewarm hard-boiled egg without breaking eye contact."
        plan = "1. Send a company-wide email congratulating everyone on Tuesday.\n2. When asked about your deliverables, describe a vivid dream you had about a forklift.\n3. Request your annual salary in vintage Chuck E. Cheese prize tickets."
        silence = "34.1 seconds of awkward calendar shuffling"
        diag = "CORPORATE INEPTITUDE LEVEL 9"
    elif any(w in text_lower for w in ["alarm", "class", "late", "school", "exam", "homework", "teacher", "professor"]):
        answer = f"Do not apologize for tardiness. Simply walk backwards into the lecture hall, sit in the front row facing the other students, and take meticulous handwritten notes on their posture."
        plan = "1. Claim you were observing daylight saving time from the 18th century.\n2. Submit your assignment written entirely in green crayon on a paper napkin.\n3. If questioned, whisper 'the prophecy forbade it' and look suspiciously at the ceiling."
        silence = "18.9 seconds of collective classroom silence"
        diag = "ACADEMIC TIMELINE DISRUPTOR"
    else:
        answer = f"The only logical response to '{prompt_text}' is to execute the exact inverse of common decency: nod vigorously, offer an unexplained handshake, and slowly crab-walk out of the room while maintaining absolute stillness from the waist up."
        plan = "1. Announce to anyone nearby that you did not do what you clearly just did.\n2. Replace all verbal responses with varied pitches of humming.\n3. Formally declare that you are now entering standby power mode."
        silence = "16.8 seconds of deafening quiet"
        diag = "TERMINAL OPPOSITE REACTION"

    return {
        "awkward_answer": answer,
        "opposite_advice": plan,
        "cringe_score": random.randint(88, 98),
        "social_ruin": random.randint(90, 99),
        "awkward_silence": silence,
        "awkward_diagnosis": diag,
        "roast": answer,
        "ragebait_advice": plan,
        "emotional_damage": 94,
        "delusion_index": 98,
        "copium_level": 92,
        "damage_tier": diag,
        "diagnosis_tag": diag,
        "overall_score": 95,
        "verdict": diag,
        "short_reason": answer,
        "detailed_reason": plan,
        "improved_excuse": plan,
        "risk_level": "Catastrophic"
    }

def _generate_fallback_escalate(prompt_text, previous_answer):
    """Fallback escalation generator when live API is unavailable."""
    answer = f"You thought that was awkward? It's time to escalate. Return to the scene wearing a fully buttoned trench coat, pull out a tiny chalkboard, and loudly squeak chalk across it while re-reading your dilemma word-for-word."
    plan = "1. Send a voice memo of 4 solid minutes of rhythmic finger tapping.\n2. Claim diplomat immunity under international maritime admiralty law.\n3. When asked why you did this, hand them a business card that simply says 'NO QUESTIONS'."
    diag = "APOCALYPTIC SOCIAL CATASTROPHE"
    
    return {
        "awkward_answer": answer,
        "opposite_advice": plan,
        "cringe_score": 99,
        "social_ruin": 100,
        "awkward_silence": "42.0 seconds of unbearable tension",
        "awkward_diagnosis": diag,
        "roast": answer,
        "ragebait_advice": plan,
        "emotional_damage": 99,
        "delusion_index": 100,
        "copium_level": 99,
        "damage_tier": diag,
        "diagnosis_tag": diag,
        "overall_score": 99,
        "verdict": diag,
        "short_reason": answer,
        "detailed_reason": plan,
        "improved_excuse": plan,
        "risk_level": "Extinction Level"
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

