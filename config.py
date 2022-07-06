import random
import string

gen = string.ascii_letters + string.digits + string.ascii_uppercase
key = ''.join(random.choice(gen) for i in range(12))

DEBUG = True
SQLALCHEMY_DATABASE_URI = 'mysql://root:@localhost:3306/table'
SQLALCHEMY_TRACK_MODIFICATIONS = False
MAIL_SERVER='smtp.gmail.com'
MAIL_USERNAME='tech@rodaconveniencia.com.br'
MAIL_PASSWORD='dtqhbaqsyidfxcrb'
MAIL_PORT=465
MAIL_USE_SSL=True
MAIL_USE_TLS=False
SECRET_KEY = key

