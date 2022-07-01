import random
import string

gen = string.ascii_letters + string.digits + string.ascii_uppercase
key = ''.join(random.choice(gen) for i in range(12))

DEBUG = True
SQLALCHEMY_DATABASE_URI = 'mysql://dbadminroda:!roda02!@rodadb-1.c5mkq9lio737.us-east-1.rds.amazonaws.com:3306/rodadevelopment'
SQLALCHEMY_TRACK_MODIFICATIONS = False
MAIL_SERVER='smtp.gmail.com'
MAIL_USERNAME='tech@rodaconveniencia.com.br'
MAIL_PASSWORD='9e%J<n8Y'
MAIL_PORT=465
MAIL_USE_SSL=True
MAIL_USE_TLS=False
SECRET_KEY = key

