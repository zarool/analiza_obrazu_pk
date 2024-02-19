import queue
import threading
import re
import sys
sys.path.append('../')
#import arducam_mipicamera as arducam
#import v4l2
import time
import numpy as np
'''
    Plik gowny. Tutaj pracuje main program i w nim interpretowane sa komendy od PC.
    Tutaj tworzony jest:
    - obiekt kamery (do akwizycji obrazu)
    - obiekt detektora (do wykrywania koloru na obrazie
    - obiekt kontroler (do sterowania pojazdem na podstawie informacji z detektora)
    - obiekty: Morse, Magpie, NMEA0183 do komunikacji swietlnej.
'''
#from isp_lib import *
import math
import copy

### Do obslugi kamery
import cv2
### Z moich plików ###
from RPi_Rozp_Kontroler import Kontroler
from Jetson_Rozp_Kamerka import Camera_Maszt
from RPi_Rozp_Detector import Detektor
from RPi_Rozp_Morse import Morse
from RPi_Rozp_Magpie import Magpie
from RPi_Rozp_nmea0183 import NMEA0183

class Speed:
    def __init__(self,a):
        self.a = a

class Brightness:
    def __init__(self,a):
        self.a = a
class Mask_Lb:
    def __init__(self,a):
        self.a = a
class Mask_Ub:
    def __init__(self,a):
        self.a = a



def DekodowanieWiadomosci(message):
    func = re.search('.+?(?=:)', message)[0]
    func = str(func)
    message = message[::-1]  # Funkcja do odwaracanie ciagu znakow
    value = re.search('.+?(?=:)', message)[0]
    value = value[::-1]  # Funkcja do odwaracanie ciagu znakow
    return func, value

def ZmianaKoloru(wartosc):
    ### Wartosci dla kolorow nad woda - wyznaczone metoda doswiadczalna
    if wartosc == 'RED':
        Mask_Lb.a = [150, 180, 10]
        Mask_Ub.a = [180, 255, 255]
    elif wartosc == 'BLUE':
        Mask_Lb.a = [105, 114, 49]
        Mask_Ub.a = [135, 255, 255]
    elif wartosc == 'GREEN':
        Mask_Lb.a = [40, 136, 78]
        Mask_Ub.a = [70, 255, 255]
    elif wartosc == 'REDLOW':
        Mask_Lb.a = [0, 180, 10]
        Mask_Ub.a = [10, 255, 255]
    elif wartosc == 'REDUW':
        Mask_Lb.a = [140, 120, 10]
        Mask_Ub.a = [180, 255, 255]
    elif wartosc == 'GREENUW':
        Mask_Lb.a = [40, 136, 78]
        Mask_Ub.a = [70, 255, 255]
    elif wartosc == 'BLUEUW':
        Mask_Lb.a = [85, 114, 49]
        Mask_Ub.a = [95, 255, 255]
    elif wartosc == 'YELLOW':
        Mask_Lb.a = [21, 39, 64]
        Mask_Ub.a = [35, 255, 255]
    elif wartosc == 'PURPLE':
        Mask_Lb.a = [140, 70, 70]
        Mask_Ub.a = [160, 255, 255]
    ### Mozliwosc rozszerzenia o wpisywanie wartosci recznie - rozszerz bazujac na module re
    return

