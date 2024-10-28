# backend/routes/qr_routes.py

from flask import Blueprint, request, jsonify, session
import qrcode
import io
import base64
import traceback

qr_routes = Blueprint("qr", __name__)

@qr_routes.route("/generate-qr", methods=["POST"])
def generate_qr():
    """Endpoint to generate a QR code."""
    try:
        data = request.json.get("data")
        if not data:
            return jsonify({"error": "No data provided"}), 400

        img = qrcode.make(data)
        img_buffer = io.BytesIO()
        img.save(img_buffer, format="PNG")
        img_str = base64.b64encode(img_buffer.getvalue()).decode("utf-8")

        return jsonify({"qr_code": img_str}), 200
    except Exception as e:
        return jsonify({"error": "An internal server error occurred"}), 500
