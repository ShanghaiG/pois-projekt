# importing OpenCV(cv2) module
import cv2
import numpy as np


# Python function to read image using OpenCV and to find a red dot coordinates that should be on the middle of the
def load_image():
	img = cv2.imread("Acacia_1.jpeg")
	red_pixels = np.argwhere(cv2.inRange(img, (0, 0, 250), (0, 0, 255)))
	for px, py in red_pixels:
		cv2.circle(img, (py, px), 5, (0, 255, 255), 1)
	cv2.imwrite("out.jpeg", img)

# Python function to set multiple line from red dot to border of image
def set_line():
	print("set_line!")

# Python function to count changes of colour and brightness on multiple lines, 
# to separate winter and summer time and calculate age of tree for every line and store it in a table
def count_color_changes():
	print("count_color_changes!")


# Python function to compare values of multiple lines and make a decision acording to rules
# 75% or more of lines have the same value: we can accept age and present to user.
# 75% or more of line have almost(1-2 years difference) te same value: we measure the average and present to user 
def compare_lines():
	print("compare_lines!")


def main():
    print("main!")



load_image()
set_line()
count_color_changes()
compare_lines()
main()