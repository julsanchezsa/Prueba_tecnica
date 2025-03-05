from flask import Blueprint, render_template

renders_bp = Blueprint('renders', __name__)

@renders_bp.route('/')
def home():
    return render_template("index.html")

@renders_bp.route('/clientes')
def clientes():
    return render_template("clientes.html")

@renders_bp.route('/productos')
def productos():
    return render_template("productos.html")