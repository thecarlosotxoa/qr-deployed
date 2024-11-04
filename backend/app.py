# backend/app.py

from flask import Flask
from flask_cors import CORS
from config import Config
from utils.session import init_session
from routes.auth_routes import auth_routes
from routes.qr_routes import qr_routes
from routes.user_routes import user_routes  # Import user routes

# Create Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize session
init_session(app)

# Configure CORS with allowed frontend origin from Config
CORS(app, supports_credentials=True, resources={r"/api/*": {"origins": Config.FRONTEND_ORIGIN}})

# Register blueprints for route separation
app.register_blueprint(auth_routes)
app.register_blueprint(qr_routes)
app.register_blueprint(user_routes)  # Register user routes

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
    
# local testing
# if __name__ == "__main__":    
    # app.run(debug=True, host='localhost', port=5000)
