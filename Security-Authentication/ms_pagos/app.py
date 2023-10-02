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

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///payments.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_SECRET_KEY'] = 'your-secret-key'
app_context = app.app_context()
app_context.push()
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
api = Api(app)
jwt = JWTManager(app)

# Modelo de pago
class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(120), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200), nullable=True)
    date = db.Column(db.DateTime, nullable=False, default=db.func.current_date())

# Definición del esquema con Marshmallow
class PaymentSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Payment

# Recursos para operaciones CRUD en Pago
class PaymentListResource(Resource):
    @jwt_required()
    def get(self):
        # user_email = get_jwt_identity()
        payments = Payment.query.all()
        payment_schema = PaymentSchema(many=True)
        return payment_schema.dump(payments), 200

    @jwt_required()
    def post(self):
        payment_schema = PaymentSchema()
        data = request.get_json()
        # Asignamos el email del usuario actual como el propietario del pago
        data['user_email'] = get_jwt_identity()
        new_payment = Payment(**data)

        db.session.add(new_payment)
        db.session.commit()
        return payment_schema.dump(new_payment), 201


api.add_resource(PaymentListResource, '/payments')

db.create_all()

if __name__ == '__main__':
    app.run(debug=True)


