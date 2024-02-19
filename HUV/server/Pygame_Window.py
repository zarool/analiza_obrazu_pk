import pygame, sys
from Joys_Calculation import Calculation
import re
import time

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class TextPrint(object):

    def __init__(self):
        """ Constructor """
        self.reset()
        self.x_pos = 10
        self.y_pos = 10
        self.line_height = 15
        self.font = pygame.font.Font(None, 20)  # rozmiar tekstu

    def print(self, my_screen, text_string):
        text_bitmap = self.font.render(text_string, True, BLACK)
        my_screen.blit(text_bitmap, [self.x_pos, self.y_pos])
        self.y_pos += self.line_height

    def reset(self):
        self.x_pos = 10
        self.y_pos = 10
        self.line_height = 15

    def indentx(self):
        self.x_pos += 10

    def unindentx(self):
        self.x_pos -= 10

    def indenty(self):
        self.y_pos += 10

    def unindenty(self):
        self.y_pos -= 10

    def second_row(self):
        self.x_pos += 300



def Joystick(joystick_que, ethernet_queue_to_HUV, magazyn):

    pygame.init()
    screen = pygame.display.set_mode([1250, 500])       # rozmiar okna
    pygame.display.set_caption("HUV control panel")     # tytuł okna

    done = False    # do pętli nieskończonej obsługującej eventy

    clock = pygame.time.Clock()     # jakiś timer
    pygame.joystick.init()  # inicjalizacja obsługi joysticka przez pygame

    # Get ready to print
    textPrint = TextPrint()

    # -------- Joystick -----------
    but = 0
    gala = 0
    hatclick = 0
    # check1 = 0
    # check3 = 0
    # joy_right = [0, 0]
    # joy_left = [0, 0]
    AxisValues = [0, 0, 0, 0]
    OldAxisValues = [0, 0, 0, 0]
    zero = 0
    joystick_rect = pygame.Rect(10, 5, 170, 325)
    # -----------------------------

    # ------ input window ---------
    user_text = ''
    input_rect = pygame.Rect(295, 300, 250, 20)
    rect_color = [0, 0, 0]
    # -----------------------------

    # ------- HUV choose window --------
    poczatek_x = 280
    poczatek_y = 30
    rozmiar_x = 60
    rozmiar_y = 40
    przesuniecie = 80
    HUV_choose_rect_color = [0, 0, 0]
    # ----------------------------------

    # ------- HUV parameter windows --------
    HUV_parameters_rect_color_grey = [230, 230, 230]    # szary kolor tła kontrolki
    HUV_parameters_rect_color_red = [255, 125, 125]     # czerwony kolor tła kontrolki
    HUV_parameters_rect_color_green = [125, 255, 125]   # zielony kolor tła kontrolki
    # -------------------------------

    # --------- HUV image ---------
    HUV_image = pygame.image.load("HUV.png")
    arrow_up_image = pygame.image.load("arrow_up.png")
    arrow_down_image = pygame.image.load("arrow_down.png")
    # -----------------------------

    # --------- Ballast Tank ----------
    slider_width = 20
    slider_height = 150
    font = pygame.font.Font(None, 20)
    slider_pos_x = 1150
    slider_pos_y = 60
    slider_pos_x, slider_pos_y
    reset_button_pos_x = slider_pos_x + 25
    reset_button_pos_y = slider_pos_y + 68

    min_value = -100
    max_value = 100
    value_range = max_value - min_value

    # Inicjalizacja wartości suwaka
    slider_value = 0
    #----------------------------------


    wcisniete = 0
    while not done:             # pętla nieskończona
        # EVENT PROCESSING STEP
        time.sleep(0.05)
        for event in pygame.event.get():    # w każej pętli sprawdz wszystkie eventy pygame
            if event.type == pygame.QUIT:   # zamknięcie działania pętli pygame
                done = True
            # Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION
            if event.type == pygame.JOYBUTTONDOWN:
                but = 1
            if event.type == pygame.JOYBUTTONUP:
                Command = str("{:>2}:{}".format(99, button))
                joystick_que.put(Command)
            if event.type == pygame.JOYAXISMOTION:
                gala = 1
            if event.type == pygame.JOYHATMOTION:
                hatclick = 1
            if event.type == pygame.KEYDOWN:            # event do pisania w oknie
                if event.key == pygame.K_BACKSPACE:     # przycisk backspace kasuje ostatni znak
                    user_text = user_text[:-1]
                elif event.key == pygame.K_RETURN:
                    print(user_text)
                    ethernet_queue_to_HUV.put(user_text)
                    user_text = ''
                else:
                    user_text += event.unicode
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
        screen.fill(WHITE)  # kolor tła okna
        textPrint.reset()   # reset pozycji kursora

        # ---------------------- JOYSTICK ------------------------
        joystick_count = pygame.joystick.get_count()  # sprawdzamy ile joystickow jest podłączonych
        textPrint.indentx()  # przesunięcie poziome kursora
        # For each joystick:
        for i in range(joystick_count):  # dla każdego joysticka (ale mamy tylko jeden!
            joystick = pygame.joystick.Joystick(i)
            joystick.init()
            pygame.draw.rect(screen, rect_color, joystick_rect, 2)
            textPrint.print(screen, "Joystick:")
            textPrint.indentx()

            # Usually axis run in pairs, up/down for one, and left/right for
            # the other.
            axes = joystick.get_numaxes()
            textPrint.print(screen, "Number of axes: {}".format(axes))
            textPrint.indentx()
            for j in range(axes):
                axis = joystick.get_axis(j)
                textPrint.print(screen, "Axis {} value: {:>6.3f}".format(j, axis))
                AxisValues[j] = int(axis*100)
            if gala == 1:
                Calculation(AxisValues, joystick_que, OldAxisValues, magazyn,)
                zero = 0
            elif AxisValues[3] == 0 and zero == 0:
                Calculation(AxisValues, joystick_que, OldAxisValues, magazyn,)

                zero = 1
            gala = 0
            OldAxisValues[0] = AxisValues[0]
            OldAxisValues[1] = AxisValues[1]
            OldAxisValues[2] = AxisValues[2]
            OldAxisValues[3] = AxisValues[3]

            textPrint.unindentx()

            buttons = joystick.get_numbuttons()
            textPrint.print(screen, "Number of buttons: {}".format(buttons))
            textPrint.indentx()

            for m in range(buttons):
                button = joystick.get_button(m)
                textPrint.print(screen, "Button {:>2} value: {}".format(m, button))
                if button == 1:
                    Command = str("{:>2}:{}".format(m, button))
                    joystick_que.put(Command)
            textPrint.unindentx()

            # Hat switch. All or nothing for direction, not like joysticks.
            # Value comes back in an array.
            hats = joystick.get_numhats()
            textPrint.print(screen, "Number of hats: {}".format(hats))
            textPrint.indentx()

            for k in range(hats):
                hat = joystick.get_hat(i)
                textPrint.print(screen, "Hat {} value: {}".format(k, str(hat)))
                if k == 0 and hatclick == 1 and str(hat) != '(0, 0)':
                    left = re.search('(?<=\()(.*?)(?=,)', str(hat))[0]
                    right = re.search('(?<=,)(.*?)(?=\))', str(hat))[0]
                    if right == ' 1':
                        Command = str("{:>2}:{}".format(30, 1))
                        joystick_que.put(Command)
                    elif right == ' -1':
                        Command = str("{:>2}:{}".format(30, 0))
                        joystick_que.put(Command)
                    elif left == '1':
                        Command = str("{:>2}:{}".format(31, 1))
                        joystick_que.put(Command)
                    elif left == '-1':
                        Command = str("{:>2}:{}".format(31, 0))
                        joystick_que.put(Command)

                hatclick = 0
            textPrint.unindentx()

            textPrint.unindentx()
        # --------------------------------------------------------

        # -------------------- INPUT WINDOW ----------------------
        textPrint.reset()           # reset pozycji tekstu do x=0, y=0
        textPrint.x_pos += 295      # przesunięcie pozycji tekstu w poziomie
        textPrint.y_pos += 270      # przesunięcie pozycji tekstu w pionie
        try:
           # jeżeli jest jakiś pojazd w magazynie to wyświetlany tekst poniżej
            textPrint.print(screen, "Message to HUV" + str(magazyn.clients_table_name[magazyn.wybor_HUV][-1]))
        except:
            pass
        textPrint.reset()
        textPrint.second_row()
        pygame.draw.rect(screen, rect_color, input_rect, 2)
        text_surface = textPrint.font.render(user_text, True, [0, 0, 0])
        screen.blit(text_surface, (input_rect.x + 3, input_rect.y + 3))
        # --------------------------------------------------------

        # --------------------- HUV IMAGE ------------------------
        # wyświetlanie poniższych zdjęć w odpowiednich miejscach na ekranie
        screen.blit(HUV_image, (800, 10))
        screen.blit(arrow_up_image, (835, 259))
        screen.blit(arrow_up_image, (987, 259))
        screen.blit(arrow_down_image, (837, 345))
        screen.blit(arrow_down_image, (989, 345))
        # --------------------------------------------------------

        # --------------- HUV selection buttons ------------------
        mouse_pos = pygame.mouse.get_pos()  # czytaj pozycję myszki
        # --------------------------------------------------------

        # --------- WYSWIETLANIE TEKSTU  "Select HUV:"------------
        pozycja_x = poczatek_x              # RESET POZYCJI TEKSTU
        textPrint.x_pos = pozycja_x         # RESET POZYCJI TEKSTU
        textPrint.y_pos = poczatek_y - 20   # RESET POZYCJI TEKSTU
        textPrint.print(screen, str("Select HUV:"))
        # --------------------------------------------------------



