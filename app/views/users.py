from werkzeug.security import generate_password_hash
from app import db
from flask import request, jsonify
from ..models.users import Users, user_schema, users_schema


def post_user():
    first_name       = request.json['first_name']
    last_name        = request.json['last_name']
    email            = request.json['email']
    user_name        = request.json['user_name']
    password         = request.json['password']
    password_hash    = generate_password_hash(password)
    user             = Users(first_name, last_name, email, user_name, password_hash)
    
    try:
        db.session.add(user)
        db.session.commit()
        result = user_schema.dump(user)
        return jsonify({'message': 'successfully registered', 'data': result}), 201
    except:
        return jsonify({'message': 'unable to create', 'data': {}}), 500
    
    
    