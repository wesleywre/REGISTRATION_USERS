import datetime
from app import db, ma
from flask_login import UserMixin


ACCESS = {
    'guest': 0,
    'user': 1,
    'admin': 2
}

#Definição da classe/tabela dos usuários e seus campos
class Users(UserMixin, db.Model):
    __tablename__ = 'user'
    id                  = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name          = db.Column(db.String(255), nullable=False)
    last_name           = db.Column(db.String(255), nullable=False)
    email               = db.Column(db.String(50), unique=True, nullable=False)
    email_confirmed     = db.Column(db.Boolean, default=False)
    user_name           = db.Column(db.String(255), unique=True, nullable=False)
    password_hash       = db.Column(db.String(155), nullable=False)
    security_stamp      = db.Column(db.String(255), default=None)
    access_failed_count = db.Column(db.SmallInteger)
    lockout_enabled     = db.Column(db.Boolean, default=False)
    lockout_end         = db.Column(db.DateTime, default=None)
    created_on          = db.Column(db.DateTime, default=datetime.datetime.now())
    access              = db.Column(db.Integer)
    
    def __init__(self, first_name, last_name, email, user_name, password_hash, security_stamp, access=ACCESS['guest']):
        self.first_name       = first_name
        self.last_name        = last_name
        self.email            = email
        self.user_name        = user_name
        self.password_hash    = password_hash
        self.security_stamp   = security_stamp
        self.access           = access
        
    def is_admin(self):
        return self.access == ACCESS['admin']

    def is_user(self):
        return self.access == ACCESS['user']

    def allowed(self, access_level):
        return self.access >= access_level
        
#Definindo o Schema do MArshmallow para facilitar a utilização do JSON
class UsersSchema(ma.Schema):
    class Meta:
        fields = ('id', 'first_name', 'last_name', 'email', 'email_confirmed', 'user_name', 'password_hash', 'security_stamp', 'access_failed_count', 'lockout_enabled', 'lockout_end', 'created_on', 'access')
        
        
user_schema  = UsersSchema()
users_schema = UsersSchema(many=True)