import interception
import time
import math

def smooth_move_to(target_x, target_y, duration_ms):
    start_x, start_y = interception.mouse_position()
    distance_x = target_x - start_x
    distance_y = target_y - start_y
    steps = int(duration_ms / 10)  # Number of steps based on duration and update interval (10ms)
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