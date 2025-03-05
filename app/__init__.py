from flask import Flask, render_template
# Configuración
from app.config import Config
# SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(Config)
# Inicializar SQLAlchemy
db = SQLAlchemy(app)
# Importar modelos
from app.models import *

# @app.route('/')
# def home():
#     return render_template("index.html")

# Blueprints
from app.routes.clientes import clientes_bp
from app.routes.reportes import reportes_bp
from app.routes.compras import compras_bp
from app.routes.productos import productos_bp
from app.routes.renders import renders_bp
# Registrar blueprints
app.register_blueprint(clientes_bp, url_prefix='/api/clientes')
app.register_blueprint(reportes_bp, url_prefix='/api/reportes')
app.register_blueprint(compras_bp, url_prefix='/api/compras')
app.register_blueprint(productos_bp, url_prefix='/api/productos')
app.register_blueprint(renders_bp)