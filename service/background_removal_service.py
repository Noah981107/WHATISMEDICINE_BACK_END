import cv2
import numpy as np
from rembg.bg import remove
import io
from PIL import Image, ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True


def image_background_removal():
    input_path = 'service/person.png'
    output_path = 'out.png'

    f = np.fromfile(input_path)
    print('f : ', f)
    result = remove(f)
    print('result type: ', type(result))

    data_io = io.BytesIO(result)
    print('data io type : ', type(data_io))

    img = Image.open(data_io).convert("RGBA")
    img.save(output_path)

    return 'test'
