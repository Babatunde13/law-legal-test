from app.utils.response_format import ResponseFormat
from . import users_bp

@users_bp.route('/auth/signup', methods=['POST'])
def signup():
    return ResponseFormat(
        "Successfully created user",
        {},
        "ok"
    ).toObject()

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