def main_program(parser_que, Camera_Detect_Queue,camera_ctrl_que, flag, magazyn):
    print('Rozpoczynam dzialaniem petli glownej - kontrola kamery!!!')

    # Wielkosc klatki
    size = [480, 640]
    Speed.a = 0
    Brightness.a = 40
    ### Wstepne wartosci do wykrycia - czerwony
    Mask_Lb.a = [0, 180, 10]
    Mask_Ub.a = [20, 255, 255]
    ### Magazyn obiektuow
    detektory = {}  #### Aktulanie stworzone obiekty -detektorow koloru
    kontrolery = {} ### Aktulanie dzialajace detektory - dla danych kolorow - elementow
    detektory_watki = {} #### Aktulanie dzialajace watki detektorow kolorów
    kontrolery_watki = {} ### Aktulanie dzialajace watki kontrolerow
    morsy = {} ### Aktulanie stworzone obiekty - odczyt kodu morsa z specyficznego koloru
    morsy_watki = {} ### Aktulanie dzialajace watki co odczytuja kod Morsa
    magpiee = {} ### Aktulanie stworzone obiekty- odczyt kody Magpie z kolorów
    magpiee_watki = {} ### Aktulanie dziajalace watki odczytujace kod Magpie
    nmea = {} ### Aktualnie stworzone obiekty - protokół NMEA0183
    nmea_watki = {}  ### Aktulanie dzialajce watki protkołu NMEA0183
    ### Speed to set
    speed = 0

    while True:
        message = Camera_Detect_Queue.get() # Odbierz wiadomosc dla modulu detekcji koloru
        print("wiadomosc" + str(message))
        try:
            funkcja, wartosc = DekodowanieWiadomosci(message) # Dekodowanie wiadomosci
        
            # print(funkcja, wartosc) # Testowe  na potrzeby kontroli wiadomosci
            ### Dekodowanie i obsluga funkcji
            if funkcja == 'KOLOR':
                ZmianaKoloru(str(wartosc))  ### Usawt kolor ktory bedzie wykrywany RGB
                time.sleep(0.2)
                #print(wartosc)
            elif funkcja == 'WYKRYWAJ': ### Rozpocznij komunikacje z kamera i wykrywanie obiektu w danym kolorze
                detektory[str(wartosc)] = (Detektor(copy.deepcopy(Mask_Lb.a), copy.deepcopy(Mask_Ub.a))) ## Tworzeni obiektu
                print(Mask_Ub.a, Mask_Lb.a) ### Podaj jaka maske nakladasz
                print(detektory[str(wartosc)])
                detektory_watki[str(wartosc)] = (threading.Thread(target=detektory[str(wartosc)].Detekcja_Koloru,
                                                                  args=(magazyn, str(wartosc))))  ### Tworzenie watku
                detektory_watki[str(wartosc)].start()
                time.sleep(0.2)
            elif funkcja == 'NIEWYKRYWAJ': ### Zakończ wykrywanie i zatrzymaj prace pętli kontroli
                print('Zatrzymaj wykrywanie')
                detektory[str(wartosc)].show_on_screen = False ### Zamknij okno danego detektora
                time.sleep(1) ### zaczekaj
                detektory[str(wartosc)].run = False ### Zatrzymaj detektor
                print('OK zatrzymano detektor koloru {}'.format(wartosc))
                pass

            elif funkcja == 'WYKRYWAJSHOW':
                detektory[str(wartosc)].show_on_screen = True
                time.sleep(0.2)

            elif funkcja == 'KONTROLER':
                flag_kontroler = False
                kontrolery[str(wartosc)] = Kontroler() ### Stworz obiekt kontorlera
                kontrolery_watki[str(wartosc)] = threading.Thread(target=kontrolery[str(wartosc)].TrackColour,args=(parser_que, size, magazyn,camera_ctrl_que, str(wartosc), lambda: flag_kontroler))
                kontrolery_watki[str(wartosc)].start() ### Uruchom dany watek kontrolera
                time.sleep(0.2)
            elif funkcja == 'KONTROLERSTOP':
                print('Zatrzymaj kontroler')
                flag_kontroler = True
                print('Zatrzymano kontroler')
                time.sleep(3)
                del kontrolery[str(wartosc)] ### usun obiekt kontrolera - do rozowoju bo ta flaga moze byc inaczej rozwiazana

            elif funkcja == 'DYSTANS':
                print("Ustaw dystans {}".format(wartosc))
                magazyn.set_rozpoznawanie_distance =  float(wartosc)
                time.sleep(0.2)

            elif funkcja == 'PREDKOSC':
                print("Ustaw predkosc {}".format(wartosc))
                magazyn.set_rozpoznawanie_speed =  float(wartosc)/10
                time.sleep(0.2)
            elif funkcja == 'PREDKOSCKP':
                print("Ustaw predkosc Kp {}".format(wartosc))
                magazyn.rozpoznawanie_speed_Kp=  float(wartosc)
                time.sleep(0.2)
            elif funkcja == 'PREDKOSCKI':
                print("Ustaw predkosc Ki {}".format(wartosc))
                magazyn.rozpoznawanie_speed_Ki =  float(wartosc)
                time.sleep(0.2)
            elif funkcja == 'PREDKOSCKD':
                print("Ustaw predkosc Kd {}".format(wartosc))
                magazyn.rozpoznawanie_speed_Kd =  float(wartosc)
                time.sleep(0.2)

            elif funkcja == 'KAMERA': ### Rozpocznij akwizycje obrazu z kamery
                print("Rozpocznij akwizycje obrazu.")
                kamera = Camera_Maszt()
                flag_kamera = False
                t1 = threading.Thread(target=Camera_Maszt.Camera_Maszt_Akwizycja, args=(kamera, magazyn, flag_kamera))
                t1.start()
                time.sleep(0.2)
            elif funkcja == 'KAMERASTOP':
                flag_kamera = True
                time.sleep(6)
                print('Zatrzymano akwizycje obrazu')
                del kamera
            elif funkcja == "AK":
                pass
            elif funkcja == "PRZESLONA":
                kamera.camera.shutter_speed = int(wartosc)
                time.sleep(0.2)
            elif funkcja == "FRAMERATE":
                kamera.camera.framerate = int(wartosc)
                time.sleep(0.2)
            elif funkcja == "POZYCJE":
                print(magazyn.colours)
                time.sleep(0.2)

            ### Obsluga Morse
            elif funkcja == 'MORSE':
                morsy[str(wartosc)] = (
                    Morse(magazyn, str(wartosc)))  ## Tworzeni obiektu
                morsy_watki[str(wartosc)] = threading.Thread(target=morsy[str(wartosc)].receiver, args=(magazyn, ))  ### Tworzenie watku
                morsy_watki[str(wartosc)].start()

            elif funkcja == 'MORSESTOP':  ### Zakończ wykrywanie i zatrzymaj prace pętli kontroli
                print('Zatrzymaj dekodowanie kodu Morse')
                morsy[str(wartosc)].run = False  ### Zatrzymaj detektor
                time.sleep(1)
                print('OK zatrzymano dekoder Morsa: {}'.format(wartosc))
                del morsy[str(wartosc)]
                print('Usunieto obiekt dekodera Morsa - {}'.format(str(wartosc)))

            ### Obsluga MAGPIE
            elif funkcja == 'MAGPIE':
                magpiee[str(wartosc)] = (Magpie(magazyn, 'R', 'G', 'B', 'Y', 'P')) ### Tworzenie obiektu
                magpiee_watki[str(wartosc)] = threading.Thread(target=magpiee[str(wartosc)].receiver, args=()) ### Tworzenie watku
                magpiee_watki[str(wartosc)].start()
            elif funkcja == 'MAGPIESTOP':
                print('Zatrzymaj dekodowanie kodu Magpie')
                magpiee[str(wartosc)].run = False  ### Zatrzymaj detektor
                time.sleep(1)
                print('OK zatrzymano dekoder Magpie: {}'.format(wartosc))
                del magpiee[str(wartosc)]
                print('Usunieto obiekt dekodera Magpie - {}'.format(str(wartosc)))

            ### OBSLUGA NMEA0183

            elif funkcja == 'NMEA':
                nmea[str(wartosc)] = (NMEA0183(str(wartosc)) ) ### Tworzenie obiektu
                nmea_watki[str(wartosc)] = threading.Thread(target=nmea[str(wartosc)].dekoder,
                                                               args=(magazyn, ))  ### Tworzenie watku
                nmea_watki[str(wartosc)].start()
            elif funkcja == 'NMEASTOP':
                print('Zatrzymaj dekodowanie wiadomosci NMEA')
                nmea[str(wartosc)].run = False  ### Zatrzymaj detektor
                time.sleep(1)
                print('OK zatrzymano dekoder NMEA: {}'.format(wartosc))
                del nmea[str(wartosc)]
                print('Usunieto obiekt dekodera NMEA - {}'.format(str(wartosc)))
            if flag(): # Warunek wyjścia z petli glownej
                break
        except Exception as error:
            print("An exception occurred:", error) # An exception occurred: division by zero
