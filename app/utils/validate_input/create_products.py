from typing import Dict, Union
from app.utils.response_format import ResponseFormat

def validate_product(data: Dict[str, Union[str,int]]):
    # validate name, description, image_url, price, quantity
    if not data or not data.get('name', None) or not data.get('image', None) \
        or not data.get('description', None) or not data.get('price', None):
        return ResponseFormat(
            "name, image, description and price must be passed",
            None,
            "bad"
        ).toObject(), 400
    try:
        data['price'] = int(data['price'])
        if data['price'] < 1:
            return ResponseFormat(
                "Price must be an integer and should be greater than #1",
                None,
                "bad"
            ).toObject(), 400
    except:
        return ResponseFormat(
                "Price must be an integer and should be greater than #1",
                None,
                "bad"
            ).toObject(), 400