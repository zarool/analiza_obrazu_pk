### Propozycja sposoby kodowania danych przy pomocy polozenia kolorów ###

import time
import itertools





class Magpie():
    ### zdeklaruj tablice prawd
    #### HERE ####

    def __init__(self, magazyn, R, G, B, Y, P):
        ### Obiekty z schowka
        self.keys = [R, G, B, Y, P]
        self.red = R
        self.green = G
        self.blue = B
        self.yellow = Y
        self.purple = P
        self.ilosc_probek = 3
        self.magazyn = magazyn
        self.run = True
        self.values = []
        self.keys = []
        self.permutacje = []
        self.generate()
        self.kolor = 'RED'

    def rotate(self, l, n):
        return l[n:] + l[:n]

    def generate(self):
        kolory = ['R', 'G', 'B', 'Y', 'P']  ## Kolor RED/GREEN/BLUE/YELLOW/PURPLE
        segmenty = 5

        for subset in itertools.permutations(kolory, segmenty):
            self.permutacje.append(list(subset))

    def decoder(self):
        sign = []
        while len(self.values) > 0:
            maksimum = min(self.values)
            maks_index = self.values.index(maksimum)
            sign.append(self.keys[maks_index])
            del self.values[maks_index]
            del self.keys[maks_index]
        #print(sign)
        return sign

    def aquire_message(self):
        for key in self.magazyn.colours:
            self.values.append(self.magazyn.colours[key][1])
            self.keys.append(str(key))
        pass

    def read_value(self, szukana):
        index = self.permutacje.index(szukana)
        #print(index)
        #print(self.permutacje[index])
        #print(chr(index + 36))
        return chr(index + 36)


    def receiver(self):
        start_time = 0
        poprzedni = '0'
        znaczek = 0
        self.magazyn.messages[self.kolor] = []

        odbieraj = False
        dlugosc = 88
        wait_duration = 0.3

        while self.run:

            self.aquire_message()
            sekwencja = self.decoder()
            value = self.read_value(sekwencja)
            #print(self.magazyn.messages[self.kolor])
            #print(self.magazyn.messages[self.kolor])

            if value == '$':
                self.magazyn.messages[self.kolor].append(value)
                odbieraj = True
                time.sleep(wait_duration)
            elif odbieraj:
                time.sleep(wait_duration)
                self.magazyn.messages[self.kolor].append(value)
                #print(self.magazyn.messages[self.kolor])
                if value == '*':
                    dlugosc = len(self.magazyn.messages[self.kolor])

            if len(self.magazyn.messages[self.kolor]) - dlugosc == 2:
                #print(self.magazyn.messages[self.kolor])
                odbieraj = False
                dlugosc = 88

            if (len(self.magazyn.messages[self.kolor]) == 83):
                #print(self.magazyn.messages[self.kolor])
                self.magazyn.messages[self.kolor] = []

            try:
                self.magazyn.messages[self.kolor].index('$')
            except:
                dlugosc = 88
                self.magazyn.messages[self.kolor] = []






