import cv2
import numpy as np


def empty(a):
    pass


class Window:
    def __init__(self):
        self.window_main = "Image processing"
        self.window_option = "Options"
        cv2.namedWindow(self.window_option)
        cv2.resizeWindow(self.window_option, 500, 300)
        cv2.createTrackbar("Threshold 1", self.window_option, 150, 255, empty)
        cv2.createTrackbar("Threshold 2", self.window_option, 120, 255, empty)
        cv2.createTrackbar("Min area", self.window_option, 350, 3000, empty)
        cv2.createTrackbar("Max area", self.window_option, 2000, 3000, empty)
        cv2.createTrackbar("Brightness", self.window_option, 100, 200, empty)
        cv2.createTrackbar("Contrast", self.window_option, 10, 20, empty)
        cv2.createTrackbar("H low", self.window_option, 0, 179, empty)
        cv2.createTrackbar("S low", self.window_option, 0, 255, empty)
        cv2.createTrackbar("V low", self.window_option, 0, 255, empty)
        cv2.createTrackbar("H high", self.window_option, 179, 179, empty)
        cv2.createTrackbar("S high", self.window_option, 255, 255, empty)
        cv2.createTrackbar("V high", self.window_option, 255, 255, empty)

        cv2.createTrackbar("Search for red", self.window_option, 0, 1, self.set_hsv_color_red)
        cv2.createTrackbar("Search for green", self.window_option, 0, 1, self.set_hsv_color_green)
        cv2.createTrackbar("Search for blue", self.window_option, 0, 1, self.set_hsv_color_blue)
        cv2.createTrackbar("Reset HSV", self.window_option, 0, 1, self.set_hsv_color_clear_buffer)

        self.threshold1 = 0
        self.threshold2 = 0
        self.min_area = 0
        self.max_area = 0
        self.brightness_v = 0
        self.contrast_v = 0
        self.lower_color = [0, 0, 0]
        self.upper_color = [0, 0, 0]

        self.get_trackbar_value()

    def get_trackbar_value(self):
        # updating trackbar values
        self.threshold1 = cv2.getTrackbarPos("Threshold 1", self.window_option)
        self.threshold2 = cv2.getTrackbarPos("Threshold 2", self.window_option)
        self.min_area = cv2.getTrackbarPos("Min area", self.window_option)
        self.max_area = cv2.getTrackbarPos("Max area", self.window_option)
        self.brightness_v = cv2.getTrackbarPos("Brightness", self.window_option)
        self.contrast_v = cv2.getTrackbarPos("Contrast", self.window_option)
        self.lower_color = np.array([cv2.getTrackbarPos("H low", self.window_option),
                                     cv2.getTrackbarPos("S low", self.window_option),
                                     cv2.getTrackbarPos("V low", self.window_option)])
        self.upper_color = np.array([cv2.getTrackbarPos("H high", self.window_option),
                                     cv2.getTrackbarPos("S high", self.window_option),
                                     cv2.getTrackbarPos("V high", self.window_option)])

    def set_hsv_color_red(self, x=0):
        self.lower_color = [80, 70, 50]
        self.upper_color = [100, 255, 255]

        cv2.setTrackbarPos("H low", self.window_option, 80)
        cv2.setTrackbarPos("S low", self.window_option, 70)
        cv2.setTrackbarPos("V low", self.window_option, 50)
        cv2.setTrackbarPos("H high", self.window_option, 100)
        cv2.setTrackbarPos("S high", self.window_option, 255)
        cv2.setTrackbarPos("V high", self.window_option, 255)

    def set_hsv_color_green(self, x=0):
        self.lower_color = [36, 0, 0]
        self.upper_color = [86, 255, 255]

        cv2.setTrackbarPos("H low", self.window_option, 36)
        cv2.setTrackbarPos("S low", self.window_option, 0)
        cv2.setTrackbarPos("V low", self.window_option, 0)
        cv2.setTrackbarPos("H high", self.window_option, 86)
        cv2.setTrackbarPos("S high", self.window_option, 255)
        cv2.setTrackbarPos("V high", self.window_option, 255)

    def set_hsv_color_blue(self, x=0):
        self.lower_color = [110, 50, 50]
        self.upper_color = [130, 255, 255]

        cv2.setTrackbarPos("H low", self.window_option, 110)
        cv2.setTrackbarPos("S low", self.window_option, 50)
        cv2.setTrackbarPos("V low", self.window_option, 50)
        cv2.setTrackbarPos("H high", self.window_option, 130)
        cv2.setTrackbarPos("S high", self.window_option, 255)
        cv2.setTrackbarPos("V high", self.window_option, 255)

    def set_hsv_color_clear_buffer(self, x=0):
        self.lower_color = [0, 0, 0]
        self.upper_color = [179, 255, 255]

        cv2.setTrackbarPos("H low", self.window_option, 0)
        cv2.setTrackbarPos("S low", self.window_option, 0)
        cv2.setTrackbarPos("V low", self.window_option, 0)
        cv2.setTrackbarPos("H high", self.window_option, 255)
        cv2.setTrackbarPos("S high", self.window_option, 255)
        cv2.setTrackbarPos("V high", self.window_option, 255)
