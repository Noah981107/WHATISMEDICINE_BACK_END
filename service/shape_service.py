import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
import requests

from enums import shape_enum
from util import file_name_generator, config_parser
from service import s3_service


def convex(image_url):
    image_nparray = np.asarray(bytearray(requests.get(image_url).content), dtype=np.uint8)
    image = cv2.imdecode(image_nparray, cv2.IMREAD_COLOR)

    imgray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, thr = cv2.threshold(imgray, 127, 255, 0)
    contours, _ = cv2.findContours(thr, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    cnt = contours[0]
    x, y, w, h = cv2.boundingRect(cnt)
    rect = cv2.minAreaRect(cnt)
    box = cv2.boxPoints(rect)
    box = np.int0(box)

    cv2.drawContours(image, [box], 0, (0, 255, 0), 3)

    return rect[1][0] / rect[1][1]


def get_shape_from_file(image_url):
    image_nparray = np.asarray(bytearray(requests.get(image_url).content), dtype=np.uint8)
    image = cv2.imdecode(image_nparray, cv2.IMREAD_COLOR)
    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    img_gray = cv2.threshold(img_gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)

    img_gray = cv2.bitwise_not(img_gray[1])
    img_gray_blur = cv2.GaussianBlur(img_gray, (21, 21), 0)

    img_gray_blur = cv2.dilate(img_gray_blur, (9, 9), cv2.CV_8UC1)
    img_gray_blur = cv2.dilate(img_gray_blur, (9, 9), cv2.CV_8UC1)
    img_gray_blur = cv2.dilate(img_gray_blur, (9, 9), cv2.CV_8UC1)
    img_gray_blur = cv2.dilate(img_gray_blur, (9, 9), cv2.CV_8UC1)
    img_gray_blur = cv2.dilate(img_gray_blur, (9, 9), cv2.CV_8UC1)

    img_gray_blur = cv2.erode(img_gray_blur, (9, 9), cv2.CV_8UC1)
    img_gray_blur = cv2.erode(img_gray_blur, (9, 9), cv2.CV_8UC1)
    img_gray_blur = cv2.erode(img_gray_blur, (9, 9), cv2.CV_8UC1)
    img_gray_blur = cv2.erode(img_gray_blur, (9, 9), cv2.CV_8UC1)
    img_gray_blur = cv2.erode(img_gray_blur, (9, 9), cv2.CV_8UC1)

    contours, _ = cv2.findContours(img_gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    for cont in contours:
        # approxPolyDP(curve, epsilon, closed, approxCurve=None)
        # curve: 외곽선좌표(contour), epsilon: 극사화정밀도
        # closed: True 폐곡선, approxCurve: 극사화된 곡선의 좌표

        # arcLength(cuve, closed)
        # closed: True(폐곡선)
        # retval: 외곽선 길이(폐곡선이라면 둘레)
        approx = cv2.approxPolyDP(cont, cv2.arcLength(cont, True) * 0.02, True)
        vtc = len(approx)

        result = ''

        if vtc >= 7:
            circle_contours, _ = cv2.findContours(img_gray_blur, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

            for i in range(0, len(circle_contours)):
                length = cv2.arcLength(circle_contours[0], True)

            for contour in circle_contours:
                cv2.drawContours(img_gray_blur, [contour], -1, (255, 0, 255), 2)

            circles = cv2.HoughCircles(img_gray_blur, cv2.HOUGH_GRADIENT, 1, img_gray_blur.shape[0] / 20, param1=8,
                                       param2=13, minRadius=0, maxRadius=int(length / 15))

            if circles is None:
                result = shape_enum.shapeEnum.CIRCLE.name
            elif convex(image_url) > 1.3 or convex(image_url) < 0.7:
                result = shape_enum.shapeEnum.ELLIPSE.name
            else:
                angle = circles.shape[1]
                if angle == 1:
                    result = shape_enum.shapeEnum.CIRCLE.name
                elif angle == 2:
                    result = shape_enum.shapeEnum.ELLIPSE.name
                elif angle == 3:
                    result = shape_enum.shapeEnum.TRIANGLE.name
                elif angle == 4:
                    result = shape_enum.shapeEnum.SQUARE.name
                elif angle == 5:
                    result = shape_enum.shapeEnum.PENTAGON.name
                elif angle == 6:
                    result = shape_enum.shapeEnum.HEXAGON.name
                elif angle == 8:
                    result = shape_enum.shapeEnum.OCTAGON.name
        else:
            if vtc == 3:
                result = shape_enum.shapeEnum.TRIANGLE.name
            elif vtc == 4:
                result = shape_enum.shapeEnum.SQUARE.name
            elif vtc == 5:
                result = shape_enum.shapeEnum.PENTAGON.name
            elif vtc == 6:
                result = shape_enum.shapeEnum.HEXAGON.name
            elif vtc == 8:
                result = shape_enum.shapeEnum.OCTAGON.name

    BASE_DIR = os.getcwd()
    IMAGE_DIR = os.path.join(BASE_DIR, 'shape')
    detected_shape_image_name = file_name_generator.make_detected_image_name()
    file_path = os.path.join(IMAGE_DIR, detected_shape_image_name)
    plt.imshow(img_gray_blur)
    plt.savefig(file_path)

    with open(file_path, 'rb') as data:
        uploaded_detected_shape_image_url = s3_service.upload_detected_shape_image(data, detected_shape_image_name)

    shape_code = 0
    shape_name = ''

    if result == '':
        not_detected_color_result = (
            'https://' + config_parser.get_s3_bucket_name() + '.s3.'
            + config_parser.get_s3_region_name() + '.amazonaws.com/' + config_parser.get_s3_template_folder_name() + '/'
            + 'no_result.jpg', '미 검출', ''
        )
        return not_detected_color_result
    else:
        for shape_enum_shape in shape_enum.shapeEnum:
            if result == shape_enum_shape.name:
                shape_code = shape_enum_shape.code
                shape_name = shape_enum_shape.shape_name

    color_result = (uploaded_detected_shape_image_url, shape_name, shape_code)

    return color_result
