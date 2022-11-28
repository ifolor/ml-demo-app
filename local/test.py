import numpy as np
import cv2
from  PIL import Image
from crop_utils import create_threshold_image, ignore_small_contours, crop_image

output_dir = "output_test"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

image = Image.open(uploaded_file)
saliency_map, threshold_map = create_threshold_image(image)

cv2.imshow('image', image)
    #cv2.imwrite(os.path.join(out_dir, "".join([image_name, "_image_rect.png"])), image)
    cv2.imwrite(os.path.join("dir/", "".join([image_name, "_image_rect.png"])), image)

 
    cv2.waitKey(1000)

threshold_map_exclude_small_contours = ignore_small_contours(threshold_map)
rectangle_image, cropped_image = crop_image(image, threshold_map_exclude_small_contours)