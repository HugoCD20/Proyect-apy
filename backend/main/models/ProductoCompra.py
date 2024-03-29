from .. import db

class ProductoCompra(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    productoId=db.Column(db.Integer,db.ForeignKey('producto.id'),nullable=False)
    producto=db.relationship('Producto',back_populates='productoscompras',uselist=False)
    compraId=db.Column(db.Integer,db.ForeignKey('compra.id'),nullable=False)
    compra=db.relationship('Compra',back_populates='productoscompras',uselist=False)

    def __repr__(self):
        return f"{self.id}"
    
    def to_json(self):
        productocompra_json={
            'id':self.id,
            'producto':self.producto.to_json(),
            'compra':self.compra.to_json()
        }
        return productocompra_json
    @staticmethod

    def from_json(productocompra_json):
        id=productocompra_json.get('id')
        productoId=productocompra_json.get('productoId')
        compraId=productocompra_json.get('compraId')

        return ProductoCompra(
            id=id,
            productoId=productoId,
            compraId=compraId
        )


