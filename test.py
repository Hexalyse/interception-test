import interception
from utils import smooth_move_to, organic_move_to


interception.auto_capture_devices(keyboard=True, mouse=True, verbose=True)

organic_move_to(500, 500, 1000)