import cv2
import os
from  PIL import Image, ImageOps
import numpy as np


def create_threshold_image(image):
    '''
    Creates a threshold image from the input image where the white regions
    correspond to the regions with high saliency values
    Parameters:
        image (PIL.Image object): PIL.Image object from the uploaded file
    Returns:
        threshold_map (np.array): threshold image array with binary values
    '''
    # read the image as a greyscale image and convert it into an array
    image_grey = ImageOps.grayscale(image)
    image_grey = np.array(image_grey)
    # blur the image to reduce noise
    image_blurred = cv2.GaussianBlur(image_grey,(5,5),0)
    # create the saliency map
    saliency = cv2.saliency.StaticSaliencySpectralResidual_create()
    (success, saliency_map) = saliency.computeSaliency(image_blurred)
    saliency_map = (saliency_map * 255).astype("uint8")
    # create the threshold map based on adaptive thresholding
    _, threshold_map = cv2.threshold(saliency_map, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    return saliency_map, threshold_map


def ignore_small_contours(threshold_map, min_fraction=0.01):
    '''
    Creates an updated threshold map from the existing threshold map by excluding 
    small contours if their area is less than the minimum fraction (1%) of the total image area
    Parameters:
        threshold_map (np.array): threshold image array with binary values
        min_fraction (float): the minimum fraction of the image area that a contour should occupy
    Returns:
        threshold_map (np.array): threshold image array with binary values
    '''
    # find the contours in the threshold map
    contours, _ = cv2.findContours(image=threshold_map, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
    # ignore contours if their size is less than 1% of the image size
    for contour in contours:
        if cv2.contourArea(contour) < min_fraction*threshold_map.shape[0]*threshold_map.shape[1]:
            # it seems like this function works only with the for loop:
            cv2.drawContours(threshold_map,[contour], 0, (0, 0, 0), -1)
    return threshold_map


def crop_image(image, threshold_map):
    '''
    Crops the input image based on the threshold map
    Parameters:
        image (PIL.Image object): PIL.Image object from the uploaded file
        threshold_map (np.array): threshold image array with binary values
    '''
    image = np.array(image)
    # draw the bounding rectangle to encapsulate all contours detected in the threshold map
    start_x, start_y, width, height = cv2.boundingRect(threshold_map)
    # crop the image based on the bounding rectangle
    cropped_image = image[start_y:start_y+height,  start_x:start_x+width]
    # draw the rectangle on the original image
    start_vertex = (start_x, start_y)
    end_vertex = (start_x+width, start_y+height)
    colour = (232, 254, 199)
    thickness = 30
    rectangle_image = cv2.rectangle(image, start_vertex, end_vertex, colour, thickness)
    return rectangle_image, cropped_image

