from app import app
from flask import jsonify
from ..views import users, helper


@app.route('/send_email', methods=['GET', 'POST'])
def send_email():
    return users.send_email()

@app.route('/confirm_email/<token>')
def confirm_email(token):
    return users.confirm_email(token)

@app.route('/users', methods=['POST'])
def post_user():
    return users.post_user()

@app.route('/users/<id>', methods=['PUT'])
def update_user(id):
    return users.update_user(id)

@app.route('/users', methods=['GET'])
def get_users():
    return users.get_users()

@app.route('/users/<id>', methods=['GET'])
def get_user(id):
    return users.get_user(id)

@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    return users.delete_user(id)

@app.route('/auth', methods=['POST'])
def authenticate():
    return helper.auth()

@app.route('/', methods=['GET'])
@helper.token_required
def root(current_user):
    return jsonify({'message': f'User {current_user.user_name} autorizado'})