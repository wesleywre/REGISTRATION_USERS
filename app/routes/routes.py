from app import app
from flask import jsonify
from ..views import users, helper

ACCESS = {
    'guest': 0,
    'user': 1,
    'admin': 2
}


@app.route('/v1', methods=['GET'])
@helper.token_required
def root(current_user):
    return jsonify({'message': f'User {current_user.user_name} autorizado'})

@app.route('/v1/authenticate', methods=['POST'])
def authenticate():
    return helper.auth()

@app.route('/v1/users', methods=['GET'])
@helper.token_required
@helper.requires_access_level(ACCESS['guest'])
def get_users(current_user):
    return users.get_users(current_user)

@app.route('/v1/users/<id>', methods=['GET'])
@helper.token_required
@helper.requires_access_level(ACCESS['guest'])
def get_user(current_user, id):
    return users.get_user(current_user, id)

@app.route('/v1/users', methods=['POST'])
@helper.token_required
def post_user(current_user):
    return users.post_user(current_user)

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