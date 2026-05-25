from .models import User, Posts
from .extensions import db
from sqlalchemy.exc import SQLAlchemyError

#CREATE

def create_user_service (data):
    try:
        new_user = User(
            name = data['name'].strip(),
            email = data['email'].lower().strip(),
            age = data['age']
        )
        db.session.add(new_user)
        db.session.commit()

        return new_user
    except SQLAlchemyError:
        db.session.rollback()
        raise

def create_post_service(data):
    try:
        new_post = Posts(
             title = data ['title'],
            body = data['body'],
            user_id = data['user_id']
        )
        db.session.add(new_post)
        db.session.commit()
        return new_post
    except SQLAlchemyError:
        db.session.rollback()
        raise

#READ (all)

def get_all_users_service():
    return User.query.all()

def get_all_posts_service():
    return Posts.query.all()

#READ (BY ID)

def get_user_by_id_service(user_id):
    return User.query.get(user_id)

def get_post_by_id_service(post_id):
    return Posts.query.get(post_id)

#UPDATE 

def update_user_service (user_id,data):
    try:
        user = User.query.get(user_id)

        if not user:
            return None
    
        user.name = data.get('name', user.name).strip()
        user.email = data.get ('email', user.email).lower().strip()
        user.age = data.get ('age', user.age)

        db.session.commit()

        return user
    except SQLAlchemyError:
        db.session.rollback()
        raise

def update_post_service (post_id,data):
    try:
        post = Posts.query.get(post_id)
        if not post:
            return None
        post.title = data.get ('title', post.title).strip()
        post.body = data.get ('body', post.body)
        post.user_id = data.get ('user_id', post.user_id)

        db.session.commit()

        return post
    except SQLAlchemyError:
        db.session.rollback()
        raise

#DELETE

def delete_user_service (user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return None
    
        db.session.delete(user)
        db.session.commit()

        return user
    except SQLAlchemyError:
        db.session.rollback()
        raise

def delete_post_service (post_id):
    try:
        post = Posts.query.get(post_id)
        if not post:
            return None
        db.session.delete(post)
        db.session.commit()
    
        return post
    except SQLAlchemyError:
        db.session.rollback()
        raise
    
#Optimization Paginating

def get_users_paginated_service (page=1,limit = 10, name= None, age= None):

    query = User.query
    if name:
        query = query.filter(User.name.ilike(f"%{name}%"))

    if age:
        query = query.filter (User.age == age)

    total = query.count()

    users = query.order_by(User.id).offset ((page - 1) * limit).limit(limit).all()
    
    return users, total