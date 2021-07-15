from app.models import Categories
from app.users import token_required, admin_required
from app.utils.response_format import ResponseFormat
from . import categories_bp
from app import db

@categories_bp.route('/', methods=['POST'])
@token_required
@admin_required
def create_categories():
    return ResponseFormat(
        "successfully created new category",
        {},
        "ok"
    ).toObject()

@categories_bp.route('/')
def get_categories():
    categories = Categories.query.all()
    
    return ResponseFormat(
        "Successfully retrieved Categories",
        categories,
        "ok"
    ).toObject()

@categories_bp.route('/<id>')
def get_category(id):
    category = Categories.query.get(id)
    if not category:
        return ResponseFormat(
            "Category Not found",
            None,
            "bad"
        ).toObject(), 404
    return ResponseFormat(
        "Successfully retrieved Category",
        category,
        "ok"
    ).toObject()

@categories_bp.route('/<id>', methods=['PUT'])
@token_required
@admin_required
def update_categorie(id):
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
@admin_required
def delete_categorie(id):
    category = Categories.query.get(id)
    if not category:
        return ResponseFormat(
            "Category Not found",
            None,
            "bad"
        ).toObject(), 404
    db.session.delete(category)
    db.session.commit()
    return ResponseFormat(
        "successfully deleted category",
        {},
        "ok"
    ).toObject()
