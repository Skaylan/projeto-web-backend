import base64
import os
import imghdr

def convert_base64_to_image(img_base64_string: str, image_uuid: str, save_path: str) -> None:
    """This function decodes and converts a base64 string to an image file and saves it to the given path.

    Args:
        img_base64_string (str): The base64 string you want to decode.
        image_uuid (str): A unique uuid to name the image file.
        save_path (str): The path where you want to save the image.
    """
    try:
        if img_base64_string.startswith("data:image/png;base64,"):
            img_base64_string = img_base64_string.split(",", 1)[1]
            file_extension = 'png'
        elif img_base64_string.startswith("data:image/jpeg;base64,"):
            img_base64_string = img_base64_string.split(",", 1)[1]
            file_extension = 'jpeg'
        else:
            raise ValueError("Unsupported image format")

        img_data = base64.b64decode(img_base64_string)

        filename = f'{image_uuid}.{file_extension}'
        with open(f'{save_path}/{filename}', 'wb') as f:
            f.write(img_data)

    except base64.binascii.Error as e:
        raise ValueError("Invalid Base64 string") from e


def convert_image_to_base64(img_path: str, img_uuid: str) -> str:
    """This function converts an image file to a base64 string

    Args:
        img_path (str): the path to the image file
        img_uuid (str): uuid string

    Returns:
        str: Base64 string
    """
    img_file_path = f'{img_path}//{img_uuid}.png'
    if not os.path.exists(img_file_path):
        img_file_path = f'{img_path}//{img_uuid}.jpeg'
        if not os.path.exists(img_file_path):
            raise FileNotFoundError(f"Image not found: {img_uuid}.png or {img_uuid}.jpeg")

    with open(img_file_path, 'rb') as img_file:
        base64_string = str(base64.b64encode(img_file.read()))
        base64_string = base64_string.replace('dataimage/jpegbase64', "")

    return str(base64_string)[2:].replace("'", '')