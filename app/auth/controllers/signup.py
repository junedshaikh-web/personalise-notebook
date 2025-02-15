from flask import request
from flask_restful import Resource
from app.exception import PGAPIException
from app.md.models import User
from app import db
from app.md.serde import UserSchema
from werkzeug.security import generate_password_hash

class SignUpView(Resource):
    def get(self):
        return {"signup": "successfully"}

    def post(self):
        data = request.get_json()

        existing_username = User.query.filter_by(username=data['username']).count()
        existing_email = User.query.filter_by(email=data['email']).count()
        if existing_username:
            raise PGAPIException({'username': 'username is already in use'})
        
        if existing_email:
            raise PGAPIException({'email': 'email is already in use'})
        
        if len(data['name']) < 2:
            raise PGAPIException({'name': 'first name must be greater than 1 character'})
        
        if data['password'] != data['password2']:
            raise PGAPIException({'password': 'passwords do not match'})
        
        if len(data['password']) < 7:
            raise PGAPIException({'password': 'password must be at least 7 characters'})
        
        user = User(name=data['name'],username=data['username'],email=data['email'],password=data['password'])
        
        db.session.add(user)
        db.session.commit()

        return UserSchema().dump(user), 201
