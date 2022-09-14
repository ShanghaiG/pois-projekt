import copy
import math
from matplotlib import pyplot as plt
import cv2
import numpy as np
import statistics


def calculate_center(image):
    blue_pixels = np.argwhere(cv2.inRange(image, (255, 0, 0), (255, 2, 2)))
    for py, px in blue_pixels:
        cv2.circle(image, (px, py), 5, (0, 255, 255), 1)
    center = (blue_pixels[0][1], blue_pixels[0][0])

    return center


def image_size(image):
    height, width = image.shape[:2]
    return height, width


def create_lines(center, height, width):
    line1 = (0, 0)
    line2 = (0, width)
    line3 = (height, width)
    line4 = (height, 0)
    line5 = (height, center[1])
    line6 = (center[0], width)
    line7 = (center[0], 0)
    line8 = (0, center[1])
    # Appending lines to list for easier manipulation
    lines = [line1, line2, line3, line4, line5, line6, line7, line8]

    return lines


def create_threshold(image):
    image = cv2.medianBlur(image, 5)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)

    return image


def create_points_in_line(lines, center, height, width):
    summary_lines_points = []
    for line_ in lines:
        # Setting flags and current point for visual analysis
        points_in_line = []
        current_point = [center[0], center[1]]
        horizontal_movement = True
        vertical_movement = True

        # If current_point reaches end of the line or end of image break the loop
        while current_point != [line_[0], line_[1]] and current_point[1] != width - 1 and current_point[0] != height -1:
            if vertical_movement:
                if current_point[0] == line_[0] or current_point[0] >= width or current_point[0] <= 0:
                    vertical_movement = False
                elif current_point[0] > line_[0]:
                    current_point[0] -= 1
                elif current_point[0] < line_[0]:
                    current_point[0] += 1
            if horizontal_movement:
                if current_point[1] == line_[1] or current_point[1] >= height or current_point[1] <= 0:
                    horizontal_movement = False
                elif current_point[1] > line_[1]:
                    current_point[1] -= 1
                elif current_point[1] < line_[1]:
                    current_point[1] += 1

            points_in_line.append((current_point[0], current_point[1]))

        summary_lines_points.append(copy.deepcopy(points_in_line))
    return summary_lines_points


def remove_background(image, points_list_before_deepcoopy):

    # Data preprocesing
    points_list = copy.deepcopy(points_list_before_deepcoopy)

    for line_ in points_list:

        while image[line_[-1][0],line_[-1][1]] == 255:
            del line_[-1]
    return points_list


def points_color_recognition(points_list, img):
    # Analiza danych
    final_data = []
    result = []

    for line_ in points_list:
        final_data_unit = []
        state = None

        # Switch Treshold to zmienna która definiuje ile pixeli musi nastąpić po sobie aby zaliczyć zmiane jako słój a
        # nie szum jesli ustawiona jest na 5 wymagane jest 5 pixeli o tej samej barwie po sobie aby zapisać punkt jako
        # słój
        switch_threshold = 1
        dark_noise_detection = 0
        light_noise_detection = 0

        for point in line_:

            # Czytanie koloru pierwszego pixela dla danej linii
            if img[point[0], point[1]] == 0 and state is None:
                state = "DARK"
            elif img[point[0], point[1]] == 255 and state is None:
                state = "LIGHT"

            # Przy przejściu z czarnego na jasny zapisuje koordynaty punktu
            if state == "DARK" and img[point[0], point[1]] == 255:

                state = "LIGHT"
                dark_noise_detection += 1

                # Wykrywanie szumu, jeśli dany kolor nie utrzymuje się przez następne pixele, wtedy zostaje uznany
                # jako szum
                if dark_noise_detection == switch_threshold:
                    state = "LIGHT"
                    final_data_unit.append((point[0], point[1]))
                    dark_noise_detection = 0

            # Jeśli stan jest biały a pixel ma wartość czarnego zmień stan
            elif state == "LIGHT" and img[point[0], point[1]] == 0:
                state = "DARK"
                light_noise_detection += 1

                if light_noise_detection == switch_threshold:
                    state = "DARK"
                    light_noise_detection = 0

        # dodaj liste do final_data
        final_data.append(final_data_unit)

    # Zmiana na RGB żeby zaznaczyć słoje (nie wiem, chyba tak)
    img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)

    circle_colors = [(0, 0, 255), (0, 255, 0), (255, 0, 0),
                     (255, 0, 255), (0, 255, 255), (255, 255, 0),
                     (100, 100, 100), (50, 50, 50)]

    for index, line_ in enumerate(final_data):
        for point in line_:
            img = cv2.circle(img, [point[0], point[1]], 5, circle_colors[index], 2)

    for line_ in final_data:
        result.append(len(line_))

    cv2.imshow("out.jpeg", img)
    cv2.waitKey(0)

    return result, final_data


