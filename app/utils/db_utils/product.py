from app.models import Categories, Products
from app import db

def create_product(product, user, categories=[]):
    product = Products(
        name=product['name'],
        description=product['description'],
        quantity=product.get('quantity', 1),
        price=product['price'],
        image_url=product['image_url'],
        user_id=user.id
    )
    db.session.add(product)
    db.session.commit()
    return product
    # for category in categories:
    #     product.categories.append(Categories.query.filter_by(id=category).first())
    # db.session.commit()
    