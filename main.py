# importing OpenCV(cv2) module
import cv2


# Python function to read image using OpenCV
def load_image():
	# Save image in set directory
	# Read RGB image
	img = cv2.imread('Acacia_1.jpeg')
	cv2.imshow('image', img)
	cv2.waitKey(0)       
	cv2.destroyAllWindows()

# Python function to find a red dot coordinates that should be on the middle of the
def find_dot():
	print("find_dot!")


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
find_dot()
set_line()
count_color_changes()
compare_lines()
main()