import configparser as parser

properties = parser.ConfigParser()
properties.read('config.ini')


def get_s3_bucket_name():
    return properties['s3']['bucket_name']


def get_s3_region_name():
    return properties['s3']['region']


def get_s3_access_key():
    return properties['s3']['access_key']


def get_s3_secret_access_key():
    return properties['s3']['secret_access_key']