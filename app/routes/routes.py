from app import app
from flask import jsonify
from ..views import users, helper

ACCESS = {
    'user': 0,
    'admin': 1
}


@app.route('/v1', methods=['GET'])
@helper.token_required
def root(current_user):
    return jsonify({'message': f'User {current_user.user_name} autorizado'})

@app.route('/v1/login', methods=['POST'])
def authenticate():
    return helper.login()

@app.route('/v1/users', methods=['GET'])
@helper.token_required
@helper.requires_access_level(ACCESS['user'])
def get_users(current_user):
    return users.get_users(current_user)

@app.route('/v1/users/<id>', methods=['GET'])
@helper.token_required
@helper.requires_access_level(ACCESS['user'])
def get_user(current_user, id):
    return users.get_user(current_user, id)

@app.route('/v1/registration', methods=['POST'])
def registration_user():
    return users.registration_user()

@app.route('/v1/users/<id>', methods=['DELETE'])
@helper.token_required
def delete_user(current_user, id):
    return users.delete_user(current_user, id)

@app.route('/v1/users/<id>', methods=['PUT'])
@helper.token_required
def update_user(current_user, id):
    return users.update_user(current_user, id)

@app.route('/v1/auth', methods=['POST'])
def auth():
    pass

@app.route('/send_email', methods=['GET', 'POST'])
def send_email():
    return users.send_email()

@app.route('/confirm_email/<token>')
def confirm_email(token):
    return users.confirm_email(token)

@app.route('/v1/logout', methods=['POST'])
@helper.token_required
def logout(current_user):
    return helper.logout(current_user)