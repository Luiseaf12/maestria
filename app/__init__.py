from flask import Flask
from app.config import Config

def create_app(config_class=Config):
    """Crea y configura la aplicación Flask"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Registrar blueprints
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)
    
    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    
    return app
