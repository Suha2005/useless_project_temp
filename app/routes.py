import random
from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for, g
from app.models import db, User, Analysis, Leaderboard, Achievement
from app.auth import login_required, get_current_user
from app.scoring import generate_fallback_roast, get_double_down_roast
from app.ai_service import (
    generate_awkward_answer,
    escalate_awkwardness,
    roast_user,
    double_down_roast,
    CURATED_VIRAL_PROMPTS
)
from app.utils import check_and_grant_achievements, ACHIEVEMENTS_DEF

routes_bp = Blueprint("routes", __name__)

@routes_bp.before_app_request
def load_user():
    g.user = get_current_user()

# =========================================================================
# Page Routes (Simpler, Non-Nerdy, Punchy)
# =========================================================================

@routes_bp.route("/")
def index():
    featured_prompt = "Should I text my ex? It's 2:30 AM and I feel like they still love me."
    return render_template("index.html", user=g.user, featured_prompt=featured_prompt)

@routes_bp.route("/wall-of-shame")
@routes_bp.route("/leaderboard")
def leaderboard_page():
    entries = Leaderboard.query.order_by(Leaderboard.score.desc(), Leaderboard.created_at.desc()).limit(50).all()
    return render_template("leaderboard.html", user=g.user, entries=entries)

@routes_bp.route("/trauma-log")
@routes_bp.route("/dashboard")
@login_required
def dashboard_page():
    analyses = Analysis.query.filter_by(user_id=g.user.id).order_by(Analysis.created_at.desc()).all()
    user_achievements = {a.code: a for a in g.user.achievements}
    
    total_count = len(analyses)
    avg_score = int(round(sum(a.overall_score for a in analyses) / total_count)) if total_count > 0 else 0
    worst_score = max((a.overall_score for a in analyses), default=0) # highest damage = most cooked!
    
    return render_template(
        "dashboard.html",
        user=g.user,
        analyses=analyses,
        total_count=total_count,
        avg_score=avg_score,
        worst_score=worst_score,
        achievements_def=ACHIEVEMENTS_DEF,
        user_achievements=user_achievements
    )

@routes_bp.route("/history")
@login_required
def history_page():
    analyses = Analysis.query.filter_by(user_id=g.user.id).order_by(Analysis.created_at.desc()).all()
    return render_template("history.html", user=g.user, analyses=analyses)

@routes_bp.route("/demo")
def demo_page():
    return render_template("demo.html", user=g.user)

@routes_bp.route("/about")
def about_page():
    return render_template("about.html", user=g.user)

@routes_bp.route("/login")
def login_page():
    if g.user:
        return redirect(url_for("routes.dashboard_page"))
    return render_template("login.html")

@routes_bp.route("/register")
def register_page():
    if g.user:
        return redirect(url_for("routes.dashboard_page"))
    return render_template("register.html")


# =========================================================================
# REST API Endpoints (100% Live AI Awkward Opposite)
# =========================================================================

@routes_bp.route("/api/awkward", methods=["POST"])
@routes_bp.route("/api/roast", methods=["POST"])
@routes_bp.route("/api/analyze", methods=["POST"])
def api_awkward():
    data = request.get_json() or {}
    prompt = (data.get("prompt") or data.get("excuse") or "").strip()
    
    if not prompt:
        return jsonify({
            "success": False,
            "error": "You said nothing. While socially safe, it gives me nothing to invert."
        }), 400
        
    if len(prompt) < 3:
        return jsonify({
            "success": False,
            "error": "Give me a dilemma, question, or confession with slightly more detail."
        }), 400

    try:
        awkward_result = generate_awkward_answer(prompt)
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"AI generation encountered a glitch: {str(e)}"
        }), 500
    
    saved = False
    analysis_id = None
    new_achievements = []
    
    user = get_current_user()
    if user:
        record = Analysis(
            user_id=user.id,
            excuse_text=prompt,
            situation=awkward_result.get("awkward_diagnosis", "Awkward Dilemma"),
            believability=20,
            creativity=95,
            originality=92,
            specificity=88,
            plausibility=15,
            desperation=awkward_result.get("cringe_score", 94),
            suspiciousness=awkward_result.get("social_ruin", 98),
            bullshit_level=awkward_result.get("cringe_score", 94),
            overall_score=awkward_result.get("cringe_score", 94),
            verdict=awkward_result.get("awkward_diagnosis", "TERMINALLY AWKWARD"),
            short_reason=awkward_result.get("awkward_answer"),
            detailed_reason=awkward_result.get("opposite_advice"),
            improved_excuse=awkward_result.get("opposite_advice"),
            risk_level="Social Hazard"
        )
        db.session.add(record)
        db.session.commit()
        saved = True
        analysis_id = record.id
        new_achievements = check_and_grant_achievements(user)
    else:
        record = Analysis(
            user_id=None,
            excuse_text=prompt,
            situation=awkward_result.get("awkward_diagnosis", "Awkward Dilemma"),
            believability=20,
            creativity=95,
            originality=92,
            specificity=88,
            plausibility=15,
            desperation=awkward_result.get("cringe_score", 94),
            suspiciousness=awkward_result.get("social_ruin", 98),
            bullshit_level=awkward_result.get("cringe_score", 94),
            overall_score=awkward_result.get("cringe_score", 94),
            verdict=awkward_result.get("awkward_diagnosis", "TERMINALLY AWKWARD"),
            short_reason=awkward_result.get("awkward_answer"),
            detailed_reason=awkward_result.get("opposite_advice"),
            improved_excuse=awkward_result.get("opposite_advice"),
            risk_level="Social Hazard"
        )
        db.session.add(record)
        db.session.commit()
        analysis_id = record.id

    return jsonify({
        "success": True,
        "analysis_id": analysis_id,
        "saved": saved,
        "awkward_answer": awkward_result["awkward_answer"],
        "opposite_advice": awkward_result["opposite_advice"],
        "cringe_score": awkward_result["cringe_score"],
        "social_ruin": awkward_result["social_ruin"],
        "awkward_silence": awkward_result["awkward_silence"],
        "awkward_diagnosis": awkward_result["awkward_diagnosis"],
        # Backward compatibility
        "roast": awkward_result["awkward_answer"],
        "ragebait_advice": awkward_result["opposite_advice"],
        "emotional_damage": awkward_result["cringe_score"],
        "delusion_index": awkward_result["social_ruin"],
        "copium_level": awkward_result["cringe_score"],
        "damage_tier": awkward_result["awkward_diagnosis"],
        "diagnosis_tag": awkward_result["awkward_diagnosis"],
        "analysis": awkward_result,
        "new_achievements": new_achievements
    })

