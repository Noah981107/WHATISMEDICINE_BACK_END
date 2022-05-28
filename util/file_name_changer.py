import datetime
import re


def change_user_uploaded_file_name(file_name):

    split_file_name_list = re.split('[.png,.jpg,.jpeg]', file_name)

    real_file_name = split_file_name_list[0]
    suffix = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
    changed_file_name = "_".join([real_file_name, suffix]) + '.jpg'
    return changed_file_name
