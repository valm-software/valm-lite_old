from database import db
from models.Gastos import Gasto

class Usuario(db.Model):
    __tablename__ = 'Usuarios'
    Id = db.Column(db.Integer, primary_key=True)
    Nombre = db.Column(db.String(255))

    # Definir la relación uno a muchos con Cuotas y VentasEncabezados
    #cuotas = db.relationship('Cuota', backref='usuario', lazy=True)
    gastos = db.relationship('Gasto', backref='usuario', lazy=True)
    cuotas = db.relationship('Cuota', backref='usuario', lazy=True)
    ventas_encabezados = db.relationship('VentaEncabezado', backref='usuario', lazy=True)
