"""
MediaPipe Face Mesh Detector wrapper for facial landmark and eye coordinate extraction.
"""

import cv2
import mediapipe as mp
import numpy as np
from src.config import LEFT_EYE_INDICES, RIGHT_EYE_INDICES


class FaceMeshDetector:
    def __init__(self, max_num_faces=1, refine_landmarks=True, min_detection_confidence=0.5, min_tracking_confidence=0.5):
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=max_num_faces,
            refine_landmarks=refine_landmarks,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence
        )

    def extract_eye_landmarks(self, frame):
        """
        Processes a BGR frame, runs MediaPipe Face Mesh, and extracts
        pixel coordinates (x, y) for both left and right eyes.
        
        Returns:
            tuple: (left_eye_coords, right_eye_coords, raw_face_landmarks)
                   Returns (None, None, None) if no face detected.
        """
        h, w, _ = frame.shape
        # Convert BGR to RGB for MediaPipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        rgb_frame.flags.writeable = False
        results = self.face_mesh.process(rgb_frame)
        rgb_frame.flags.writeable = True

        if not results.multi_face_landmarks:
            return None, None, None

        # Primary face
        face_landmarks = results.multi_face_landmarks[0]

        left_eye_coords = []
        for idx in LEFT_EYE_INDICES:
            lm = face_landmarks.landmark[idx]
            left_eye_coords.append((int(lm.x * w), int(lm.y * h)))

        right_eye_coords = []
        for idx in RIGHT_EYE_INDICES:
            lm = face_landmarks.landmark[idx]
            right_eye_coords.append((int(lm.x * w), int(lm.y * h)))

        return left_eye_coords, right_eye_coords, face_landmarks

    def close(self):
        self.face_mesh.close()
