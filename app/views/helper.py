
from datetime import datetime, timedelta
from functools import wraps
from app import app
from flask import request, jsonify
from .users import user_by_username
import jwt
from werkzeug.security import check_password_hash
from flask_login import current_user, login_user, logout_user

def login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return jsonify({'message': 'could not verify', 'WWW-Authenticate': 'Basic auth="Login Required"'}), 401
    
    user = user_by_username(auth.username)
    if not user:
        return jsonify({'message': 'user not found', 'data': {}}), 401
    
    if user and check_password_hash(user.password_hash, auth.password):
        if user.email_confirmed == 0:
            return jsonify({'message': 'Please confirm your email to enter.'}), 401
        login_user(user)
        token = jwt.encode({'username': user.user_name, 'exp': datetime.utcnow() + timedelta(minutes=20)}, app.config['SECRET_KEY'], algorithm="HS256")
        return jsonify({'message': 'Validate successfully', 'token': token, 'exp': datetime.utcnow() + timedelta(hours=1)})
    return jsonify({'message': 'could not verify', 'WWW-Authenticate': 'Basic auth="Login Required"'}), 401

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({'message': 'token is missing', 'data': {}}), 401
        try:
            token = token.split(' ')[1]
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms="HS256")
            current_user = user_by_username(user_name=data['username'])
        except:
            return jsonify({'message': 'token is invalid or expired', 'data': {}}), 401
        return f(current_user, *args, **kwargs)
    return decorated

def requires_access_level(access_level):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated: #the user is not logged in
                return jsonify({'message': 'User is not logged in'}), 401

            if not current_user.allowed(access_level):
                return jsonify({'message': 'You do not have access to this resource.'}), 401
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def logout(current_user):
    if current_user.is_authenticated:
        logout_user()
        return jsonify({'message': f'{current_user.user_name} logout'}), 200
    return jsonify({'message': 'User is not logged in'}), 401
    
