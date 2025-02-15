from app import db
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash,check_password_hash

class Note(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True),default=func.now())
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))

class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(150))
    username = db.Column(db.String(150))
    email = db.Column(db.String(150),unique=True)
    _password = db.Column(db.String(150))
    notes = db.relationship('Note')

    @property
    def password(self):
        raise AttributeError("cannot read password")
    
    @password.setter
    def password(self,password):
        self._password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self._password, password)
    
    