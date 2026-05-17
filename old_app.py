from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import request, jsonify

app = Flask (__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://flaskuser:1234@localhost/flaskdb'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

@app.route ('/')
def home():
    return "Connected to MySQL!"
@app.route('/users', methods= ['POST'])
def create_user():
    data = request.get_json()
    new_user = User (
        name=data['name']
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify ({
        "message":"User created",
        "name": new_user.name
    }), 201

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    result = []
    for user in users:
        result.append ({
            "id":user.id,
            "name": user.name
        })
    return jsonify(result)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)