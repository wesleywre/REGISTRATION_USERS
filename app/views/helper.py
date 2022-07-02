
import datetime
from functools import wraps
from app import app
from flask import request, jsonify
from .users import user_by_username
import jwt
from werkzeug.security import check_password_hash

def auth():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return jsonify({'message': 'could not verify', 'WWW-Authenticate': 'Basic auth="Login Required"'}), 401
    
    user = user_by_username(auth.username)
    if not user:
        return jsonify({'message': 'user not found', 'data': {}}), 401
    
    if user and check_password_hash(user.password_hash, auth.password):
        token = jwt.encode({'username': user.user_name, 'exp': datetime.datetime.now() + datetime.timedelta(hours=1)}, app.config['SECRET_KEY'])
        
        return jsonify({'message': 'Validate successfully', 'token': token, 'exp': datetime.datetime.now() + datetime.timedelta(hours=1)})
    return jsonify({'message': 'could not verify', 'WWW-Authenticate': 'Basic auth="Login Required"'}), 401

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'message': 'token is missing', 'data': {}}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            print(data['username'])
            current_user = user_by_username(user_name=data['username'])
        except:
            return jsonify({'message': 'token is invalid or expired', 'data': {}}), 401
        return f(current_user, *args, **kwargs)
    return decorated