import cv2
import numpy as np
import copy
import time

class Detektor():
    def __init__(self, mask_lb, mask_ub):
        """Podaj jaki kolor detektora ma wykrywac - jego dolna i grona granice"""
        self.mask_lb = mask_lb
        self.mask_ub = mask_ub
        self.show_on_screen = True
        self.frame_copy = []
        self.hsv = []
        self.mask = []
        self.run = True

    def Detekcja_Koloru(self, magazyn, kolor):
        magazyn.colours[kolor] = [0, 0, 0, 0] ### Tworze miejsce w magazynie na info o polozeniu danego koloru
        jest = 0
        start = time.time()
        frame_count = 0
        while self.run:
            self.frame_copy = copy.deepcopy(magazyn.getframe()) ### Pobierz ramek z magazynu
            self.hsv = cv2.cvtColor(self.frame_copy, cv2.COLOR_BGR2HSV)  # Zamiana warstwy zdjecia na format HSV
            
            # define range of red color in HSV
            lower_b = np.array(self.mask_lb)
            upper_b = np.array(self.mask_ub)
            
            self.mask = cv2.inRange(self.hsv, lower_b, upper_b) # Nałożenie Maski - potrzebne do wykrycia elementu o danym kolorze
            
            contours = cv2.findContours(self.mask.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[-2] # Wykrywanie koloru
            if len(contours) > 0:                              # jeżeli wykryto jakiś kształt kształt
                red_area = max(contours, key=cv2.contourArea)  # wybierz największy z nich (mniejsze pomiń)
                x, y, w, h = cv2.boundingRect(red_area)        # wyznacz prawy górny róg 
                cv2.rectangle(self.frame_copy, (x, y), (x + w, y + h), (100, 200, 150), 1) #narysuj prostokąt od prawego górnego rogu
                magazyn.colours[kolor] = [x, y, w, h] ### Zapis informacji o wykrytym konturze do magazynu 
                print([x, y, w, h])
            else:
                magazyn.colours[kolor] = [0, 0, 0, 0] ### Obiekt niewykryty
            if self.show_on_screen == True:
                cv2.imshow(kolor, self.mask)
                cv2.imshow("test", magazyn.getframe())
              
                jest = 1
            if self.show_on_screen == False and jest == 1:
                cv2.destroyWindow(kolor)
                jest = 0
            self.frame_copy = None
            if not(self.run):
                self.frame_copy = None
                print('Koncze prace detekora')
                break
            cv2.waitKey(1)
            frame_count += 1
            if time.time() - start >= 1:
                print("{}fps detector".format(frame_count))
                start = time.time()
                frame_count = 0

        pass

# To sluzy do testow
if __name__ == "__main__":
    det = Detektor([0,0,0],[180,255,255])