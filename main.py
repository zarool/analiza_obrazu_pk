import cv2
import numpy as np
import utils
import system

# CONST
CAMERA_DISP = 0
WINDOW_DRAW_CONT = 0
WINDOW_DRAW_DETECT = 0
WINDOW_DRAW_INFO = 0
CURRENT_IMG = 0
CAPTURE_FLIP = 2
CAPTURE_MODE = 0
# for image render
RENDER_WIDTH = 600
RENDER_HEIGHT = 400

# CAPTURE MODES
CAPTURE_WIDTH = 3264
CAPTURE_HEIGHT = 2464
CAPTURE_FPS = 21

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
        camera = system.set_camera(RENDER_WIDTH, RENDER_HEIGHT, CAPTURE_WIDTH, CAPTURE_HEIGHT,
                                   CAPTURE_FPS, CAPTURE_FLIP, exp_value)


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
cv2.createTrackbar("Search for red", window_option, 0, 1, empty)
cv2.createTrackbar("Search for green", window_option, 0, 1, empty)
cv2.createTrackbar("Search for blue", window_option, 0, 1, empty)
cv2.createTrackbar("Reset HSV", window_option, 0, 1, empty)


def recognition():
    global CURRENT_IMG, RUN
    current_img = CURRENT_IMG
    print(
        f"=======================\n"
        f"Running image processing program\n"
        f"Use camera: {bool(CAMERA_DISP)}\n"
        f"Output stream resolution:\n"
        f"W = {CAPTURE_WIDTH} | H = {CAPTURE_HEIGHT} | FPS = {CAPTURE_FPS}\n"
        f"Draw contour: {bool(WINDOW_DRAW_CONT)}\n"
        f"Draw rectangles: {bool(WINDOW_DRAW_DETECT)}\n"
        f"Display info: {bool(WINDOW_DRAW_INFO)}\n"
        f"Current image: cam{CURRENT_IMG}.jpg\n"
        f"=======================\n")

    # main loop
    while True:
        # 0
        # capturing video frame
        if CAMERA_DISP:
            if camera is not None:
                # read from external camera
                image = camera.read()
                RUN = True
            else:
                # read from laptop camera if is any
                _, image = video.read()
        else:
            # read from images/cam*.jpg
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
                                             draw=WINDOW_DRAW_CONT)

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
        utils.display_info(image, final_contours, draw_detect=WINDOW_DRAW_DETECT, draw_info=WINDOW_DRAW_INFO)

        # 4
        # showing final image
        cv2.imshow(window_main, image)

        # waiting for ESC button to exit (1ms interval - increasing it will cause program to wait
        # and therefore - producing lag)
        if cv2.waitKey(1) == ord('q'):
            print("Closing program without errors.")
            break

        # keyboard functionality - only when not using camera, because it slows the program
        if not CAMERA_DISP:
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
    (CAMERA_DISP, WINDOW_DRAW_CONT, WINDOW_DRAW_DETECT, WINDOW_DRAW_INFO, CURRENT_IMG,
     CAPTURE_FLIP, RENDER_WIDTH, RENDER_HEIGHT, CAPTURE_MODE, CAPTURE_WIDTH, CAPTURE_HEIGHT,
     CAPTURE_FPS) = system.arguments()

    # check which device to use, load images or camera
    camera, video, images = system.prepare_devices(CAMERA_DISP, RENDER_WIDTH, RENDER_HEIGHT,
                                                   CAPTURE_WIDTH, CAPTURE_HEIGHT,
                                                   CAPTURE_FPS, CAPTURE_FLIP)

    # main script with recognition
    recognition()
