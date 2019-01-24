import os
import secrets

from PIL import Image
from flask import Flask
from format_picture import format_image

app = Flask(__name__)


def save_profile_picture(form_picture):
    random_hex = secrets.token_hex(8)
    f_name, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    i = Image.open(form_picture)
    i = format_image(i)
    i.save(picture_path)
    return picture_fn
