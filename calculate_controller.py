from calculate_methods import *


def calculate_controller(calculate_mode, img):
    if calculate_mode == 'calculate_age':
        center = calculate_center(img)
        height, width = image_size(img)
        img = create_threshold(img)
        summary_lines_points = create_points_in_line(create_lines(center, height, width), center, height, width)
        reduced_summary_points = remove_background(img, summary_lines_points)
        calculate_data, data_for_rings_distance_analisys = points_color_recognition(reduced_summary_points, img)
        return f'The tree was {calculate_age(calculate_data)} years old'
    elif calculate_mode == 'tree_growth_conditions':
        center = calculate_center(img)
        height, width = image_size(img)
        img = create_threshold(img)
        summary_lines_points = create_points_in_line(create_lines(center, height, width), center, height, width)
        reduced_summary_points = remove_background(img, summary_lines_points)
        calculate_data, data_for_rings_distance_analisys = points_color_recognition(reduced_summary_points, img)
        tree_rings_growing_score = identify_tree_growth_conditions(data_for_rings_distance_analisys, 11)
        return tree_rings_growing_score
    elif calculate_mode == 'identify_tree_anomalies':
        return f'Tree have {crack_analysis(img)} % of cracks'