################################### PRZYCISKI DOSTEPNYCH HUV #####################################

        for i in magazyn.clients_table_name:                                            # drukowanie tylu przycisków ile pojazdów dostępnych w tabeli w magazynie
            HUV_choose_rect = pygame.Rect(pozycja_x, poczatek_y, rozmiar_x, rozmiar_y)  # ustalanie pozycji ramki przycisku
            if magazyn.clients_table_name.index(i) == magazyn.wybor_HUV:                # jeżeli wybrany któryś z pojazdów to ustaw tło przycisku na zielone
                pygame.draw.rect(screen, [125, 255, 125], HUV_choose_rect, 0)               # rysowanie zielonego tła przycisku
            else:
                pass
            pygame.draw.rect(screen, HUV_choose_rect_color, HUV_choose_rect, 2)         # rysowanie czarnej ramki przycisku

            if HUV_choose_rect.collidepoint(mouse_pos):                                                             # sprawdzamy czy mysz wchodzi na któryś z przycisków
                if pygame.mouse.get_pressed()[0] and (magazyn.clients_table_name.index(i) != magazyn.wybor_HUV):    # jeżeli wchodzi i lewy przycisk myszy wciśnięty oraz aktualnie wybrany pojazd jest inny niż ten po dprzyciskiem to zmień na ten pojazd
                    magazyn.wybor_HUV = int(str(magazyn.clients_table_name.index(i)))                               # tu zmieniamy pojazd na ten na który klikneliśmy

            pozycja_x += przesuniecie                                                   # przesunięcie, żeby następny przycisk drukować dalej a nie w tym samy miejscu co poprzedni

        pozycja_x = poczatek_x              # RESET POZYCJI TEKSTU
        textPrint.x_pos = pozycja_x         # RESET POZYCJI TEKSTU
        textPrint.y_pos = poczatek_y - 20   # RESET POZYCJI TEKSTU

        for i in magazyn.clients_table_name:    # drukowanie tylu przycisków ile pojazdów dostępnych w tabeli w magazynie

            textPrint.x_pos = pozycja_x + 14                    # przesunięcie tekstu względem ramki przycisku w poziomie
            textPrint.y_pos = poczatek_y + 14                   # przesunięcie tekstu względem ramki przycisku w pionie
            textPrint.print(screen, str("HUV" + str(i[-1])))    # dopisanie do "HUV" ostatniego znaku z elementu i czyli numeru pojazdu
            textPrint.y_pos += 25                               # NIE WIEM CO TO ROBI xD
            pozycja_x += przesuniecie                           # przesunięcie tekstu, żeby następny tekst drukować obok a nie w tym samy miejscu co poprzedni
        # --------------------------------------------------------
        pozycja_x = poczatek_x

