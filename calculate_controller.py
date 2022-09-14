from calculate_methods import *
from DATA_ANALISYS import crack_analysis


def calculate_controller(calculate_mode, img):
    center = calculate_center(img)
    height, width = image_size(img)
    img = create_threshold(img)
    summary_lines_points = create_points_in_line(create_lines(center, height, width), center, height, width)
    reduced_summary_points = remove_background(img, summary_lines_points)
    calculate_data, data_for_rings_distance_analisys = points_color_recognition(reduced_summary_points, img)
    tree_rings_growing_score = identify_tree_growth_conditions(data_for_rings_distance_analisys, 11)

    if calculate_mode == 'calculate_age':
        print(f'The tree was {calculate_age(calculate_data)} years old')
        return
    elif calculate_mode == 'tree_growth_conditions':
        return tree_rings_growing_score
    elif calculate_mode == 'identify_tree_anomalies':
        print(f'Tree have {crack_analysis(img)} % of cracks')
