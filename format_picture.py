from PIL import Image, ExifTags
import numpy as np
import functools


def image_transpose_exif(i):
    """
        Apply Image.transpose to ensure 0th row of pixels is at the visual
        top of the image, and 0th column is the visual left-hand side.
        Return the original image if unable to determine the orientation.

        As per CIPA DC-008-2012, the orientation field contains an integer,
        1 through 8. Other values are reserved.
    """

    exif_orientation_tag = 0x0112
    exif_transpose_sequences = [                   # Val  0th row  0th col
        [],                                        #  0    (reserved)
        [],                                        #  1   top      left
        [Image.FLIP_LEFT_RIGHT],                   #  2   top      right
        [Image.ROTATE_180],                        #  3   bottom   right
        [Image.FLIP_TOP_BOTTOM],                   #  4   bottom   left
        [Image.FLIP_LEFT_RIGHT, Image.ROTATE_90],  #  5   left     top
        [Image.ROTATE_270],                        #  6   right    top
        [Image.FLIP_TOP_BOTTOM, Image.ROTATE_90],  #  7   right    bottom
        [Image.ROTATE_90],                         #  8   left     bottom
    ]

    try:
        seq = exif_transpose_sequences[i._getexif()[exif_orientation_tag]]
    except Exception:
        return i
    else:
        return functools.reduce(type(i).transpose, seq, i)


def centered_crop_np(i, new_height, new_width):
    width = np.size(i, 1)
    height = np.size(i, 0)

    left = np.ceil((width - new_width) / 2.)
    top = np.ceil((height - new_height) / 2.)
    right = np.floor((width + new_width) / 2.)
    bottom = np.floor((height + new_height) / 2.)
    center_cropped_image = i[top:bottom, left:right]
    return center_cropped_image


def centered_crop_pil(i, new_width, new_height):
    width = i.size[0]
    height = i.size[1]
    left = (width - new_width) / 2
    top = (height - new_height) / 2
    right = (width + new_width) / 2
    bottom = (height + new_height) / 2
    centered_crop_image = i.crop((left, top, right, bottom))
    return centered_crop_image


def resize_image(i, base_width):
    wpercent = (base_width / float(i.size[0]))
    hsize = int((float(i.size[1]) * float(wpercent)))
    resized_image = i.resize((base_width, hsize), Image.ANTIALIAS)
    return resized_image


def format_image(i):
    i = image_transpose_exif(i)
    i = resize_image(i, 500)
    i = centered_crop_pil(i, 300, 300)
    return i
