import sys
import cv2
import numpy as np
import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame as pg
from pygame.locals import *
from app.ui import UI, Menu


class Window:
    def __init__(self, screen_width, screen_height, image_width, image_height, btn_param, maszt_info):
        pg.init()
        pg.display.set_caption("Maszt")

        self.screen_width = screen_width
        self.screen_height = screen_height
        self.image_width = int(image_width)
        self.image_height = int(image_height)

        self.screen = pg.display.set_mode([self.screen_width, self.screen_height])

        self.btn_param = btn_param
        self.maszt_info = maszt_info

        UI.init(self)
        self.menu = Menu(self, self.btn_param, self.maszt_info)

    def display_window(self):
        self.screen.fill(UI.colors['main-color'])
        self.menu.run()

    def display_frame(self, frame, pos_x, pos_y):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = np.fliplr(frame)
        frame = np.rot90(frame)
        frame = pg.surfarray.make_surface(frame)
        self.screen.blit(frame, (pos_x, pos_y))

    def update_info(self, maszt_info):
        self.menu.maszt_info = maszt_info

    def moved_sliders(self):
        return self.menu.moved_sliders()

    def get_sliders_value(self):
        return self.menu.get_sliders_value()

    def get_buttons_value(self):
        return self.menu.get_buttons_value()

    @staticmethod
    def update():
        pg.display.update()

    @staticmethod
    def event_handler(maszt):
        for event in pg.event.get():
            if event.type == KEYDOWN:
                if event.key == pg.K_q:
                    print("Closing program without problems.")
                    maszt.close()
                    pg.quit()
                    sys.exit(0)
                if event.key == pg.K_n:
                    maszt.next_img()
                elif event.key == pg.K_b:
                    maszt.previous_img()
