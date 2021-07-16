from os import abort
from flask import request
from app.utils.validate_input.create_products import validate_product
from app.utils.response_format import ResponseFormat
from app.utils.db_utils import product
from app.models import Products
from app.users import token_required
from app import db
from . import products_bp

@products_bp.route('/', methods=['POST'])
@token_required
def create_product(current_user):
    if not current_user.is_admin:
        abort(403)
    data = request.get_json()
    # validate input
    if validate_product(data):
        return validate_product(data)
    # upload image to an image server and store the url
    data['image_url']=data['image']
    # create product
    new_product=product.create_product(data, current_user, categories=data['category_ids'])
    if new_product:
        return ResponseFormat(
            "Successfully create product",
            new_product.to_dict(),
            "ok"
        ).toObject(), 201
    return ResponseFormat(
            "Error creating product, did you pass a valid category id?",
            data['category_ids'],
            "bad"
        ).toObject(), 400

@products_bp.route('/')
def get_products():
    products = Products.query.filter_by(active=True).all()
    products = [
        product.to_dict() for product in products
    ]
    return ResponseFormat(
        "Successfully retrieved products",
        products,
        "ok"
    ).toObject()

@products_bp.route('/<id>')
def get_product(id):
    product = Products.query.filter_by(id=id, active=True).first()
    if not product:
        return ResponseFormat(
            "Product NOt found",
            None,
            "bad"
        ).toObject(), 404
    return ResponseFormat(
        "Successfully retrieved product",
        product.to_dict(),
        "ok"
    ).toObject()

@products_bp.route('/<id>', methods=['PUT'])
@token_required
def update_product(current_user, id):
    if not current_user.is_admin:
        abort(403)
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
def delete_product(current_user, id):
    if not current_user.is_admin:
        abort(403)
    product = Products.query.get(id)
    if not product:
        return ResponseFormat(
            "Product NOt found",
            None,
            "bad"
        ).toObject(), 404
    product.active=False
    db.session.commit()
    return ResponseFormat(
        "Successfully deleted product",
        None,
        "ok"
    ).toObject()
