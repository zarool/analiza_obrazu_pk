import time

class Morse():
    """Obiekt pozwala na odbiru i dekodowania sygnalu zakodowanych w
        kodzie Morse dla dowolnego kolor. Podaj referencje do magazynu i kolor jaki ma wykrywac jako string"""
    # Dictionary representing the morse code chart
    MORSE_CODE_DICT = {'A': '.-', 'B': '-...',
                       'C': '-.-.', 'D': '-..', 'E': '.',
                       'F': '..-.', 'G': '--.', 'H': '....',
                       'I': '..', 'J': '.---', 'K': '-.-',
                       'L': '.-..', 'M': '--', 'N': '-.',
                       'O': '---', 'P': '.--.', 'Q': '--.-',
                       'R': '.-.', 'S': '...', 'T': '-',
                       'U': '..-', 'V': '...-', 'W': '.--',
                       'X': '-..-', 'Y': '-.--', 'Z': '--..',
                       '1': '.----', '2': '..---', '3': '...--',
                       '4': '....-', '5': '.....', '6': '-....',
                       '7': '--...', '8': '---..', '9': '----.',
                       '0': '-----', ', ': '--..--', '.': '.-.-.-',
                       '?': '..--..', '/': '-..-.', '-': '-....-',
                       '(': '-.--.', ')': '-.--.-', '$': '...-..-',
                       ',': '--..--', '*': '...-..-.'}
    def __init__(self, magazyn, kolor):
        self.kolor = kolor
        self.magazyn = magazyn
        self.run = True
        self.magazyn.messages[kolor] = []

    def decoder(self, message):
        # extra space added at the end to access the
        # last morse code
        message += ' '
        decipher = ''
        citext = ''
        for letter in message:

            # checks for space
            if (letter != ' '):

                # counter to keep track of space
                i = 0

                # storing morse code of a single character
                citext += letter

                # in case of space
            else:
                # if i = 1 that indicates a new character
                i += 1

                # if i = 2 that indicates a new word
                if i == 2:

                    # adding space to separate words
                    decipher += ' '
                else:

                    # accessing the keys using their values (reverse of encryption)
                    decipher += list(self.MORSE_CODE_DICT.keys())[list(self.MORSE_CODE_DICT
                                                                  .values()).index(citext)]
                    citext = ''

        return decipher

    def on(self, magazyn, kolor):
        param = magazyn.colours[kolor]
        return all(i > 8 for i in param)

    def znakmorse(self, time):
        if time < 0.7:
            return  ('.')
        else:
            return  ('-')
    def spacja(self, time, znaknasz):
        if time > 0.8 and time < 2.6 and len(znaknasz) != 0:
            try:
                znak = self.decoder(znaknasz)
                print(znak)
                self.magazyn.messages[self.kolor].append(znak)
            except:
                pass
                print('Bladny znak')
            return True
        elif time > 2 and len(znaknasz) == 0:
            #print(' ')
            return True
        return False
    def receiver(self, magazyn):
        start_time = 0
        magazyn.messages[self.kolor] = []
        znaknasz = []
        while self.run:
            if self.on(magazyn, self.kolor):
                start_time = time.time()
                while self.on(magazyn, self.kolor):
                    pass
                #print((time.time() - start_time))
                znaknasz.append(self.znakmorse((time.time() - start_time)))

            else:
                start_time = time.time()
                while not(self.on(magazyn, self.kolor)):
                    if (time.time() - start_time) > 2:
                        if self.spacja((time.time() - start_time), znaknasz):
                            znaknasz = []
                        break
                    pass
                if self.spacja((time.time() - start_time), znaknasz):
                    znaknasz = []
