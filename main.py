"""
VigilEye AI: Real-Time Driver Drowsiness Detection System
Main Entrypoint Application
"""

import sys
import time
import cv2
import numpy as np

from src.config import (
    CAMERA_INDEX,
    FRAME_WIDTH,
    FRAME_HEIGHT,
    EAR_THRESHOLD,
    CONSECUTIVE_FRAMES,
    ALERT_SOUND_PATH,
)
from src.ear_calculator import calculate_ear
from src.alerts import AlertSystem, draw_hud, draw_eye_contours
from src.face_mesh_detector import FaceMeshDetector


def run_pipeline():
    print("=" * 60)
    print("  VIGIL-EYE AI: REAL-TIME DRIVER DROWSINESS DETECTION  ")
    print("=" * 60)

    # 1. Initialize Webcam Video Capture
    print(f"[*] Initializing camera stream (Index: {CAMERA_INDEX})...")
    cap = cv2.VideoCapture(CAMERA_INDEX)
    
    # Configure resolution
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

    if not cap.isOpened():
        print(f"[Error] Could not access webcam at index {CAMERA_INDEX}.")
        print("[*] Please check if camera is connected and not in use by another app.")
        return

    # 2. Initialize MediaPipe Detector and Alert System
    detector = FaceMeshDetector(max_num_faces=1, refine_landmarks=True)
    alert_system = AlertSystem(sound_file=ALERT_SOUND_PATH)

    # 3. State Variables
    frame_counter = 0
    drowsiness_detected = False
    prev_time = time.time()

    print("[*] Video pipeline started successfully. Press 'q' to quit.")

    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("[Warning] Empty or dropped frame received. Retrying...")
                time.sleep(0.01)
                continue

            # Mirror view for natural interaction
            frame = cv2.flip(frame, 1)

            # Process Facial Landmarks
            left_eye, right_eye, face_landmarks = detector.extract_eye_landmarks(frame)

            avg_ear = 0.0

            if left_eye is not None and right_eye is not None:
                # Calculate EAR for both eyes
                left_ear = calculate_ear(left_eye)
                right_ear = calculate_ear(right_eye)
                avg_ear = (left_ear + right_ear) / 2.0

                # Render eye contours
                contour_color = (0, 0, 255) if drowsiness_detected else ((0, 255, 255) if avg_ear < EAR_THRESHOLD else (0, 255, 0))
                draw_eye_contours(frame, left_eye, color=contour_color)
                draw_eye_contours(frame, right_eye, color=contour_color)

                # Drowsiness Decision Logic
                if avg_ear < EAR_THRESHOLD:
                    frame_counter += 1
                    if frame_counter >= CONSECUTIVE_FRAMES:
                        drowsiness_detected = True
                        alert_system.trigger_audio_alarm()
                else:
                    frame_counter = 0
                    if drowsiness_detected:
                        drowsiness_detected = False
                        alert_system.stop_audio_alarm()
            else:
                # No face detected: reset counter safely and silence alarm
                frame_counter = 0
                if drowsiness_detected:
                    drowsiness_detected = False
                    alert_system.stop_audio_alarm()

            # Render HUD and Visual Alerts
            draw_hud(
                frame=frame,
                ear=avg_ear,
                threshold=EAR_THRESHOLD,
                frame_count=frame_counter,
                max_frames=CONSECUTIVE_FRAMES,
                drowsiness_detected=drowsiness_detected
            )

            # Display Output Window
            cv2.imshow("VigilEye AI - Real-Time Driver Drowsiness Monitor", frame)

            # Key Controls
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q') or key == 27:  # 'q' or ESC
                print("[*] User initiated exit.")
                break
            elif key == ord('r'):  # 'r' to reset
                frame_counter = 0
                drowsiness_detected = False
                alert_system.stop_audio_alarm()
                print("[*] Alert state reset.")

    except KeyboardInterrupt:
        print("\n[*] Program interrupted by user.")
    finally:
        # Cleanup Resources
        print("[*] Cleaning up resources...")
        alert_system.stop_audio_alarm()
        detector.close()
        cap.release()
        cv2.destroyAllWindows()
        print("[*] Pipeline closed successfully.")


if __name__ == "__main__":
    run_pipeline()
