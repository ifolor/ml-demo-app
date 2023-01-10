import os
import numpy as np
from PIL import Image
import cv2
from google.cloud import vision  
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "369410-4d30b4b7a194.json"

client = vision.ImageAnnotatorClient()

def create_bounding_box(image_bytes, aspect_ratio=None):
    '''
    Utilizes GCP crop hints function to return the bounding box coordinates for a given image
    Parameters:
        image_bytes (bytes): image that was uploaded using the Streamlit app
        aspect_ratio (float): width/height of the desired bounding box, e.g. 16/9, optional
    Returns:
        vertices (list): list of 4 strings containing the x- and y-coordinates of the bounding 
            box, e.g. ['(0,1161)', '(3023,1161)', '(3023,2870)', '(0,2870)']
        hint.confidence (float): the confidence level of the detected bounding box
        hint.importance_fraction (float): the importance level of the detected bounding 
        box
    '''
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
    '''
    Parses the vertices response from the GCP crop_hints function to extract the upper left corner
        of the bounding box with its width and height
    Parameters:
        vertices (list): list of 4 strings containing the x- and y-coordinates of the bounding 
            box, e.g. ['(0,1161)', '(3023,1161)', '(3023,2870)', '(0,2870)']
    Returns:
        start_x (int): the x-coordinate of the upper left corner of the bounding box
        start_y (int): the y-coordinate of the upper left corner of the bounding box
        width (int): width of the bounding box
        height (int): height of the bounding box
    '''
    start_x = int(vertices[0].split(",")[0].replace('(', ''))
    start_y = int(vertices[0].split(",")[1].replace(')', ''))
    width = int(vertices[1].split(",")[0].replace('(', '')) - start_x
    height = int(vertices[2].split(",")[1].replace(')', '')) - start_y
    return start_x, start_y, width, height


def create_cropped_image(image, start_x, start_y, width, height):
    '''
    Crops the image based on the bounding rectangle
    Parameters:
        image (PIL.Image class)
        start_x (int): the x-coordinate of the upper left corner of the bounding box
        start_y (int): the y-coordinate of the upper left corner of the bounding box
        width (int): width of the bounding box
        height (int): height of the bounding box
    Returns:
        cropped_image (array): image where only the area within the bounding box is preserved
    '''
    image_array = np.asarray(image)
    cropped_image = image_array[start_y:start_y+height,  start_x:start_x+width]
    return cropped_image

def create_rectangle_image(image, start_x, start_y, width, height, colour = (238, 40, 103)):
    '''
    Draws the bounding box on the original image
    Parameters:
        image (PIL.Image class)
        start_x (int): the x-coordinate of the upper left corner of the bounding box
        start_y (int): the y-coordinate of the upper left corner of the bounding box
        width (int): width of the bounding box
        height (int): height of the bounding box
        color (tuple): RGB color representation, optional
    Returns:
        rectangle_image (array): image containing the bounding box
    '''
    image_array = np.asarray(image)
    start_vertex = (start_x, start_y)
    end_vertex = (start_x+width, start_y+height)
    thickness = int(0.02*min(image_array.shape[0], image_array.shape[1]))
    rectangle_image = cv2.rectangle(image_array, start_vertex, end_vertex, colour, thickness)
    return rectangle_image