import os
from google.cloud import vision  
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "369410-4d30b4b7a194.json"

client = vision.ImageAnnotatorClient()

def create_bounding_box(image_bytes, aspect_ratio=None):

    image = vision.Image(content=image_bytes)
    if aspect_ratio is None:
        response = client.crop_hints(image=image)
    else:
        crop_hints_params = vision.CropHintsParams(aspect_ratios=[aspect_ratio])
        image_context = vision.ImageContext(crop_hints_params=crop_hints_params)
        response = client.crop_hints(image=image, image_context=image_context)
    
    hints = response.crop_hints_annotation.crop_hints
    for n, hint in enumerate(hints):
        vertices = (['({},{})'.format(vertex.x, vertex.y)
                for vertex in hint.bounding_poly.vertices])
    return vertices, hint.confidence, hint.importance_fraction


def calculate_bounding_box_coords(vertices):

    start_x = int(vertices[0].split(",")[0].replace('(', ''))
    start_y = int(vertices[0].split(",")[1].replace(')', ''))
    width = int(vertices[1].split(",")[0].replace('(', '')) - start_x
    height = int(vertices[2].split(",")[1].replace(')', '')) - start_y
    return start_x, start_y, width, height