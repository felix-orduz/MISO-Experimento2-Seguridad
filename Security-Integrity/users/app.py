import hashlib
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'supersecretkey'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    public_key = db.Column(db.String(500))  # Aquí almacenamos la clave pública del usuario

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    password = bcrypt.generate_password_hash(data['password']).decode('utf-8')

    # Generamos una clave pública/privada para el usuario
    public_key = hashlib.sha256(username.encode()).hexdigest()  # Esto es un ejemplo simplificado
    print(public_key)
    new_user = User(username=username, password=password, public_key=public_key)
    db.session.add(new_user)
    print(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()

    if user and bcrypt.check_password_hash(user.password, data['password']):
        access_token = create_access_token(identity=user.id)
        return jsonify({"access_token": access_token}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401

@app.route('/user/profile', methods=['GET'])
@jwt_required()
def user_profile():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({'msg': 'User not found'}), 404

    # Aquí puedes personalizar los datos que deseas devolver en el perfil del usuario.
    # Por ejemplo, podrías devolver el nombre y el correo electrónico.
    profile_data = {
        'username': user.username,
        'public_key': user.public_key
    }

    return jsonify(profile_data), 200

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
