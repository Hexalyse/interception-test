import interception
from utils import matchTemplate_with_threshold, grab_frame
import dxcam
import cv2
from time import perf_counter



interception.auto_capture_devices(keyboard=True, mouse=True)
camera = dxcam.create(output_color="GRAY")
patch = cv2.imread('images/image2.png', 0)

t1_start = perf_counter() 
for i in range(50):
  frame = grab_frame(camera)
  match_found = matchTemplate_with_threshold(patch, frame, 0.98)
  if match_found:
      print('Match found')

t1_stop = perf_counter()
 
print("Elapsed time in seconds:",
                                        t1_stop-t1_start)
print("framerate:", 50/(t1_stop-t1_start))