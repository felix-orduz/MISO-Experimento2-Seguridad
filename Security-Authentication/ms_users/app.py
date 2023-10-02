from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_restful import Resource, Api
from flask_jwt_extended import JWTManager, create_access_token
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from flask_cors import CORS

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from json import JSONEncoder
from flask_wtf import FlaskForm


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_SECRET_KEY'] = 'your-secret-key'
app_context = app.app_context()
app_context.push()
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
api = Api(app)
jwt = JWTManager(app)

# Modelo de Usuario
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

# Definición del esquema con Marshmallow
class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User

# Ruta para registrarse (sign-up) utilizando Flask-RESTful
class SignUpResource(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return {'message': 'El correo electrónico ya está registrado'}, 400

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        new_user = User(email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return {'message': 'Registro exitoso'}, 201

api.add_resource(SignUpResource, '/sign-up')

# Ruta para iniciar sesión (sign-in) utilizando Flask-RESTful
class SignInResource(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password):
            access_token = create_access_token(identity=user.email)
            return {'message': 'Inicio de sesión exitoso', 'access_token': access_token}, 200
        else:
            return {'message': 'Credenciales incorrectas'}, 401

api.add_resource(SignInResource, '/sign-in')

db.create_all()

if __name__ == '__main__':
    app.run(debug=True)


