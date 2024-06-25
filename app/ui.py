import pygame


# print(pygame.font.get_fonts())


class UI:
    font = None

    colors = {}

    s_size = ()
    s_center = ()

    b_size = ()
    b_center = ()

    l_x_pos = 0

    o_size = ()
    o_center = ()

    @staticmethod
    def init(app):
        UI.font = pygame.font.SysFont('ubuntu', 20)

        # pos and size for sliders
        x_pos = app.screen.get_size()[0] // 10
        UI.s_size = (x_pos * 1.8, x_pos / 10)
        UI.s_center = (x_pos, UI.s_size[1] * 3)

        # pos and size for buttons on right
        x_pos_right = app.screen.get_size()[0] * 9 // 10
        UI.b_size = (x_pos * 1.8, x_pos / 5)
        UI.b_center = (x_pos_right, UI.s_size[1] * 3)

        # x pos for labels on right
        UI.l_x_pos = UI.b_center[0] - int(UI.b_size[0] / 2)

        # pos for object info labels
        UI.o_center = (app.screen.get_size()[0] * 3 / 5, UI.b_size[1] * 21)

        UI.colors = {
            'text': "white",
            'text-value': "darkslategray4",  # "gold3",
            'main-color': (30, 30, 30),
            'bg': "darkslategrey",
            'hovered': "darkslategray4",
            'not_hovered': "darkslategrey",
            'disabled': "gray60",  # "azure3",
            'clicked': "darkslategray4"
        }


