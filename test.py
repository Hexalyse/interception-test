import interception
from utils import smooth_move_to, organic_move_to, find_patch_with_threshold
import dxcam
from PIL import Image
import cv2

camera = dxcam.create(output_color="BGR")

interception.auto_capture_devices(keyboard=True, mouse=True)
frame = camera.grab()

patch = cv2.imread('images/firefox.png')
match_found = find_patch_with_threshold(patch, frame, 0.998, debug=True)
if match_found:
    print('Match found')