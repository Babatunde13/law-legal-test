from app.utils.response_format import ResponseFormat
from . import categories_bp

@categories_bp.route('/', methods=['POST'])
def create_categories():
    return ResponseFormat(
        "successfully created new category",
        {},
        "ok"
    ).toObject()

@categories_bp.route('/')
def get_categories():
    return ResponseFormat(
        "successfully retrieved categories",
        {},
        "ok"
    ).toObject()

@categories_bp.route('/<id>')
def get_categorie(id):
    return ResponseFormat(
        "successfully retrieved category",
        {},
        "ok"
    ).toObject()

@categories_bp.route('/<id>', methods=['PUT'])
def update_categorie(id):
    return ResponseFormat(
        "successfully updated category",
        {},
        "ok"
    ).toObject()

@categories_bp.route('/<id>', methods=['DELETE'])
def delete_categorie(id):
    return ResponseFormat(
        "successfully deleted category",
        {},
        "ok"
    ).toObject()
