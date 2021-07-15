from typing import Dict, Union
from app.utils.response_format import ResponseFormat

def validate_product(data: Dict[str, Union[str,int]]):
    # validate name, description, image_url, price, quantity
    if not data or not data['name'] or not data['image'] \
        or not data['description'] or not data['price']:
        return ResponseFormat(
            "name, image, description and price must be passed",
            None,
            "bad"
        ).toObject(), 400
    if type(data['price']) != int  or data['price'] < 1:
        return ResponseFormat(
            "Price must be an integer and should be greater than #1",
            None,
            "bad"
        ).toObject(), 400