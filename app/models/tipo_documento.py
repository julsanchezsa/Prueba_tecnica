from app import db

class TipoDocumento(db.Model):
    __tablename__ = 'tipo_documento'
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(50), nullable=False)
    # Relación: Un tipo de documento puede estar asociado a muchos clientes
    clientes = db.relationship('Cliente', backref='tipo_documento', lazy=True)
