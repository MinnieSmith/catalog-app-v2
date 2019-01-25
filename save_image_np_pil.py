from PIL import Image
import numpy as np
import os
import secrets
from format_picture import resize_image, centered_crop_np
from flask import Flask

app = Flask(__name__)


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    f_name, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    i = Image.open(form_picture)
    i = resize_image(i, 600)
    i = np.asarray(i)
    i = centered_crop_np(i, 300, 300)
    i = Image.fromarray(np.uint8(i))
    i.save(picture_path)
    return picture_fn