class Menu:
    def __init__(self, app, btn_param, m_info, o_info=None) -> None:
        # pygame app object
        self.app = app

        # maszt image processing parameters (array)
        self.maszt_info = m_info
        self.maszt_len = len(self.maszt_info)

        # maszt init parameters
        self.btn_param = btn_param

        # object info (pos, color, distance)
        if o_info is None:
            o_info = [0, 0, 0, 0, 0, 0]
        self.object_info = o_info

        self.sliders = [
            Slider((UI.s_center[0], UI.s_center[1] + UI.s_size[1] * 0), 0.47244, 0, 254, "Threshold 1:"),
            Slider((UI.s_center[0], UI.s_center[1] + UI.s_size[1] * 3), 0.59, 0, 254, "Threshold 2:"),
            Slider((UI.s_center[0], UI.s_center[1] + UI.s_size[1] * 6), 0.666, 0, 3000, "Max area:"),
            Slider((UI.s_center[0], UI.s_center[1] + UI.s_size[1] * 9), 0.117, 0, 3000, "Min area:"),
            Slider((UI.s_center[0], UI.s_center[1] + UI.s_size[1] * 12), 0.5, -100, 100, "Brightness:"),
            Slider((UI.s_center[0], UI.s_center[1] + UI.s_size[1] * 15), 0.5, 0, 20, "Contrast:"),
            Slider((UI.s_center[0], UI.s_center[1] + UI.s_size[1] * 18), 0.5, -2, 2, "Exposure:"),
            Slider((UI.s_center[0], UI.s_center[1] + UI.s_size[1] * 21), 0, 0, 179, "H low:"),
            Slider((UI.s_center[0], UI.s_center[1] + UI.s_size[1] * 24), 0, 0, 254, "S low:"),
            Slider((UI.s_center[0], UI.s_center[1] + UI.s_size[1] * 27), 0, 0, 254, "V low:"),
            Slider((UI.s_center[0], UI.s_center[1] + UI.s_size[1] * 30), 1, 0, 179, "H high:"),
            Slider((UI.s_center[0], UI.s_center[1] + UI.s_size[1] * 33), 1, 0, 254, "S high:"),
            Slider((UI.s_center[0], UI.s_center[1] + UI.s_size[1] * 36), 1, 0, 254, "L high:"),
        ]

        self.buttons = [
            Button((UI.b_center[0], UI.b_center[1] + UI.b_size[1] * 0), UI.b_size,
                   "Read images", self.btn_param[0], (1, 0)),
            Button((UI.b_center[0], UI.b_center[1] + UI.b_size[1] * 1.2), UI.b_size,
                   "Show contours", self.btn_param[1], (0, 1)),
            Button((UI.b_center[0], UI.b_center[1] + UI.b_size[1] * 2.4), UI.b_size,
                   "Show detected rect", self.btn_param[2], (0, 1)),
            Button((UI.b_center[0], UI.b_center[1] + UI.b_size[1] * 3.6), UI.b_size,
                   "Show info", self.btn_param[3], (0, 1)),
            Button((UI.b_center[0], UI.b_center[1] + UI.b_size[1] * 4.8), UI.b_size,
                   "Flip camera 180 deg", self.btn_param[4], (2, 0)),
            Button((UI.b_center[0], UI.b_center[1] + UI.b_size[1] * 6), UI.b_size,
                   "Next image", 1, (10, 100)),
            Button((UI.b_center[0], UI.b_center[1] + UI.b_size[1] * 7.2), UI.b_size,
                   "Previous image", -1, (10, 100))
        ]

        self.labels = [
            Label("Use camera: ", self.maszt_info[0], "", (UI.l_x_pos, UI.b_size[1] * 11)),
            Label("Width: ", str(self.maszt_info[1]), "", (UI.l_x_pos, UI.b_size[1] * 13)),
            Label("Height: ", str(self.maszt_info[2]), "", (UI.l_x_pos, UI.b_size[1] * 14)),
            Label("FPS: ", str(self.maszt_info[3]), "", (UI.l_x_pos, UI.b_size[1] * 15)),
            Label("Draw contour: ", str(self.maszt_info[4]), "", (UI.l_x_pos, UI.b_size[1] * 16)),
            Label("Draw rectangles: ", str(self.maszt_info[5]), "", (UI.l_x_pos, UI.b_size[1] * 17)),
            Label("Display info: ", str(self.maszt_info[6]), "", (UI.l_x_pos, UI.b_size[1] * 18)),
            Label("Current image: ", self.maszt_info[7], ".jpg", (UI.l_x_pos, UI.b_size[1] * 19)),
            Label("Camera stream resolution:", "", "", (UI.l_x_pos, UI.b_size[1] * 12)),
            Label("NEXT IMAGE = ", "N", "", (UI.l_x_pos, UI.b_size[1] * 21)),
            Label("PREV IMAGE = ", "B", "", (UI.l_x_pos, UI.b_size[1] * 22)),
            Label("QUIT PROGRAM = ", "Q", "", (UI.l_x_pos, UI.b_size[1] * 23))
        ]

        self.object_labels = [
            Label("Pos x:", str(self.object_info[0]), "", (UI.o_center[0], UI.o_center[1])),
            Label("Pos y:", str(self.object_info[1]), "", (UI.o_center[0], UI.o_center[1] + UI.b_size[1])),
            Label("Color:", str(self.object_info[2]), "", (UI.o_center[0], UI.o_center[1] + UI.b_size[1] * 2)),
            Label("Width [px]:", str(self.object_info[3]), "", (UI.o_center[0], UI.o_center[1] + UI.b_size[1] * 3)),
            Label("Height [px]:", str(self.object_info[4]), "", (UI.o_center[0], UI.o_center[1] + UI.b_size[1] * 4)),
            Label("Distance [cm]:", str(self.object_info[5]), "", (UI.o_center[0], UI.o_center[1] + UI.b_size[1] * 5)),
        ]

    def run(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse = pygame.mouse.get_pressed()

        for slider in self.sliders:
            slider.event_handler(mouse, mouse_pos)
            slider.render(self.app)
            slider.display_value(self.app)

        for index, btn in enumerate(self.buttons):
            btn.event_handler(mouse, mouse_pos)
            btn.render(self.app)
            btn.display_value(self.app)
            btn.disable_btn(index, self.get_buttons_value())

        for index, label in enumerate(self.labels):
            if index < self.maszt_len:
                label.update_text(self.maszt_info[index])
            label.render(self.app)

        for index, label in enumerate(self.object_labels):
            label.update_text(self.object_info[index])
            label.render(self.app)

    def moved_sliders(self):
        for slider in self.sliders:
            if slider.grabbed:
                return True
        return False

    def get_sliders_value(self):
        return [slider.get_value() for slider in self.sliders]

    def get_buttons_value(self):
        return [btn.get_value() for btn in self.buttons[:-2]]


class Slider:
    def __init__(self, pos: tuple, initial_val: float, min_v: int, max_v: int, name: str) -> None:
        self.s_color = {
            True: UI.colors['hovered'],
            False: UI.colors['disabled']
        }

        self.pos = pos
        self.size = UI.s_size

        self.hovered = False
        self.grabbed = False

        self.slider_left_pos = self.pos[0] - (self.size[0] // 2)
        self.slider_right_pos = self.pos[0] + (self.size[0] // 2)
        self.slider_top_pos = self.pos[1] - (self.size[1] // 2)

        self.min = min_v
        self.max = max_v
        self.initial_val = (self.slider_right_pos - self.slider_left_pos) * initial_val  # <- percentage

        self.container_rect = pygame.Rect(self.slider_left_pos, self.slider_top_pos, self.size[0], self.size[1])
        self.button_rect = pygame.Rect(self.slider_left_pos + self.initial_val - 5, self.slider_top_pos, 10,
                                       self.size[1])

        # label
        self.name = name
        self.label_text = str(f"{self.name} {int(self.get_value())}")
        self.text = UI.font.render(self.label_text, True, UI.colors['text'], None)
        self.label_rect = self.text.get_rect(center=(self.pos[0], self.slider_top_pos - 10))
        self.label_rect.left = self.slider_left_pos

    def move_slider(self, mouse_pos):
        pos = mouse_pos[0]
        if pos < self.slider_left_pos:
            pos = self.slider_left_pos
        if pos > self.slider_right_pos:
            pos = self.slider_right_pos
        self.button_rect.centerx = pos

    def hover(self):
        self.hovered = True

    def render(self, app):
        pygame.draw.rect(app.screen, UI.colors['bg'], self.container_rect, border_radius=10)
        pygame.draw.rect(app.screen, self.s_color[self.hovered], self.button_rect, border_radius=10)

    def get_value(self):
        val_range = self.slider_right_pos - self.slider_left_pos - 1
        button_val = self.button_rect.centerx - self.slider_left_pos

        return round((button_val / val_range) * (self.max - self.min) + self.min)

    def update_value(self):
        self.label_text = str(f"{self.name :15} {int(self.get_value()) :4}")
        self.text = UI.font.render(self.label_text, True, UI.colors['text'], None)

    def display_value(self, app):
        self.update_value()
        app.screen.blit(self.text, self.label_rect)

    def event_handler(self, mouse, mouse_pos):
        if self.container_rect.collidepoint(mouse_pos):
            if mouse[0]:
                self.grabbed = True
        if not mouse[0]:
            self.grabbed = False
        if self.button_rect.collidepoint(mouse_pos):
            self.hover()
        if self.grabbed:
            self.move_slider(mouse_pos)
            self.hover()
        else:
            self.hovered = False


class Button:
    def __init__(self, pos: tuple, size: tuple, text: str, value: int, values: tuple) -> None:
        self.pos_center = pos
        self.size = size
        self.pos = (self.pos_center[0] - (self.size[0] / 2), self.pos_center[1] - (self.size[1] / 2))

        self.text = text
        self.color = UI.colors['bg']

        self.hovered = False
        self.clicked = False
        self.disabled = False

        self.button_rect = pygame.Rect(self.pos, self.size)

        self.label_text = str(text)
        self.text = UI.font.render(self.label_text, True, UI.colors['text'])
        self.label_rect = self.text.get_rect(center=self.button_rect.center)

        # self.value_name = name
        self.value = value
        self.range = values

    def render(self, app):
        pygame.draw.rect(app.screen, self.color, self.button_rect, border_radius=10)

    def disable_btn(self, index, param):
        # if reading images - disable flip option
        if param[0] == 0 and index == 4:
            self.disabled = True
        # if using camera - disable next and prev option
        elif param[0] == 1 and (index == 5 or index == 6):
            self.disabled = True
        else:
            self.disabled = False

    def display_value(self, app):
        app.screen.blit(self.text, self.label_rect)

    def click(self):
        if self.value == self.range[0]:
            self.value = self.range[1]
        else:
            self.value = self.range[0]

    def event_handler(self, mouse, mouse_pos):
        if not self.disabled:
            if self.button_rect.collidepoint(mouse_pos):
                self.color = UI.colors['hovered']
                if mouse[0]:
                    if not self.clicked:
                        self.click()
                        self.clicked = True
                else:
                    self.clicked = False
            else:
                if self.value == self.range[1]:
                    self.color = UI.colors['clicked']
                else:
                    self.color = UI.colors['not_hovered']
        else:
            self.color = UI.colors['disabled']

    def get_value(self):
        return self.value


class Label:
    def __init__(self, pretext: str, content: str, after_text: str, pos: tuple) -> None:
        self.pretext = pretext

        self.content = content
        self.after_text = after_text
        self.text = self.create_text()

        self.pos = pos

        # left side of label - desc
        self.left_text = UI.font.render(self.pretext, True, UI.colors['text'], None)
        self.left_text_rect = self.left_text.get_rect(center=pos)
        self.left_text_rect.left = self.pos[0]

        # right side of label - value
        self.right_text = UI.font.render(self.text, True, UI.colors['text-value'], None)
        self.right_text_rect = self.right_text.get_rect(center=pos)
        self.right_text_rect.right = self.pos[0] + (UI.b_size[0] * 0.95)

    def create_text(self):
        if self.after_text == ".jpg":
            return "cam" + str(self.content) + self.after_text
        return str(self.content) + self.after_text

    def update_text(self, new_text):
        self.content = new_text
        self.text = self.create_text()

        self.left_text = UI.font.render(self.pretext, True, UI.colors['text'], None)
        self.right_text = UI.font.render(self.text, True, UI.colors['text-value'], None)

    def render(self, app):
        app.screen.blit(self.left_text, self.left_text_rect)
        app.screen.blit(self.right_text, self.right_text_rect)

# FONTS TEST
# UI.sfont = pygame.font.Font(None, 20)
# UI.lfont = pygame.font.Font(None, 40)
# UI.xlfont = pygame.font.Font(None, 50)
# UI.fonts = {
#     'sm': UI.sfont,
#     'm': UI.font,
#     'l': UI.lfont,
#     'xl': UI.xlfont,
#     'n': pygame.font.SysFont('ubuntu', 20)
# }
