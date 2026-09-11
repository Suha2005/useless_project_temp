import os
from pathlib import Path
from flask import Flask
from app.config import Config
from app.models import db, Analysis, Leaderboard

def create_app(config_class=Config):
    base_dir = Path(__file__).resolve().parent.parent
    app = Flask(
        __name__,
        template_folder=str(base_dir / "templates"),
        static_folder=str(base_dir / "static")
    )
    app.config.from_object(config_class)
    
    db.init_app(app)
    
    from app.routes import routes_bp
    from app.auth import auth_bp
    
    app.register_blueprint(routes_bp)
    app.register_blueprint(auth_bp)
    
    with app.app_context():
        try:
            db.create_all()
            _seed_initial_leaderboard()
        except Exception as e:
            app.logger.warning(f"Database initialization warning: {e}")
        
    return app

def _seed_initial_leaderboard():
    """Seeds initial iconic Hall of Fame excuses if database is empty."""
    if Leaderboard.query.first() is not None:
        return
        
    seed_data = [
        {
            "excuse": "My WiFi was emotionally unavailable and refused to connect with my feelings.",
            "situation": "Late Assignment",
            "score": 98,
            "display_name": "QuantumProcrastinator",
            "verdict": "LEGENDARY EXCUSE",
            "bs": 88
        },
        {
            "excuse": "My alarm clock entered sleep mode to prioritize its own mental wellness.",
            "situation": "Missed Class",
            "score": 95,
            "display_name": "CircadianDisrupter",
            "verdict": "LEGENDARY EXCUSE",
            "bs": 65
        },
        {
            "excuse": "The assignment draft crossed the cosmic event horizon during local file synchronization.",
            "situation": "Late Assignment",
            "score": 91,
            "display_name": "AstrophysicsDropout",
            "verdict": "LEGENDARY EXCUSE",
            "bs": 94
        },
        {
            "excuse": "I was ready to complete the task, but destiny scheduled a higher-priority existential crisis.",
            "situation": "Failed to Complete Work",
            "score": 84,
            "display_name": "NietzscheanCoder",
            "verdict": "HIGHLY CONVINCING",
            "bs": 42
        },
        {
            "excuse": "My cat initiated an unscheduled code review and stepped directly on the hard-reset button.",
            "situation": "Late Assignment",
            "score": 88,
            "display_name": "FelineQA",
            "verdict": "HIGHLY CONVINCING",
            "bs": 35
        }
    ]
    
    for item in seed_data:
        analysis = Analysis(
            user_id=None,
            excuse_text=item["excuse"],
            situation=item["situation"],
            believability=max(10, item["score"] - 15),
            creativity=95,
            originality=92,
            specificity=78,
            plausibility=max(20, 100 - item["bs"]),
            desperation=30,
            suspiciousness=35,
            bullshit_level=item["bs"],
            overall_score=item["score"],
            verdict=item["verdict"],
            short_reason="Iconic hall of fame induction.",
            detailed_reason="Evaluated by the EXCUSE.AI central committee as an exquisite demonstration of linguistic deflection.",
            improved_excuse=item["excuse"],
            risk_level="Low",
            is_public=True,
            display_name=item["display_name"]
        )
        db.session.add(analysis)
        db.session.flush()
        
        entry = Leaderboard(
            analysis_id=analysis.id,
            display_name=item["display_name"],
            score=item["score"],
            excuse_text=item["excuse"],
            situation=item["situation"]
        )
        db.session.add(entry)
        
    db.session.commit()
