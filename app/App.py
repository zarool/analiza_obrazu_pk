from app.Window import Window
from system.Maszt import Maszt


class App:
    def __init__(self, cam_disp=1, contour=0, detect=1, info=1, flip=2, current=0, mode=0,
                 display_w=1280, display_h=780,
                 object_w=4, object_l=15):
        self.screen_width = display_w
        self.screen_height = display_h
        self.image_width = display_w * 3 / 5
        self.image_height = display_h * 2 / 3

        # maszt array parameters
        self.cam_disp = cam_disp
        self.contour = contour
        self.detect = detect
        self.info = info
        self.flip = flip
        self.current = current
        self.mode = mode
        self.param = [self.cam_disp, self.contour, self.detect, self.info, self.flip]

        self.object_w = object_w
        self.object_l = object_l

        self.maszt = Maszt(self.cam_disp, self.contour, self.detect, self.info, self.flip, self.current, self.mode,
                           self.image_width, self.image_height, self.object_w, self.object_l)
        self.window = Window(self.screen_width, self.screen_height, self.image_width, self.image_height, self.param,
                             self.maszt.get_info())

    def update_maszt(self, new_param):
        self.param = new_param
        self.cam_disp = self.param[0]
        self.contour = self.param[1]
        self.detect = self.param[2]
        self.info = self.param[3]
        self.flip = self.param[4]
        self.current = self.maszt.get_current_img()

        self.maszt.close()

        self.maszt = Maszt(self.cam_disp, self.contour, self.detect, self.info, self.flip, self.current, self.mode,
                           self.image_width, self.image_height, self.object_w, self.object_l)

    def window_display(self):
        # display window and render camera image
        self.window.display_window()
        self.window.display_frame(self.maszt.image, self.screen_width / 5, 0)

        # display contour if needed
        if self.contour:
            self.window.display_frame(self.maszt.image_contour, self.screen_width / 5, self.image_height)

    def ui_updates(self):
        # UPDATING MASZT PARAMETERS
        # update image parameters if changed values in slider
        if self.window.moved_sliders():
            self.maszt.update_image_param(self.window.get_sliders_value())

        # change maszt setting (initialize new object) after click of specific button
        buttons_value = self.window.get_buttons_value()
        if buttons_value != self.param:
            self.update_maszt(buttons_value)

        # update labels
        self.window.update_info(self.maszt.get_info())

    def run(self):
        # update maszt according to ui
        self.ui_updates()

        # start recognition software
        self.maszt.start()

        # render frames on display
        self.window_display()

        # event handler for keyboard interrupts, closing program etc.
        self.window.event_handler(self.maszt)

        # update screen
        self.window.update()
