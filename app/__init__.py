from flask import Flask, jsonify, request, url_for
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
ma = Marshmallow(app)
mail = Mail(app)


from .models import users
from .routes import routes
