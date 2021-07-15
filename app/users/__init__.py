from app.utils.response_format import ResponseFormat
import jwt
from flask import Blueprint, request, current_app, jsonify
from app import models

users_bp = Blueprint('users', __name__)

from functools import wraps


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(' ')[1]
        if not token: 
            return ResponseFormat(
                'You did not provide a token',
                None,
                "unauthorized"
            ), 401
        try:
            data=jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user=models.User.query.get_or_404(int(data['user_id']))
            if current_user is None:
                return ResponseFormat(
                'Invalid token',
                None,
                "unauthorized"
            ), 401
        except Exception as e:
            return ResponseFormat(
                'Something went wrong',
                None,
                "bad"
            ), 500

        return f(current_user, *args, **kwargs)

    return decorated

from . import views