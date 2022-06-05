import cv2
import numpy as np
from rembg.bg import remove
import requests


def image_background_removal(image_url):

    image_nparray = np.asarray(bytearray(requests.get(image_url).content), dtype=np.uint8)
    image = cv2.imdecode(image_nparray, cv2.IMREAD_COLOR)

    output2 = remove(image)
    cv2.imwrite('output2.png', output2)

    return 'test'
