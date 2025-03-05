from flask import Blueprint, jsonify
from app.models import Producto

productos_bp = Blueprint('productos', __name__)

@productos_bp.route('/todos', methods=['GET'])
def obtener_todos_productos():
    """
    Retorna todos los productos en formato JSON.
    
    Proceso:
    - Consulta la tabla Producto para obtener todos los registros.
    - Itera sobre cada producto y extrae sus campos (id, nombre, precio).
    - Retorna la lista completa de productos con un código de estado 200.
    """
    productos = Producto.query.all()
    productos_list = []
    for producto in productos:
        productos_list.append({
            "id": producto.id,
            "nombre": producto.nombre,
            "precio": producto.precio
        })
    return jsonify(productos_list), 200