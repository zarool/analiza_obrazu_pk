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

# todo UI
# todo create label that will return value (pos, color) of picked object
# todo display labels as grid - name on the left, value on the right
# todo buttons change color depending on current state - if button is will not do anything then disable it

# todo maszt
# todo return one contour object as main to follow
# todo add algorithm that will search for object and automatically change parameters of image processing
