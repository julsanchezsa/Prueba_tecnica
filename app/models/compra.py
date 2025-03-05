from app import db

class Compra(db.Model):
    __tablename__ = 'compra'
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    # Relación: Una compra tiene uno o varios detalles de compra
    detalles = db.relationship('ItemCompra', backref='compra', lazy=True)
