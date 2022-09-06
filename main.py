# importing OpenCV(cv2) module
import cv2
import numpy as np
import statistics


# Python function to read image, and set up the lines
def load_image():
	img = cv2.imread("Acacia_1.jpeg")
	red_pixels = np.argwhere(cv2.inRange(img, (0, 0, 251), (0, 0, 255)))
	for px, py in red_pixels:
		cv2.circle(img, (py, px), 5, (0, 255, 255), 1)


	# Grayscaling the image
	img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	cv2.imwrite("out.jpeg", img)

	# Calculating the size of image
	height, width = img.shape[:2]
	halfwidth = int(width/2)
	halfheight = int(height/2)

	# Set the points for lines
	center = (py, px)
	line1 = (0, 0)
	line2 = (0, width)
	line3 = (height, width)
	line4 = (height, 0)
	line5 = (height, halfwidth)
	line6 = (halfheight, width)
	line7 = (halfheight, 0)
	line8 = (0, halfwidth)

	# Line Color in BGR Format
	color = (1, 0, 0)  # will be Blue

	# Thickness and line type
	thickness = 2
	linetype = cv2.LINE_AA

	# Draw lines on image
	img = cv2.line(img, center, line1, color, thickness, linetype)
	img = cv2.line(img, center, line2, color, thickness, linetype)
	img = cv2.line(img, center, line3, color, thickness, linetype)
	img = cv2.line(img, center, line4, color, thickness, linetype)
	img = cv2.line(img, center, line5, color, thickness, linetype)
	img = cv2.line(img, center, line6, color, thickness, linetype)
	img = cv2.line(img, center, line7, color, thickness, linetype)
	img = cv2.line(img, center, line8, color, thickness, linetype)

	# show image
	cv2.imshow("out.jpeg", img)
	cv2.waitKey(0)


# Python function to count changes of colour and brightness on multiple lines,
# to separate winter and summer time and calculate age of tree for every line and store it in a table
def count_color_changes():
	print("count_color_changes!")


# Python function to compare values of multiple lines and make a decision acording to rules
# 75% or more of lines have the same value: we can accept age and present to user.
# 75% or more of line have almost(1-2 years difference) te same value: we measure the median and present to user
def calculate_age() -> float:
	print("compare_lines!")

	# tu będą jakieś wyniki pomiarów, np lista
	results = []
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


def main():
	print("main!")


load_image()
count_color_changes()
calculate_age()
main()
