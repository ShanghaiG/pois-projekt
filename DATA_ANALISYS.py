import numpy

from calculate_methods import *
import cv2
from matplotlib import pyplot as plt
import numpy as np
from skimage.io import imread_collection
import copy

img = cv2.imread("Images/jeszcze_ladniejsza_nazwa.png")
img_to_analisys = copy.deepcopy(img)
center = calculate_center(img)
height, width = image_size(img)
img = create_threshold(img)
summary_lines_points = create_points_in_line(create_lines(center, height, width), center, height, width)
reduced_summary_points = remove_background(img, summary_lines_points)

for line in summary_lines_points:
    print(line)

for line in reduced_summary_points:
    print(line)



def produce_plots(data, name, dir):

    for index,data_unit in enumerate(data):

        name_unit = name[index - 1]

        for index, line in enumerate(data_unit):

            x = np.array([])
            dane = []

            for point in line:
                dane.append(img[point[0], point[1]])

            plt.title(f'{name_unit}_{index}')
            plt.xlabel('Pixel Index')
            plt.ylabel('Pixel Value')
            print(f'{dir}/{name_unit}_{index}')
            plt.plot(dane)
            plt.savefig(f'{dir}/{name_unit}_{index}')
            plt.close()

            dane = []


def compare_plots(dir):
    col_dir = f'{dir}/*.png'
    images = imread_collection(col_dir)

    fig = plt.figure(figsize=(10, 7))

    plt.imshow(images[1])


def crack_analisys(image):

    # Calculate amount of pixels on screen that are not white (background)
    image_without_white_color = np.argwhere(cv2.inRange(image, (0, 0, 0), (250, 250, 250)))
    pixels_amount = len(image_without_white_color)

    # Find dark pixels associated with cracks
    dark_pixels = np.argwhere(cv2.inRange(image, (0, 0, 0), (3, 3, 3)))

    # create canvas with 0's for visualization in shape of orginal image
    canvas = numpy.zeros([image.shape[0], image.shape[1]])

    # Replace places where dark pixels are with 1's
    for pixel in dark_pixels:
        canvas[pixel[0]][pixel[1]] = 1

    # Display graph
    plt.imshow(canvas, cmap='hot', interpolation='nearest')
    plt.show()

    # Print message with calculated amount
    print(f"Tree have {round((len(dark_pixels) / pixels_amount),2)} % of cracks")


crack_analisys(img_to_analisys)
produce_plots([summary_lines_points,reduced_summary_points],['reduced_summary', 'summary_lines'],'data_images')
compare_plots("data_images")