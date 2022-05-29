class Drug:
    shape_image_url = ''
    shape_name = ''
    color_image_url = ''
    color_name = ''
    ocr_image_url = ''
    ocr_result = ''
    image = ''
    drug_name = ''
    component_info = ''
    how_to_save = ''
    effectiveness = ''
    usage_capacity = ''
    precautions = ''

    def __init__(self,
                 shape_image_url,
                 shape_name,
                 color_image_url,
                 color_name,
                 ocr_image_url,
                 ocr_result,
                 image,
                 drug_name,
                 component_info,
                 how_to_save,
                 effectiveness,
                 usage_capacity,
                 precautions):
        self.shape_image_url = shape_image_url
        self.shape_name = shape_name
        self.color_image_url = color_image_url
        self.color_name = color_name
        self.ocr_image_url = ocr_image_url
        self.ocr_result = ocr_result
        self.image = image
        self.drug_name = drug_name
        self.component_info = component_info
        self.how_to_save = how_to_save
        self.effectiveness = effectiveness
        self.usage_capacity = usage_capacity
        self.precautions = precautions
