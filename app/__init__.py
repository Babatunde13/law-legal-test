from flask import Flask, request, jsonify, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import jwt

db = SQLAlchemy()
migrate = Migrate()

from app import models

def create_app(config=None):
    app = Flask(__name__)
    if config:
        app.config.from_object(config)
    db.init_app(app)
    migrate.init_app(app, db)

    from .users import users_bp
    app.register_blueprint(users_bp, url_prefix='/api/v1/users')

    from .products import products_bp
    app.register_blueprint(products_bp, url_prefix='/api/v1/products')

    from .categories import categories_bp
    app.register_blueprint(categories_bp, url_prefix='/api/v1/categories')

    return app