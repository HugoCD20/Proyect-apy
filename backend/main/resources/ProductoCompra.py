from flask_restful import Resource
from flask import request,jsonify
from .. import db
from main.models import ProductoCompraModel

class ProductoCompra(Resource):
    
    def get(self,id):
        productocompra=db.session.query(ProductoCompraModel).get_or_404(id)
        try:
            return productocompra.to_json()
        except:
            return 'No se ha encontrado un productocompra',404
        
    def put(self,id):
        productocompra=db.session.query(ProductoCompraModel).get_or_404(id)
        data=request.get_json().items()
        for key,values in data:
            setattr(productocompra,key,values)
        try:
            db.session.add(productocompra)
            db.session.commit()
            return productocompra.to_json()
        except:
            return 'request not found',404
    
    def delete(self,id):
        productocompra=db.session.query(ProductoCompraModel).get_or_404(id)
        try:
            db.session.delete(productocompra)
            db.session.commit()
            return 'Eliminacion exitosa',201
        except:
            return 'not found',404
        
        
class ProductosCompras(Resource):
    
    def get(self):
        page=1
        per_page=1
        productocompra=db.session.query(ProductoCompraModel)
        try:
            if request.get_json():
                filters=request.get_json().items()
                for key,value in filters:
                    if key == 'page':
                        page=int(value)
                    elif key == 'per_page':
                        per_page=int(value)
        except:
            pass
        productocompra=productocompra.paginate(page,per_page,True,5)
        return jsonify({
            'ProductosCompra':[producto.to_json() for producto in productocompra.items],
            'total':productocompra.total,
            'pages':productocompra.pages,
            'page':page
        })
    
    def post(self):
        productocompra=ProductoCompraModel.from_json(request.get_json())
        db.session.add(productocompra)
        db.session.commit()
        return productocompra.to_json()