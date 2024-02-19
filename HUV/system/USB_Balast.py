import serial
import time
import re

def Balast(balast_que, magazyn,nucleo_que):
    if magazyn.NUCLEOUsbAddress:
        while True:   ### Petla glowna komunikacji
            command_string = str(balast_que.get())
            try: # sprawdz czy zawiera dodatkową komendę
                device = re.search('.+?(?=:)', command_string)[0] # czyli przeszukaj string. od lewej bierz ile mozliwe a od prawej do znaku :
                cut = int(len(str(device))) + 1
                command_send = command_string[cut:]
                
                if str(device) == "STATICDEPTH": #ok 
                    magazyn.set_static_depth= command_send
                    msg = str('<{}, {}>'.format(1,float(command_send), ))
                    nucleo_que.put(msg.encode('utf-8'))
                    print(msg)
            
                elif str(device) == "DYNAMICPITCH": #ok 
                    magazyn.set_dynamic_pitch = command_send
                    msg = str('<{}, {}>'.format(3,float(command_send), ))
                    nucleo_que.put(msg.encode('utf-8'))
                    print(msg)

                elif str(device) == "DYNAMICDEPTH": #ok
                    magazyn.set_dynamic_depth = command_send
                    msg = str('<{}, {}>'.format(2,float(command_send), ))
                    nucleo_que.put(msg.encode('utf-8'))
                    print(msg)
            
                elif str(device) == "FORCE": #ok
                    magazyn.set_depth = -1
                    msg = str('<{}, {}>'.format(4,int(command_send), )) # start pomiaru zanurzenia
                    nucleo_que.put(msg.encode('utf-8'))
                    print(msg)

                elif str(device) == "KOREKTA": # no
                    msg = str('<{}, {}>'.format(6,float(command_send), )) # start pomiaru zanurzenia
                    nucleo_que.put(msg.encode('utf-8'))
                    print(msg)
            except: # jeżeli nie zawiera, to to są Hz 
                print('Bledna ramka dla balastu')
        
    else:
        pass
    
    
        