import easyocr
import cv2
import matplotlib.pyplot as plt
import matplotlib.image as img
import os

from service import s3_service
from util import file_name_generator, config_parser


def get_text_from_file(image_url):
    reader = easyocr.Reader(['ko', 'en'])
    result = reader.readtext(image_url)
    top_left = tuple(result[0][0][0])
    bottom_right = tuple(result[0][0][2])
    text = result[0][1]
    font = cv2.FONT_HERSHEY_SIMPLEX

    ndarray = img.imread(image_url)
    ndarray = cv2.rectangle(ndarray, top_left, bottom_right, (0, 255, 0), 3)
    ndarray = cv2.putText(ndarray, text, top_left, font, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

    BASE_DIR = os.getcwd()
    IMAGE_DIR = os.path.join(BASE_DIR, 'ocr')
    detected_color_image_name = file_name_generator.make_detected_image_name()
    file_path = os.path.join(IMAGE_DIR, detected_color_image_name)
    plt.imshow(ndarray)
    plt.savefig(file_path)

    with open(file_path, 'rb') as data:
        uploaded_detected_color_image_url = s3_service.upload_detected_ocr_image(data, detected_color_image_name)

    spacer = 100
    detected_ocr_result = []
    ocr_result = ()

    for detection in result:
        text = detection[1]
        if text not in detected_ocr_result:
            detected_ocr_result.append(text)
        spacer += 15

    if len(detected_ocr_result) == 0:
        not_detected_ocr_result = (
            'https://' + config_parser.get_s3_bucket_name() + '.s3.'
            + config_parser.get_s3_region_name() + '.amazonaws.com/' + config_parser.get_s3_template_folder_name() + '/'
            + 'no_result.jpg', ''
        )
        return not_detected_ocr_result
    else:
        txt = ' '.join(detected_ocr_result)
        ocr_result = (uploaded_detected_color_image_url, txt)
        return ocr_result
