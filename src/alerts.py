"""
Module for audio alerts and visual UI overlays (Day 2 requirements).
"""

import os
import wave
import struct
import math
import cv2
import numpy as np
import pygame

# Initialize pygame mixer safely
try:
    pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
    _MIXER_INITIALIZED = True
except Exception as e:
    print(f"[Warning] Failed to initialize pygame mixer: {e}")
    _MIXER_INITIALIZED = False


def _generate_sine_wave_file(filepath: str, duration_sec: float = 1.0, freq: int = 1200):
    """
    Generate a pure high-pitch sine wave alert WAV file if assets are not present.
    """
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    sample_rate = 44100
    num_samples = int(sample_rate * duration_sec)
    
    with wave.open(filepath, 'w') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 16-bit
        wav_file.setframerate(sample_rate)
        
        for i in range(num_samples):
            # Create beep burst pattern (e.g. oscillating alarm)
            t = float(i) / sample_rate
            mod = 1.0 if (int(t * 10) % 2 == 0) else 0.4
            value = int(32767.0 * 0.5 * mod * math.sin(2.0 * math.pi * freq * t))
            data = struct.pack('<h', value)
            wav_file.writeframesraw(data)


class AlertSystem:
    def __init__(self, sound_file="assets/alarm.wav"):
        self.sound_file = sound_file
        self.sound = None
        self.is_playing = False
        self._init_sound()

    def _init_sound(self):
        if not _MIXER_INITIALIZED:
            return
        
        if not os.path.exists(self.sound_file):
            try:
                _generate_sine_wave_file(self.sound_file)
            except Exception as e:
                print(f"[Warning] Could not generate fallback sound: {e}")
                return

        try:
            self.sound = pygame.mixer.Sound(self.sound_file)
        except Exception as e:
            print(f"[Warning] Failed to load alert sound file: {e}")

    def trigger_audio_alarm(self):
        """
        Play alert sound in a non-blocking loop if not already playing.
        """
        if not _MIXER_INITIALIZED or self.sound is None:
            return

        if not self.is_playing:
            self.sound.play(loops=-1)  # Continuous loop until stopped
            self.is_playing = True

    def stop_audio_alarm(self):
        """
        Stop alert sound.
        """
        if not _MIXER_INITIALIZED or self.sound is None:
            return

        if self.is_playing:
            self.sound.stop()
            self.is_playing = False


def draw_eye_contours(frame, eye_coords, color=(0, 255, 0)):
    """
    Draw polygon contours around detected eye landmarks.
    """
    if eye_coords is not None and len(eye_coords) > 0:
        pts = np.array(eye_coords, np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv2.polylines(frame, [pts], isClosed=True, color=color, thickness=1, lineType=cv2.LINE_AA)
        for pt in eye_coords:
            cv2.circle(frame, tuple(pt), 2, color, -1, lineType=cv2.LINE_AA)


def draw_hud(frame, ear: float, threshold: float, frame_count: int, max_frames: int, drowsiness_detected: bool):
    """
    Draw professional real-time HUD with telemetry, EAR gauges, and alert banner.
    """
    h, w, _ = frame.shape

    # Top Status Bar Background
    overlay = frame.copy()
    cv2.rectangle(overlay, (0, 0), (w, 70), (20, 20, 20), -1)
    
    # Bottom Telemetry Bar Background
    cv2.rectangle(overlay, (0, h - 45), (w, h), (20, 20, 20), -1)
    cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)

    # Status Indicators
    title_text = "VIGIL-EYE AI | DRIVER MONITORING SYSTEM"
    cv2.putText(frame, title_text, (20, 28), cv2.FONT_HERSHEY_DUPLEX, 0.7, (240, 240, 240), 1, cv2.LINE_AA)

    # EAR metric display
    state_color = (0, 0, 255) if drowsiness_detected else ((0, 255, 255) if ear < threshold else (0, 255, 0))
    ear_text = f"EAR: {ear:.3f} (Threshold: {threshold:.2f})"
    cv2.putText(frame, ear_text, (20, 56), cv2.FONT_HERSHEY_DUPLEX, 0.65, state_color, 2, cv2.LINE_AA)

    # Frame continuity progress bar
    bar_x = w - 240
    bar_y = 25
    bar_w = 200
    bar_h = 16
    progress = min(1.0, frame_count / float(max_frames)) if max_frames > 0 else 0
    cv2.rectangle(frame, (bar_x, bar_y), (bar_x + bar_w, bar_y + bar_h), (80, 80, 80), 1)
    fill_w = int(bar_w * progress)
    fill_color = (0, 0, 255) if progress >= 1.0 else ((0, 255, 255) if progress > 0.5 else (0, 255, 0))
    cv2.rectangle(frame, (bar_x + 1, bar_y + 1), (bar_x + fill_w, bar_y + bar_h - 1), fill_color, -1)
    cv2.putText(frame, f"CLOSURE: {frame_count}/{max_frames}", (bar_x, 56), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (200, 200, 200), 1, cv2.LINE_AA)

    # Bottom Instructions
    cv2.putText(frame, "Press 'Q' or 'ESC' to Exit | Press 'R' to Reset Counter", (20, h - 16), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (180, 180, 180), 1, cv2.LINE_AA)

    # Prominent Warning Banner if Drowsiness is Detected
    if drowsiness_detected:
        # Flashing red alert banner
        banner_h = 90
        center_y = h // 2
        banner_overlay = frame.copy()
        cv2.rectangle(banner_overlay, (0, center_y - banner_h // 2), (w, center_y + banner_h // 2), (0, 0, 180), -1)
        cv2.addWeighted(banner_overlay, 0.85, frame, 0.15, 0, frame)
        
        cv2.rectangle(frame, (0, center_y - banner_h // 2), (w, center_y + banner_h // 2), (0, 0, 255), 3)

        alert_text = "! DROWSINESS DETECTED: WAKE UP !"
        text_size = cv2.getTextSize(alert_text, cv2.FONT_HERSHEY_DUPLEX, 1.1, 2)[0]
        text_x = (w - text_size[0]) // 2
        text_y = center_y + (text_size[1] // 2)
        cv2.putText(frame, alert_text, (text_x, text_y), cv2.FONT_HERSHEY_DUPLEX, 1.1, (255, 255, 255), 2, cv2.LINE_AA)


# Self-test block for Day 2 independent verification with dummy variables
if __name__ == "__main__":
    print("[Testing alerts.py independently with dummy variables...]")
    dummy_frame = np.zeros((720, 1280, 3), dtype=np.uint8)
    alert = AlertSystem()
    print("Simulating SAFE state...")
    draw_hud(dummy_frame, ear=0.32, threshold=0.25, frame_count=0, max_frames=20, drowsiness_detected=False)
    print("Simulating DROWSINESS DETECTED state...")
    draw_hud(dummy_frame, ear=0.18, threshold=0.25, frame_count=25, max_frames=20, drowsiness_detected=True)
    alert.trigger_audio_alarm()
    pygame.time.delay(500)
    alert.stop_audio_alarm()
    print("Alerts module test passed successfully!")