################################### PRZYCISKI THRUSTER ENABLE HUV ####################################

        for i in magazyn.clients_table_name:  # drukowanie tylu przycisków ile pojazdów dostępnych w tabeli w magazynie
            HUV_choose_rect = pygame.Rect(pozycja_x, poczatek_y + 80, rozmiar_x,rozmiar_y -10)  # ustalanie pozycji ramki przycisku
            try:
                if int(magazyn.clients_table[magazyn.clients_table_name.index(i)].parameter_magazyn[6]) == 1:  # jeśli wartość -1 to znaczy że moduł nie jest uruchamiany (pojazd go nie ma)
                    pygame.draw.rect(screen, [125, 255, 125], HUV_choose_rect, 0)
                if int(magazyn.clients_table[magazyn.clients_table_name.index(i)].parameter_magazyn[6]) == 0:  # jeśli wartość -1 to znaczy że moduł nie jest uruchamiany (pojazd go nie ma)
                    pygame.draw.rect(screen, [255, 125, 125], HUV_choose_rect, 0)
                else:
                    pass
            except:
                pass
            pygame.draw.rect(screen, HUV_choose_rect_color, HUV_choose_rect, 2)  # rysowanie czarnej ramki przycisku

            if HUV_choose_rect.collidepoint(mouse_pos):  # sprawdzamy czy mysz wchodzi na któryś z przycisków
                if pygame.mouse.get_pressed()[0] and wcisniete == 0:  # jeżeli wchodzi i lewy przycisk myszy wciśnięty oraz aktualnie wybrany pojazd jest inny niż ten po dprzyciskiem to zmień na ten pojazd
                    wcisniete = 1
                    magazyn.clients_table[magazyn.clients_table_name.index(i)].send2("THRUSTERENABLE:1")
                elif wcisniete == 1 and pygame.mouse.get_pressed()[0] == 0:
                    wcisniete = 0
            pozycja_x += przesuniecie  # przesunięcie, żeby następny przycisk drukować dalej a nie w tym samy miejscu co poprzedni

