from flask import Flask
from routes import FirmasRoutes

app = Flask(__name__)


def init_app():
    app.register_blueprint(FirmasRoutes.app, url_prefix='/firmas')
    
    return app