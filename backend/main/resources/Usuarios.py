from flask_restful import Resource
from flask import request,jsonify
from .. import db
from main.models import UsuarioModel

class Usuario(Resource):

    def get(self,id):
        usuario=db.session.query(UsuarioModel).get_or_404(id)
        try:
            return usuario.to_json()
        except:
            return "Lo siento no hemos encontrado el usuario",404
    
    def put(self,id):
        usuario=db.session.query(UsuarioModel).get_or_404(id)
        data=request.get_json().items()
        for key,value in data:
            setattr(usuario,key,value)
        try:
            db.session.add(usuario)
            db.session.commit()
            return usuario.to_json(),201
        except:
            return "lo siento pero no existe un usuario con este id",404

    def delete(self,id):
        usuario=db.session.query(UsuarioModel).get_or_404(id)
        try:
            db.session.delete(usuario)
            db.session.commit()
            return 'Eliminacion exitosa',201
        except:
            return 'Ha sucedido un problema inesperado',500


class Usuarios(Resource):

    def get(self):
        page=1
        per_page=5
        usuarios=db.session.query(UsuarioModel)
        try:
            if request.get_json():
                filters=request.get_json().items()
                for key,value in filters:
                    if key=='page':
                        page=int(value)
                    elif key=='per_page':
                        per_page=int(value)
        except:
            pass

        usuarios=usuarios.paginate(page,per_page,True, 5)
        return jsonify({
            "total":usuarios.total,
            "pages":usuarios.pages,
            "page":page,
            "Usuarios":[usuario.to_json() for usuario in usuarios.items]            
        })
    
    def post(self):
        usuario=UsuarioModel.from_json(request.get_json())
        db.session.add(usuario)
        db.session.commit()
        return usuario.to_json()