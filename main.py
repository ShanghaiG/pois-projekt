# importing OpenCV(cv2) module
import cv2
import numpy as np


# Python function to read image, and set up the lines
def load_image():
	img = cv2.imread("Acacia_1.jpeg")
	Red_pixels = np.argwhere(cv2.inRange(img, (0, 0, 251), (0, 0, 255)))
	for px, py in Red_pixels:
		cv2.circle(img, (py, px), 5, (0, 255, 255), 1)
	cv2.imwrite("out.jpeg", img)

	# Calculating the size of image
	height, width = img.shape[:2]
	halfwidth = int(width/2)
	halfheight = int(height/2)

	# Set the points for lines
	center = (py, px)
	line1 = (0,0)
	line2 = (0, width)
	line3 = (height, width)
	line4 = (height, 0)
	line5 = (height, halfwidth)
	line6 = (halfheight, width)
	line7 = (halfheight, 0)
	line8 = (0, halfwidth)

	# Line Color in BGR Format
	color = (1, 0, 0) # will be Blue

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
# 75% or more of line have almost(1-2 years difference) te same value: we measure the average and present to user 
def compare_lines():
	print("compare_lines!")


def main():
    print("main!")


load_image()
count_color_changes()
compare_lines()
main()