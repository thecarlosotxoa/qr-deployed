# backend/config.py

import os
from dotenv import load_dotenv
from datetime import timedelta

# Load environment variables from .env file
load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")  # Secure secret key
    SESSION_TYPE = os.getenv("SESSION_TYPE", "filesystem")
    SESSION_COOKIE_SECURE = True          # Set to True if using HTTPS
    SESSION_COOKIE_HTTPONLY = True        # Prevents JavaScript access for added security
    SESSION_COOKIE_SAMESITE = 'Lax'       # Helps prevent CSRF attacks; set 'None' if CORS is needed
    SESSION_COOKIE_DOMAIN = None          # Default to None, allowing CORS settings
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)

    # CORS configuration for allowed frontend origin
    FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN")

    # Database configuration
    DATABASE_URL = os.getenv("DATABASE_URL")  # PostgreSQL connection string