################################### WYSWIETLANIE KOLOROW MASZTOW ###################################

        pozycja_x = poczatek_x
        for i in magazyn.clients_table_name:  # drukowanie tylu przycisków ile pojazdów dostępnych w tabeli w magazynie
            HUV_choose_rect = pygame.Rect(pozycja_x, poczatek_y + 38, rozmiar_x,rozmiar_y -10)
            try:
                if int(magazyn.clients_table[magazyn.clients_table_name.index(i)].parameter_magazyn[9]) == 4:  # jeśli wartość -1 to znaczy że moduł nie jest uruchamiany (pojazd go nie ma)
                    pygame.draw.rect(screen, [50, 50, 255], HUV_choose_rect, 0)
                if int(magazyn.clients_table[magazyn.clients_table_name.index(i)].parameter_magazyn[9]) == 3:  # jeśli wartość -1 to znaczy że moduł nie jest uruchamiany (pojazd go nie ma)
                    pygame.draw.rect(screen, [255, 50, 50], HUV_choose_rect, 0)
                if int(magazyn.clients_table[magazyn.clients_table_name.index(i)].parameter_magazyn[9]) == 2:  # jeśli wartość -1 to znaczy że moduł nie jest uruchamiany (pojazd go nie ma)
                    pygame.draw.rect(screen, [50, 255, 50], HUV_choose_rect, 0)
                if int(magazyn.clients_table[magazyn.clients_table_name.index(i)].parameter_magazyn[9]) == 1:  # jeśli wartość -1 to znaczy że moduł nie jest uruchamiany (pojazd go nie ma)
                    pygame.draw.rect(screen, [255, 255, 255], HUV_choose_rect, 0)
                if int(magazyn.clients_table[magazyn.clients_table_name.index(i)].parameter_magazyn[9]) == 0:  # jeśli wartość -1 to znaczy że moduł nie jest uruchamiany (pojazd go nie ma)
                    pygame.draw.rect(screen, [100, 100, 100], HUV_choose_rect, 0)
                else:
                    pass
            except:
                pass
            pygame.draw.rect(screen, HUV_choose_rect_color, HUV_choose_rect, 2)  # rysowanie czarnej ramki przycisku

            textPrint.x_pos = pozycja_x + 14  # przesunięcie tekstu względem ramki przycisku w poziomie
            textPrint.y_pos = poczatek_y + 48 # przesunięcie tekstu względem ramki przycisku w pionie
            textPrint.print(screen, str("MAST"))
            pozycja_x += przesuniecie

