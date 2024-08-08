from PIL import Image

def resize_image(image_path, target_width, target_height):
    with Image.open(image_path) as im:
        im_resized = im.resize((target_width, target_height))
    return im_resized