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