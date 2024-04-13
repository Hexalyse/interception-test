import interception
from utils import get_center_of_match, smooth_move_to, organic_move_to, matchTemplate_with_threshold, findAllTemplate_with_threshold, grab_frame
import dxcam
import cv2
import random
import time

def generate_mouse_delay():
    return random.randint(30, 100) / 1000

interception.auto_capture_devices(keyboard=True, mouse=True)
camera = dxcam.create(output_color="GRAY")
patch = cv2.imread('images/image2.png', 0)


frame = grab_frame(camera)
matches = findAllTemplate_with_threshold(patch, frame, 0.98)
print

for match in matches:
    center = get_center_of_match(match, patch)
    organic_move_to(center[0], center[1], 200, generate_mouse_delay())
    #interception.mouse_down("left", generate_mouse_delay())
    #interception.mouse_up("left", 0)
    time.sleep(0.5)
