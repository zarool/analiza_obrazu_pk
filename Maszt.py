import cv2

from Camera import Camera
from Utils import Utils
from Window import Window

# [WIDTH, HEIGHT, FPS]
CAMERA_MODES = [
    [3264, 2454, 21],
    [3264, 1848, 28],
    [1920, 1090, 30],
    [1640, 1232, 30],
    [1280, 720, 60],
    [1280, 720, 120]
]


class Maszt:
    def __init__(self, cam_disp=1, contour=0, detect=1, info=1, flip=0, current=0, mode=0, display_w=600, display_h=400,
                 object_w=4, object_l=15):
        # system arguments default values
        self.cam_disp = cam_disp
        self.contour = contour
        self.detect = detect
        self.info = info
        self.current_img = current

        # 0 - default, 2 - turn 180 [deg]
        self.FLIP = flip

        # display window size
        self.display_w = display_w
        self.display_h = display_h

        # CAPTURE MODE
        # all modes in main configuration script file
        self.WIDTH = CAMERA_MODES[mode][0]
        self.HEIGHT = CAMERA_MODES[mode][1]
        self.FPS = CAMERA_MODES[mode][2]

        # OBJECT TO DETECT
        self.OBJECT_W = object_w  # [cm]
        self.OBJECT_L = object_l  # [cm]

        # BOOL to don't open camera twice at beginning of program (used for changing exposure in set_exposure())
        self.RUN = False

        # OBJECT CAMERA
        self.camera_obj = Camera(self.WIDTH, self.HEIGHT, self.FPS, self.FLIP)

        # OPENCV CAMERA OBJECT, VIDEO FROM THAT OBJECT, IMAGES TO READ FROM
        self.camera, self.video, self.images = self.camera_obj.prepare_devices(self.cam_disp)
        print(self.images)

        # WINDOW OBJECT
        self.window = Window()
        cv2.createTrackbar("Exposure", self.window.window_option, 20, 40, self.set_exposure)

        # UTILS
        self.utils = Utils()

    def update_image_param(self, threshold1, threshold2, min_area, max_area, brightness_v, contrast_v, lower_color,
                           upper_color):
        self.window.threshold1 = threshold1
        self.window.threshold2 = threshold2
        self.window.min_area = min_area
        self.window.max_area = max_area
        self.window.brightness_v = brightness_v
        self.window.contrast_v = contrast_v
        self.window.lower_color = lower_color
        self.window.upper_color = upper_color

    def update_image_exposure(self, exposure_value):
        self.set_exposure(exposure_value)

    def set_exposure(self, value):
        if self.RUN:
            exp_value = (value - 20) / 10

            # reset camera and create new one with different exposure
            self.camera.cap.release()
            self.camera = None
            self.camera = self.camera_obj.run_camera(exposure=exp_value)

    def start(self):

        # updating trackbars
        # COMMENT IF NOT USING OPENCV WINDOW MANAGER
        self.window.get_trackbar_value()

        # 0
        # capturing video frame
        if self.camera:
            if self.camera is not None:
                image = self.camera.read()
                self.RUN = True
            else:
                _, image = self.video.read()
        else:
            # capturing image
            img = self.images[self.current_img]
            image = cv2.resize(img, (640, 640))

        # ===============

        # 1
        # image operations to get black and white contours
        image = self.utils.masking(image, self.window.lower_color, self.window.upper_color)
        image, contours = Utils.get_contours(image, [self.window.threshold1, self.window.threshold2],
                                             self.window.contrast_v, self.window.brightness_v,
                                             draw=self.contour)

        # 2
        # detecting squares from image and returning it with square contours
        # finals_contours = [index, x, y, w, h [straight rectangle around object], box corner points [box],
        # width [cm], height [cm], color]
        image, final_contours = self.utils.detect_square(contours, image, self.window.min_area, self.window.max_area,
                                                         self.OBJECT_W, self.OBJECT_L)

        # 3
        # display detected rectangles and
        # display info about length, width and color
        self.utils.display_info(image, final_contours, draw_detect=self.detect, draw_info=self.info)

        # 4
        # showing final image
        cv2.imshow(self.window.window_main, image)

        # KEYBOARD HANDLING
        # keyboard functionality - only when not using camera, because it slows the program
        if not self.cam_disp:
            if cv2.waitKey(50) == ord('n'):
                self.current_img = self.current_img + 1 if self.current_img < 12 else 0
                print(f"Current image: cam{self.current_img}.jpg")
            if cv2.waitKey(50) == ord('b'):
                current_img = self.current_img - 1 if self.current_img > 0 else 12
                print(f"Current image: cam{current_img}.jpg")

    def close(self):
        # closing camera only if using it
        if self.camera is not None:
            self.camera.cap.release()
        elif self.video is not None:
            self.video.release()
        cv2.destroyAllWindows()
