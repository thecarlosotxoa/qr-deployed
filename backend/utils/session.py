# backend/utils/session.py

from flask_session import Session
from flask import Flask

def init_session(app: Flask):
    """Initialize server-side session with Flask app."""
    app.config.from_object("config.Config")  # Load config from the Config class
    Session(app)  # Initialize Flask-Session
