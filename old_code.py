# importing OpenCV(cv2) module
import copy
import cv2
import numpy as np
import statistics
# from matplotlib import pyplot as plt


# Python function to read image, and set up the lines
def load_image():
	img = cv2.imread("jeszcze_ladniejsza_nazwa.png")
	Blue_pixels = np.argwhere(cv2.inRange(img, (255, 0, 0), (255, 2, 2)))
	for py, px in Blue_pixels:
		cv2.circle(img, (px, py), 5, (0, 255, 255), 1)

	# Calculating the size of image
	height, width = img.shape[:2]

	# Set the points for lines
	cv2.circle(img, (Blue_pixels[0][1], Blue_pixels[0][0]), 5, (0, 255, 255), 1)
	cv2.imwrite("out.jpeg", img)
	center = (Blue_pixels[0][1], Blue_pixels[0][0])
	line1 = (0,0)
	line2 = (0, width)
	line3 = (height, width)
	line4 = (height, 0)
	line5 = (height, center[1])
	line6 = (center[0], width)
	line7 = (center[0], 0)
	line8 = (0, center[1])

	# Appending lines to list for easier manipulation
	lines = [line1, line2, line3, line4, line5, line6, line7, line8]

	# Line Color in BGR Format
	color = (1, 0, 0) # will be Blue

	# Thickness and line type
	thickness = 2
	linetype = cv2.LINE_AA

	# Image maniputalion section
	img = cv2.medianBlur(img, 5)
	img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,11,2)

	####color change section

	output_main = []
	result = []
	for line_ in lines:

		# Setting flags and current point for visual analysis
		output_unit = []
		current_point = [center[0], center[1]]
		horizontal_movement = True
		vertical_movement = True

		# If current_point reaches end of the line or end of image break the loop
		while current_point != [line_[0], line_[1]]: # and current_point[1] != 1000 and current_point[0] != 1000:

			if vertical_movement:
				if current_point[0] == line_[0] or current_point[0] >= width or current_point[0] <= 0:
					vertical_movement = False
				elif current_point[0] > line_[0]:
					current_point[0] -= 1
				elif current_point[0] < line_[0]:
					current_point[0] += 1

			if horizontal_movement:
				if current_point[1] == line_[1] or current_point[1] >= width or current_point[1] <= 0:
					horizontal_movement = False
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

	for line_ in output_main:

		final_data_unit = []
		state = None

		# Switch Treshold to zmienna która definiuje ile pixeli musi nastąpić po sobie aby zaliczyć zmiane jako słój a
		# nie szum jesli ustawiona jest na 5 wymagane jest 5 pixeli o tej samej barwie po sobie aby zapisać punkt jako
		# słój
		switch_threshold = 5
		dark_noise_detection = 0
		light_noise_detection = 0

		# Pętla for https://www.w3schools.com/python/python_for_loops.asp
		for point in line_:

			# Czytanie koloru pierwszego pixela dla danej linii
			if img[point[0], point[1]] == 0 and state is None:
				state = "DARK"
			elif img[point[0], point[1]] == 255 and state is None:
				state = "LIGHT"

			# Przy przejściu z czarnego na jasny zapisuje koordynaty punktu
			if state == "DARK" and img[point[0], point[1]] == 255:

				final_data_unit.append((point[0], point[1]))
				state = "LIGHT"
				dark_noise_detection += 1

				# Wykrywanie szumu, jeśli dany kolor nie utrzymuje się przez następne pixele, wtedy zostaje uznany
				# jako szum
				if dark_noise_detection == switch_threshold:
					state = "LIGHT"
					final_data_unit.append((point[0],point[1]))
					dark_noise_detection = 0

			# Jeśli stan jest biały a pixel ma wartość czarnego zmień stan
			elif state == "LIGHT" and img[point[0], point[1]] == 0:
				state = "DARK"
				dark_noise_detection += 1

				if light_noise_detection == switch_threshold:
					state = "DARK"
					light_noise_detection = 0

				# Jesli swich threshold osiągnął określoną wartość zapisz go do listy
				if dark_noise_detection == switch_threshold:
					state = "DARK"
					dark_noise_detection = 0


			# dodaj liste do final_data
		final_data.append(final_data_unit)

	# Zmiana na RGB żeby zaznaczyć słoje (nie wiem, chyba tak)
	img =cv2.cvtColor(img,cv2.COLOR_GRAY2RGB)

	for line_ in final_data:
		for point in line_:
			img = cv2.circle(img, [point[0], point[1]], 5, (0, 0, 255), 2)

	for line_ in final_data:
		result.append(len(line_))

	cv2.imshow("out.jpeg", img)
	cv2.waitKey(0)

	return result


# Python function to count changes of colour and brightness on multiple lines,
# to separate winter and summer time and calculate age of tree for every line and store it in a table
def count_color_changes():
	print("count_color_changes!")

# Python function to compare values of multiple lines and make a decision acording to rules
# 75% or more of lines have the same value: we can accept age and present to user.
# 75% or more of line have almost(1-2 years difference) te same value: we measure the average and present to user
def calculate_age(results) -> float:
	print("compare_lines!")

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


def main():
	print("main!")


lines = load_image()
print(f'Age = {calculate_age(lines)}')
main()