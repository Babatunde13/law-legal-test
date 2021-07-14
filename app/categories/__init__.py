from flask import Blueprint

cateories_bp = Blueprint('categories', __name__)

from . import views