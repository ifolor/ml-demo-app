
import os
import numpy as np
import cv2
from  PIL import Image
from crop_utils import create_threshold_image, ignore_small_contours, crop_image

output_dir = "local/output_test"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

uploaded_file = "local/assets/IMG_2.jpeg"    

image = Image.open(uploaded_file)
image_array = np.array(image)
print(image_array.shape)
saliency_map, threshold_map = create_threshold_image(image)
cv2.imwrite("local/output_test/IMG_2_saliency_map.png", saliency_map)
cv2.imwrite("local/output_test/IMG_2_threshold.png", threshold_map)

start_x, start_y, width, height = cv2.boundingRect(threshold_map)
print(start_x, start_y, width, height)


start_vertex = (start_x, start_y)
end_vertex = (start_x+width, start_y+height)
colour = (232, 254, 199)
thickness = 30
rectangle_image = cv2.rectangle(image_array, start_vertex, end_vertex, colour, thickness) 

cv2.imshow('image', rectangle_image)
 
# waitKey() waits for a key press to close the window and 0 specifies indefinite loop
cv2.waitKey(10000)
 
# cv2.destroyAllWindows() simply destroys all the windows we created.
cv2.destroyAllWindows()





threshold_map_exclude_small_contours = ignore_small_contours(threshold_map)
rectangle_image, cropped_image = crop_image(image, threshold_map_exclude_small_contours)
print(rectangle_image.shape)

cv2.imwrite("/local/output_test/IMG_2_rectangle_image.png", rectangle_image)
cv2.imwrite("local/output_test/IMG_2_cropped_image.png", cropped_image)