import math
import time
import copy
from numpy import interp
class Kontroler():
    def __init__(self):
        self.predkosc = 0              # Predkosc default = 0 , ustawiane z poziomu modul rozpoznawania
        self.kolor = 'RED'             # Jaki kolor wykrywa - to jest default ystawiamy przy wywolaniu funkcji
        self.rozkazuj = True           # Możliwość wyłączania wysyłania sygnałów
        self.sygnal_sterujacy_old = 0
        
        self.uchyb_odleglosc = 0
        self.odleglosc_rzeczywista = 0 # odleglosc zadana z Storage_HUV2
        
        
        self.predkosc_set = 0
        self.Kp_predkosc = 100
        
        self.tolerancja_odleglosci_zadanej = 0.05 #(+/- ile jest akceptowalne od odległości zadanej)
        
        self.kamera_ustawienie_poczatkowe = 1500
        self.kamera_ustawienie = 1500  # kąt ustawienia kamery (zmienia się wraz z podążaniem kamery za wykrytym obiektem)
        self.bearing = 0               # kąt ustawienia pojazdu
        self.sygnal_bearing = 0        # sygnał sterujący idący na regulator kursu pojazdu
        self.chwilowe = 0
        
    def PowierzchniaObiektu(self, x, y):
        # print(x, y)
        area = x * y
        return area

    def Srednia(self, lst):
        return sum(lst) / len(lst)
    
    def Kontrola_kamery(self,camera_ctrl_que): # funkcja odpowiedzialna za podążanie kamery za wyrytym kolorem. Wynikiem jest 
        if (self.chwilowe > 30 and self.chwilowe < 100) or (self.chwilowe < -30 and self.chwilowe > -100):
            if ((self.kamera_ustawienie-1500)) <= 800 and ((self.kamera_ustawienie-1500)) >= -800:
                self.kamera_ustawienie = self.kamera_ustawienie - int(self.chwilowe*0.5)
                camera_ctrl_que.put(self.kamera_ustawienie)         
            #print("ustawienie kamery: " + str(self.kamera_ustawienie-1500) + " chwilowe: " + str(self.chwilowe*0.5))    
            self.chwilowe = 0
    
    def Kontrola_predkosci(self,magazyn):
        
        self.uchyb = self.odleglosc_rzeczywista - magazyn.set_rozpoznawanie_distance
        print(self.uchyb)
        if magazyn.thruster_enable == 1:
            if self.uchyb < 0:
                self.predkosc_set = self.uchyb * self.Kp_predkosc * magazyn.set_rozpoznawanie_speed-60
            else:
                self.predkosc_set = self.uchyb * self.Kp_predkosc * magazyn.set_rozpoznawanie_speed
               #print(self.predkosc_set)
               
 

        
    def WydajRozkaz(self, parser_que,magazyn): # wydawanie rozkazów pędnikom.
        if self.rozkazuj and self.sygnal_bearing != self.sygnal_sterujacy_old or self.predkosc_set > 10 or self.predkosc_set < -10:
            Command = 'THRUSTER:2:{}'.format(int(1500 + self.sygnal_bearing + (self.predkosc_set * magazyn.set_rozpoznawanie_speed)))
            parser_que.put(Command)
            print(Command) # Check if command work properly
            Command = 'THRUSTER:1:{}'.format(int(1500 - self.sygnal_bearing + (self.predkosc_set * magazyn.set_rozpoznawanie_speed)))
            parser_que.put(Command)
            print(Command) # Check if command work properly
        self.sygnal_sterujacy_old = self.sygnal_bearing

    def TrackColour(self, parser_que, size, magazyn,camera_ctrl_que, kolor, flag):
        ### Petla sledzaca
        
        zadany_kat_kamery = size[-1] / 2
        zakres = [-3, 4]
        wspolczynnik_p = 100
        ilosc_probek = 1 # ile próbek musi mieć prawidłowo wykryty obszar kolorowy żeby realizować sterowanie
        sygnal_lista = []
        ctr = 0
        p_old = 0
        wykryto = False
        kierunek = 'L'
        self.kolor  = str(kolor)
        
        stop = 1
        kierunek = 'R'
        while True:
            

            x, y, w, h = magazyn.colours[self.kolor] ### Pobierz informacje i sprawdz czy nowa ramka lub zgubiona - wtedy obsluz
            p = self.PowierzchniaObiektu(w, h)  # Oblicz powierzchnie p - wykrytego obiektu
            # zakres zmiany x jest od 0 do 630
            #### JEŻELI WYKRYTO OBIEKT #### 
            if h > w and h / w < 10:  # Warunek 1 - obiekt musi byc prostokątem a stosunek wysokosci do szerokosci nie powinien byc wiekszy niz 3
                if p > 150 and p < 25000:  # Warunek 2 - obiektu wykrytu musi byc większy niż penwa granica
                    #print(str(w) + "," + str(h))
                    
                    wykryto = True # FLAGA POTWIERDZAJĄCA WYKRYCIE (używana w momencie, gdy wykryto ale uciekł/zniknął)

                    self.sygnal_bearing = interp((self.kamera_ustawienie - 1500), [-800,800],[-100,100])

                    if len(sygnal_lista) == ilosc_probek: # JEŻELI WYKRYTO
                        self.sygnal_bearing = self.Srednia(sygnal_lista) # średnia wykrycia z ilości próbek
                        if self.sygnal_bearing > 0:
                            self.sygnal_bearing = self.sygnal_bearing + 20
                        elif self.sygnal_bearing < 0:
                            self.sygnal_bearing = self.sygnal_bearing - 20
                        self.chwilowe = interp(zadany_kat_kamery - (x + (1 / 2) * w),[-300,300],[-100,100]) # położenie na obrazie

                        if self.chwilowe < 0:
                            kierunek = 'L'
                        elif self.chwilowe > 0:
                            kierunek = 'P'

                        
                        self.Kontrola_predkosci(magazyn)
                            
                        self.Kontrola_kamery(camera_ctrl_que)  # OBRÓT KAMERY za wykrytym kolorem    
                        self.WydajRozkaz(parser_que,magazyn)
                        
                        sygnal_lista = [] # jeżeli wykonały się komendy sterujące to wyczysc tablice sygnałów
                        time.sleep(0.1)
                        stop = 0
                    else:   # jeżeli nie ma jeszcze odpowiedniej ilości sygnałów w tablicy to dodaj nowy poniżej.
                        sygnal_lista.append(int(self.sygnal_bearing))
                    self.odleglosc_rzeczywista = 83/h
                    
                    #print("odleglosc" + str(self.odleglosc_rzeczywista) + "wysokosc" + str(h))
                        ##############################################################
                else:  # jeżeli nie ma wykrytego obiektu o określonej minimalnej wielkości
                    if len(sygnal_lista) == ilosc_probek: # to podobnie jak wczesniej sprawdz ile jest juz sygnalow w taabeli
                        self.sygnal_bearing = self.Srednia(sygnal_lista) # jeżeli wystarczająco 
                        # Narazie nie wykorzystane
                        sygnal_lista = []
                    else:
                        sygnal_lista.append(int(0)) # jeżeli nie ma odpowiedniej liczby sygałów to dodaj nowy zerowy
                        
            #### JEŻELI WYKRYTO ALE UCIEKŁ W PRAWO LUB W LEWO ####
            elif wykryto == True: 
                if kierunek == 'L' and (self.kamera_ustawienie-1500) > -700 and (self.kamera_ustawienie-1500) <700:
                    self.kamera_ustawienie = self.kamera_ustawienie + 50
                    camera_ctrl_que.put(self.kamera_ustawienie)
                    time.sleep(0.1)
                elif kierunek == 'P'and (self.kamera_ustawienie-1500) > -700 and (self.kamera_ustawienie-1500) <700:
                    self.kamera_ustawienie = self.kamera_ustawienie - 50
                    camera_ctrl_que.put(self.kamera_ustawienie)
                    time.sleep(0.1)
                else:
                    self.kamera_ustawienie = 1500
                    camera_ctrl_que.put(self.kamera_ustawienie)
                    Command = 'THRUSTER:2:{}'.format(1500)
                    parser_que.put(Command)
                    Command = 'THRUSTER:1:{}'.format(1500)
                    parser_que.put(Command)
                    wykryto = False
            #### JEŻELI NIEWYKRYTO OBIEKTU ####
            else:
                Command = 'THRUSTER:2:{}'.format(1500)
                #parser_que.put(Command)
                Command = 'THRUSTER:1:{}'.format(1500)
                #parser_que.put(Command)   
                stop = 1
                time.sleep(0.2)
             
