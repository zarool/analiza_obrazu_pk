import serial
import time
import re

def Krokowy(krokowy_que, magazyn, nucleo_que):
    if magazyn.NUCLEOUsbAddress:
        while True:   ### Petla glowna komunikacji
            command_string = str(krokowy_que.get())
            try: # sprawdz czy zawiera dodatkową komendę
                device = re.search('.+?(?=:)', command_string)[0] # czyli przeszukaj string. od lewej bierz ile mozliwe a od prawej do znaku :
                cut = int(len(str(device))) + 1
                command_send = command_string[cut:]
                
                if str(device) == "ENABLE": # jeżeli dodatkowa komenda ENABLE
                    msg = str('<{}, {}>'.format(15, 1, ))
                    nucleo_que.put(msg)
                    print(msg)
            except: # jeżeli nie zawiera, to to są Hz 
                try:
                    msg = str('<{}, {}>'.format(16, 1000 + int(command_string), ))
                    nucleo_que.put(msg)
                    print(msg) 
                except:
                    print('Bledna ramka dla krokowego')
        
    else:
        pass