"""
Module for mathematical computation of the Eye Aspect Ratio (EAR).
"""

import numpy as np


def euclidean_distance(pt1, pt2):
    """
    Calculate Euclidean distance between two 2D/3D points.
    """
    return np.linalg.norm(np.array(pt1) - np.array(pt2))


def calculate_ear(eye_landmarks):
    """
    Calculate the Eye Aspect Ratio (EAR) for a given eye.
    
    Formula:
        EAR = (||p2 - p6|| + ||p3 - p5||) / (2 * ||p1 - p4||)
        
    Parameters:
        eye_landmarks (list of tuples/arrays): 6 (x, y) coordinates representing
            p1: Left corner
            p2: Top-left vertical
            p3: Top-right vertical
            p4: Right corner
            p5: Bottom-right vertical
            p6: Bottom-left vertical
            
    Returns:
        float: Computed Eye Aspect Ratio
    """
    if len(eye_landmarks) != 6:
        raise ValueError(f"Expected 6 landmarks for eye EAR calculation, got {len(eye_landmarks)}")

    # Vertical landmark distances
    vertical_1 = euclidean_distance(eye_landmarks[1], eye_landmarks[5])  # ||p2 - p6||
    vertical_2 = euclidean_distance(eye_landmarks[2], eye_landmarks[4])  # ||p3 - p5||

    # Horizontal landmark distance
    horizontal = euclidean_distance(eye_landmarks[0], eye_landmarks[3])  # ||p1 - p4||

    if horizontal == 0:
        return 0.0

    ear = (vertical_1 + vertical_2) / (2.0 * horizontal)
    return float(ear)
