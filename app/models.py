from .extensions import db

class User (db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    posts = db.relationship('Posts', back_populates = 'user')
    name = db.Column(db.String(100), nullable = False)
    email = db.Column(db.String(120), nullable = False, unique = True)
    age = db.Column(db.Integer, nullable = False)
    phone = db.Column(db.String(20), nullable = True)
    zip_code = db.Column(db.String(20), nullable = True)
    is_active = db.Column(db.Boolean, default = True, nullable = False)
    password = db.Column(db.String(255), nullable = False)
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "age": self.age
        }
class Posts (db.Model):
    __tablename__ = 'posts'
    user = db.relationship('User', back_populates='posts')
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200), nullable = False)
    body = db.Column (db.Text, nullable = False)
    user_id = db.Column (db.Integer, db.ForeignKey('users.id'), nullable = False)


    def to_dict(self):
        return {
            "id" : self.id,
            "title" : self.title,
            "body" : self.body,
            "user": {
                "id": self.user.id,
                "name": self.user.name,
                "email": self.user.email

            }
        }