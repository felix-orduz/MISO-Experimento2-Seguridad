import hashlib
from hashlib import blake2b
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'supersecretkey'
db = SQLAlchemy(app)
jwt = JWTManager(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    hash = db.Column(db.String(64))  # Almacenamos el hash del contenido

@app.route('/post', methods=['POST'])
@jwt_required()
def create_post():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    title = data['title']
    content = data['content']

    # Calculamos el hash del contenido usando la tecnica de keyed hashing para autenticacion
    # con el hash criptografico Blake
    h = blake2b(key=b't3<};{%MvdX5u@_w=2gTY', digest_size=16)
    h.update(content.encode())
    #content_hash = hashlib.sha256(content.encode()).hexdigest()
    content_hash = h.hexdigest()
    
    print(content_hash)
    new_post = Post(title=title, content=content, user_id=current_user_id, hash=content_hash)
    db.session.add(new_post)
    db.session.commit()

    return jsonify({"message": "Post created successfully"}), 201


@app.route('/post/<int:id>', methods=['PUT'])
@jwt_required()
def update_post(id):
    current_user_id = get_jwt_identity()
    data = request.get_json()
    new_content = data['content']

    # Obtener la publicación actual
    post = Post.query.get_or_404(id)

    # Calcular el hash del nuevo contenido
    # usando la tecnica de keyed hashing para autenticacion con el hash criptografico Blake
    h = blake2b(key=b't3<};{%MvdX5u@_w=2gTY', digest_size=16)
    h.update(new_content.encode())
    new_content_hash = h.hexdigest()

    # Verificar si el usuario actual es el autor de la publicación
    if current_user_id != post.user_id:
        return jsonify({"message": "You are not authorized to update this post."}), 403

    # Actualizar el contenido y el hash
    post.content = new_content
    post.hash = new_content_hash

    db.session.commit()

    return jsonify({"message": "Post updated successfully"}), 200

@app.route('/post/<int:id>', methods=['GET'])
def get_post(id):
    post = Post.query.get_or_404(id)

    # Verificar la integridad del contenido
    # Calcular el hash del nuevo contenido
    # usando la tecnica de keyed hashing para autenticacion con el hash criptografico Blake
    h = blake2b(key=b't3<};{%MvdX5u@_w=2gTY', digest_size=16)
    h.update(post.content.encode())
    content_hash = h.hexdigest()
    if content_hash != post.hash:
        return jsonify({"message": "Integrity check failed. Content has been tampered."}), 400

    # Si la verificación de integridad pasa, puedes devolver el contenido del post
    return jsonify({"id": post.id ,"title": post.title, "content": post.content}), 200

@app.route('/posts', methods=['GET'])
def get_posts():

    posts = Post.query.all()
    valid_posts = []

    for post in posts:
        # Verificar la integridad del contenido
        h = blake2b(key=b't3<};{%MvdX5u@_w=2gTY', digest_size=16)
        h.update(post.content.encode())
        content_hash = h.hexdigest()
        if content_hash == post.hash:
            # El post es válido, lo agregamos a la lista de posts válidos
            valid_posts.append({"id": post.id, "title": post.title, "content": post.content})

    return jsonify(valid_posts), 200


@app.route('/unsec-post/<int:id>', methods=['PUT'])
@jwt_required()
def unsecure_update_post(id):
    current_user_id = get_jwt_identity()
    data = request.get_json()
    new_content = data['content']

    # Obtener la publicación actual
    post = Post.query.get_or_404(id)

    # Evitamos verificar si el usuario actual es el autor de la publicación para permitir el ataque
    # Y comprobar si detectamos el tampering de los datos

    # El usuario malicioso calcularia solo un hash SHA256 del nuevo contenido
    new_content_hash = hashlib.sha256(new_content.encode()).hexdigest()

    # Actualizar el contenido y el hash
    post.content = new_content
    post.hash = new_content_hash

    db.session.commit()

    return jsonify({"message": "Post updated successfully"}), 200


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)