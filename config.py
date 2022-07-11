import random
import string
import configparser
import os

# Armazena a localização atual do arquivo
basedir = os.path.dirname(os.path.realpath(__file__))

# Ler as configurações do banco de um arquivo
config = configparser.ConfigParser()
config.read(f'{basedir}/config.ini')

user     = config['DATABASE']['user']
passwd   = config['DATABASE']['pass']
database = config['DATABASE']['base']
host     = config['DATABASE']['host']
port     = int(config['DATABASE']['port'])

email_server   = config['EMAIL']['email_server']
email_username = config['EMAIL']['email_username']
email_pass     = config['EMAIL']['email_pass']
email_port     = config['EMAIL']['email_port']


gen = string.ascii_letters + string.digits + string.ascii_uppercase
key = ''.join(random.choice(gen) for i in range(12))

DEBUG = True
SQLALCHEMY_DATABASE_URI = f'mysql://{user}:{passwd}@{host}:{port}/{database}'
SQLALCHEMY_TRACK_MODIFICATIONS = False
MAIL_SERVER=f'{email_server}'
MAIL_USERNAME=f'{email_username}'
MAIL_PASSWORD=f'{email_pass}'
MAIL_PORT=f'{email_port}'
MAIL_USE_SSL=True
MAIL_USE_TLS=False
SECRET_KEY = key

