import interception
import time
import math
import random
import cv2
import numpy as np

last_frame = None


def grab_frame(camera):
    global last_frame
    frame = camera.grab()
    if frame is not None:
        last_frame = frame
    return last_frame


def smooth_move_to(target_x, target_y, duration_ms):
    start_x, start_y = interception.mouse_position()
    distance_x = target_x - start_x
    distance_y = target_y - start_y
    steps = int(
        duration_ms / 10
    )  # Number of steps based on duration and update interval (10ms)
    for i in range(steps):
        progress = i / steps
        # Apply ease-in and ease-out effect
        progress -= math.sin(2 * math.pi * progress) / (2 * math.pi)

        # Calculate intermediate position
        current_x = start_x + distance_x * progress
        current_y = start_y + distance_y * progress

        # Move the mouse to the new position
        interception.move_to(int(current_x), int(current_y))
        time.sleep(0.01)  # Wait for a short period before moving to the next position

    # Ensure the mouse ends up at the exact target position
    interception.move_to(target_x, target_y)


def organic_move_to(target_x, target_y, duration_ms, delay_after=0.0):
    start_x, start_y = interception.mouse_position()
    steps = int(duration_ms / 10)
    distance_x = abs(target_x - start_x)
    distance_y = abs(target_y - start_y)

    # Control points for Bezier curve, with random deviation
    mid_x = (start_x + target_x) / 2 + random.randint(
        int(-distance_x / 7), int(distance_x / 7)
    )
    mid_y = (start_y + target_y) / 2 + random.randint(
        int(-distance_y / 7), int(distance_y / 7)
    )

    # Adding horizontal deviation if the movement is mostly vertical
    if (
        distance_x <= distance_y / 4
    ):  # if the x distance is significantly less than the y distance
        mid_x += random.randint(
            int(-distance_y / 7), int(distance_y / 7)
        )  # horizontal deviation

    for i in range(steps):
        progress = i / steps
        progress -= math.sin(2 * math.pi * progress) / (2 * math.pi)

        one_minus_t = 1 - progress
        current_x = (
            one_minus_t * one_minus_t * start_x
            + 2 * one_minus_t * progress * mid_x
            + progress * progress * target_x
        )
        current_y = (
            one_minus_t * one_minus_t * start_y
            + 2 * one_minus_t * progress * mid_y
            + progress * progress * target_y
        )

        # Move the mouse to the new position
        interception.move_to(int(current_x), int(current_y))
        time.sleep(0.01)  # Pause for smooth transition

    # Ensure the mouse ends up at the exact target position
    interception.move_to(target_x, target_y)
    if delay_after > 0:
        time.sleep(delay_after)


def matchTemplate_with_threshold(
    patch, image, similarity_threshold, debug=False, showMatched=False
):
    # Ensure the input threshold is within the expected range
    if not (0 <= similarity_threshold <= 1):
        raise ValueError("The similarity threshold must be between 0 and 1.")

    # Perform the matching operation
    result = cv2.matchTemplate(image, patch, cv2.TM_CCORR_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)
    if debug:
        print(f"Max similarity: {max_val}")
    if showMatched:
        top_left = max_loc
        bottom_right = (top_left[0] + patch.shape[0], top_left[1] + patch.shape[1])
        # Draw a rectangle around the matched region
        cv2.rectangle(image, top_left, bottom_right, 255, 2)
        resized = cv2.resize(image, (1920, 1080))
        cv2.imshow("Matched Image", resized)
        cv2.waitKey(0)

    # Return True if the best match meets or exceeds the percentage threshold, otherwise False
    return max_val >= similarity_threshold


def findAllTemplate_with_threshold(
    patch, image, similarity_threshold, debug=False, showMatched=False
):
    # Ensure the input threshold is within the expected range
    if not (0 <= similarity_threshold <= 1):
        raise ValueError("The similarity threshold must be between 0 and 1.")

    # Perform the matching operation
    result = cv2.matchTemplate(image, patch, cv2.TM_CCORR_NORMED)
    loc = np.where(result >= similarity_threshold)
    locations = list(zip(*loc[::-1]))
    if debug:
        print(f"Matches: {locations}")
    if showMatched:
        for pt in locations:
            top_left = pt
            bottom_right = (top_left[0] + patch.shape[0], top_left[1] + patch.shape[1])
            # Draw a rectangle around the matched region
            cv2.rectangle(image, top_left, bottom_right, 255, 2)
        resized = cv2.resize(image, (1920, 1080))
        cv2.imshow("Matched Image", resized)
        cv2.waitKey(0)

    # Return True if the best match meets or exceeds the percentage threshold, otherwise False
    return locations


def image_at_position(image, patch, position, threshold, percentage_similar):
    # Extract the region of the image around the specified position
    cut_frame = image[
        position[1] : position[1] + patch.shape[0],
        position[0] : position[0] + patch.shape[1],
    ]
    # Check if the extracted region is similar to the patch
    return check_images_similar(cut_frame, patch, threshold, percentage_similar)


# Use this to compare images with a threshold and percentage of similarity
# This is faster than calling matchTemplate_with_threshold on two images of the same size
def check_images_similar(image1, image2, threshold, percentage_similar, debug=False):
    # Calculate the absolute differences between the two images
    differences = np.abs(image1 - image2)
    
    # Check if differences are less than the threshold
    similar_pixels = differences <= threshold
    
    # Calculate the percentage of pixels that are similar
    total_pixels = similar_pixels.size
    similar_count = np.sum(similar_pixels)
    similar_percentage = (similar_count / total_pixels) * 100

    if debug:
        print(f"Similarity: {similar_percentage:.2f}%")
    
    # Return True if the percentage of similar pixels is at least percentage_similar
    return similar_percentage >= percentage_similar


def check_pixel_color(image, position, color, threshold=0):
    # Extract the color of the pixel at the specified position
    pixel_color = image[position[1], position[0]]
    # Check if the pixel color matches the expected color within the threshold
    return all(abs(pixel_color[i] - color[i]) <= threshold for i in range(3))


def check_pixel_grayscale(image, position, color, threshold=0):
    # Extract the color of the pixel at the specified position
    pixel_color = image[position[1], position[0]]
    # Check if the pixel color matches the expected color within the threshold
    return abs(pixel_color - color) <= threshold


def get_center_of_match(location, patch):
    return location[0] + patch.shape[0] / 2, location[1] + patch.shape[1] / 2
