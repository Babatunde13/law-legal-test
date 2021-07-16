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
    try:
        for category_id in categories:
            print(type(category_id))
            category = Categories.query.get(int(category_id))
            if category:
                product.categories.append(category)
            else:
                return None
        db.session.commit()
        print(product.categories)
    except:
        return None
    return product
    