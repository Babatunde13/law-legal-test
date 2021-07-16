from flask import request
from app.models import Categories
from app.users import token_required
from app.utils.response_format import ResponseFormat
from . import categories_bp
from app import db

@categories_bp.route('/', methods=['POST'])
@token_required
def create_categories(current_user):
    if not current_user.is_admin:
        return ResponseFormat(
            'Invalid user',
            None,
            "unauthorized"
        ).toObject(), 403
    data = request.get_json()
    if not data['name']:
        return ResponseFormat(
        "Name of category must be passed",
        None,
        "ok"
    ).toObject()
    try:
        category = Categories(name=data['name'], user_id=current_user.id)
        db.session.add(category)
        db.session.commit()
        return ResponseFormat(
            "successfully created new category",
            category.to_dict(),
            "ok"
        ).toObject(), 201
    except Exception as e:
        return ResponseFormat(
            "Error creating `category` could be that the category exist before",
            None,
            "bad"
        ).toObject(), 400

@categories_bp.route('/')
def get_categories():
    categories = Categories.query.filter_by().all()
    categories = [
        category.to_dict() for category in categories
    ]
    return ResponseFormat(
        "Successfully retrieved categories",
        categories,
        "ok"
    ).toObject()

@categories_bp.route('/<id>')
def get_category(id):
    category = Categories.query.filter_by(id=id).first()
    if not category:
        return ResponseFormat(
            "Category Not found",
            None,
            "bad"
        ).toObject(), 404
    return ResponseFormat(
        "Successfully retrieved Category",
        category.to_dict(),
        "ok"
    ).toObject()

@categories_bp.route('/<id>', methods=['PUT'])
@token_required
def update_category(current_user, id):
    if not current_user.is_admin:
        return ResponseFormat(
            'Invalid user',
            None,
            "unauthorized"
        ).toObject(), 403
    category = Categories.query.get(id)
    if not category:
        return ResponseFormat(
            "Category Not found",
            None,
            "bad"
        ).toObject(), 404
    data = request.get_json()
    try:
        if data:
            category.name = data.get('name', category.name)
            db.session.commit()
        return ResponseFormat(
            "successfully updated category",
            category.to_dict(),
            "ok"
        ).toObject()
    except Exception as e:
        return ResponseFormat(
            str(e),
            None,
            "bad"
        ).toObject()


@categories_bp.route('/<id>', methods=['DELETE'])
@token_required
def delete_category(current_user, id):
    if not current_user.is_admin:
        return ResponseFormat(
            'Invalid user',
            None,
            "unauthorized"
        ).toObject(), 403
    category = Categories.query.get(id)
    if not category:
        return ResponseFormat(
            "Category Not found",
            None,
            "bad"
        ).toObject(), 404
    category.active=False
    db.session.delete(category)
    db.session.commit()
    return ResponseFormat(
        "successfully deleted category",
        None,
        "ok"
    ).toObject()
