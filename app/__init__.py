from flask import Flask,jsonify
from .extensions import db, migrate, jwt
from .routes import register_routes
from dotenv import load_dotenv
from .response import error_response
import os

load_dotenv ()

def create_app():
    app = Flask(__name__)

    import os
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv ('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    
    jwt.init_app(app)
    db.init_app(app)    
    migrate.init_app(app, db)

    register_routes(app)

    @app.errorhandler(404)
    def not_found(e):
        return jsonify ({"success": False, "error": "Route not found", "data": None}), 404
    
    @jwt.unauthorized_loader
    def missing_token(callback):
        return error_response ("Missing or invalid Authorization header", 401)
    
    @app.errorhandler(405)
    def method_not_allowed(e):
        return jsonify ({"success": False, "error": "Method not allowed", "data": None}), 405
    
    @jwt.invalid_token_loader
    def invalid_token(callback, error):
        return error_response ("Invalid token", 401)
    
    
    @app.errorhandler(500)
    def internal_error(e):
        return jsonify ({"success": False, "error": "Internal server error", "data": None}), 500
    
    @jwt.expired_token_loader
    def expired_token(jwt_header, jwt_data):
        return error_response ("Token has expired", 401)


    return app