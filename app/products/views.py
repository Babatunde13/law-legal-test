from app.models import Products
from app.users import token_required, admin_required
from app import db
from . import products_bp
from app.utils.response_format import ResponseFormat

@products_bp.route('/', methods=['POST'])
@token_required
@admin_required
def create_products(current_user):
    return ResponseFormat(
        "Successfully create products",
        {},
        "ok"
    ).toObject()

@products_bp.route('/')
def get_products():
    products = Products.query.all()
    return ResponseFormat(
        "Successfully retrieved products",
        products,
        "ok"
    ).toObject()

@products_bp.route('/<id>')
def get_product(id):
    product = Products.query.get(id)
    if not product:
        return ResponseFormat(
            "Product NOt found",
            None,
            "bad"
        ).toObject(), 404
    return ResponseFormat(
        "Successfully retrieved product",
        product,
        "ok"
    ).toObject()

@products_bp.route('/<id>', methods=['PUT'])
@token_required
@admin_required
def update_product(id):
    product = Products.query.get(id)
    if not product:
        return ResponseFormat(
            "Product NOt found",
            None,
            "bad"
        ).toObject(), 404
    return ResponseFormat(
        "Successfully updated product",
        {},
        "ok"
    ).toObject()

@products_bp.route('/<id>', methods=['DELETE'])
@token_required
@admin_required
def delete_product(id):
    product = Products.query.get(id)
    if not product:
        return ResponseFormat(
            "Product NOt found",
            None,
            "bad"
        ).toObject(), 404
    db.session.delete(product)
    db.session.commit()
    return ResponseFormat(
        "Successfully deleted product",
        None,
        "ok"
    ).toObject()
