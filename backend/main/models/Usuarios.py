from .. import db
import datetime as dt 
from werkzeug.security import generate_password_hash, check_password_hash
class Usuario(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    nombre=db.Column(db.String(45), nullable=False)
    apellido=db.Column(db.String(45), nullable=False)
    email=db.Column(db.String(60), nullable=False,unique=True,index=True)
    role=db.Column(db.String(45), nullable=False,default="cliente")
    telefono=db.Column(db.Integer, nullable=False)
    password=db.Column(db.String(100),nullable=False )
    fecha_registro=db.Column(db.DateTime,default=dt.datetime.now() ,nullable=False)
    compra=db.relationship('Compra', back_populates='usuario',cascade="all,delete-orphan")
    
    @property
    def plain_password(self):
        raise AttributeError('Password can\'t be read')
    
    @plain_password.setter
    def plain_password(self,password):
        self.password=generate_password_hash(password)
    
    def validate_password(self,password):
        return check_password_hash(self.password,password)


    def __repr__(self):
        return f"{self.nombre}"
    
    def to_json(self):
        Usuario_json={
            'id':self.id,
            'nombre':self.nombre,
            'apellido':self.apellido,
            'email':self.email,
            'role':self.role,
            'telefono':self.telefono,
            'fecha':str(self.fecha_registro)
        }
        return Usuario_json
    @staticmethod
    def from_json(Usuario_json):
        id=Usuario_json.get('id')
        nombre=Usuario_json.get('nombre')
        apellido=Usuario_json.get('apellido')
        email=Usuario_json.get('email')
        role=Usuario_json.get('role')
        telefono=Usuario_json.get('telefono')
        password=Usuario_json.get('password')
        fecha_registro=Usuario_json.get('fecha_registro')
        return Usuario(
            id=id,
            nombre=nombre,
            apellido=apellido,
            email=email,
            role=role,
            telefono=telefono,
            plain_password=password,
            fecha_registro=fecha_registro
        )