@routes_bp.route("/api/escalate", methods=["POST"])
@routes_bp.route("/api/double-down", methods=["POST"])
def api_escalate():
    data = request.get_json() or {}
    prompt = (data.get("prompt") or data.get("excuse") or "").strip()
    previous_answer = (data.get("previous_answer") or data.get("original_roast") or "").strip()
    
    try:
        escalated = escalate_awkwardness(prompt, previous_answer)
        return jsonify({
            "success": True,
            "escalated": escalated,
            "awkward_answer": escalated["awkward_answer"],
            "opposite_advice": escalated["opposite_advice"],
            "cringe_score": escalated["cringe_score"],
            "social_ruin": escalated["social_ruin"],
            "awkward_silence": escalated["awkward_silence"],
            "awkward_diagnosis": escalated["awkward_diagnosis"],
            # Backward compatibility
            "double_down_roast": escalated["awkward_answer"]
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Escalation failed: {str(e)}"
        }), 500

@routes_bp.route("/api/improve", methods=["POST"])
def api_improve():
    data = request.get_json() or {}
    prompt = (data.get("excuse") or data.get("prompt") or "").strip()
    roast_data = roast_user(prompt)
    return jsonify({
        "success": True,
        "original": prompt,
        "improved_excuse": roast_data["ragebait_advice"]
    })

@routes_bp.route("/api/history", methods=["GET"])
@login_required
def api_history():
    user = get_current_user()
    analyses = Analysis.query.filter_by(user_id=user.id).order_by(Analysis.created_at.desc()).all()
    return jsonify({
        "success": True,
        "analyses": [a.to_dict() for a in analyses]
    })

@routes_bp.route("/api/analysis/<int:analysis_id>", methods=["GET"])
def api_get_analysis(analysis_id):
    item = db.session.get(Analysis, analysis_id)
    if not item:
        return jsonify({"success": False, "error": "Roast record not found"}), 404
    user = get_current_user()
    if item.user_id and (not user or user.id != item.user_id) and not item.is_public:
        return jsonify({"success": False, "error": "Unauthorized"}), 403
    return jsonify({
        "success": True,
        "analysis": item.to_dict()
    })

@routes_bp.route("/api/wall-of-shame", methods=["GET"])
@routes_bp.route("/api/leaderboard", methods=["GET"])
def api_leaderboard():
    limit = min(100, int(request.args.get("limit", 50)))
    entries = Leaderboard.query.order_by(Leaderboard.score.desc(), Leaderboard.created_at.desc()).limit(limit).all()
    return jsonify({
        "success": True,
        "leaderboard": [e.to_dict() for e in entries]
    })

@routes_bp.route("/api/wall-of-shame/submit", methods=["POST"])
@routes_bp.route("/api/leaderboard/submit", methods=["POST"])
def api_submit_leaderboard():
    data = request.get_json() or {}
    analysis_id = data.get("analysis_id")
    display_name = (data.get("display_name") or "Anonymous Victim").strip()[:50]
    
    if not analysis_id:
        return jsonify({"success": False, "error": "Analysis ID required"}), 400
        
    item = db.session.get(Analysis, analysis_id)
    if not item:
        return jsonify({"success": False, "error": "Record not found"}), 404
        
    item.is_public = True
    item.display_name = display_name
    
    existing = Leaderboard.query.filter_by(analysis_id=item.id).first()
    if not existing:
        entry = Leaderboard(
            analysis_id=item.id,
            display_name=display_name,
            score=item.overall_score,
            excuse_text=item.excuse_text,
            situation=item.situation
        )
        db.session.add(entry)
        
    db.session.commit()
    return jsonify({"success": True, "message": "Inducted into the Wall of Shame!"})

@routes_bp.route("/api/random-prompt", methods=["GET"])
@routes_bp.route("/api/generate", methods=["POST"])
def api_generate():
    prompt = random.choice(CURATED_VIRAL_PROMPTS)
    return jsonify({
        "success": True,
        "prompt": prompt,
        "excuse": prompt,
        "situation": "Life Decision"
    })

@routes_bp.route("/api/daily", methods=["GET"])
def api_daily():
    prompt = "I told my crush I was an undercover billionaire to see if they loved me for who I am."
    return jsonify({
        "success": True,
        "daily": {
            "excuse": prompt,
            "score": 99,
            "verdict": "💀 SPIRITUALLY EVICTED",
            "blurb": "Peak delusional fiction."
        }
    })

@routes_bp.route("/api/achievements", methods=["GET"])
@login_required
def api_achievements():
    user = get_current_user()
    unlocked = [a.to_dict() for a in user.achievements]
    return jsonify({
        "success": True,
        "all_achievements": ACHIEVEMENTS_DEF,
        "unlocked": unlocked
    })
