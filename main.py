# importing OpenCV(cv2) module
import copy
import cv2
import numpy as np
from matplotlib import pyplot as plt


# Python function to read image, and set up the lines
def load_image():
	img = cv2.imread("zdj6-edit.png")
	Red_pixels = np.argwhere(cv2.inRange(img, (0, 2, 251), (0, 2, 255)))
	for px, py in Red_pixels:
		cv2.circle(img, (py, px), 5, (0, 255, 255), 1)
	cv2.imwrite("out.jpeg", img)

	# Calculating the size of image
	height, width = img.shape[:2]
	halfwidth = int(width/2)
	halfheight = int(height/2)

	# Set the points for lines
	center = (Red_pixels[0][0], Red_pixels[0][1])
	line1 = (0,0)
	line2 = (0, width)
	line3 = (height, width)
	line4 = (height, 0)
	line5 = (height, halfwidth)
	line6 = (halfheight, width)
	line7 = (halfheight, 0)
	line8 = (0, halfwidth)

	# Appending lines to list for easier manipulation
	lines = [line1, line2, line3, line4, line5, line6, line7, line8]

	# Line Color in BGR Format
	color = (1, 0, 0) # will be Blue

	# Thickness and line type
	thickness = 2
	linetype = cv2.LINE_AA

	# TODO Repair adaptive threshold
	# Image maniputalion section
	img = cv2.medianBlur(img, 5)
	img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,11,2)

	####color change section


	output_main = []
	for line_ in lines:

		# Setting flags and current point for visual analysis
		output_unit = []
		current_point = [center[0], center[1]]
		current_value = 0
		flag_1 = True
		flag_2 = True



		# TODO Adaptive screen limitation
		# If current_point reaches end of the line or end of image break the loop
		while current_point != [line_[0], line_[1]] and current_point[1] != 999 and current_point[0] != 999:

			# If point [0] is higher go up otherwise go down, if point reaches its destination the loop will deactivate
			if flag_1:
				if current_point[0] == line_[0]:
					flag_1 = False
				elif current_point[0] >= height:
					flag_1 = False
				elif current_point[0] > line_[0]:
					current_point[0] -= 1
				elif current_point[0] < line_[0]:
					current_point[0] += 1

			# If point [1] is higher go up otherwise go down, if point reaches its destination the loop will deactivate
			if flag_2:
				if current_point[1] == line_[1]:
					flag_2 = False
				elif current_point[1] >= height:
					flag_2 = False
				elif current_point[1] > line_[1]:
					current_point[1] -= 1
				elif current_point[1] < line_[1]:
					current_point[1] += 1

			output_unit.append((current_point[0], current_point[1]))

		output_main.append(copy.deepcopy(output_unit))

	# Data preprocesing

	for line_ in output_main:
		for point in line_:
			if img[point[0], point[1]] == 255:
				line_.pop(len(list(line_)) - 1)
			elif img[point[0], point[1]] == 0:
				continue

	# Analiza danych

	final_data = []

	# Dla każdej lini w output_main
	for line_ in output_main:

		final_data_unit = []
		state = None

		# Switch Treshold to zmienna która definiuje ile pixeli musi nastąpić po sobie aby zaliczyć zmiane jako słój a
		# nie szum jesli ustawiona jest na 5 wymagane jest 5 pixeli o tej samej barwie po sobie aby zapisać punkt jako
		# słój

		switch_threshold = 5
		switch_threshold_current = 0

		# Dla każdego punktu w lini
		for point in line_:

			# Jeśli pierwszy piksel jest czarny ustaw stan na czarny jeśli biały - biały
			if img[point[0], point[1]] == 0 and state == None:
				state = "DARK"
			elif img[point[0], point[1]] == 255 and state == None:
				state = "LIGHT"

			# Jeśli stan jest czarny a punkt ma wartość jasnego zapisz punkt
			if state == "DARK" and img[point[0], point[1]] == 255:

				final_data_unit.append((point[0], point[1]))
				state = "LIGHT"

				# Jeśli switch treshold jest równy 0 przypisz tymczasowo punkt na którym jako pierwszy nastąpiła zmiana
				if switch_threshold_current == 0:
					temporary_point = ((point[0], point[1]))

				# Zwieksz licznik o 1
				switch_threshold_current += 1

				#Jesli swich threshold osiągnął określoną wartość zapisz go do listy
				if switch_threshold_current == switch_threshold:
					state = "LIGHT"
					final_data_unit.append((point[0],point[1]))
					switch_threshold_current = 0

			# Jeśli stan jest biały a pixel ma wartość czarnego zmień stan
			elif state == "LIGHT" and img[point[0], point[1]] == 0:

				# Jeśli switch treshold jest równy 0 przypisz tymczasowo punkt na którym jako pierwszy nastąpiła zmiana
				if switch_threshold_current == 0:
					temporary_point = ((point[0], point[1]))

				# Zwieksz licznik o 1
				switch_threshold_current += 1

				# Jesli swich threshold osiągnął określoną wartość zapisz go do listy
				if switch_threshold_current == switch_threshold:
					state = "DARK"
					# final_data_unit.append((temporary_point[0],temporary_point[1]))
					switch_threshold_current = 0


			# dodaj liste do final_data
		final_data.append(final_data_unit)





			#if 240 >= current_value >= 180:
			#	if timer == 0:
			#		temp_pos = current_point
			#	timer += 1
			#	if timer >= 5 and end_flag:
			#		small_output.append((temp_pos[0], temp_pos[1]))
			#		end_flag = False
			#elif current_value < 180:
			#	timer = 0
			#	end_flag = True



	# 	big_data_output.append(points_position_output)
	# 	output.append(small_output)
	# 	points_position_output = []
	# 	small_output = []
	#
	# # other method
	#
	# # generacja średnich lokalnych
	#
	# big_output = []
	# output = []
	# sekcje = 20
	# mean = 0
	# for liness in big_data_output:
	# 	for index, x in enumerate(liness):
	# 		mean += img[x[0], x[1]]
	# 		if index == len(line_):
	# 			mean /= index % sekcje
	# 			output.append(int(mean))
	# 		if index % sekcje == 0:
	# 			mean /= 30
	# 			output.append(int(mean))
	# 	big_output.append(output)
	# 	output = []
	#
	#
	# final_data = []
	# final_data_unit = []
	#
	# for index ,linee in enumerate(big_data_output):
	# 	state = "DARK"
	# 	counter = 0
	# 	iterator = 0
	# 	for point in linee:
	# 		if img[point[0], point[1]] > big_output[index][counter] and state == "DARK":
	# 			final_data_unit.append((point[0],point[1]))
	# 			state = "LIGHT"
	# 		elif img[point[0], point[1]] <= big_output[index][counter] and state == "LIGHT":
	# 			final_data_unit.append((point[0], point[1]))
	# 			state = "DARK"
	# 		iterator += 1
	#
	# 		if iterator >= sekcje:
	# 			iterator = 0
	# 			counter += 1
	# 	final_data.append(final_data_unit)

	# Draw lines on image

	img =cv2.cvtColor(img,cv2.COLOR_GRAY2RGB)

	for line_ in final_data:
		print(line_)
		for point in line_:
			print(point)
			img = cv2.circle(img, [point[0], point[1]], 5, (0, 0, 255), 2)

	for line_ in final_data:
		print(len(line_))

	# for line_ in lines:
	# 	img = cv2.line(img, center, line_, color, thickness, linetype)


	cv2.imshow("out.jpeg", img)
	cv2.waitKey(0)
	return(lines)


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


lines = load_image()
count_color_changes(lines)
compare_lines()
main()