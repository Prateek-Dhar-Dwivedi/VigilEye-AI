# Configuration Parameters for VigilEye AI

# Eye Aspect Ratio (EAR) Thresholds
EAR_THRESHOLD = 0.25
CONSECUTIVE_FRAMES = 20  # Number of consecutive frames with EAR < threshold to trigger alarm

# MediaPipe Face Mesh Eye Landmark Indices
# Left eye indices: 6 points (horizontal corners, vertical top & bottom pairs)
LEFT_EYE_INDICES = [362, 385, 387, 263, 373, 380]

# Right eye indices: 6 points
RIGHT_EYE_INDICES = [33, 160, 158, 133, 153, 144]

# Webcam Settings
CAMERA_INDEX = 0
FRAME_WIDTH = 1280
FRAME_HEIGHT = 720

# UI Colors (BGR Format)
COLOR_SAFE = (0, 255, 0)      # Green
COLOR_WARNING = (0, 0, 255)   # Red
COLOR_INFO = (255, 255, 255)  # White
COLOR_BG = (30, 30, 30)       # Dark Gray

# Sound Settings
ALERT_SOUND_PATH = "assets/alarm.wav"
AUDIO_FREQUENCY = 1000  # Hz pure tone for procedural fallback
AUDIO_DURATION = 1.0    # Seconds
