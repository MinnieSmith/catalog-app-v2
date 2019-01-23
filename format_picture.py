from PIL import Image
import numpy as np


def centered_crop_np(i, new_height, new_width):
    width = np.size(i, 1)
    height = np.size(i, 0)

    left = np.ceil((width - new_width) / 2.)
    top = np.ceil((height - new_height) / 2.)
    right = np.floor((width + new_width) / 2.)
    bottom = np.floor((height + new_height) / 2.)
    center_cropped_image = i[top:bottom, left:right]
    return center_cropped_image


def centered_crop_PIL(i, new_width, new_height):
    width = i.size[0]
    height = i.size[1]
    left = (width - new_width) / 2
    top = (height - new_height) / 2
    right = (width + new_width) / 2
    bottom = (height + new_height) / 2
    centered_crop_pil = i.crop((left, top, right, bottom))
    return centered_crop_pil


def resize_image(i, base_width):
    wpercent = (base_width / float(i.size[0]))
    hsize = int((float(i.size[1]) * float(wpercent)))
    resized_image = i.resize((base_width, hsize), Image.ANTIALIAS)
    return resized_image

