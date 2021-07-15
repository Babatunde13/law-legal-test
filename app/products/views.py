from . import products_bp
from app.utils.response_format import ResponseFormat

@products_bp.route('/', methods=['POST'])
def create_products():
    return ResponseFormat(
        "Successfully create products",
        {},
        "ok"
    ).toObject()

@products_bp.route('/')
def get_products():
    return ResponseFormat(
        "Successfully retrieved products",
        {},
        "ok"
    ).toObject()

@products_bp.route('/<id>')
def get_product(id):
    return ResponseFormat(
        "Successfully retrieved product",
        {},
        "ok"
    ).toObject()

@products_bp.route('/<id>', methods=['PUT'])
def update_product(id):
    return ResponseFormat(
        "Successfully updated product",
        {},
        "ok"
    ).toObject()

@products_bp.route('/<id>', methods=['DELETE'])
def delete_product(id):
    return ResponseFormat(
        "Successfully deleted product",
        {},
        "ok"
    ).toObject()
