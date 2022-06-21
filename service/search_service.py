import requests
import json
from bs4 import BeautifulSoup

from service import s3_service
from util import file_name_generator
from domain import drug


def search_drugs(shape_image_url, shape_name,
                 color_image_url, color_name, ocr_image_url,
                 shape_code, color_code, ocr_result):

    result = []
    shape_code = ''

    request_url = 'https://terms.naver.com/medicineSearch.naver?mode=exteriorSearch&shape=' + shape_code + \
                  '&color=' + color_code + \
                  '&dosageForm=&divisionLine=&identifier=' + ocr_result + '&page=1'

    html = requests.get(request_url)
    soup = BeautifulSoup(html.content, "html.parser")
    next_url_list = []
    tmp = soup.select('ul>li>div>div>a')
    for value in tmp:
        default = 'https://terms.naver.com/'
        next_url_list.append(default + value['href'])

    if len(next_url_list) == 0:
        return "검색 결과가 없습니다."

    for url in next_url_list:
        html2 = requests.get(url)
        soup2 = BeautifulSoup(html2.content, 'html.parser')

        drug_image_url = soup2.find('img', id='innerImage0')['data-src']
        response = requests.get(drug_image_url, stream=True)
        drug_image_file = response.content
        file_name = file_name_generator.make_detected_image_name()

        uploaded_drug_image_url = s3_service.upload_searched_drug_image(drug_image_file, file_name)
        drug_name = soup2.find('h2', class_='headword').text
        p_tag = soup2.find_all('p', class_='txt')
        component_info = p_tag[1].text.rstrip()
        how_to_save = p_tag[2].text.rstrip()
        effectiveness = p_tag[3].text.rstrip()
        usage_capacity = p_tag[4].text.rstrip()
        precautions = p_tag[5].text.rstrip()

        result_drug = drug.Drug(shape_image_url, shape_name,
                                color_image_url,
                                color_name,
                                ocr_image_url,
                                ocr_result,
                                uploaded_drug_image_url,
                                drug_name,
                                component_info,
                                how_to_save,
                                effectiveness,
                                usage_capacity,
                                precautions)

        result.append(result_drug.__dict__)

    result_json = json.dumps(result)
    return result_json
