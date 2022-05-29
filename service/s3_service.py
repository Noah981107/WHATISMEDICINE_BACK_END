from util import s3, file_name_generator


def upload_to_s3_user_uploaded_file(file):
    connected_s3 = s3.s3_connection()
    changed_file_name = file_name_generator.change_user_uploaded_file_name(file.filename)
    s3.s3_put_object(connected_s3, file, changed_file_name)
    s3_image_url = s3.s3_get_image_url(connected_s3, changed_file_name)
    return s3_image_url


def upload_detected_color_image(file, file_name):
    connected_s3 = s3.s3_connection()
    s3.s3_put_color_pyplot_image(connected_s3, file, file_name)
    s3_image_url = s3.s3_get_color_image_url(connected_s3, file_name)
    return s3_image_url


def upload_detected_ocr_image(file, file_name):
    connected_s3 = s3.s3_connection()
    s3.s3_put_ocr_pyplot_image(connected_s3, file, file_name)
    s3_image_url = s3.s3_get_ocr_image_url(connected_s3, file_name)
    return s3_image_url


def upload_searched_drug_image(file, file_name):
    connected_s3 = s3.s3_connection()
    s3.s3_put_searched_drug_image(connected_s3, file, file_name)
    s3_image_url = s3.s3_get_searched_drug_image_url(connected_s3, file_name)
    return s3_image_url
