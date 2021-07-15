from app.models import User
from app.utils.validate_input.signup import validate_sign_up_data
from flask import request
from app.utils.response_format import ResponseFormat
from . import users_bp
from app.utils import validate
from app.utils.db_utils import auth
from app import db

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
            data['email'], 
            data['email'], 
            data['password']
        )
        db.session.add(new_user)
        db.session.commit()
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
        return ResponseFormat(
                "Something went wrong!",
                None,
                "bad"
            ).toObject(), 500 

@users_bp.route('/auth/login', methods=['POST'])
def login():
    return ResponseFormat(
        "Successfully fetched auth token",
        {},
        "ok"
    ).toObject()

@users_bp.route('/')
def get_current_user():
    return ResponseFormat(
        "Successfully retrieved user profile",
        {},
        "ok"
    )

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
