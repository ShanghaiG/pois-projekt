import pygame

from calculate_controller import calculate_controller
import tkinter
from tkinter import filedialog
import cv2

pygame.init()
pygame.font.init()
image = None
screen_resolution = (1280, 720)
window = pygame.display.set_mode(screen_resolution)
pygame.display.set_caption("Tree's age verification")
background = pygame.image.load("background.png")
fps = 20
width = window.get_width()
height = window.get_height()
font = pygame.font.Font("font.ttf", 40)
calculate_tree_age_text = font.render('Calculate tree\'s age', True, (255, 255, 255))
check_growth_conditions_text = font.render('Check growth conditions', True, (255, 255, 255))
identify_tree_anomalies_text = font.render('Identify tree\'s anomalies', True, (255, 255, 255))
import_tree_photo_text = font.render('Import tree\'s photo', True, (255, 255, 255))


def draw_window():
    window.blit(background, (0, 0))
    pygame.display.update()


def open_photo():
    tkinter.Tk().withdraw()
    photo_path = filedialog.askopenfilename()

    return photo_path


def gui():
    clock = pygame.time.Clock()
    run = True
    draw_window()
    while run:
        clock.tick(fps)
        mouse_position = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # creating buttons from top-placed to bottom-placed
            if width / 2 - 300 <= mouse_position[0] <= width / 2 + 300 and height / 2 - 200 <= mouse_position[1] <= height / 2 - 120:
                pygame.draw.rect(window, (150, 150, 150), [width/2 - 300, height/2 - 200, 600, 80])
                if event.type == pygame.MOUSEBUTTONDOWN:
                    image = open_photo()
                    print(f'Opened {image}')
            else:
                pygame.draw.rect(window, (110, 110, 110), [width/2 - 300, height/2 - 200, 600, 80])

            if width / 2 - 300 <= mouse_position[0] <= width / 2 + 300 and height / 2 - 80 <= mouse_position[1] <= height / 2 - 0:
                pygame.draw.rect(window, (150, 150, 150), [width/2 - 300, height/2 - 80, 600, 80])
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if image is not None:
                        calculate_controller('calculate_age', cv2.imread(image))
                    else:
                        raise ValueError("No photo was included")
            else:
                pygame.draw.rect(window, (110, 110, 110), [width/2 - 300, height/2 - 80, 600, 80])

            if width / 2 - 300 <= mouse_position[0] <= width / 2 + 300 and height / 2 + 40 <= mouse_position[1] <= height / 2 + 120:
                pygame.draw.rect(window, (150, 150, 150), [width / 2 - 300, height / 2 + 40, 600, 80])
                if event.type == pygame.MOUSEBUTTONDOWN:
                    print(calculate_controller('tree_growth_conditions', cv2.imread(image)))
            else:
                pygame.draw.rect(window, (110, 110, 110), [width / 2 - 300, height / 2 + 40, 600, 80])

            if width / 2 - 300 <= mouse_position[0] <= width / 2 + 300 and height / 2 + 160 <= mouse_position[1] <= height / 2 + 240:
                pygame.draw.rect(window, (150, 150, 150), [width / 2 - 300, height / 2 + 160, 600, 80])
                if event.type == pygame.MOUSEBUTTONDOWN:
                    print(calculate_controller('identify_tree_anomalies', cv2.imread(image)))
            else:
                pygame.draw.rect(window, (110, 110, 110), [width / 2 - 300, height / 2 + 160, 600, 80])

        # adding text to the buttons, from top-placed to bottom-placed
        window.blit(import_tree_photo_text, (width / 2 - 240, height / 2 - 190))
        window.blit(calculate_tree_age_text, (width / 2 - 250, height / 2 - 70))
        window.blit(check_growth_conditions_text, (width / 2 - 300, height / 2 + 50))
        window.blit(identify_tree_anomalies_text, (width / 2 - 300, height / 2 + 170))

        pygame.display.update()

    pygame.quit()

gui()