################################### OKNA MODULOW HUV ###################################

        pozycja_x = poczatek_x                  # RESET POZYCJI TEKSTU
        textPrint.x_pos = pozycja_x + 445       # ustawienie tekstu w osi x
        textPrint.y_pos = poczatek_y + 410      # ustawienie tekstu w osi y
        poz_x = pozycja_x + 440                 # ustawienie ramki w osi x
        poz_y = poczatek_y + 400                 # ustawienie ramki w osi y

        j = 0
        while j < magazyn.number_of_parameters-6:                       # Wybór które parametry drukujemy jako kontrolki (parametrów jest chyba 7 i drukujemy od 0 do 3)
            HUV_parameters_rect = pygame.Rect(poz_x, poz_y, 60, 30)     # ustalanie pozycji czarnego prostokąta

            try:
                if int(magazyn.clients_table[magazyn.wybor_HUV].parameter_magazyn[j]) == -1:          # jeśli wartość -1 to znaczy że moduł nie jest uruchamiany (pojazd go nie ma)
                    pygame.draw.rect(screen, HUV_parameters_rect_color_grey, HUV_parameters_rect, 0)  # rysowanie szarego tła kontrolki
                if int(magazyn.clients_table[magazyn.wybor_HUV].parameter_magazyn[j]) == 0:
                    pygame.draw.rect(screen, HUV_parameters_rect_color_red, HUV_parameters_rect, 0)  # rysowanie czerwonego tła
                if int(magazyn.clients_table[magazyn.wybor_HUV].parameter_magazyn[j]) == 1:
                    pygame.draw.rect(screen, HUV_parameters_rect_color_green, HUV_parameters_rect, 0)  # rysowanie zielonego tła
            except:
                pass
            textPrint.print(screen, str(magazyn.parameter_id_magazyn[j]))   # wypisanie nazwy parametru na kontrolce

            pygame.draw.rect(screen, [0, 0, 0], HUV_parameters_rect, 2)     # rysowanie ramki kontrolki

            textPrint.x_pos += 70   # przesunięcie tekstu w dół
            textPrint.y_pos = poczatek_y + 410
            poz_x += 70             # przesunięcie ramki i tła w dół

            j +=1           # przejscie do kolejnego parametru

################################### OKNO AKTUAL DEPTH ###################################

        okienko_depth_poz_x = 835
        okienko_depth_poz_y = 190
        pozycja_x = poczatek_x  # RESET POZYCJI TEKSTU
        textPrint.x_pos = pozycja_x + okienko_depth_poz_x + 20  # ustawienie tekstu w osi x
        textPrint.y_pos = poczatek_y + okienko_depth_poz_y + 5  # ustawienie tekstu w osi y
        poz_x = pozycja_x + okienko_depth_poz_x   # ustawienie ramki w osi x
        poz_y = poczatek_y + okienko_depth_poz_y  # ustawienie ramki w osi y


        HUV_parameters_rect = pygame.Rect(poz_x, poz_y, 125, 42)  # ustalanie pozycji czarnego prostokąta
        pygame.draw.rect(screen, [0, 0, 0], HUV_parameters_rect, 2)  # rysowanie ramki kontrolki

        textPrint.print(screen, "Actual Depth")  # wypisanie nazwy parametru na kontrolce

        try:
            textPrint.x_pos = pozycja_x + okienko_depth_poz_x + 42  # ustawienie tekstu w osi x
            textPrint.y_pos = poczatek_y + okienko_depth_poz_y + 22  # ustawienie tekstu w osi y
            textPrint.print(screen, magazyn.clients_table[magazyn.wybor_HUV].parameter_magazyn[10] + " [m]")
        except:
            pass


################################### OKNO THRUSTER POWER LIMIT ###################################
        thruster_power_limit_poz_x = -270
        thruster_power_limit_poz_y = 310
        pozycja_x = poczatek_x  # RESET POZYCJI TEKSTU
        textPrint.x_pos = pozycja_x + thruster_power_limit_poz_x + 5  # ustawienie tekstu w osi x
        textPrint.y_pos = poczatek_y + thruster_power_limit_poz_y  # ustawienie tekstu w osi y
        poz_x = pozycja_x + thruster_power_limit_poz_x  # ustawienie ramki w osi x
        poz_y = poczatek_y + thruster_power_limit_poz_y - 5  # ustawienie ramki w osi y

        HUV_parameters_rect = pygame.Rect(poz_x, poz_y, 200, 21)  # ustalanie pozycji czarnego prostokąta
        try:
            textPrint.print(screen, "Thruster power limit: 0 - "+ str(100-4*magazyn.ograniczenie) + " %" )  # wypisanie nazwy parametru na kontrolce
            pygame.draw.rect(screen, [0, 0, 200], HUV_parameters_rect, 2)  # rysowanie ramki kontrolki
        except:
            pass


