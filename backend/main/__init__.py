import os
from flask import Flask
from dotenv import load_dotenv
#aqui vamos a importar la clase para la api
from flask_restful import Api

#aqui voy a importar la clase para el orm de sql
from flask_sqlalchemy import SQLAlchemy
#aqui vamos a importar la libreria para los JWT
from flask_jwt_extended import JWTManager
#importo el modulo para trabajar con mail
from flask_mail import Mail

db=SQLAlchemy()
api=Api()
jwt=JWTManager()
mailsender=Mail()

def create_app():
    app = Flask(__name__)
    load_dotenv()
    #carcar las variables de entorno
    PATH=os.getenv("DATABASE_PATH")
    DB_NAME=os.getenv("DATABASE_NAME")
    if not os.path.exists(f"{PATH}{DB_NAME}"):
        os.chdir(f'{PATH}')
        file= os.open(f'{DB_NAME}', os.O_CREAT)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
    app.config['SQLALCHEMY_DATABASE_URI']=f"sqlite:///{PATH}{DB_NAME}"
    db.init_app(app)

    import main.resources as resourcest

    api.add_resource(resourcest.ClientesResources,'/clientes')
    api.add_resource(resourcest.ClienteResources,'/cliente/<id>')
    api.add_resource(resourcest.UsuariosResources,'/Usuarios')
    api.add_resource(resourcest.UsuarioResources,'/Usuario/<id>')
    api.add_resource(resourcest.ProductosResources,'/Productos')
    api.add_resource(resourcest.ProductoResources,'/Producto/<id>')
    api.add_resource(resourcest.ComprasResources,'/compras')
    api.add_resource(resourcest.CompraResources,'/compra/<id>')
    api.add_resource(resourcest.ProductosComprasResources,'/productoscompras')
    api.add_resource(resourcest.ProductoCompraResources,'/productocompra/<id>')
    api._init_app(app)

    #configuracion para los JWT
    app.config['JWT_SECRET_KEY']=os.getenv("JWT_SECRET_KEY")
    app.config['JWT_ACCESS_TOKEN_EXPIRES']=int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES"))
    jwt.init_app(app)

    #Blueprint
    from main.auth import routes
    app.register_blueprint(auth.routes.auth)
    from main.mail import functions
    app.register_blueprint(mail.functions.mail)

    #configurar mail
    app.config['MAIL_HOSTNAME']=os.getenv('MAIL_HOSTNAME')
    app.config['MAIL_SERVER']=os.getenv('MAIL_SERVER')
    app.config['MAIL_PORT']=os.getenv('MAIL_PORT')
    app.config['MAIL_USE_TLS']=os.getenv('MAIL_USE_TLS')
    app.config['MAIL_USERNAME']=os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD']=os.getenv('MAIL_PASSWORD')
    app.config['FLASKY_MAIL_SENDER']=os.getenv('FLASKY_MAIL_SENDER')
    mailsender.init_app(app)
    

    return app