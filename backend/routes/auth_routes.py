# backend/routes/auth_routes.py

from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
import re
from utils.db import get_db_connection

auth_routes = Blueprint("auth", __name__)

@auth_routes.route("/register", methods=["POST"])
def register_user():
    """Endpoint for user registration."""
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not name or not email or not password:
        return jsonify({"error": "Name, email, and password are required."}), 400

    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return jsonify({"error": "Invalid email format"}), 400

    if len(password) < 6:
        return jsonify({"error": "Password must be at least 6 characters"}), 400

    hashed_password = generate_password_hash(password)

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        if cur.fetchone():
            return jsonify({"error": "User with this email already exists."}), 400

        cur.execute(
            "INSERT INTO users (name, email, password) VALUES (%s, %s, %s) RETURNING id",
            (name, email, hashed_password),
        )
        user_id = cur.fetchone()["id"]
        conn.commit()
        cur.close()
        conn.close()

        session["user_id"] = user_id
        return jsonify({"message": "User registered successfully!", "user": {"id": user_id, "name": name, "email": email}}), 201
    except Exception as e:
        return jsonify({"error": "An error occurred during registration."}), 500

@auth_routes.route("/login", methods=["POST"])
def login_user():
    """Endpoint for user login."""
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password are required."}), 400

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        cur.close()
        conn.close()

        if user and check_password_hash(user["password"], password):
            session["user_id"] = user["id"]
            session.permanent = True
            return jsonify({"message": "Login successful!", "user": {"id": user["id"], "name": user["name"], "email": user["email"]}}), 200
        else:
            return jsonify({"error": "Invalid credentials"}), 401
    except Exception as e:
        return jsonify({"error": "An error occurred during login."}), 500

@auth_routes.route("/logout", methods=["POST"])
def logout_user():
    """Endpoint for user logout."""
    session.pop("user_id", None)
    return jsonify({"message": "Logged out successfully."}), 200
