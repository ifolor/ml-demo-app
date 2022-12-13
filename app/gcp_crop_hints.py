import os, io
from google.cloud import vision

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "369410-4d30b4b7a194.json"


path = "../assets/IMG_1.jpeg"
client = vision.ImageAnnotatorClient()

with io.open(path, 'rb') as image_file:
    content = image_file.read()
    print(type(content))


image = vision.Image(content=content)
#print(image)
#print(type(image))

## define the aspect ratio of the image
#crop_hints_params = vision.CropHintsParams(aspect_ratios=[1.77])
#image_context = vision.ImageContext(crop_hints_params=crop_hints_params)
#response = client.crop_hints(image=image, image_context=image_context)

response = client.crop_hints(image=image)
hints = response.crop_hints_annotation.crop_hints

for n, hint in enumerate(hints):
    print('\nCrop Hint: {}'.format(n))

    vertices = (['({},{})'.format(vertex.x, vertex.y)
                for vertex in hint.bounding_poly.vertices])

    print('bounds: {}'.format(','.join(vertices)))

if response.error.message:
    raise Exception(
        '{}\nFor more info on error messages, check: '
                'https://cloud.google.com/apis/design/errors'.format(
            response.error.message))


print(vertices)