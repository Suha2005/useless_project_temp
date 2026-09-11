from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    analyses = db.relationship("Analysis", backref="user", lazy=True, cascade="all, delete-orphan")
    achievements = db.relationship("Achievement", backref="user", lazy=True, cascade="all, delete-orphan")
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method="pbkdf2:sha256")
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
        
    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

class Analysis(db.Model):
    __tablename__ = "analyses"
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True, index=True)
    excuse_text = db.Column(db.Text, nullable=False)
    situation = db.Column(db.String(100), nullable=False, default="Other")
    
    # 8 Core Metrics (0 - 100)
    believability = db.Column(db.Integer, nullable=False)
    creativity = db.Column(db.Integer, nullable=False)
    originality = db.Column(db.Integer, nullable=False)
    specificity = db.Column(db.Integer, nullable=False)
    plausibility = db.Column(db.Integer, nullable=False)
    desperation = db.Column(db.Integer, nullable=False)
    suspiciousness = db.Column(db.Integer, nullable=False)
    bullshit_level = db.Column(db.Integer, nullable=False)
    
    # Result
    overall_score = db.Column(db.Integer, nullable=False, index=True)
    verdict = db.Column(db.String(100), nullable=False)
    short_reason = db.Column(db.Text, nullable=True)
    detailed_reason = db.Column(db.Text, nullable=True)
    improved_excuse = db.Column(db.Text, nullable=True)
    risk_level = db.Column(db.String(50), default="Moderate")
    
    is_public = db.Column(db.Boolean, default=False)
    display_name = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "excuse": self.excuse_text,
            "situation": self.situation,
            "believability": self.believability,
            "creativity": self.creativity,
            "originality": self.originality,
            "specificity": self.specificity,
            "plausibility": self.plausibility,
            "desperation": self.desperation,
            "suspiciousness": self.suspiciousness,
            "bullshit_level": self.bullshit_level,
            "overall_score": self.overall_score,
            "verdict": self.verdict,
            "short_reason": self.short_reason,
            "detailed_reason": self.detailed_reason,
            "improved_excuse": self.improved_excuse,
            "risk_level": self.risk_level,
            "is_public": self.is_public,
            "display_name": self.display_name,
            "created_at": self.created_at.strftime("%b %d, %Y %H:%M") if self.created_at else None
        }

class Leaderboard(db.Model):
    __tablename__ = "leaderboard"
    
    id = db.Column(db.Integer, primary_key=True)
    analysis_id = db.Column(db.Integer, db.ForeignKey("analyses.id"), nullable=False)
    display_name = db.Column(db.String(100), nullable=False)
    score = db.Column(db.Integer, nullable=False, index=True)
    excuse_text = db.Column(db.Text, nullable=False)
    situation = db.Column(db.String(100), default="Other")
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    analysis = db.relationship("Analysis", backref="leaderboard_entries", lazy=True)
    
    def to_dict(self):
        return {
            "id": self.id,
            "analysis_id": self.analysis_id,
            "display_name": self.display_name,
            "score": self.score,
            "excuse": self.excuse_text,
            "situation": self.situation,
            "created_at": self.created_at.strftime("%b %d, %Y") if self.created_at else None
        }

class Achievement(db.Model):
    __tablename__ = "achievements"
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    code = db.Column(db.String(64), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    icon = db.Column(db.String(32), default="🏆")
    unlocked_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            "id": self.id,
            "code": self.code,
            "title": self.title,
            "description": self.description,
            "icon": self.icon,
            "unlocked_at": self.unlocked_at.strftime("%b %d, %Y") if self.unlocked_at else None
        }
