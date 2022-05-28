from enum import Enum


class errorMessage(Enum):
    S3_CONNECTION_ERROR = ('S3 연결 도중 문제가 발생했습니다.', 500)
    S3_PUT_OBJECT_ERROR = ('S3 이미지 업로드 중 문제가 발생했습니다. ', 501)

    def __init__(self, message, error_code):
        self.message = message
        self.error_code = error_code
