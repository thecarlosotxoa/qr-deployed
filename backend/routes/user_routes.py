# backend/routes/user_routes.py

from flask import Blueprint, request, jsonify, session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime, timezone
from utils.db import get_db_connection
import re

user_routes = Blueprint("user", __name__)

@user_routes.route("/api/user/profile", methods=["GET"])
def get_user_profile():
    """Endpoint to get the logged-in user's profile."""
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "User not logged in"}), 403

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, name, email FROM users WHERE id = %s", (user_id,))
        user = cur.fetchone()
        cur.close()
        conn.close()

        if user:
            return jsonify(user), 200
        else:
            return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": "An error occurred while fetching profile."}), 500

@user_routes.route("/api/user/update-profile", methods=["POST"])
def update_profile():
    """Endpoint to update user profile information."""
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "User not logged in"}), 403

    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    current_password = data.get("current_password")
    new_password = data.get("new_password")

    # Validate email format
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return jsonify({"error": "Invalid email format"}), 400

    if new_password and len(new_password) < 6:
        return jsonify({"error": "Password must be at least 6 characters"}), 400

    if not name or not email or not current_password:
        return jsonify({"error": "Name, email, and current password are required."}), 400

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Verify the current password
        cur.execute("SELECT password FROM users WHERE id = %s", (user_id,))
        user = cur.fetchone()
        if not user or not check_password_hash(user["password"], current_password):
            return jsonify({"error": "Incorrect current password"}), 403

        # Update user information
        cur.execute("UPDATE users SET name = %s, email = %s WHERE id = %s", (name, email, user_id))
        
        # Update password if a new password is provided
        if new_password:
            hashed_password = generate_password_hash(new_password)
            cur.execute("UPDATE users SET password = %s WHERE id = %s", (hashed_password, user_id))

        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"message": "Profile updated successfully!"}), 200
    except Exception as e:
        return jsonify({"error": "An error occurred while updating profile."}), 500

@user_routes.route("/api/user/delete-account", methods=["DELETE"])
def delete_account():
    """Endpoint to delete a user account, with password confirmation."""
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "User not logged in"}), 403

    data = request.get_json()
    password = data.get("password")

    if not password:
        return jsonify({"error": "Password is required to delete account"}), 400

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Verify user's password
        cur.execute("SELECT password FROM users WHERE id = %s", (user_id,))
        user = cur.fetchone()

        if not user or not check_password_hash(user["password"], password):
            return jsonify({"error": "Incorrect password"}), 403

        # Delete user and associated data
        cur.execute("DELETE FROM qr_codes WHERE user_id = %s", (user_id,))
        cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
        
        conn.commit()
        cur.close()
        conn.close()

        session.pop("user_id", None)  # Remove session on account deletion
        return jsonify({"message": "Account deleted successfully!"}), 200
    except Exception as e:
        return jsonify({"error": "An error occurred while deleting the account"}), 500
