import math
from flask import Blueprint, request
from .services import (
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
    title = request.args.get('title')
    user_id = request.args.get('user_id', type=int)

    posts = get_all_posts_service(title=title, user_id=user_id)

    return success_response(
        data=[u.to_dict() for u in posts],
        meta={
            "title": title,
            "user_id": user_id,
        }
    )


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
    current_user_id = int(get_jwt_identity())
    if current_user_id != user_id:
        return error_response("You can only update your own account", 403)

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
    current_user_id = int(get_jwt_identity())
    post = get_post_by_id_service(post_id)
    if not post:
        return error_response ("Post not found", 404)
    if post.user_id != current_user_id:
        return error_response ("You can only update your own posts", 403)

    data = request.get_json()
    if not data:
        return error_response ("Request body must be a JSON", 400)
    errors = validate_post (data, partial = True)
    if errors:
        return error_response (errors, 422)

    post = update_post_service(post_id, data)
    return success_response (post.to_dict())



@users_bp.route ('/<int:user_id>', methods = ['DELETE'])
@jwt_required()
def delete_user(user_id):
    current_user_id = int(get_jwt_identity())
    if current_user_id != user_id:
        return error_response("You can only delete your own account", 403)

    user = delete_user_service (user_id)
    if not user:
        return error_response ("User not found", 404)

    return success_response ({
        "message": "User deleted successfully",
        "deleted": user.to_dict()
    })


@posts_bp.route ('/<int:post_id>', methods = ['DELETE'])
@jwt_required()
def delete_post(post_id):
    current_user_id = int(get_jwt_identity())
    post = get_post_by_id_service(post_id)
    if not post:
        return error_response ("Post not found", 404)
    if post.user_id != current_user_id:
        return error_response ("You can only delete your own posts", 403)

    deleted_data = post.to_dict()
    delete_post_service (post_id)
    return success_response ({
        "message": "Post deleted successfully",
        "deleted": deleted_data
    })
def register_routes(app):
    app.register_blueprint(users_bp)
    app.register_blueprint(posts_bp)
    app.register_blueprint(auth_bp)