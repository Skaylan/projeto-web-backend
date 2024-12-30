import base64


def convert_base64_to_image(img_base64_string: str, image_uuid: str, save_path: str) -> None:
    """This function decode and convert a base64 string to a image file and save it to the given path.

    Args:
        img_base64_string (str): The base64 string you want to decode.
        image_uuid (str): A unique uuid to name the image file
        save_path (str): The path you want to save the image in.
    """

    img_data = base64.b64decode(img_base64_string)
    filename = f'{image_uuid}.png'  # I assume you have a way of picking unique filenames
    with open(f'{save_path}/{filename}', 'wb') as f:
        f.write(img_data)

def convert_image_to_base64(img_path: str, img_uuid: str) -> str:
    """This function convert a image file to a base64 string

    Args:
        img_path (str): the path to the image file
        img_uuid (str): uuid string

    Returns:
        str: Base64 string
    """

    with open(f'{img_path}//{img_uuid}.png', 'rb') as img_file:
        base64_string = base64.b64encode(img_file.read())
    return str(base64_string)[2:].replace("'", '')