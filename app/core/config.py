"""
Application Configuration
This file contains all configurable parameters used across the project.
Changing values here automatically updates the behavior of the
entire application.
"""

from pathlib import Path

# ===========================
# Project Paths
# ===========================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "data"
VIDEO_DIR = DATA_DIR / "videos"
OUTPUT_DIR = DATA_DIR / "outputs"
MODEL_DIR = PROJECT_ROOT / "models"

# ===========================
# Model Configuration
# ===========================

MODEL_NAME = "models/yolo11n.pt"
GENERAL_MODEL = "models/yolo11n.pt"
EMERGENCY_MODEL = "models/emergency_vehicle.pt"

CONFIDENCE_THRESHOLD = 0.30

IOU_THRESHOLD = 0.50


# ===========================
# Video Configuration
# ===========================

VIDEO_PATH = VIDEO_DIR / "traffic_2min.mp4"

WINDOW_NAME = "Smart Traffic Management System"

FRAME_WIDTH = 1280
FRAME_HEIGHT = 720


# ===========================
# Drawing Configuration
# ===========================

FONT_SCALE = 0.6
FONT_THICKNESS = 2

BOX_THICKNESS = 2


# ===========================
# Supported Vehicle Classes
# ===========================

VEHICLE_CLASSES = {
    "car",
    "bus",
    "truck",
    "motorcycle",
    "bicycle"
}
# Emergency Vehicle Classes

EMERGENCY_CLASSES = {

    "ambulance",

    "fire_truck",

    "police_car",

}
# -----------------------------------------
# Stopped Vehicle Detection
# -----------------------------------------

STOPPED_TIME_THRESHOLD = 6.0      # seconds

STOPPED_DISTANCE_THRESHOLD = 10.0 # pixels
