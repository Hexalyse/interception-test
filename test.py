import interception
from utils import smooth_move_to, organic_move_to, find_patch_with_threshold
import dxcam
from PIL import Image
import cv2
from time import perf_counter

last_frame = None
def grab_frame(camera):
    global last_frame
    frame = camera.grab()
    if frame is not None:
      last_frame = frame
    return last_frame

interception.auto_capture_devices(keyboard=True, mouse=True)
camera = dxcam.create(output_color="GRAY")
patch = cv2.imread('images/image.png', 0)

t1_start = perf_counter() 
for i in range(50):
  frame = grab_frame(camera)
  match_found = find_patch_with_threshold(patch, frame, 0.98)
  if match_found:
      print('Match found')

t1_stop = perf_counter()
 
print("Elapsed time in seconds:",
                                        t1_stop-t1_start)
print("framerate:", 50/(t1_stop-t1_start))