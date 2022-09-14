# file for generating plots
from calculate_methods import *
import cv2
from matplotlib import pyplot as plt
import numpy as np
from skimage.io import imread_collection
import copy

img = cv2.imread("C:/Users/Adam/PycharmProjects/pois-projekt/Images/bardzo_ladna_nazwa.png")
img_to_analysis = copy.deepcopy(img)
center = calculate_center(img)
height, width = image_size(img)
img = create_threshold(img)
summary_lines_points = create_points_in_line(create_lines(center, height, width), center, height, width)
reduced_summary_points = remove_background(img, summary_lines_points)


def produce_plots(data, name, dir):

   for index,data_unit in enumerate(data):

       name_unit = name[index - 1]

       for index, line in enumerate(data_unit):

           x = np.array([])
           dane = []

           plt.title(f'{name_unit}_{index}')
           plt.xlabel('Pixel Index')
           plt.ylabel('Pixel Value')
           print(f'{dir}/{name_unit}_{index}')
           plt.plot(dane)
           plt.savefig(f'{dir}/{name_unit}_{index}')
           plt.close()


def compare_plots(dir):
   col_dir = f'{dir}/*.png'
   images = imread_collection(col_dir)

   fig = plt.figure(figsize=(10, 7))

   plt.imshow(images[1])

produce_plots([summary_lines_points,reduced_summary_points],['reduced_summary', 'summary_lines'],'data_images')
compare_plots("data_images")