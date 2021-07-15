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
        print(token)
        if not token: 
            return ResponseFormat(
                'You did not provide a token',
                None,
                "unauthorized"
            ).toObject(), 401
        try:
            data=jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            print(int(data['user_id']))
            current_user=models.User.query.get_or_404(int(data['user_id']))
            if current_user is None:
                return ResponseFormat(
                'Invalid token',
                None,
                "unauthorized"
            ).toObject(), 401
            print(current_user.active)
            if not current_user.active:
                return ResponseFormat(
                'Invalid user',
                None,
                "unauthorized"
            ).toObject(), 403
        except Exception as e:
            return ResponseFormat(
                'Something went wrong',
                None,
                "bad"
            ).toObject(), 500

        return f(current_user, *args, **kwargs)

    return decorated

def admin_required(f):
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
            ).toObject(), 401
        try:
            data=jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user: models.User = models.User.query.get_or_404(int(data['user_id']))
            if current_user is None:
                return ResponseFormat(
                    'Invalid token',
                    None,
                    "unauthorized"
                ).toObject(), 401
            if not current_user.is_admin:
                return ResponseFormat(
                    'Only admins are allowed to do that!',
                    None,
                    "Forbidden"
                ).toObject(), 403
        except Exception as e:
            return ResponseFormat(
                    'Something went wrong',
                    None,
                    "bad"
                ).toObject(), 500

        return f(current_user, *args, **kwargs)

    return decorated

from . import views