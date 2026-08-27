# VigilEye AI - Real-Time Driver Drowsiness Detection System

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-green.svg)](https://opencv.org/)
[![MediaPipe](https://img.shields.io/badge/MediaPipe-Face%20Mesh-orange.svg)](https://developers.google.com/mediapipe)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**VigilEye AI** is a lightweight, edge-ready computer vision application designed to prevent road accidents caused by driver fatigue and micro-sleep. By tracking 468 3D facial landmarks with Google MediaPipe Face Mesh, calculating the Eye Aspect Ratio (EAR), and evaluating consecutive frame closure metrics, VigilEye AI triggers instantaneous audio-visual alerts to re-engage the driver.

---

## 🌟 Key Features
- **Real-Time 3D Landmark Tracking**: Utilizes Google MediaPipe Face Mesh for fast sub-millisecond facial landmark extraction.
- **Robust Mathematical Modeling**: Computes Euclidean-distance-based Eye Aspect Ratio (EAR) per eye to distinguish normal blinking from micro-sleep episodes.
- **Asynchronous Audio Alerts**: Integrates `pygame.mixer` for zero-latency, non-blocking audio alerts with built-in procedural tone generation (no external audio files required).
- **Driver Telemetry HUD**: Clean OpenCV visual overlay presenting real-time EAR metrics, eye contours, closure progress bars, and high-visibility flashing warning banners.

---

## 📐 Mathematical Architecture (Eye Aspect Ratio - EAR)

The Eye Aspect Ratio (EAR) measures the ratio of the eye's vertical opening distance to its horizontal width. For each eye defined by 6 2D/3D landmark coordinates ($p_1, p_2, p_3, p_4, p_5, p_6$):

$$\text{EAR} = \frac{\|p_2 - p_6\|_2 + \|p_3 - p_5\|_2}{2 \cdot \|p_1 - p_4\|_2}$$

Where:
- $p_1, p_4$: Horizontal eye corner landmark points.
- $(p_2, p_6)$ and $(p_3, p_5)$: Upper and lower eyelid landmark coordinate pairs.
- $\|\cdot\|_2$: Euclidean distance norm.

$$\text{EAR}_{\text{average}} = \frac{\text{EAR}_{\text{left}} + \text{EAR}_{\text{right}}}{2}$$

```
           p2     p3
          /  \   /  \
     p1 o             o p4   (Horizontal distance: ||p1 - p4||)
          \  /   \  /
           p6     p5
```

### MediaPipe Landmark Index Mapping
- **Left Eye Indices**: `[362, 385, 387, 263, 373, 380]`
- **Right Eye Indices**: `[33, 160, 158, 133, 153, 144]`

---

## 📂 Project Architecture

```
VigilEye-AI/
├── assets/
│   └── alarm.wav                # High-frequency alert audio (auto-generated fallback)
├── src/
│   ├── __init__.py
│   ├── config.py                # Tuning parameters (EAR threshold, frames, indices)
│   ├── ear_calculator.py        # Euclidean vector distance & EAR formulas
│   ├── face_mesh_detector.py    # MediaPipe Face Mesh processing wrapper
│   └── alerts.py                # Asynchronous audio alarm & OpenCV HUD visualizer
├── main.py                      # Core execution loop & state machine
├── requirements.txt             # Project dependencies
├── .gitignore
└── README.md
```

---

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/Prateek-Dhar-Dwivedi/VigilEye-AI.git
cd VigilEye-AI
```

### 2. Create and Activate a Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run VigilEye AI
```bash
python main.py
```

---

## ⚙️ Configuration & Tuning

You can easily adjust sensitivity parameters in `src/config.py`:
- `EAR_THRESHOLD`: Default `0.25` (lower values for individuals with naturally narrower eyes).
- `CONSECUTIVE_FRAMES`: Default `20` (at 30 FPS, ~0.66 seconds of continuous eye closure triggers the alarm).

---

## 🎮 Interactive Controls
- `Q` or `ESC`: Exit application.
- `R`: Reset alarm and continuity counters.

---

## 👥 Contributors & Collaboration
- **Day 1**: Base pipeline setup, camera capture loop, and virtual environment configuration.
- **Day 2**: MediaPipe Face Mesh landmark extraction, EAR math engine, and Pygame audio-visual alert subsystems.
- **Day 3**: Integration, multi-device calibration, stress testing, and documentation.


