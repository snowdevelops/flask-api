import bcrypt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask import Blueprint, request
from .models import User
from .extensions import db
from .response import success_response, error_response
auth_bp = Blueprint('auth', __name__, url_prefix = '/auth')



@auth_bp.route ('/register', methods = ['POST'])
def register (): 
    data = request.get_json()

    
    if not data:
        return error_response ("Request body must be a JSON", 400)

    if not data.get('name') or not data.get ('email') or not data.get('password'):
        return error_response ("Name, email and password are required", 422)
    
    if User.query.filter_by (email=data['email'].lower()).first():
        return error_response ("Email already registered", 409)


    password = data['password']
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt ())

    user = User (
        name = data['name'],
        email = data['email'],
        password = hashed.decode('utf-8'),
        age = data.get ('age', 0)
    )
    db.session.add (user)
    db.session.commit ()

    return success_response ({
        "message": "User registered successfully",
        "id": user.id,
        'name': user.name,
        "email": user.email
    }, status = 201)

@auth_bp.route ('/login', methods = ['POST'])
def login ():
    data = request.get_json ()
    
    if not data:
        return error_response ("Request body must be a JSON", 400)
    user = User.query.filter_by(email=data.get('email', '').lower()).first ()

    if not user:
        return error_response ("Invalid email or password", 401)
    
    password = data.get('password', '')
    if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        return error_response ("Invalid email or password", 401)
    
    token = create_access_token (identity=str(user.id))
    return success_response ({
        "token": token,
        "name": user.name,
        "email": user.email
    })