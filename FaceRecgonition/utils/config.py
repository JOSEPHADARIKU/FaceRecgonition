import cv2

class Config:
    RECT_COLOR = (0, 255, 0)
    TEXT_COLOR = (0, 0, 255)
    FONT = cv2.FONT_HERSHEY_SIMPLEX
    ZONE_ONLY = True  # If True, only detect faces inside central zone