import datetime
import re


def change_user_uploaded_file_name(file_name):

    split_file_name_list = re.split('[.png,.jpg,.jpeg]', file_name)

    real_file_name = split_file_name_list[0]
    suffix = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
    changed_file_name = "_".join([real_file_name, suffix]) + '.png'
    return changed_file_name


def make_detected_image_name():
    base_name = "Image"
    suffix = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
    result_image_name = "_".join([base_name, suffix]) + '.png'
    return result_image_name
