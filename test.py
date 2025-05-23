import interception
from utils import get_center_of_match, smooth_move_to, organic_move_to, matchTemplate_with_threshold, findAllTemplate_with_threshold, grab_frame, check_images_similar
import dxcam
import cv2
import random
import time

def generate_mouse_delay():
    return random.randint(30, 100) / 1000

interception.auto_capture_devices(keyboard=True, mouse=True)
camera = dxcam.create(output_color="BGR")
patch = cv2.imread('images/image.png')


frame = grab_frame(camera)
# position patch should be : 359, 34
# use dimension of patch
cut_frame = frame[0:patch.shape[0], 0:patch.shape[1]]
# display cut_frame
match_found = matchTemplate_with_threshold(patch, cut_frame, 0.98, debug=True)
#match_found = matchTemplate_with_threshold(patch, frame, 0.98)
print(match_found)
# display frame
similar = check_images_similar(patch, cut_frame, 0, 90, debug=True)
print(similar)

# Start the timer
start_time = time.time()

# Repeat the function 100 times
for _ in range(1000):
    matchTemplate_with_threshold(patch, frame, 0.98)

# Stop the timer
end_time = time.time()

# Calculate the elapsed time
elapsed_time = end_time - start_time

# print framerate
print(f"Elapsed time: {elapsed_time:.2f} seconds")
print(f"Frame rate: {1000 / elapsed_time:.2f} frames per second")

# Start the timer
start_time = time.time()

# Repeat the function 100 times
for _ in range(10000):
    check_images_similar(patch, cut_frame, 0, 90)

# Stop the timer
end_time = time.time()

# Calculate the elapsed time
elapsed_time = end_time - start_time

# print framerate
print(f"Elapsed time: {elapsed_time:.2f} seconds")
print(f"Frame rate: {10000 / elapsed_time:.2f} frames per second")