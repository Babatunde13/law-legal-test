from app.models import User
from app.utils.validate_input.signup import validate_sign_up_data
from app.utils.validate_input.signin import validate_sign_in_data
from flask import request, current_app as app
from app.utils.response_format import ResponseFormat
from . import token_required, users_bp
from app.utils import validate
from app.utils.db_utils import auth
import jwt

@users_bp.route('/auth/signup', methods=['POST'])
def signup():
    try:
        data = request.get_json()
        print(data)
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
        print(new_user)
        if new_user:
            return ResponseFormat(
                "Successfully created user",
                new_user,
                "ok"
            ).toObject()
        return ResponseFormat(
                "Error creating account, try again!",
                new_user,
                "ok"
            ).toObject()
    except Exception as e:
        print(e)
        return ResponseFormat(
                "Something went wrong!",
                None,
                "bad"
            ).toObject(), 500 

@users_bp.route('/auth/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        print(data)
        # validate input
        if validate_sign_in_data(data):
            return validate_sign_in_data(data)

        user = auth.signin(
            data['email'], 
            data['password']
        )
        if user:
            try:
                print(user)
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
                "Error fetching auth token!",
                user,
                "ok"
            ).toObject()
    except Exception as e:
        print(e)
        return ResponseFormat(
                "Something went wrong!",
                None,
                "bad"
            ).toObject(), 500

@users_bp.route('/')
@token_required
def get_current_user(current_user: User):
    print(current_user.to_dict())
    return ResponseFormat(
        "Successfully retrieved user profile",
        current_user.to_dict(),
        "ok"
    ).toObject()

@users_bp.route('/<id>')
def profile(id):
    return ResponseFormat(
        "Successfully retrieved user profile",
        {},
        "ok"
    ).toObject()

@users_bp.route('/<id>', methods=['PUT'])
def update_profile(id):
    return ResponseFormat(
        "Successfully updated user profile",
        {},
        "ok"
    ).toObject()
