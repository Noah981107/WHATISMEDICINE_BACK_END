from flask import Flask, request, Response
import json

from exception.s3_exception_class import s3Exception
from service import s3_service, color_service, ocr_service, search_service, shape_service, background_removal_service

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/upload-test', methods=['POST'])
def upload_image_test():
    file = request.files['file']
    s3_service.upload_to_s3_user_uploaded_file(file)
    return 'upload-test'


@app.route('/upload', methods=['POST'])
def upload_image():
    file = request.files['file']

    s3_image_url = s3_service.upload_to_s3_user_uploaded_file(file)
    print('s3 image url : ', s3_image_url)

    background_removal_image_url = background_removal_service.image_background_removal(s3_image_url)
    print('back ground removal image url : ', background_removal_image_url)

    shape_image_url, shape_name, shape_code = map(str, shape_service.get_shape_from_file(background_removal_image_url))
    print('shape : ', shape_image_url, shape_name, shape_code)
    color_image_url, color_name, color_code = map(str, color_service.get_color_from_file(background_removal_image_url))
    print('color : ', color_image_url, color_name, color_code)
    ocr_image_url, ocr_result = map(str, ocr_service.get_text_from_file(background_removal_image_url))
    print('ocr : ', ocr_image_url, ocr_result)

    result_json = search_service.search_drugs(shape_image_url, shape_name, color_image_url, color_name, ocr_image_url,
                                              shape_code, color_code, ocr_result)

    return Response(result_json, mimetype='application/json', status=200)


@app.errorhandler(s3Exception)
def handle_error(e):
    response = Response()

    response.data = json.dumps({
        'exception_name': e.get_exception_name(),
        'message': e.get_message(),
        'error_code': e.get_error_code()
    })
    response.content_type = 'application/json'
    response.status_code = 500

    return response


if __name__ == '__main__':
    app.run()
