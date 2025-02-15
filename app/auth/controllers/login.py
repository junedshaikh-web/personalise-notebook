import datetime
from flask import abort, jsonify, make_response, request, session, current_app
from flask_restful import Resource
from app.md.models import User
from app import app
import jwt
from app.md.serde import UserSchema
from werkzeug.security import check_password_hash


class LoginView(Resource):
    def get(self):
        return {"login": "successful"}

    def post(self):
        data = request.get_json()  
        user = User.query.filter_by(username=data['username']).first()
        
        if not user or not user.verify_password(data["password"]):
            return make_response(jsonify({"error": "Invalid username or password"}), 401)

        session['user_id'] = user.id


        token = jwt.encode({'user_id': user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=5)},current_app.config['SECRET_KEY'],algorithm="HS256")

        return jsonify({"token": token})
