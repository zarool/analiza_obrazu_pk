import argparse
import os
import cv2
from jetcam.csi_camera import CSICamera


# OPEN CAMERA
def set_camera(width, height, fps, flip, exposure=0.0):
    return CSICamera(width=600, height=400, capture_width=width, capture_height=height, capture_fps=fps,
                     flip=flip, exposure=exposure)


def prepare_devices(cam_disp, width, height, fps, flip):
    cam = None
    vid = None
    images_a = []
    if cam_disp:
        try:
            cam = set_camera(width, height, fps, flip)
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


def arguments(d_camera, d_contour, d_detect, d_info, d_flip):
    parser = argparse.ArgumentParser(description="Additional arguments")
    parser.add_argument('--camera', type=int, default=d_camera,
                        help="Capture frames from camera or read images \n[default 1]")
    parser.add_argument('-c', '--contour', type=int, default=d_contour,
                        help="Show second window with dilation \n[default 0]")
    parser.add_argument('-d', '--detect', type=int, default=d_detect,
                        help="Show detected rect on screen \n[default 1]")
    parser.add_argument('-i', '--info', type=int, default=d_info,
                        help="Show info about size and color \n[default 1]")
    parser.add_argument('--image', type=int, default=0,
                        help="Enter a number which image to read first")
    parser.add_argument('--flip', type=int, default=d_flip,
                        help="Flip image, 0 - normal, 2 - rotate 180 degrees")

    args = parser.parse_args()

    return args.camera, args.contour, args.detect, args.info, args.image, args.flip
