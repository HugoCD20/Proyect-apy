from .. import jwt
from flask_jwt_extended import verify_jwt_in_request,get_jwt

def role_requiered(roles):
    def decorator(function):
        def wrapper(*args,**kwargs):
            #verificar qye el jwt es correcto
            verify_jwt_in_request()
            #obtener los claims(peticiones), que estan dentro de jwt
            claims=get_jwt()

            if claims['sub']['role'] in roles:
                return function(*args,**kwargs)
            else:
                return 'Rol not allowed', 403
        
        return wrapper
    return decorator

@jwt.user_identity_loader
def user_identity_lookup(usuario):
    return{
        'usuarioId':usuario.id,
        'role': usuario.role
    }

@jwt.additional_claims_loader
def add_claim_to_access_token(usuario):
    claims={
        'id':usuario.id,
        'role':usuario.role,
        'email':usuario.email
    }