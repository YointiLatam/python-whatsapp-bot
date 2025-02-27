from flask import Flask
from app.config import load_configurations, configure_logging
from .views import webhook_blueprint

app = Flask(__name__)

# Cargar configuraciones
load_configurations(app)
configure_logging()

# Registrar blueprints
app.register_blueprint(webhook_blueprint)