import functools
from flask import Blueprint, request, jsonify, session, redirect, url_for, flash
from app.models import db, User

auth_bp = Blueprint("auth", __name__)

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if "user_id" not in session:
            if request.is_json or request.path.startswith("/api/"):
                return jsonify({"success": False, "error": "Authentication required"}), 401
            return redirect(url_for("routes.login_page"))
        return view(**kwargs)
    return wrapped_view

def get_current_user():
    if "user_id" in session:
        return db.session.get(User, session["user_id"])
    return None

@auth_bp.route("/api/auth/register", methods=["POST"])
def api_register():
    data = request.get_json() or {}
    username = (data.get("username") or "").strip()
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""
    
    if not username or len(username) < 3:
        return jsonify({"success": False, "error": "Username must be at least 3 characters"}), 400
    if not email or "@" not in email:
        return jsonify({"success": False, "error": "Valid email required"}), 400
    if not password or len(password) < 6:
        return jsonify({"success": False, "error": "Password must be at least 6 characters"}), 400
        
    if User.query.filter((User.username == username) | (User.email == email)).first():
        return jsonify({"success": False, "error": "Username or email already exists"}), 409
        
    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    
    session["user_id"] = user.id
    session["username"] = user.username
    
    return jsonify({
        "success": True,
        "message": "User registered successfully",
        "user": user.to_dict()
    }), 201

@auth_bp.route("/api/auth/login", methods=["POST"])
def api_login():
    data = request.get_json() or {}
    login_id = (data.get("username") or data.get("email") or "").strip()
    password = data.get("password") or ""
    
    if not login_id or not password:
        return jsonify({"success": False, "error": "Credentials required"}), 400
        
    user = User.query.filter((User.username == login_id) | (User.email == login_id.lower())).first()
    if not user or not user.check_password(password):
        return jsonify({"success": False, "error": "Invalid username or password"}), 401
        
    session["user_id"] = user.id
    session["username"] = user.username
    
    return jsonify({
        "success": True,
        "message": "Login successful",
        "user": user.to_dict()
    })

@auth_bp.route("/api/auth/logout", methods=["POST", "GET"])
def api_logout():
    session.clear()
    if request.is_json or request.path.startswith("/api/"):
        return jsonify({"success": True, "message": "Logged out successfully"})
    return redirect(url_for("routes.index"))

@auth_bp.route("/api/auth/me", methods=["GET"])
def api_me():
    user = get_current_user()
    if not user:
        return jsonify({"authenticated": False, "user": None})
    return jsonify({"authenticated": True, "user": user.to_dict()})
