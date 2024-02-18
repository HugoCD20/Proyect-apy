from flask_restful import Resource
from flask import jsonify, request
from .. import db
from main.models import UsuarioModel
from main.auth.decorator import role_requiered
from flask_jwt_extended import get_jwt_identity

class Cliente(Resource):
    @role_requiered(roles=["admin","cliente"])
    def get(self, id):
        clientes=db.session.query(UsuarioModel).get_or_404(id)
        current_user=get_jwt_identity()
        try:
            if clientes.role == 'cliente':
                 if current_user["usuarioId"]==clientes.id or current_user['role']=='admin':
                    return clientes.to_json()
                 else:
                    return 'Unauthorized',401
            else:
                return 'no es cliente',404
        except:
            return 'ha surgido un error',500
        
    @role_requiered(roles=["cliente"])
    def put(self,id):
        clientes=db.session.query(UsuarioModel).get_or_404(id)
        current_user=get_jwt_identity()
        try:
            if clientes.role == 'cliente' and current_user['usuarioId']==clientes.id:
                data=request.get_json().items()
                for key,value in data:
                    setattr(clientes,key,value)
                db.session.add(clientes)
                db.session.commit()
                return clientes.to_json(), 201
            else:
                return 'Unauthorized',401
        except:
            return 'ha surgido un error',500
        
    @role_requiered(roles=["cliente"])
    def delete(self,id):
        clientes=db.session.query(UsuarioModel).get_or_404(id)
        current_user=get_jwt_identity()
        try:
            if clientes.role == 'cliente'and current_user['usuarioId']==clientes.id:
                db.session.delete(clientes)
                db.session.commit()
                return 'Eliminacion exitosa', 201
                
            else:
                return 'Undauthorized',401
        except:
            return 'ha surgido un error',500

class Clientes(Resource):
    @role_requiered(roles=["admin"])
    def get(self):
        page=1
        per_page=5
        clientes=db.session.query(UsuarioModel).filter(UsuarioModel.role == 'cliente')
        try:
            if request.get_json():
                filters=request.get_json().items()
                for key,value in filters:
                    if key == 'page':
                        page = int(value)
                    elif key == 'per_page':
                        per_page=int(value)
        except:
            pass
        clientes=clientes.paginate(page,per_page,True,5)
        return jsonify({
            "clientes":[cliente.to_json() for cliente in clientes.items],
            "total":clientes.total,
            "pages":clientes.pages,
            "page":page
        })
    
    def post(self):
        clientes=UsuarioModel.from_json(request.get_json())
        if clientes.role == 'cliente':
            db.session.add(clientes)
            db.session.commit()
            return clientes.to_json(),201
        else:
            return 'Solo se puede ingresar clientes',500
    
