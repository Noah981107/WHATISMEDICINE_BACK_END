import cv2
import numpy as np
import requests
import matplotlib.pyplot as plt
import os

from enums import color_enum
from util import config_parser, file_name_generator
from service import s3_service


def validation(mask):
    mask = np.array(mask)
    for i in range(len(mask)):
        if mask[i].sum() > 65000:
            return True
    return False


def get_color_from_file(image_url):

    image_nparray = np.asarray(bytearray(requests.get(image_url).content), dtype=np.uint8)
    image = cv2.imdecode(image_nparray, cv2.IMREAD_COLOR)

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    lower_white = np.array([0, 0, 180])
    upper_white = np.array([30, 30, 255])
    lower_yellow = np.array([20, 120, 175])
    upper_yellow = np.array([30, 255, 255])
    lower_orange = np.array([9, 100, 200])
    upper_orange = np.array([20, 255, 255])
    lower_pink = np.array([145, 30, 96])
    upper_pink = np.array([178, 255, 255])
    lower_red = np.array([0, 100, 150])
    upper_red = np.array([7, 255, 255])
    lower_brown = np.array([7, 45, 100])
    upper_brown = np.array([15, 200, 204])
    lower_green = np.array([35, 80, 125])
    upper_green = np.array([82, 255, 230])
    lower_turquoise = np.array([83, 88, 110])
    upper_turquoise = np.array([90, 255, 229])
    lower_blue = np.array([90, 30, 140])
    upper_blue = np.array([125, 255, 255])
    lower_purple = np.array([126, 53, 100])
    upper_purple = np.array([146, 220, 255])
    lower_gray = np.array([0, 0, 50])
    upper_gray = np.array([110, 20, 200])

    mask_white = cv2.inRange(hsv, lower_white, upper_white)
    mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)
    mask_orange = cv2.inRange(hsv, lower_orange, upper_orange)
    mask_pink = cv2.inRange(hsv, lower_pink, upper_pink)
    mask_red = cv2.inRange(hsv, lower_red, upper_red)
    mask_brown = cv2.inRange(hsv, lower_brown, upper_brown)
    mask_green = cv2.inRange(hsv, lower_green, upper_green)
    mask_turquoise = cv2.inRange(hsv, lower_turquoise, upper_turquoise)
    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
    mask_purple = cv2.inRange(hsv, lower_purple, upper_purple)
    mask_gray = cv2.inRange(hsv, lower_gray, upper_gray)

    mask_imgs = {color_enum.colorEnum.WHITE.name: mask_white,
                 color_enum.colorEnum.YELLOW.name: mask_yellow,
                 color_enum.colorEnum.ORANGE.name: mask_orange,
                 color_enum.colorEnum.PINK.name: mask_pink,
                 color_enum.colorEnum.RED.name: mask_red,
                 color_enum.colorEnum.BROWN.name: mask_brown,
                 color_enum.colorEnum.GREEN.name: mask_green,
                 color_enum.colorEnum.TURQUOISE.name: mask_turquoise,
                 color_enum.colorEnum.BLUE.name: mask_blue,
                 color_enum.colorEnum.PURPLE.name: mask_purple,
                 color_enum.colorEnum.GRAY.name: mask_gray}

    is_detected = False
    color_result = ()

    for key, value in mask_imgs.items():
        if validation(value):
            for color_enum_color in color_enum.colorEnum:
                if key == color_enum_color.name:
                    is_detected = True

                    BASE_DIR = os.getcwd()
                    IMAGE_DIR = os.path.join(BASE_DIR, 'color')
                    detected_color_image_name = file_name_generator.make_detected_image_name()
                    file_path = os.path.join(IMAGE_DIR, detected_color_image_name)
                    plt.imshow(value)
                    plt.savefig(file_path)

                    with open(file_path, 'rb') as data:
                        uploaded_detected_color_image_url = s3_service.upload_detected_color_image(data, detected_color_image_name)

                    color_result = (uploaded_detected_color_image_url, color_enum_color.color_name, color_enum_color.code)

    if is_detected:
        return color_result
    else:
        not_detected_color_result = (
            'https://' + config_parser.get_s3_bucket_name() + '.s3.'
            + config_parser.get_s3_region_name() + '.amazonaws.com/' + config_parser.get_s3_template_folder_name() + '/'
            + 'no_result.jpg', '', ''
        )
        return not_detected_color_result
