
import threading
import serial
import time
import itertools
import re
from time import sleep
# Wątek odbioru danych z kolejki do dynamixli, formatowania ramki < , > i wysyłania jej do wątku mega.
# tutaj odbywa się przeliczanie położeń w zalezności od sterowania. arduino otrzymuje tylko informacje
# jak kąt ma ustawić na którym serwie.
import serial
import time        

def RX_24F(dynamixel_que, magazyn, nucleo_que):
    
    
    polozenieRxId4 = 70
    polozenieRxId5 = 50
    
    # Petla Glowna ########
    while True:
        
        Command = str(dynamixel_que.get())
        func = re.search('.+?(?=:)', Command)[0]
        cut = int(len(str(func))) + 1
        command_string = Command[cut:]
        value_1 = re.search('.+?(?=:)', command_string)[0]
        cut = int(len(str(command_string))) + 1
        Command = command_string[::-1]
        value_2 = re.search('.+?(?=:)', Command)[0]
        value_2 = value_2[::-1]
        #### Pars and send to device #####
        if func == "SETPOSITIONZERO": #ok
            if int(value_1) == 4: # RX24f ID5
                msg = str('<{}, {}>'.format(6, int(magazyn.polozeniezeroRxId4), ))
                nucleo_que.put(msg)
                time.sleep(0.05)
                polozenieRxId4 = magazyn.polozeniezeroRxId4
                msg = str('<{}, {}>'.format(21, int(magazyn.polozeniezeroRxId4), ))
                nucleo_que.put(msg)
                time.sleep(0.05)
                #print(msg)
                #print(msg)
            if int(value_1) == 5: # RX24f ID5
                msg = str('<{}, {}>'.format(7, int(magazyn.polozeniezeroRxId5), ))
                nucleo_que.put(msg)
                time.sleep(0.05)
                polozenieRxId5 = magazyn.polozeniezeroRxId5
                msg = str('<{}, {}>'.format(22, int(magazyn.polozeniezeroRxId4), ))
                nucleo_que.put(msg)
                time.sleep(0.05)
                #print(msg)
                #print(msg)
        elif func == "SETPOSITIONHAT":
            if int(value_1) == 4: # RX24f ID5
                polozenieRxId4 = polozenieRxId4 - int(value_2)
                msg = str('<{}, {}>'.format(6, int(polozenieRxId4), ))
                nucleo_que.put(msg)
                time.sleep(0.05)
                #print(msg)
            if int(value_1) == 5: # RX24f ID5
                polozenieRxId5 = polozenieRxId5 - int(value_2)
                msg = str('<{}, {}>'.format(7, int(polozenieRxId5), ))
                nucleo_que.put(msg)
                time.sleep(0.05)
                #print(msg)
        elif func == "SETPOSITIONJOY":
            if int(value_1) == 4: # RX24f ID4
                msg = str('<{}, {}>'.format(6, int(polozenieRxId4)+int(value_2), ))
                nucleo_que.put(msg)
                time.sleep(0.05)
                #print(msg)
            if int(value_1) == 5: # RX24f ID5
                msg = str('<{}, {}>'.format(7, int(polozenieRxId5)-int(value_2), ))
                nucleo_que.put(msg)
                time.sleep(0.05)
                #print(msg)
        elif func == "BREAK":
            break
        '''elif func == "RXOSCILATION":
                if float(value_1) != 0 and magazyn.RX_oscylatory_movement_mode == 0:
                    magazyn.RX_oscylatory_movement_mode = 1
                    magazyn.RX_frequency = value_1
                    magazyn.RX_amplitude = value_2
                    WaveMove = threading.Thread(target=sin_function_RX,args=(magazyn,))
                    WaveMove.start()
                if float(value_1) != 0 and magazyn.RX_oscylatory_movement_mode == 1:
                    magazyn.RX_oscylatory_movement_mode = 1
                    magazyn.RX_frequency = value_1
                    magazyn.RX_amplitude = value_2
                if float(value_1) == 0 and magazyn.RX_oscylatory_movement_mode == 1:
                    magazyn.RX_oscylatory_movement_mode = 0
                    magazyn.RX_frequency = 0
                    magazyn.RX_amplitude = 0
        ''' 