def calculate_age(results):

    # tu będą jakieś wyniki pomiarów, np lista
    result_counter = {}
    age = 0.0
    counter_check = list(filter(lambda x: x >= 6, result_counter))

    # Checking number of repetitions of every result in results list.
    # If the result in result_counter dict already exists, incrementing the variable by 1, if not, then creating one
    for result in results:
        if result in result_counter:
            result_counter[result] += 1
        else:
            result_counter[result] = 1

    # meeting the requirement at the top of the function
    if counter_check:
        age = float(counter_check[0])
    else:
        age = statistics.median(results)
    return age


def get_mean_distance_between_rings(data, expected_average):

    # List for storing 1's and 0's which represent conditions that tree had during its development
    tree_growth_conditions_score = []

    # For every line in date
    for line in data:

        last_point = None
        average = 0

        # For every point in line
        for point in line:

            # if this is the first step in algorithm set last point
            if not last_point:
                last_point = (point[0], point[1])

            # If this is not the first step calculate distance between two points add it to average and set new last
            # point
            else:
                distance = math.sqrt(pow((last_point[0] - point[0]), 2) + pow((last_point[1] - point[1]), 2))
                average += distance
                last_point = (point[0], point[1])

        # Calculate average distance
        average = average / len(line)

        # If average distance is greater or equal to value specified append 1 if not 0
        if average < float(expected_average):
            tree_growth_conditions_score.append(0)
        elif average >= float(expected_average):
            tree_growth_conditions_score.append(1)

    return  tree_growth_conditions_score


def identify_tree_growth_conditions(data, expected_average):

    # Call for get_mean_distance_between_rings whitch returns list containing True and false values represented by 1's
    # and 0's
    tree_growth_conditions_score = get_mean_distance_between_rings(data, expected_average)

    # if to or more values in a list are one the tree had favorable conditions during development
    if sum(tree_growth_conditions_score) >= 2:
        return "the tree had favorable conditions for growth"
    elif sum(tree_growth_conditions_score) < 2:
        return "tree had unfavorable conditions for development"

def crack_analysis(chuj):

    # Calculate amount of pixels on screen that are not white (background)
    image_without_white_color = np.argwhere(cv2.inRange(chuj, (0, 0, 0), (250, 250, 250)))
    pixels_amount = len(image_without_white_color)

    # Find dark pixels associated with cracks
    dark_pixels = np.argwhere(cv2.inRange(chuj, (0, 0, 0), (3, 3, 3)))

    # create canvas with 0's for visualization in shape of orginal image
    canvas = np.zeros([chuj.shape[0], chuj.shape[1]])

    # Replace places where dark pixels are with 1's
    for pixel in dark_pixels:
        canvas[pixel[0]][pixel[1]] = 1

    # Display graph
    plt.imshow(canvas, cmap='hot', interpolation='nearest')
    plt.show()
    plt.savefig(f'data_images/crack_analysis')
    # Print message with calculated amount
    return round((len(dark_pixels) / pixels_amount), 2)
