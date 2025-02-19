from functools import wraps
from app import app
from flask import jsonify,request,session
import jwt

from app.md.models import User

def token_required(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-acces-token']

        if not token:
            return jsonify({'message':'token is missing!'})
        try:
            data = jwt.decode(token,app.config['SECRET_KEY'],algorithms=["HS256"],options=None)
            current_user=User.query.filter_by(id=data["user_id"]).first()
            if current_user.id != session["user_id"]:
                return jsonify({"message":"token is invalid!"})
        except:
            return jsonify({"message":"token is invalid"})
        
        return f(current_user)
    
    
    return decorated