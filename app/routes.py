import math
from flask import Blueprint, request
from .services import (
    create_user_service,
    get_user_by_id_service,
    update_user_service,
    delete_user_service,
    get_users_paginated_service
)
from .services import (
    create_post_service,
    get_post_by_id_service,
    update_post_service,
    delete_post_service,
    get_all_posts_service
)
from .validators import validate_user, validate_post
from .response import success_response, error_response
from .auth import auth_bp
from flask_jwt_extended import jwt_required, get_jwt_identity

users_bp = Blueprint ('users', __name__, url_prefix='/users')
posts_bp = Blueprint ('posts',__name__ , url_prefix ='/posts')

@users_bp.route('', methods = ['GET'])
@jwt_required()
def get_users():

    page=request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)
    name = request.args.get('name')
    age = request.args.get('age', type=int)
    limit = min(limit, 100)

    users, total = get_users_paginated_service(page=page, limit=limit, name =name, age=age)

    return success_response(
        data=[u.to_dict() for u in users],
        meta={
            "page": page,
            "limit": limit,
            "total": total,
            "total_pages": math.ceil(total / limit) if total > 0 else 0
        }
    )

@posts_bp.route ('', methods = ['GET'])
@jwt_required()

def get_posts():
    post = request.args.get('post', 1, type = int)   
    title = request.args.get ('title')
    body = request.args.get ('body')
    user_id =request.args.get ('user_id', 1, type = int) 

    posts = get_all_posts_service()

    return success_response(
        data = [u.to_dict() for u in posts],
        meta = {
            "post": post,
            "title": title,
            "body": body,
            "user_id": user_id,
        }
    )


@users_bp.route('', methods = ['POST'])


def create_user():
    data = request.get_json()

    if not data:
        return error_response("Request body must be a JSON", 400)
    errors = validate_user(data)
    if errors:
        return error_response (errors, 422)

    from .models import User
    user = create_user_service(data)
    return success_response(user.to_dict(), status =201)

@posts_bp.route('', methods = ['POST'])
def create_post():
    data = request.get_json()
    if not data:
        return error_response ("Request body must be a JSON", 400)
    errors = validate_post(data)
    if errors:
        return error_response (errors, 422)
    
    from.models import Posts
    post = create_post_service(data)
    return success_response(post.to_dict(), status =201)

@users_bp.route('/<int:user_id>', methods = ['GET'])
@jwt_required()

def get_user_by_id(user_id):
    user = get_user_by_id_service(user_id)
    if not user:
        return error_response ("User not found", 404)
    return success_response (user.to_dict())

@posts_bp.route ('/<int:post_id>', methods = ['GET'])
@jwt_required()

def get_post_by_id(post_id):
    post = get_post_by_id_service(post_id)
    if not post:
        return error_response ("Post not found", 404)
    return success_response (post.to_dict())

@users_bp.route('/<int:user_id>', methods = ['PUT'])
@jwt_required()

def update_user(user_id):
    data = request.get_json()
    if not data:
        return error_response ("Request body must be JSON", 400)
    errors = validate_user (data, partial=True)
    if errors:
        return error_response (errors, 422)
    
    user = update_user_service (user_id, data)

    if not user:
        return error_response ("User not found", 404)
    return success_response (user.to_dict())
    
@posts_bp.route ('/<int:post_id>', methods = ['PUT'])
@jwt_required()

def update_post(post_id):
    data = request.get_json()
    if not data:
        return error_response ("Request body must be a JSON", 400)
    errors = validate_post (data, partial = True)
    if errors:
        return error_response (errors, 422)
    
    post = update_post_service(post_id, data)

    if not post:
        return error_response ("Post not found", 404)
    return success_response (post.to_dict())



@users_bp.route ('/<int:user_id>', methods = ['DELETE'])
@jwt_required()
def delete_user(user_id):
    user = delete_user_service (user_id)
    if not user:
        return error_response ("User not found", 400)
    
    return success_response ({
        "message": "User deleted successfully",
        "deleted": user.to_dict()
    })


@posts_bp.route ('/<int:post_id>', methods = ['DELETE'])
@jwt_required()
def delete_post(post_id):
    post = delete_post_service (post_id)
    if not post:
        return error_response ("Post not found", 404)
    
    return success_response ({
        "message": "Post deleted successfully",
        "deleted": post.to_dict()
    })
def register_routes(app):
    app.register_blueprint(users_bp)
    app.register_blueprint(posts_bp)
    app.register_blueprint(auth_bp)