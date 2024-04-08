import os
import cv2
from jetcam.csi_camera import CSICamera


class Camera:
    def __init__(self, width, height, display_w, display_h, fps, flip, exposure=0.0):
        self.width = width
        self.height = height
        self.fps = fps
        self.flip = flip
        self.exposure = exposure

        self.display_w = display_w
        self.display_h = display_h

    def run_camera(self, exposure=0.0):
        return CSICamera(width=self.display_w, height=self.display_h, capture_width=self.width, capture_height=self.height,
                         capture_fps=self.fps,
                         flip=self.flip, exposure=exposure)

    def prepare_devices(self, cam_disp):
        cam = None
        vid = None
        images_a = []
        if cam_disp:
            try:
                cam = self.run_camera()
                print("\nUsing external camera.")
            except Exception as e:
                print(e)
                print("\nUsing build-in webcam.")
                vid = cv2.VideoCapture(0)
        else:
            try:
                files = os.listdir("./images/")
                size = len(files)
            except FileNotFoundError:
                size = 0

            for index in range(0, size):
                images_a.append(cv2.imread(f"./images/cam{index}.jpg"))

        return cam, vid, images_a
