from flask_restful import Resource
from flask import request,jsonify
from .. import db
from main.models import CompraModel
from main.auth.decorator import role_requiered
from flask_jwt_extended import get_jwt_identity
class Compra(Resource):
    @role_requiered(roles=["admin","cliente"])
    def get(self,id):
        compra=db.session.query(CompraModel).get_or_404(id)
        current_user=get_jwt_identity()
        if current_user['usuarioId']==compra.usuarioId or current_user["role"]=="admin":
            try:
                return compra.to_json()
            except:
                return 'Compra no encontrada', 404
        else:
            return 'Unauthorized',401
        
    @role_requiered(roles=["admin","cliente"])
    def delete(self,id):
        compra=db.session.query(CompraModel).get_or_404(id)
        current_user=get_jwt_identity()
        if current_user['usuarioId']==compra.usuarioId or current_user['role']=="admin":
            try:
                db.session.delete(compra)
                db.session.commit()
                return "Eliminación exitosa",201
            except:
                return "Ha ocurrido un error",401
        else:
            return 'Unauthorized',401
    
    @role_requiered(roles=["admin","cliente"])
    def put(self,id):
        compra=db.session.query(CompraModel).get_or_404(id)
        current_user=get_jwt_identity()
        if current_user['usuarioId']==compra.usuarioId or current_user['role']=="admin":
            data=request.get_json().items()
            for key,value in data:
                setattr(compra,key,value)
            try:
                db.session.add(compra)
                db.session.commit()
                return compra.to_json(), 201
            except:
                return "Ha sucedido un error",401
        else:
            return 'Unauthorized',401

        
class Compras(Resource):
    
    @role_requiered(roles=["admin"])
    def get(self):
        page=1
        per_page=5
        compras=db.session.query(CompraModel)
        try:
            if request.get_json():
                filters=request.get_json().items()
                for key,value in filters:
                    if key == 'page':
                        page=int(value)
                    elif key =='per_page':
                        per_page=int(value)
        except:
            pass
        compras=compras.paginate(page,per_page,True,5)
        return jsonify({
            "Compras":[compra.to_json() for compra in compras.items],
            "total":compras.total,
            "pages":compras.pages,
            "page":page
        })
    @role_requiered(roles=["admin","cliente"])
    def post(self):
        compra=CompraModel.from_json(request.get_json())
        db.session.add(compra)
        db.session.commit()

        return compra.to_json(),201