from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

migrate = Migrate ()
db = SQLAlchemy()
jwt = JWTManager()