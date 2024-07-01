from app.App import App
from system.args import arguments
import cv2

# CONSTANT
(CAMERA_DISP, WINDOW_DRAW_CONT, WINDOW_DRAW_DETECT, WINDOW_DRAW_INFO, CURRENT_IMG, CAPTURE_FLIP, RENDER_WIDTH,
 RENDER_HEIGHT, CAPTURE_MODE, CAPTURE_WIDTH, CAPTURE_HEIGHT, CAPTURE_FPS) = arguments()

app = App(cam_disp=CAMERA_DISP, contour=WINDOW_DRAW_CONT, detect=WINDOW_DRAW_DETECT, info=WINDOW_DRAW_INFO,
          flip=CAPTURE_FLIP, current=CURRENT_IMG, mode=CAPTURE_MODE, display_w=RENDER_WIDTH, display_h=RENDER_HEIGHT)

while True:
    app.run()

# todo modernize maszt code to be more readable

# todo maszt
# todo add algorithm that will search for object and automatically change parameters of image processing
