from app import db

class ItemCompra(db.Model):
    __tablename__ = 'item_compra'
    id = db.Column(db.Integer, primary_key=True)
    compra_id = db.Column(db.Integer, db.ForeignKey('compra.id'), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey('producto.id'), nullable=False)
    cantidad = db.Column(db.Integer, default=1, nullable=False)
    # Guarda el precio unitario en el momento de la compra para preservar el historial
    precio_unitario = db.Column(db.Float, nullable=False)
