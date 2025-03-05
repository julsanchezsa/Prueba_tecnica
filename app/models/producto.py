from app import db

class Producto(db.Model):
    __tablename__ = 'producto'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    # Relación: Un producto puede aparecer en varios detalles de compra
    detalles = db.relationship('ItemCompra', backref='producto', lazy=True)
