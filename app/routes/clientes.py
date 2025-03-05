from flask import Blueprint, request, jsonify, Response
from app.models import Cliente, TipoDocumento
import pandas as pd

# Crear un blueprint para agrupar los endpoints relacionados con clientes.
clientes_bp = Blueprint('clientes', __name__)

@clientes_bp.route('/buscar', methods=['GET'])
def buscar_cliente():
    """
    Busca un cliente en la base de datos utilizando el tipo de documento y el número de documento.
    
    Proceso:
    - Recibe 'tipo_documento' y 'numero_documento' como parámetros en la solicitud GET.
    - Verifica que ambos parámetros estén presentes.
    - Realiza un join entre Cliente y TipoDocumento para validar y filtrar el registro.
    - Si no encuentra el cliente, retorna error 404; de lo contrario, retorna el JSON con la información.
    """
    # Recuperar los parámetros desde la query string
    tipo_documento = request.args.get('tipo_documento')
    numero_documento = request.args.get('numero_documento')
    
    # Verificar que se hayan enviado ambos parámetros
    if not tipo_documento or not numero_documento:
        # Si falta algún parámetro, se responde con un error 400
        return jsonify({"error": "Se requieren los parámetros 'tipo_documento' y 'cedula'"}), 400

    # Realizar la consulta combinando la tabla Cliente con TipoDocumento
    cliente = Cliente.query.join(TipoDocumento).filter(
        TipoDocumento.descripcion == tipo_documento,
        Cliente.numero_documento == numero_documento
    ).first()

    # Comprobar si se encontró el cliente
    if not cliente:
        # Si el cliente no existe, retornar error 404
        return jsonify({"error": "Cliente no encontrado"}), 404

    # Preparar el diccionario con los datos del cliente
    data = {
        "id": cliente.id,
        "tipo_documento": cliente.tipo_documento.descripcion,
        "numero_documento": cliente.numero_documento,
        "nombre": cliente.nombre,
        "apellido": cliente.apellido,
        "correo": cliente.correo,
        "telefono": cliente.telefono
    }
    # Retornar la información del cliente en formato JSON; código 200 indica éxito
    return jsonify(data), 200

@clientes_bp.route('/exportar', methods=['GET'])
def exportar_cliente_con_pandas():
    """
    Exporta la información de un cliente a un archivo CSV utilizando Pandas.
    
    Proceso:
    - Extrae 'tipo_documento' y 'numero_documento' de la solicitud GET.
    - Verifica la existencia de ambos parámetros.
    - Realiza un join entre Cliente y TipoDocumento para buscar el cliente.
    - Si no se encuentra, retorna error 404; en caso contrario, crea un DataFrame.
    - Convierte el DataFrame a CSV (se usa ";" como separador y UTF-8-SIG para la codificación).
    - Retorna el CSV como archivo adjunto en la respuesta.
    """
    # Recuperar parámetros enviados en la petición GET
    tipo_documento = request.args.get('tipo_documento')
    numero_documento = request.args.get('numero_documento')
    
    # Verificar que los parámetros requeridos estén presentes
    if not tipo_documento or not numero_documento:
        # Si falta algún parámetro, retornar error 400
        return jsonify({"error": "Se requieren los parámetros 'tipo_documento' y 'numero_documento'"}), 400

    # Realizar consulta para obtener el cliente que coincida con los parámetros
    cliente = Cliente.query.join(TipoDocumento).filter(
        TipoDocumento.descripcion == tipo_documento,
        Cliente.numero_documento == numero_documento
    ).first()

    # Si el cliente no existe, devolver error 404
    if not cliente:
        return jsonify({"error": "Cliente no encontrado"}), 404

    # Crear un diccionario con los datos del cliente para construir el DataFrame
    data = {
        'numero_documento': [cliente.numero_documento],
        'tipo_documento': [cliente.tipo_documento.descripcion],
        'nombre': [cliente.nombre],
        'apellido': [cliente.apellido],
        'correo': [cliente.correo],
        'telefono': [cliente.telefono]
    }
    # Construir el DataFrame a partir del diccionario
    df = pd.DataFrame(data)
    
    # Convertir el DataFrame a formato CSV sin el índice
    csv_data = df.to_csv(index=False, encoding='utf-8-sig', sep=';')

    # Retornar la respuesta con el CSV como archivo adjunto
    return Response(
        csv_data,
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=cliente.csv"}
    )

@clientes_bp.route('/todos', methods=['GET'])
def obtener_todos_los_clientes():
    """
    Retorna todos los clientes de la base de datos en formato JSON.
    
    Proceso:
    - Consulta la tabla Cliente para obtener todos los registros.
    - Itera sobre cada cliente extrayendo sus datos y también el tipo de documento.
    - Retorna la lista completa de clientes en formato JSON con código 200.
    """
    # Ejecutar consulta para obtener todos los clientes
    clientes = Cliente.query.all()
    clientes_list = []
    # Recorrer cada cliente y preparar su representación JSON
    for cliente in clientes:
        clientes_list.append({
            "id": cliente.id,
            "tipo_documento": cliente.tipo_documento.descripcion,
            "numero_documento": cliente.numero_documento,
            "nombre": cliente.nombre,
            "apellido": cliente.apellido,
            "correo": cliente.correo,
            "telefono": cliente.telefono
        })
    # Devolver la lista de clientes junto con el código de estado 200 (éxito)
    return jsonify(clientes_list), 200