from flask import Flask, request, jsonify, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import jwt
from werkzeug.utils import redirect
from app.utils.response_format import ResponseFormat

db = SQLAlchemy()
migrate = Migrate()

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

    @app.route('/')
    def docs():
        return redirect('https://documenter.getpostman.com/view/11853513/TzmBEuBu')

    @app.route('/api/v1/upload_image', methods=['POST'])
    def upload_image():
        data = request.files
        print(data)
        return ResponseFormat(
            "successfully uploaded image",
            None,
            "ok"
        ).toObject(), 201

    @app.errorhandler(403)
    def forbidden(error):
        return ResponseFormat(
            'Invalid user',
            None,
            "forbidden"
        ).toObject(), 403

    @app.errorhandler(404)
    def page_not_found(error):
        return ResponseFormat(
            'Resource not found',
            None,
            "not found"
        ), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return ResponseFormat(
            'SOmethign went wrong',
            None,
            "bad"
        ).toObject(), 500

    @app.errorhandler(405)
    def method_not_found(error):
        return ResponseFormat(
            'That HTTP verb isn\'t allowed for that request',
            None,
            "bad"
        ).toObject(), 405

    return app