import cv2
import numpy as np
import utils
import system

# system arguments default values
default_disp_cam = 1
default_contour = 0
default_detect = 1
default_info = 1
default_flip = 0

# CAPTURE MODE
# all modes in main configuration script file
WIDTH = 3264
HEIGHT = 2464
FPS = 21
# 0 - default, 2 - turn 180 [deg]
FLIP = 0

# OBJECT TO DETECT
OBJECT_W = 4  # [cm]
OBJECT_L = 15  # [cm]

# OBJECT CAMERA
camera = None

# BOOL to don't open camera twice at beginning of program (used for changing exposure in set_exposure())
RUN = False


# OPEN CV TRACKBARS
# function is called whenever trackbar change its value
def empty(a):
    pass


def set_exposure(value):
    global RUN, camera
    if RUN:
        exp_value = (value - 20) / 10

        # reset camera and create new one with different exposure
        camera.cap.release()
        camera = None
        camera = system.set_camera(WIDTH, HEIGHT, FPS, FLIP, exp_value)


window_main = "Image processing"
window_option = "Options"
cv2.namedWindow(window_option)
cv2.resizeWindow(window_option, 500, 300)
cv2.createTrackbar("Threshold 1", window_option, 150, 255, empty)
cv2.createTrackbar("Threshold 2", window_option, 120, 255, empty)
cv2.createTrackbar("Min area", window_option, 350, 3000, empty)
cv2.createTrackbar("Max area", window_option, 2000, 3000, empty)
cv2.createTrackbar("Brightness", window_option, 100, 200, empty)
cv2.createTrackbar("Contrast", window_option, 10, 20, empty)
cv2.createTrackbar("Exposure", window_option, 20, 40, set_exposure)
cv2.createTrackbar("H low", window_option, 0, 179, empty)
cv2.createTrackbar("S low", window_option, 0, 255, empty)
cv2.createTrackbar("V low", window_option, 0, 255, empty)
cv2.createTrackbar("H high", window_option, 179, 179, empty)
cv2.createTrackbar("S high", window_option, 255, 255, empty)
cv2.createTrackbar("V high", window_option, 255, 255, empty)


def recognition():
    global CURRENT_IMG, RUN
    current_img = CURRENT_IMG
    print(
        f"=======================\n"
        f"Running image processing program\n"
        f"Use camera: {bool(CAM_DISP)}\n"
        f"Draw contour: {bool(DRAW_CONT)}\n"
        f"Draw rectangles: {bool(DRAW_DETECT)}\n"
        f"Display info: {bool(DRAW_INFO)}\n"
        f"Current image: cam{CURRENT_IMG}.jpg\n"
        f"=======================\n")

    # main loop
    while True:
        # 0
        # capturing video frame
        if CAM_DISP:
            if camera is not None:
                image = camera.read()
                RUN = True
            else:
                _, image = video.read()
        else:
            # capturing image
            img = images[current_img]
            image = cv2.resize(img, (640, 640))

        # updating trackbar values
        threshold1 = cv2.getTrackbarPos("Threshold 1", window_option)
        threshold2 = cv2.getTrackbarPos("Threshold 2", window_option)
        min_area = cv2.getTrackbarPos("Min area", window_option)
        max_area = cv2.getTrackbarPos("Max area", window_option)
        brightness_v = cv2.getTrackbarPos("Brightness", window_option)
        contrast_v = cv2.getTrackbarPos("Contrast", window_option)
        lower_color = np.array([cv2.getTrackbarPos("H low", window_option),
                                cv2.getTrackbarPos("S low", window_option),
                                cv2.getTrackbarPos("V low", window_option)])
        upper_color = np.array([cv2.getTrackbarPos("H high", window_option),
                                cv2.getTrackbarPos("S high", window_option),
                                cv2.getTrackbarPos("V high", window_option)])
        # 1
        # image operations to get black and white contours
        image = utils.masking(image, lower_color, upper_color)
        image, contours = utils.get_contours(image, [threshold1, threshold2], contrast_v, brightness_v,
                                             draw=DRAW_CONT)

        # 2
        # detecting squares from image and returning it with square contours
        # finals_contours = [index, x, y, w, h [straight rectangle around object], box corner points [box],
        # width [cm], height [cm], color]
        image, final_contours = utils.detect_square(contours, image, min_area, max_area, OBJECT_W, OBJECT_L)

        # TODO
        # 2) approx length based on real value cm
        # 3) delete contour which is above and have similar area
        # 4) plug to HUV code (test)
        # 5) pygame screen live camera display

        # 3
        # display detected rectangles and
        # display info about length, width and color
        utils.display_info(image, final_contours, draw_detect=DRAW_DETECT, draw_info=DRAW_INFO)

        # 4
        # showing final image
        cv2.imshow(window_main, image)

        # waiting for ESC button to exit (1ms interval - increasing it will cause program to wait
        # and therefore - producing lag)
        if cv2.waitKey(1) == ord('q'):
            print("Closing program without errors.")
            break

        # keyboard functionality - only when not using camera, because it slows the program
        if not CAM_DISP:
            if cv2.waitKey(50) == ord('n'):
                current_img = current_img + 1 if current_img < 12 else 0
                print(f"Current image: cam{current_img}.jpg")
            if cv2.waitKey(50) == ord('b'):
                current_img = current_img - 1 if current_img > 0 else 12
                print(f"Current image: cam{current_img}.jpg")

    # closing camera only if using it
    if camera is not None:
        camera.cap.release()
    elif video is not None:
        video.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    # using script arguments to display additional things (or not)
    # python3 main.py
    # --camera <CAM_DISP 1/0>
    # -c <DRAW_CONT 1/0>
    # -d <DRAW_DETECT 1/0>
    # -i <DRAW_INFO 1/0>
    # --image <current_img 13-0>
    CAM_DISP, DRAW_CONT, DRAW_DETECT, DRAW_INFO, CURRENT_IMG, FLIP = system.arguments(default_disp_cam,
                                                                                      default_contour,
                                                                                      default_detect,
                                                                                      default_info,
                                                                                      default_flip)

    # check which device to use, load images or camera
    camera, video, images = system.prepare_devices(CAM_DISP, WIDTH, HEIGHT, FPS, FLIP)

    # main script with recognition
    recognition()
