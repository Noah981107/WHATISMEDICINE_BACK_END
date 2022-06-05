import cv2
import numpy as np
from rembg.bg import remove
import requests

from util import file_name_generator
from service import s3_service


def image_background_removal(image_url):

    image_nparray = np.asarray(bytearray(requests.get(image_url).content), dtype=np.uint8)
    image = cv2.imdecode(image_nparray, cv2.IMREAD_COLOR)

    output = remove(image)
    image_name = file_name_generator.make_detected_image_name()
    file_path = 'background/' + image_name
    cv2.imwrite(file_path, output)

    with open(file_path, 'rb') as data:
        return s3_service.upload_background_removal_image(data, image_name)


