from flask import Blueprint, Response, jsonify
import pandas as pd
from datetime import datetime, timedelta
from app.models import Cliente

reportes_bp = Blueprint('reportes', __name__)

def calcular_total_compra(compra):
    """
    Calcula el total de una compra sumando el precio unitario por la cantidad de cada ítem.
    """
    return sum(item.precio_unitario * item.cantidad for item in compra.detalles)

@reportes_bp.route('/reporte_fidelizacion', methods=['GET'])
def reporte_fidelizacion():
    # Fecha límite para considerar el último mes (30 días atrás)
    fecha_hoy = datetime.now().date()
    fecha_limite = fecha_hoy - timedelta(days=30)

    reporte = []

    # Iterar sobre todos los clientes
    clientes = Cliente.query.all()
    for cliente in clientes:
        # Sumar el total de cada compra realizada en el último mes
        total_ultimo_mes = sum(
            calcular_total_compra(compra) 
            for compra in cliente.compras 
            if compra.fecha >= fecha_limite
        )
        # Solo se incluyen clientes que superen 5’000.000 COP en compras en el último mes
        if total_ultimo_mes > 5000000:
            reporte.append({
                "numero_documento": cliente.numero_documento,
                "tipo_documento": cliente.tipo_documento.descripcion,
                "nombre": cliente.nombre,
                "apellido": cliente.apellido,
                "correo": cliente.correo,
                "telefono": cliente.telefono,
                "total_ultimo_mes": total_ultimo_mes
            })

    if not reporte:
        return jsonify({"message": "No se encontraron clientes que cumplan el criterio."}), 404

    df = pd.DataFrame(reporte)
    csv_data = df.to_csv(index=False, encoding='utf-8-sig', sep=';')

    return Response(
        csv_data,
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=reporte_fidelizacion.csv"}
    )


@reportes_bp.route('/reporte_compras', methods=['GET'])
def reporte_compras():
    # Fecha límite para considerar el último mes (30 días atrás)
    fecha_hoy = datetime.now().date()
    fecha_limite = fecha_hoy - timedelta(days=30)

    reporte = []

    # Iterar sobre todos los clientes
    clientes = Cliente.query.all()
    for cliente in clientes:
        # Calcular el total histórico sumando todas las compras
        total_historico = sum(
            calcular_total_compra(compra) 
            for compra in cliente.compras
        )
        # Calcular el total de compras en el último mes
        total_ultimo_mes = sum(
            calcular_total_compra(compra) 
            for compra in cliente.compras 
            if compra.fecha >= fecha_limite
        )
        
        reporte.append({
            "numero_documento": cliente.numero_documento,
            "tipo_documento": cliente.tipo_documento.descripcion,
            "nombre": cliente.nombre,
            "apellido": cliente.apellido,
            "correo": cliente.correo,
            "telefono": cliente.telefono,
            "total_historico": total_historico,
            "total_ultimo_mes": total_ultimo_mes
        })

    if not reporte:
        return jsonify({"message": "No se encontraron datos para generar el reporte."}), 404

    df = pd.DataFrame(reporte)
    csv_data = df.to_csv(index=False, encoding='utf-8-sig', sep=';')

    return Response(
        csv_data,
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=reporte_compras.csv"}
    )
