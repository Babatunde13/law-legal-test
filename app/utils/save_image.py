from PIL import Image
import secrets, os
from flask import current_app as app

def save_pic(picture):
    file_name = secrets.token_hex(8) +os.path.splitext(picture.filename)[1]
    file_path = os.path.join(app.root_path, 'static/img', file_name)
    picture = Image.open(picture)
    picture.thumbnail((150, 150))
    picture.save(file_path)
    return file_name