import pynmea2
import time
#msg = pynmea2.GGA('GP', 'GGA', ('184353.07', '1929.045', 'S', '02410.506', 'E', '1', '04', '2.6', '100.00', 'M', '-33.9', 'M', '', '0000'))
# msg = pynmea2.HDT('US',  'GNS', ('0.0', 'T'))
# msg = pynmea2.GNS('US', 'GNS', ('2', 'b'))
# print(str(msg))
# msg = str(msg)
# print(msg)
# msg = pynmea2.parse(str(msg))
# print(str(msg))

# streamreader = pynmea2.NMEAStreamReader()

# while 1:
#     data = input('ok')
#     for msg in streamreader.next(data):
#         print(msg)
import copy

class NMEA0183 ():

   def  __init__ (self,  kolor):
       self.run = True
       self.kolor = str(kolor)


   def dekoder(self, magazyn):
       while self.run:
           time.sleep(0.1)
           if '$' in magazyn.messages[self.kolor]:
               if '*' in magazyn.messages[self.kolor]:
                   if (len(magazyn.messages[self.kolor]) - magazyn.messages[self.kolor].index('*')) == 3:
                       # print(magazyn.messages[self.kolor])
                       msg = ''.join(magazyn.messages[self.kolor])
                       try:
                           ### Miejsce na obsluzenie odczytanej wiadomosci ###
                           msg = pynmea2.parse(str(msg))
                           print(str(msg))
                       except:
                           print('Bledna wiadomosc')
                           print(magazyn.messages[self.kolor])
                       magazyn.messages[self.kolor] = []
           if len(magazyn.messages[self.kolor]) == 83:
               magazyn.messages[self.kolor] = []

