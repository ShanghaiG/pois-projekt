from calculate_methods import *
import cv2

img = cv2.imread("Images/zdjecie99.png")
center = calculate_center(img)
height, width = image_size(img)
img = create_threshold(img)
summary_lines_points = create_points_in_line(create_lines(center, height, width), center, height, width)
reduced_summary_points = remove_background(img, summary_lines_points)
calculate_data = points_color_recognition(reduced_summary_points, img)

if __name__ == '__main__':
    print(f'Wiek drzewa wynosi: {calculate_age(calculate_data)}')
