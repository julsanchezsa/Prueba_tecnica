from flask import Blueprint, request, jsonify
from app.models import Cliente, Compra, TipoDocumento, ItemCompra, Producto

compras_bp = Blueprint('compras', __name__)

def calcular_total_compra(compra):
    """Calcula el total de una compra a partir de sus ítems."""
    return sum(item.precio_unitario * item.cantidad for item in compra.detalles)

@compras_bp.route('/buscar', methods=['GET'])
def buscar_compras_por_cliente():
    """
    Retorna las compras de un cliente identificado por 'tipo_documento' y 'numero_documento'.
    """
    # Extraer parámetros de la solicitud
    tipo_documento = request.args.get('tipo_documento')
    numero_documento = request.args.get('numero_documento')
    
    if not tipo_documento or not numero_documento:
        return jsonify({"error": "Se requieren los parámetros 'tipo_documento' y 'numero_documento'"}), 400

    # Buscar el cliente realizando un join con TipoDocumento para validar la descripción
    cliente = Cliente.query.join(TipoDocumento).filter(
        TipoDocumento.descripcion == tipo_documento,
        Cliente.numero_documento == numero_documento
    ).first()

    if not cliente:
        return jsonify({"error": "Cliente no encontrado"}), 404

    # Generar una lista con cada compra y su total calculado
    compras_list = []
    for compra in cliente.compras:
        compras_list.append({
            "compra_id": compra.id,
            "fecha": compra.fecha.isoformat(),  # Formatear la fecha a ISO
            "total": calcular_total_compra(compra)
        })

    return jsonify(compras_list), 200

@compras_bp.route('/detalle/<int:compra_id>', methods=['GET'])
def detalle_compra(compra_id):
    """
    Devuelve el detalle de una compra, incluyendo datos de cada ítem y su total.
    """
    # Buscar la compra por ID
    compra = Compra.query.get(compra_id)
    if not compra:
        return jsonify({"error": "Compra no encontrada"}), 404

    # Armar una lista con el detalle de cada ítem de la compra
    detalle_list = []
    for item in compra.detalles:
        # Acceder al producto relacionado al ítem
        producto = item.producto
        detalle_list.append({
            "item_id": item.id,
            "producto_id": producto.id,
            "producto_nombre": producto.nombre,
            "cantidad": item.cantidad,
            "precio_unitario": item.precio_unitario,
            "total": item.precio_unitario * item.cantidad
        })

    return jsonify({
        "compra_id": compra.id,
        "fecha": compra.fecha.isoformat(),
        "detalle": detalle_list
    }), 200

@compras_bp.route('/todas', methods=['GET'])
def todas_compras():
    """
    Retorna una lista de todas las compras con su total, fecha y el cliente asociado.
    """
    compras = Compra.query.all()
    compras_list = []
    for compra in compras:
        compras_list.append({
            "id": compra.id,
            "cliente_id": compra.cliente_id,
            "fecha": compra.fecha.isoformat(),  # Convertir la fecha a un string ISO
            "total": calcular_total_compra(compra)
        })
    return jsonify(compras_list), 200