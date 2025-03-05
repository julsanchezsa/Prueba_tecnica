from app import app, db
from app.models.tipo_documento import TipoDocumento
from app.models.cliente import Cliente
from app.models.compra import Compra
from app.models.producto import Producto
from app.models.item_compra import ItemCompra
from datetime import datetime

with app.app_context():
    # Opcional: Limpiar la base de datos para comenzar desde cero
    db.drop_all()
    db.create_all()
    
    # 1. Insertar Tipos de Documento
    nit = TipoDocumento(descripcion='NIT')
    cedula = TipoDocumento(descripcion='Cedula')
    pasaporte = TipoDocumento(descripcion='Pasaporte')
    db.session.add_all([nit, cedula, pasaporte])
    db.session.commit()
    
    # 2. Insertar Clientes
    cliente1 = Cliente(
        tipo_documento_id=cedula.id,
        numero_documento='123456789',
        nombre='Juan',
        apellido='Perez',
        correo='juan.perez@example.com',
        telefono='3001234567'
    )
    cliente2 = Cliente(
        tipo_documento_id=nit.id,
        numero_documento='987654321',
        nombre='Ana',
        apellido='Gomez',
        correo='ana.gomez@example.com',
        telefono='3107654321'
    )
    db.session.add_all([cliente1, cliente2])
    db.session.commit()
    
    # 3. Insertar Productos
    producto1 = Producto(nombre='Producto A', precio=15000.0)
    producto2 = Producto(nombre='Producto B', precio=25000.0)
    producto3 = Producto(nombre='Producto C', precio=35000.0)
    db.session.add_all([producto1, producto2, producto3])
    db.session.commit()
    
    # 4. Insertar Compras
    compra1 = Compra(cliente_id=cliente1.id, fecha=datetime(2023, 3, 15).date())
    compra2 = Compra(cliente_id=cliente2.id, fecha=datetime(2023, 3, 16).date())
    compra3 = Compra(cliente_id=cliente1.id, fecha=datetime(2023, 3, 17).date())
    compra4 = Compra(cliente_id=cliente2.id, fecha=datetime(2023, 3, 18).date())
    compra5 = Compra(cliente_id=cliente1.id, fecha=datetime.today().date())
    compra6 = Compra(cliente_id=cliente2.id, fecha=datetime.today().date())
    db.session.add_all([compra1, compra2, compra3, compra4,compra5, compra6])
    db.session.commit()
    
    # 5. Insertar Items (líneas) de Compra
    item1 = ItemCompra(compra_id=compra1.id, producto_id=producto1.id, cantidad=2, precio_unitario=producto1.precio)
    item2 = ItemCompra(compra_id=compra1.id, producto_id=producto2.id, cantidad=1, precio_unitario=producto2.precio)
    item3 = ItemCompra(compra_id=compra2.id, producto_id=producto3.id, cantidad=3, precio_unitario=producto3.precio)
    item4 = ItemCompra(compra_id=compra3.id, producto_id=producto1.id, cantidad=1, precio_unitario=producto1.precio)
    item5 = ItemCompra(compra_id=compra4.id, producto_id=producto2.id, cantidad=2, precio_unitario=producto2.precio)
    item6 = ItemCompra(compra_id=compra4.id, producto_id=producto3.id, cantidad=1, precio_unitario=producto3.precio)
    item7 = ItemCompra(compra_id=compra5.id, producto_id=producto1.id, cantidad=334, precio_unitario=producto1.precio)  # Total: 5,010,000.0
    item8 = ItemCompra(compra_id=compra5.id, producto_id=producto2.id, cantidad=1, precio_unitario=producto2.precio)    # Total: 25,000.0
    item9 = ItemCompra(compra_id=compra6.id, producto_id=producto3.id, cantidad=140, precio_unitario=producto3.precio)  # Total: 5,005,000.0
    item10 = ItemCompra(compra_id=compra6.id, producto_id=producto1.id, cantidad=1, precio_unitario=producto1.precio)   # Total: 15,000.0
    db.session.add_all([item1, item2, item3, item4, item5, item6, item7, item8, item9, item10])
    db.session.commit()
    
    print("Datos insertados correctamente.")
