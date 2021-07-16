from flask import request, current_app as app
import jwt
from app.utils.validate_input.signup import validate_sign_up_data
from app.utils.validate_input.signin import validate_sign_in_data
from app.utils.response_format import ResponseFormat
from app.utils.db_utils import auth
from app.models import User
from app import db
from . import token_required, users_bp
from app import users

@users_bp.route('/auth/signup', methods=['POST'])
def signup():
    try:
        data = request.get_json()
        # validate input
        if validate_sign_up_data(data):
            return validate_sign_up_data(data)

        user = User.query.filter_by(email=data['email']).first()
        if user:
            return ResponseFormat(
                "Email chosen",
                None,
                "ok"
            ).toObject(), 400
        new_user = auth.signup(
            data['name'], 
            data['email'], 
            data['password']
        )
        if new_user:
            return ResponseFormat(
                "Successfully created user",
                new_user,
                "ok"
            ).toObject(), 201
        return ResponseFormat(
                "Error creating account, try again!",
                new_user,
                "ok"
            ).toObject()
    except Exception as e:
        return ResponseFormat(
                "Something went wrong!",
                None,
                "bad"
            ).toObject(), 500 

@users_bp.route('/auth/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        # validate input
        if validate_sign_in_data(data):
            return validate_sign_in_data(data)

        user = auth.signin(
            data['email'], 
            data['password']
        )
        if user:
            try:
                user['token'] = jwt.encode(
                    {'user_id': str(user['_id'])},
                    app.config['SECRET_KEY']
                )
                return ResponseFormat(
                "Successfully fetched auth token",
                user,
                "ok"
            ).toObject()
            except Exception as e:
                return {
                    'error': 'Something went wrong',
                    'message': str(e)
                }, 500
        return ResponseFormat(
                "Error fetching auth token!, invalid email or password",
                user,
                "ok"
            ).toObject(), 400
    except Exception as e:
        return ResponseFormat(
                "Something went wrong!",
                None,
                "bad"
            ).toObject(), 500

@users_bp.route('/')
@token_required
def get_current_user(current_user: User):
    return ResponseFormat(
        "Successfully retrieved user profile",
        current_user.to_dict(),
        "ok"
    ).toObject()

@users_bp.route('/<id>')
def profile(id: str):
    user: User = User.query.get(id)
    if user:
        return ResponseFormat(
            "Successfully retrieved user profile",
            user.to_dict(),
            "ok"
        ).toObject()
    return ResponseFormat(
            "User not found",
            None,
            "bad"
        ).toObject(), 404

@users_bp.route('/', methods=['PUT'])
@token_required
def update_profile(current_user):
    data = request.get_json()
    user: User = User.query.get(current_user.id)
    if data['name']:
        user.name=data['name']
    db.session.commit()
    return ResponseFormat(
        "Successfully updated user profile",
        user.to_dict(),
        "ok"
    ).toObject()

@users_bp.route('/become_admin', methods=['POST'])
@token_required
def become_admin(current_user: User):
    user: User = User.query.get(current_user.to_dict()['_id'])
    user.is_admin=True
    db.session.commit()
    return ResponseFormat(
        "Successfully updated user profile",
        user.to_dict(),
        "ok"
    ).toObject()
