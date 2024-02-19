import pygame
import math

def rysuj_strzalke(dlugosc_strzalki):
    # Inicjalizacja Pygame
    pygame.init()

    # --------- HUV image ---------
    HUV_image = pygame.image.load("HUV.png")
    arrow_up_image = pygame.image.load("arrow_up.png")
    arrow_down_image = pygame.image.load("arrow_down.png")
    # -----------------------------

    # --------- Ballast Tank ----------
    slider_width = 20
    slider_height = 150
    font = pygame.font.Font(None, 20)
    slider_pos_x = 100
    slider_pos_y = 60
    slider_pos_x, slider_pos_y
    reset_button_pos_x = slider_pos_x + 25
    reset_button_pos_y = slider_pos_y + 68

    min_value = -100
    max_value = 100
    value_range = max_value - min_value

    # Inicjalizacja wartości suwaka
    slider_value = 0

    # Ustawienie rozmiaru okna
    screen_width, screen_height = 800, 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Strzałka")

    # Ustawienie kolorów
    RED = (255, 0, 0)
    WHITE = (255, 255, 255)

    # Początkowe współrzędne strzałki
    x_pocz_prostokata = screen_width // 2
    y_pocz_prostokata = screen_height // 2



    # Kąt strzałki (w stopniach, początkowo ustawiony na 45 stopni)
    kat = 45

    # Długość strzałki (można dostosować)
    dlugosc = dlugosc_strzalki
    dlugosc_prostokata = 0

    # Szerokość prostokąta (można dostosować)
    szerokosc_prostokata = 5

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
        mouse_pos = pygame.mouse.get_pos()
        # Wyczyszczenie ekranu
        screen.fill(WHITE)

        # Narysowanie prostokąta
        if dlugosc_prostokata > 0:
            HUV_parameters_rect = pygame.Rect(x_pocz_prostokata, y_pocz_prostokata, szerokosc_prostokata, dlugosc_prostokata)  # ustalanie pozycji czarnego prostokąta
            pygame.draw.rect(screen, RED, HUV_parameters_rect)  # rysowanie ramki kontrolki
        if dlugosc_prostokata < 0:
            HUV_parameters_rect = pygame.Rect(x_pocz_prostokata, y_pocz_prostokata - abs(dlugosc_prostokata), szerokosc_prostokata,abs(dlugosc_prostokata))  # ustalanie pozycji czarnego prostokąta
            pygame.draw.rect(screen, RED, HUV_parameters_rect)  # rysowanie ramki kontrolki

        # Narysowanie trójkąta na końcu strzałki
        # Obliczenie końcowych współrzędnych strzałki na podstawie długości i kąta
        if dlugosc_prostokata > 0:
            koniec_x = x_pocz_prostokata * math.cos(math.radians(kat))
            koniec_y = (y_pocz_prostokata + dlugosc_prostokata + 10) * math.sin(math.radians(kat))
            trójkąt_wierzchołki = [(x_pocz_prostokata+2, y_pocz_prostokata + dlugosc_prostokata+20), (x_pocz_prostokata - 7,  y_pocz_prostokata + dlugosc_prostokata), (x_pocz_prostokata + 11, y_pocz_prostokata + dlugosc_prostokata)]
            pygame.draw.polygon(screen, RED, trójkąt_wierzchołki)
        if dlugosc_prostokata < 0:
            pass
        ################################### OKNO BALLAST TANK PUMP CONTROL ###################################

        # Sprawdzenie, czy kursor znajduje się na suwaku
        if pygame.Rect((slider_pos_x, slider_pos_y), (slider_width, slider_height)).collidepoint(mouse_pos):
            # Sprawdzenie, czy lewy przycisk myszy został wciśnięty
            if pygame.mouse.get_pressed()[0]:
                # Obliczenie wartości suwaka na podstawie pozycji kursora
                relative_pos = mouse_pos[1] - (slider_pos_x, slider_pos_y)[1]
                slider_value = int((relative_pos / slider_height) * value_range + min_value)
                dlugosc_prostokata = slider_value
                print(slider_value)


        # Sprawdzenie, czy przycisk myszy został wciśnięty
        if pygame.mouse.get_pressed()[0]:
            # Sprawdzenie, czy kursor znajduje się na przycisku zerowania
            if pygame.Rect((reset_button_pos_x, reset_button_pos_y), (100, 40)).collidepoint(mouse_pos):
                # Wyzerowanie wartości suwaka
                slider_value = 0
                print(slider_value)
                dlugosc_prostokata = slider_value


        # Rysowanie ramki

        pygame.draw.rect(screen, (0, 0, 0),
                         ((slider_pos_x - 35, slider_pos_y - 35), (slider_width + 105, slider_height + 40)), 2)
        arrow_down_text = font.render("Ballast Tank", True, (0, 0, 0))
        arrow_down_text_pos = (slider_pos_x - 10, slider_pos_y + -30)
        screen.blit(arrow_down_text, arrow_down_text_pos)
        arrow_down_text = font.render("Pump Control", True, (0, 0, 0))
        arrow_down_text_pos = (slider_pos_x - 15, slider_pos_y + -15)
        screen.blit(arrow_down_text, arrow_down_text_pos)
        # Rysowanie suwaka

        pygame.draw.rect(screen, (200, 200, 200), ((slider_pos_x, slider_pos_y), (slider_width, slider_height)))
        slider_button_pos = ((slider_pos_x), slider_pos_y + int((slider_value - min_value) / value_range * (slider_height - slider_width)))
        pygame.draw.circle(screen, (200, 0, 0),(slider_button_pos[0] + slider_width // 2, slider_button_pos[1] + slider_width // 2),slider_width // 2)

        # Rysowanie wartości suwaka
        value_text = font.render(str(int(slider_value)), True, (0, 0, 0))
        value_text_pos = (slider_pos_x - value_text.get_width() - 5, slider_pos_y + slider_height // 2 - value_text.get_height() // 2)
        screen.blit(value_text, value_text_pos)

        # Rysowanie przycisku zerowania
        pygame.draw.rect(screen, (100, 100, 100), ((reset_button_pos_x, reset_button_pos_y), (60, 20)))
        reset_text = font.render("Zero", True, (255, 255, 255))
        reset_text_pos = (reset_button_pos_x + (60 - reset_text.get_width()) // 2,reset_button_pos_y + (20 - reset_text.get_height()) // 2)
        screen.blit(reset_text, reset_text_pos)

        screen.blit(arrow_up_image, (slider_pos_x + 23, slider_pos_y + 8))
        arrow_up_text = font.render("Pump Out", True, (200, 0, 0))
        arrow_up_text_pos = (slider_pos_x + 23, slider_pos_y + 48)
        screen.blit(arrow_up_text, arrow_up_text_pos)

        screen.blit(arrow_down_image, (slider_pos_x + 25, slider_pos_y + 108))
        arrow_down_text = font.render("Pump In", True, (200, 0, 0))
        arrow_down_text_pos = (slider_pos_x + 23, slider_pos_y + 95)
        screen.blit(arrow_down_text, arrow_down_text_pos)

        # Odświeżenie ekranu
        pygame.display.flip()

    pygame.quit()

# Przykładowe użycie funkcji z różnymi długościami strzałki i prostokąta
dlugosc_strzalki_1 = 50
dlugosc_prostokata_1 = 100
rysuj_strzalke(dlugosc_strzalki_1)






