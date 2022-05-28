class s3Exception(Exception):

    exception_name = ''
    message = ''
    error_code = ''

    def __init__(self, exception_name, message, error_code):
        super().__init__(exception_name, message, error_code)
        self.exception_name = exception_name
        self.message = message
        self.error_code = error_code

    def get_exception_name(self):
        return self.exception_name

    def get_message(self):
        return self.message

    def get_error_code(self):
        return self.error_code
