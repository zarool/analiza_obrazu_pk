import argparse
import os

# system arguments default values
default_disp_cam = 1
default_contour = 0
default_detect = 0
default_info = 0
default_image = 0
default_flip = 2

default_mode = 0
default_r_width = 1280
default_r_height = 720

camera_modes = [[3264, 2464, 21],
                [3264, 1848, 28],
                [1920, 1090, 30],
                [1640, 1232, 30],
                [1280, 720, 60],
                [1280, 720, 120]]


def arguments():
    parser = argparse.ArgumentParser(description="Additional arguments", formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--camera', choices=[1, 0], type=int, default=default_disp_cam,
                        help="Capture frames from camera or read images \n[default 1]")
    parser.add_argument('-c', '--contour', choices=[0, 1], type=int, default=default_contour,
                        help="Show second window with dilation \n[default 0]")
    parser.add_argument('-d', '--detect', choices=[1, 0], type=int, default=default_detect,
                        help="Show detected rect on screen \n[default 1]")
    parser.add_argument('-i', '--info', choices=[1, 0], type=int, default=default_info,
                        help="Show info about size and color \n[default 1]")
    parser.add_argument('--image', type=int, default=default_image,
                        help="Enter a number which image to read first")
    parser.add_argument('--flip', choices=[2, 0], type=int, default=default_flip,
                        help="Flip image, 2 - default, 0 - rotate 180 degrees")
    parser.add_argument('--width', type=int, default=default_r_width,
                        help="Specify the width (in pixels) of rendering window \n[default 600]")
    parser.add_argument('--height', type=int, default=default_r_height,
                        help="Specify the height (in pixels) of rendering window \n[default 400]")
    parser.add_argument('-m', '--mode', choices=[0, 1, 2, 3, 4, 5], type=int, default=default_mode,
                        help=(
                            'Select the IMX219 camera mode (output stream)'
                            '\nFuture releases will support more cameras'
                            '\n[default 0 - 3264x2464, FPS=21'
                            '\n -------------'
                            '\nMode | Width | Height | FPS |'
                            '\n 0   | 3264  | 2464   | 21  |'
                            '\n 1   | 3264  | 1848   | 28  |'
                            '\n 2   | 1920  | 1090   | 30  |'
                            '\n 3   | 1640  | 1232   | 30  |'
                            '\n 4   | 1280  | 720    | 60  |'
                            '\n 5   | 1280  | 720    | 120 |'
                            '\n -------------'))

    args = parser.parse_args()

    return args.camera, args.contour, args.detect, args.info, args.image, args.flip, args.width, args.height, \
        args.mode, camera_modes[args.mode][0], camera_modes[args.mode][1], camera_modes[args.mode][2]
