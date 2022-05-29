import boto3
import urllib.parse

from util import config_parser
from exception import s3_exception_class
from error_message.error_message import errorMessage


def s3_connection():
    try:
        region = config_parser.get_s3_region_name()
        access_key = config_parser.get_s3_access_key()
        secret_access_key = config_parser.get_s3_secret_access_key()

        s3 = boto3.client(
            service_name='s3',
            region_name=region,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_access_key
        )
    except Exception:
        raise s3_exception_class.s3Exception(
            errorMessage.S3_CONNECTION_ERROR.name,
            errorMessage.S3_CONNECTION_ERROR.message,
            errorMessage.S3_CONNECTION_ERROR.error_code
        )
    else:
        return s3


def s3_put_object(s3, file, file_name):
    try:
        s3.put_object(
            Body=file,
            Bucket=config_parser.get_s3_bucket_name(),
            Key=file_name,
            ContentType=file.content_type,
            ACL='public-read'
        )
    except Exception as e:
        print(e)
        raise s3_exception_class.s3Exception(
            errorMessage.S3_PUT_OBJECT_ERROR.name,
            errorMessage.S3_PUT_OBJECT_ERROR.message,
            errorMessage.S3_PUT_OBJECT_ERROR.error_code
        )


def s3_put_color_pyplot_image(s3, file, file_name):
    try:
        s3.put_object(
            Body=file,
            Bucket=config_parser.get_s3_bucket_name(),
            Key=f'{config_parser.get_s3_color_folder_name()}/{file_name}',
            ContentType='image/jpg',
            ACL='public-read'
        )
    except Exception as e:
        print(e)
        raise s3_exception_class.s3Exception(
            errorMessage.S3_PUT_OBJECT_ERROR.name,
            errorMessage.S3_PUT_OBJECT_ERROR.message,
            errorMessage.S3_PUT_OBJECT_ERROR.error_code
        )


def s3_get_image_url(s3, file_name):
    location = s3.get_bucket_location(
        Bucket=config_parser.get_s3_bucket_name()
    )["LocationConstraint"]

    encoded_file_name = urllib.parse.quote(file_name)
    return "https://" + config_parser.get_s3_bucket_name() + ".s3." + location + ".amazonaws.com/" + encoded_file_name


def s3_get_color_image_url(s3, file_name):
    location = s3.get_bucket_location(
        Bucket=config_parser.get_s3_bucket_name()
    )["LocationConstraint"]

    encoded_file_name = urllib.parse.quote(file_name)
    return "https://" + config_parser.get_s3_bucket_name() + ".s3." + location + ".amazonaws.com/" \
           + config_parser.get_s3_color_folder_name() + '/' + encoded_file_name
