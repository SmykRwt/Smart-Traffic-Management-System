"""
Color definitions used throughout the application.

All colors are stored in BGR format because OpenCV
uses BGR instead of RGB.
"""

# Vehicle Colors

CAR_COLOR = (0, 255, 0)

BUS_COLOR = (255, 0, 0)

TRUCK_COLOR = (0, 165, 255)

MOTORCYCLE_COLOR = (255, 255, 0)

BICYCLE_COLOR = (255, 0, 255)

PERSON_COLOR = (0, 255, 255)


DEFAULT_COLOR = (255, 255, 255)


CLASS_COLORS = {

    "car": CAR_COLOR,

    "bus": BUS_COLOR,

    "truck": TRUCK_COLOR,

    "motorcycle": MOTORCYCLE_COLOR,

    "bicycle": BICYCLE_COLOR,

    "person": PERSON_COLOR,

    "ambulance": (0, 165, 255),      # Orange/Red

    "fire_truck": (0, 0, 255),       # Red

    "police_car": (255, 0, 0),       # Blue
}