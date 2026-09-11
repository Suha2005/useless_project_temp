from datetime import datetime, date
from app.models import db, Achievement, Analysis

ACHIEVEMENTS_DEF = [
    {
        "code": "FIRST_EXCUSE",
        "title": "FIRST EXCUSE",
        "description": "Analyze your very first excuse.",
        "icon": "🚀"
    },
    {
        "code": "MASTER_LIAR",
        "title": "MASTER LIAR",
        "description": "Produce a legendary excuse scoring 90 or higher.",
        "icon": "🧠"
    },
    {
        "code": "PROFESSIONAL_PROCRASTINATOR",
        "title": "PROFESSIONAL PROCRASTINATOR",
        "description": "Analyze 10 or more excuses in your scientific career.",
        "icon": "⏳"
    },
    {
        "code": "ABSOLUTE_CINEMA",
        "title": "ABSOLUTE CINEMA",
        "description": "Generate or submit an excuse with 95+ creativity.",
        "icon": "🎬"
    },
    {
        "code": "BRO_JUST_STUDY",
        "title": "BRO JUST STUDY",
        "description": "Receive an absolute disaster score below 20.",
        "icon": "📉"
    }
]

DAILY_EXCUSES = [
    {
        "excuse": "I didn't forget the assignment. I was giving it more time to develop.",
        "situation": "Late Assignment",
        "score": 87,
        "verdict": "HIGHLY CONVINCING",
        "blurb": "Presents procrastination as artisanal intellectual curation."
    },
    {
        "excuse": "My WiFi was emotionally unavailable and refused to connect with my feelings.",
        "situation": "Late Assignment",
        "score": 92,
        "verdict": "LEGENDARY EXCUSE",
        "blurb": "Poetically shifts blame to non-corporeal network trauma."
    },
    {
        "excuse": "My alarm entered sleep mode to prioritize its own wellness cycle.",
        "situation": "Missed Class",
        "score": 84,
        "verdict": "HIGHLY CONVINCING",
        "blurb": "Subversive anthropomorphism confuses authoritative figures."
    },
    {
        "excuse": "I was ready to complete the task, but destiny had other priorities.",
        "situation": "Failed to Complete Work",
        "score": 73,
        "verdict": "DECENT EXCUSE",
        "blurb": "Fatalism has a 43% pass rate with tired professors."
    },
    {
        "excuse": "My laptop suffered an abrupt existential reboot during the compile stage.",
        "situation": "Late Assignment",
        "score": 89,
        "verdict": "HIGHLY CONVINCING",
        "blurb": "Blends verifiable hardware terminology with sheer desperation."
    }
]

SYSTEM_MESSAGES_POOL = [
    "Consulting the excuse archives...",
    "Questioning your credibility...",
    "Detecting suspicious behavior...",
    "Calculating bullshit coefficient...",
    "Asking the neural network if it believes you...",
    "Cross-referencing with absolutely unnecessary data...",
    "Doing advanced mathematics for no reason...",
    "Almost finished wasting computational resources...",
    "Calibrating emotional desperation detectors...",
    "Scanning narrative for structural inconsistencies..."
]

def check_and_grant_achievements(user):
    """
    Evaluates user's history and unlocks any eligible achievements.
    Returns list of newly unlocked achievement dicts.
    """
    if not user:
        return []
        
    existing_codes = {a.code for a in user.achievements}
    newly_unlocked = []
    
    total_analyses = Analysis.query.filter_by(user_id=user.id).count()
    best_score = db.session.query(db.func.max(Analysis.overall_score)).filter_by(user_id=user.id).scalar() or 0
    worst_score = db.session.query(db.func.min(Analysis.overall_score)).filter_by(user_id=user.id).scalar() or 100
    max_creativity = db.session.query(db.func.max(Analysis.creativity)).filter_by(user_id=user.id).scalar() or 0
    
    for defn in ACHIEVEMENTS_DEF:
        code = defn["code"]
        if code in existing_codes:
            continue
            
        unlocked = False
        if code == "FIRST_EXCUSE" and total_analyses >= 1:
            unlocked = True
        elif code == "MASTER_LIAR" and best_score >= 90:
            unlocked = True
        elif code == "PROFESSIONAL_PROCRASTINATOR" and total_analyses >= 10:
            unlocked = True
        elif code == "ABSOLUTE_CINEMA" and max_creativity >= 95:
            unlocked = True
        elif code == "BRO_JUST_STUDY" and worst_score < 20 and total_analyses >= 1:
            unlocked = True
            
        if unlocked:
            ach = Achievement(
                user_id=user.id,
                code=code,
                title=defn["title"],
                description=defn["description"],
                icon=defn["icon"],
                unlocked_at=datetime.utcnow()
            )
            db.session.add(ach)
            newly_unlocked.append(defn)
            
    if newly_unlocked:
        db.session.commit()
        
    return newly_unlocked

def get_excuse_of_the_day():
    """Returns today's featured excuse deterministically by calendar date."""
    day_index = date.today().toordinal() % len(DAILY_EXCUSES)
    return DAILY_EXCUSES[day_index]
