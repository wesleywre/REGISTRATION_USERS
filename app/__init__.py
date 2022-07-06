from flask import Flask, jsonify, request, url_for
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from flask_login import LoginManager


app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
ma = Marshmallow(app)
mail = Mail(app)
login = LoginManager(app)
login.login_view = 'login'
login.login_message_category = 'danger'

from .models import users
from .views import users, helper
from .routes import routes
