from werkzeug.security import generate_password_hash
from app import db
from flask import request, jsonify
from ..models.users import Users, user_schema, users_schema
import uuid
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from app import Message, mail, url_for, login

def send_email():
    if request.method == 'GET':
        return '<form action="/send_email" method="POST"><input name="email"><input type="submit"></form>'

    email = request.form['email']
    user = Users.query.filter(Users.email == email).one()
    token = user.security_stamp

    msg = Message('Confirm Email', sender='tech@rodaconveniencia.com.br', recipients=[email])

    link = url_for('confirm_email', token=token, _external=True)

    msg.body = 'Your link is {}'.format(link)

    mail.send(msg)

    return '<h1>The email you entered is {}. The token is {}</h1>'.format(email, token)

def confirm_email(token):
    try:
        user = Users.query.filter(Users.security_stamp == token).one()
        if token == user.security_stamp:
            user.email_confirmed  = 1
            db.session.commit()
            return '<h1>The token works!</h1>'
    except:
        return '<h1>The token invalid!</h1>'
    

def registration_user():
    first_name       = request.json['first_name']
    last_name        = request.json['last_name']
    email            = request.json['email']
    user_name        = email
    password         = request.json['password']
    password_hash    = generate_password_hash(password)
    security_stamp   = str(uuid.uuid4())
    user             = Users(first_name, last_name, email, user_name, password_hash, security_stamp)
    
    try:
        db.session.add(user)
        db.session.commit()
        result = user_schema.dump(user)
        return jsonify({'message': 'successfully registered', 'data': result}), 201
    except:
        return jsonify({'message': 'unable to create', 'data': {}}), 500
    
    
def update_user(user, id):
    first_name       = request.json['first_name']
    last_name        = request.json['last_name']
    email            = request.json['email']
    password         = request.json['password']
    
    user = Users.query.get(id)
    
    if not user:
        return jsonify({'message': "user don't exist", 'data': {}}), 404
    
    password_hash    = generate_password_hash(password)
    
    try:
        user.first_name = first_name
        user.last_name  = last_name
        user.email      = email
        user.user_name  = email
        user.password   = password_hash
        db.session.commit()
        result = user_schema.dump(user)
        return jsonify({'message': 'successfully updated', 'data': result}), 201
    except:
        return jsonify({'message': 'unable to update', 'data': {}}), 500
    
def get_users(users):
    users = Users.query.all()
    if users:
        result = users_schema.dump(users)
        return jsonify({'message': 'successfully fetched', 'data': result})
    
    return jsonify({'message': 'nothing found', 'data': {}})

def get_user(user, id):
    user = Users.query.get(id)
    if user:
        result = user_schema.dump(user)
        return jsonify({'message': 'successfully fetched', 'data': result}), 201
    
    return jsonify({'message': "user don't exist", 'data': {}}), 404

def delete_user(user, id):
    user = Users.query.get(id)
    if not user:
        return jsonify({'message': "user don't exist", 'data': {}}), 404
    
    if user:
        try:
            db.session.delete(user)
            db.session.commit()
            result = user_schema.dump(user)
            return jsonify({'message': 'successfully deleted', 'data': result}), 200
        except:
            return jsonify({'message': 'unable to delete', 'data': {}}), 500
        
        
def user_by_username(user_name):
    try:
        return Users.query.filter(Users.user_name == user_name).one()
    except:
        return None
    
    
@login.user_loader
def load_user(id):
    return Users.query.get(int(id))