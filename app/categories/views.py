from app.models import Categories
from app.users import token_required, admin_required
from app.utils.response_format import ResponseFormat
from . import categories_bp
from app import db

@categories_bp.route('/', methods=['POST'])
@token_required
def create_categories(current_user):
    if not current_user.active:
        return ResponseFormat(
            'Invalid user',
            None,
            "unauthorized"
        ).toObject(), 403
    return ResponseFormat(
        "successfully created new category",
        {},
        "ok"
    ).toObject()

@categories_bp.route('/')
def get_categories():
    categories = Categories.query.filter_by(active=True).all()
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
    category = Categories.query.filter_by(id=id, active=True).first()
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
def update_categorie(current_user, id):
    if not current_user.active:
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
    db.session.commit()
    return ResponseFormat(
        "successfully updated category",
        {},
        "ok"
    ).toObject()

@categories_bp.route('/<id>', methods=['DELETE'])
@token_required
def delete_categorie(current_user, id):
    if not current_user.active:
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
    db.session.commit()
    return ResponseFormat(
        "successfully deleted category",
        {},
        "ok"
    ).toObject()
