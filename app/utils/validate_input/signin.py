from typing import Dict
from app.utils.response_format import ResponseFormat
from app.utils import validate

def validate_sign_in_data(data: Dict[str, str]):
    if not data or not data.get('email') or not data.get('password'):
        return ResponseFormat(
            "email and password must be passed",
            None,
            "bad"
        ).toObject(), 400
    if not validate.validate_email(data['email']):
        return ResponseFormat(
            "Invalid email",
            None,
            "bad"
        ).toObject(), 400
    if not validate.validate_password(data['password']):
        return ResponseFormat(
            "Invalid password, Password must be between 8 and 20 and must contain a character",
            None,
            "bad"
        ).toObject(), 400
    