################################### OKNO BALLAST TANK PUMP CONTROL ###################################

        # Sprawdzenie, czy kursor znajduje się na suwaku
        if pygame.Rect((slider_pos_x, slider_pos_y), (slider_width, slider_height)).collidepoint(mouse_pos):
            # Sprawdzenie, czy lewy przycisk myszy został wciśnięty
            if pygame.mouse.get_pressed()[0]:
                # Obliczenie wartości suwaka na podstawie pozycji kursora
                relative_pos = mouse_pos[1] - (slider_pos_x, slider_pos_y)[1]
                slider_value = int((relative_pos / slider_height) * value_range + min_value)
                print(slider_value)
                ethernet_queue_to_HUV.put('BALAST:FORCE:'+str(slider_value))

        # Sprawdzenie, czy przycisk myszy został wciśnięty
        if pygame.mouse.get_pressed()[0]:
            # Sprawdzenie, czy kursor znajduje się na przycisku zerowania
            if pygame.Rect((reset_button_pos_x, reset_button_pos_y), (100, 40)).collidepoint(mouse_pos):
                # Wyzerowanie wartości suwaka
                slider_value = 0
                print(slider_value)
                ethernet_queue_to_HUV.put('BALAST:FORCE:' + str(slider_value))


        # Rysowanie ramki

        pygame.draw.rect(screen, (0, 0, 0), ((slider_pos_x-35, slider_pos_y-35), (slider_width+105, slider_height+40)),2)
        arrow_down_text = font.render("Ballast Tank", True, (0, 0, 0))
        arrow_down_text_pos = (slider_pos_x - 10, slider_pos_y + -30)
        screen.blit(arrow_down_text, arrow_down_text_pos)
        arrow_down_text = font.render("Pump Control", True, (0, 0, 0))
        arrow_down_text_pos = (slider_pos_x -15, slider_pos_y + -15)
        screen.blit(arrow_down_text, arrow_down_text_pos)
        # Rysowanie suwaka

        pygame.draw.rect(screen, (200, 200, 200), ((slider_pos_x,slider_pos_y), (slider_width, slider_height)))
        slider_button_pos = ((slider_pos_x), slider_pos_y + int((slider_value - min_value) / value_range * (slider_height - slider_width)))
        pygame.draw.circle(screen, (200, 0, 0), (slider_button_pos[0] + slider_width // 2, slider_button_pos[1] + slider_width // 2), slider_width // 2)

        # Rysowanie wartości suwaka
        value_text = font.render(str(int(slider_value)), True, (0, 0, 0))
        value_text_pos = (slider_pos_x - value_text.get_width() - 5, slider_pos_y + slider_height // 2 - value_text.get_height() // 2)
        screen.blit(value_text, value_text_pos)

        # Rysowanie przycisku zerowania
        pygame.draw.rect(screen, (100, 100, 100), ((reset_button_pos_x, reset_button_pos_y), (60, 20)))
        reset_text = font.render("Zero", True, (255, 255, 255))
        reset_text_pos = (reset_button_pos_x + (60 - reset_text.get_width()) // 2, reset_button_pos_y + (20 - reset_text.get_height()) // 2)
        screen.blit(reset_text, reset_text_pos)

        screen.blit(arrow_up_image, (slider_pos_x + 23, slider_pos_y + 8))
        arrow_up_text = font.render("Pump Out", True, (200, 0, 0))
        arrow_up_text_pos = (slider_pos_x + 23, slider_pos_y + 48)
        screen.blit(arrow_up_text, arrow_up_text_pos)

        screen.blit(arrow_down_image, (slider_pos_x + 25, slider_pos_y + 108))
        arrow_down_text = font.render("Pump In", True, (200, 0, 0))
        arrow_down_text_pos = (slider_pos_x + 23, slider_pos_y + 95)
        screen.blit(arrow_down_text, arrow_down_text_pos)

        pygame.display.flip()   # allows the entire area of screen to update,

        clock.tick(60)

    pygame.quit()
