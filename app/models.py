from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app as app
from . import db

class User(db.Model):
    id=db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(30), index=True)
    email=db.Column(db.String(30), index=True, unique=True)
    password_hash=db.Column(db.String(108))
    is_confirmed=db.Column(db.Boolean, default=False)
    is_admin=db.Column(db.Boolean, default=False)
    payment=db.Column(db.Boolean, default=False)
    created_at=db.Column(db.DateTime, default=datetime.utcnow)
    updated_at=db.Column(db.DateTime, default=datetime.utcnow)
    categories=db.relationship('Categories', backref='users', lazy='dynamic')
    products=db.relationship('Products', backref='users', lazy='dynamic')
    transactions=db.relationship('Transactions', backref='users', lazy='dynamic')
   
    def set_password(self, password):
        self.password_hash=generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_token(self, expires_sec=1800):
        '''Generates a timed token to reset password'''
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod 
    def verify_reset_token(token):
        '''Verifies the timed token generated in the function above'''
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id=s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        '''This functions describes how the user model will be displayed'''
        return f"User('{self.email}')"
    
    def to_dict(self):
        return {
            'name': self.name, 'email': self.email, '_id': self.id,
            'is_confirmed': self.is_confirmed, 'is_admin': self.is_admin,
        }

products_categories = db.Table(
    'products_categories',
    db.Column('product_id', db.Integer, db.ForeignKey('product.id'), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('category.id'), primary_key=True)
)

class Categories(db.Model):
    id=db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(30), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        '''This functions describes how the user model will be displayed'''
        return f"User('{self.email}')"
    
    def to_dict(self):
        return {
            'name': self.name, 'products': self.self.products, '_id': self.id,
            'creator': self.user
        }

class Products(db.Model):
    id=db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(30), index=True)
    quantity = db.Column(db.Integer, default=1)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    categories = db.relationship('Categories', secondary=products_categories, lazy='subquery',
        backref=db.backref('products', lazy=True))

    def __repr__(self):
        '''This functions describes how the user model will be displayed'''
        return f"User('{self.name}')"
    
    def to_dict(self):
        return {
            'name': self.name, 'quantity': self.quantity, '_id': self.id,
            'categories': self.categories, 'creeator': self.user
        }

class Transactions(db.Model):
    id=db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(30), index=True)
    desctiption = db.Column(db.String(30), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)

    def __repr__(self):
        '''This functions describes how the user model will be displayed'''
        return f"Transactions('{self.name}')"
    
    def to_dict(self):
        return {
            'name': self.name, 'description': self.description, '_id': self.id,
            'user': self.user, 'product': self.product
        }
    