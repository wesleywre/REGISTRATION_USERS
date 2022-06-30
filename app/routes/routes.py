from app import app
from flask import jsonify
from ..views import users


@app.route('/', methods=['GET'])
def root():
    return jsonify({'message': 'Hello, world!'})

@app.route('/users', methods=['POST'])
def post_user():
    return users.post_user()