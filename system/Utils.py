import cv2
import numpy as np
import warnings


class Utils:

    def __init__(self):
        self.threshold1 = 150
        self.threshold2 = 120
        self.min_area = 350
        self.max_area = 2000
        self.brightness_v = 0
        self.contrast_v = 10
        self.lower_color = np.array([0, 0, 0])
        self.upper_color = np.array([179, 255, 255])
        self.exposure = 0

    # USER FUNCTIONS
    # ADDING MASKS FOR IMAGE
    @staticmethod
    def masking(img, lower, upper):
        hsv_image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv_image, lower, upper)
        masked_img = cv2.bitwise_and(img, img, mask=mask)
        return masked_img

    # FIRST FUNCTION TO GET CONTOURS (BLACK AND WHITE IMAGE)
    @staticmethod
    def get_contours(img, c_thr, contrast, brightness, draw=True):
        # 1.0
        # change image according to trackbars (brightness, contrast, color masks)
        # alpha - contrast value (0 - 2)
        # beta - brightness value (-100 - 100)
        image2 = cv2.convertScaleAbs(img, alpha=(contrast / 10), beta=brightness)

        # 1.1
        # adding gray filter to image
        if c_thr is None:
            c_thr = [150, 120]
        gray_image = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

        # 1.2
        # https://docs.opencv.org/3.4/da/d22/tutorial_py_canny.html
        # new threshold method (Canny), better than standard opencv threshold
        canny = cv2.Canny(gray_image, c_thr[0], c_thr[1])

        # 1.3
        # https://docs.opencv.org/3.4/db/df6/tutorial_erosion_dilatation.html
        # dilation of lines to have thicker contours
        kernel = np.ones((5, 5))
        dilation = cv2.dilate(canny, kernel, iterations=1)
        erode = cv2.erode(dilation, kernel, iterations=1)

        # if draw:
        #     cv2.imshow("Contour", erode)

        return image2, erode

    # APPROXIMATING REAL LENGTH AND COLOR OF OBJECT
    @staticmethod
    def approx_length(rect, object_w, object_l):
        # 1
        # https://stackoverflow.com/questions/14038002/opencv-how-to-calculate-distance-between-camera-and-object-using-image
        # 2
        # https://stackoverflow.com/questions/6714069/finding-distance-from-camera-to-object-of-known-size
        # 3
        # https://pyimagesearch.com/2015/01/19/find-distance-camera-objectmarker-using-python-opencv/

        # focal_length = (width [px] * real_distance)  / real_width
        # dist = (real_width * focal_length) / width [px]
        focal_length = (290 * 24) / object_w
        dist = (object_w * focal_length) / rect[1][0]
        distance_m = round(dist, 2)

        width_px = rect[1][0]
        height_px = rect[1][1]
        # distance_m = round(83 / height_px, 2)
        length_cm = height_px
        width_cm = width_px
        return width_cm, length_cm, distance_m

    @staticmethod
    def approx_color(img, x, y, w, h):
        closest_color = "black"
        fit = "0"
        colors = {
            # "white": (255, 255, 255),
            "black": (0, 0, 0),
            "red": (255, 0, 0),
            "green": (0, 255, 0),
            "blue": (0, 0, 255)
        }

        # first method
        scale = (w * (w < h) + h * (w > h)) * 0.4
        p1 = [int(x - scale), int(y - scale)]
        p2 = [int(x + w + scale), int(y + h + scale)]

        rect = img[p1[1]:p2[1], p1[0]:p2[0]]
        # ignoring warning from mean calculation
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=RuntimeWarning)
            avg_color_bgr = np.mean(rect, axis=(0, 1))

        # algorithm to calculate the closest color to given set of colors
        if not (np.isnan(avg_color_bgr).any() or np.isinf(avg_color_bgr).any()):
            avg_color_bgr = np.round(avg_color_bgr).astype(int)
            avg_color_rgb = avg_color_bgr[::-1]
            r = avg_color_rgb[0]
            g = avg_color_rgb[1]
            b = avg_color_rgb[2]

            min_distance = float("inf")
            for color, value in colors.items():
                dist = sum([(i - j) ** 2 for i, j in zip((r, g, b), value)])
                if dist < min_distance:
                    min_distance = dist
                    closest_color = color
            fit = int(100 - (min_distance * 0.001))

        # if closest_color is not "black":
        # draw rect to calculate avg color
        img = cv2.rectangle(img, (p1[0], p1[1]), (p2[0], p2[1]),
                            (255, 255, 255), 1)

        return closest_color, fit

    # SECOND FUNCTION THAT WILL DETECT SQUARES AND RECTANGLES BASED ON IMAGE CONTOURS
    # AND RETURNING FINAL CONTOURS OF ALL OBJECTS THAT WERE DETECTED
    def detect_square(self, model_image, final_image, min_area, max_area, object_w, object_l):
        # finding contours with cv2 function
        contours, hierarchy = cv2.findContours(model_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # cv2.CHAIN_APPROX_SIMPLE
        final_contours = []
        # looping through every contour (one contour = set of points)
        for i, cnt in enumerate(contours):
            area = cv2.contourArea(cnt)

            # drawing contours within area value to cancel the noise
            if min_area < area < max_area:
                # getting minimal area and rotating the contours
                # box have four points of rectangle
                rect = cv2.minAreaRect(cnt)
                box = cv2.boxPoints(rect)
                box = np.intp(box)

                # getting straight rectangle
                epsilon = 0.02 * cv2.arcLength(cnt, True)
                approx = cv2.approxPolyDP(cnt, epsilon, True)
                x, y, w, h = cv2.boundingRect(approx)

                # getting object properties
                width_cm, length_cm, dist = self.approx_length(rect, object_w, object_l)
                color, fit = self.approx_color(final_image, x, y, w, h)

                # array with final contours
                # ignoring black color
                if color != "black":
                    final_contours.append([i, x, y, w, h, box, width_cm, length_cm, dist, color, fit])

                # adding all contours
                # final_contours.append([i, x, y, w, h, box, width_cm, length_cm, dist, color, fit])

        return final_image, final_contours

    # THIRD FUNCTION TO DISPLAY ALL DATA ON FINAL IMAGE
    @staticmethod
    def display_info(final_image, contour, draw_detect=True, draw_info=True):
        for i, cnt in enumerate(contour):
            x = cnt[1]
            y = cnt[2]
            w = cnt[3]
            h = cnt[4]
            box = cnt[5]
            width_cm = cnt[6]
            length_cm = cnt[7]
            dist = cnt[8]
            color = cnt[9]
            fit = cnt[10]

            if draw_detect:
                cv2.drawContours(final_image, [box], 0, (0, 0, 255), 2)

            if draw_info:
                # displaying info
                # cv2.putText(final_image, "Width [cm]: " + str(int(width_cm)), (int(x + w / 2), int(y + h + 20)),
                #             cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                #             (255, 255, 255), 2)
                # cv2.putText(final_image, "Length [cm]: " + str(int(length_cm)), (int(x + w / 2), int(y + h + 35)),
                #             cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                #             (255, 255, 255), 2)

                # fit show how close it is to desired color
                cv2.putText(final_image, str(color) + " " + str(fit) + "%", (int(x + w / 2), int(y + h + 20)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                            (255, 255, 255), 2)

                # real distance from camera
                cv2.putText(final_image, str(dist) + " cm", (int(x + w / 2), int(y + h + 35)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                            (255, 255, 255), 2)

                # testing - delete later
                cv2.putText(final_image, str(round(width_cm, 2)) + " width [px]", (int(x + w / 2), int(y + h + 50)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                            (255, 255, 255), 2)

    def print_param(self):
        print(f"Threshold1: {self.threshold1} \n"
              f"Threshold2; {self.threshold2} \n"
              f"Min_area: {self.min_area} \n"
              f"Max_area: {self.max_area} \n"
              f"Brightness: {self.brightness_v} \n"
              f"Contrast: {self.contrast_v} \n"
              f"Exposure: {self.exposure} \n"
              f"Lower color: {self.lower_color} \n"
              f"Upper color: {self.upper_color} \n")
