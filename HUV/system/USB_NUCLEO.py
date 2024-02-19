import serial
import time
import threading
import re
import io
from datetime import datetime
from serial.tools import list_ports

def time_cutter(time_): # funkcja wycinająca z datetime.now() tylko sekundy
        device = re.search('.+?(?=:)', time_)[0]
        cut = int(len(str(device))) + 1
        command_send = time_[cut:]
        device = re.search('.+?(?=:)', command_send)[0]
        cut = int(len(str(device))) + 1
        device = command_send[cut:]
        return device

def communicationNUCLEO(nucleo_que, magazyn):
    ### Sprawdz czy obiekt portu istnieje - jezeli nie podlacz
    if magazyn.NUCLEOUsbAddress == None:
        print("NUCLEO- WYSZUKIWANIE")
        ConnectToNucleo(magazyn,nucleo_que)
    
    magazyn.status = 'IDLE'
    
    t1 = threading.Thread(target=send, args=(nucleo_que, magazyn)) # wątek ciągłego wysyłania ramek do MEGA
    t1.start()
    
    t2 = threading.Thread(target=recv, args=(magazyn,nucleo_que)) # wątek odbierania ramek z mega i rutowania dalej
    t2.start()
 
def ReconnectToNucleo(magazyn,):
    time.sleep(1)
    device_list = list_ports.comports()
    
    for device in device_list:
        if (device.vid == magazyn.NUCLEO_VID) and (device.pid == magazyn.NUCLEO_PID):
            port_USB = device.device
    try:
        magazyn.NUCLEOUsbAddress  = serial.Serial(port=port_USB, baudrate=230400, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=0, xonxoff=False, rtscts=False, write_timeout=None, dsrdtr=True, inter_byte_timeout=None, exclusive=None) # w razie problemów z komunikacją podmień na 0  
       
        if magazyn.NUCLEO != 1:
                magazyn.NUCLEO = 1
        connection = True
        print("Nucleo - reconnection OK")
    except:
        pass
def ConnectToNucleo(magazyn,nucleo_que):
    connection = False
    device_list = list_ports.comports()
    
    for device in device_list:
        if (device.vid == magazyn.NUCLEO_VID) and (device.pid == magazyn.NUCLEO_PID):
            port_USB = device.device
            print(port_USB)
            #port_USB = '/dev/ttyUSB1'#'/dev/ttyUSB2'
    try:
        magazyn.NUCLEOUsbAddress  = serial.Serial(port=port_USB, baudrate=230400, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=0, xonxoff=False, rtscts=False, write_timeout=None, dsrdtr=True, inter_byte_timeout=None, exclusive=None) # w razie problemów z komunikacją podmień na 0  
        if magazyn.NUCLEO != 1:
                magazyn.NUCLEO = 1
        connection = True
        time.sleep(0.5)
        msg = str('<{}, {}>'.format(5, 1, )) # start wysylania ramek
        magazyn.NUCLEOUsbAddress.write(msg.encode('utf-8'))
        msg = str('<{}, {}>'.format(21, magazyn.polozeniezeroRxId4, )) # zerowanie RX lewy ID4
        magazyn.NUCLEOUsbAddress.write(msg.encode('utf-8'))
        msg = str('<{}, {}>'.format(22, magazyn.polozeniezeroRxId5, )) # zerowanie RX prawy ID5
        magazyn.NUCLEOUsbAddress.write(msg.encode('utf-8'))
        
    except:
        print("No NUCLEO")
        magazyn.NUCLEO = 0
 
     
def send(nucleo_que, magazyn):
    old_time = 0
    while True:
        
        msg = str(nucleo_que.get())
        #print(msg.encode('utf-8'))
        try:
            magazyn.NUCLEOUsbAddress.write(msg.encode('utf-8'))
            #print(msg.encode('utf-8'))
            if magazyn.NUCLEO != 1:
                magazyn.NUCLEO = 1
        except:
            pass #print("bledna ramka") #pass #magazyn.NUCLEO = 0

                            


            

def recv(magazyn,nucleo_que):
    milliseconds = int(round(time.time() * 1000))
    start = milliseconds = int(round(time.time() * 1000))
    old_time = 0
    suma = 0
    pomocnicza = 0
    licznik_scenariuszy = 0
    while True:   # ciągłe oczekiwanie na ramki danych z NUCLEO, interpretacja i ewentualne logowanie do pliku.

        if magazyn.logowanie_NUCLEO == 1 and magazyn.NUCLEO == 1 and pomocnicza == 0 : # tworzenie pliku .txt do logowania danych z NUCLEO
            pomocnicza = 1    
            print('OpenFIle for NUCLEO Data Log')
            now = datetime.now()
            current_time = now.strftime("%H.%M.%S")
            file_name_1 = "{0} plik a_nr:_{1}.txt".format(current_time,licznik_scenariuszy)
            text_file_1 = open(str(file_name_1), 'w')
            text_file_1.write(str("Logowanie danych z Rasp. Format danych: \n"))
            text_file_1.write(str("T200_L:T200_P:curTime:actualDepth:katPletw:ThrustForce\n"))
            
            file_name_2 = "{0} plik b_nr:_{1}.txt".format(current_time,licznik_scenariuszy)
            text_file_2 = open(str(file_name_2), 'w')
            text_file_2.write(str("Logowanie danych z Rasp. Format danych: \n"))
            text_file_2.write(str("kpp:kii:error:de:RASP_ustaw_zanurzenie_dynamiczne\n"))
            licznik_scenariuszy = licznik_scenariuszy + 1
        
            
        elif magazyn.logowanie_NUCLEO == 0 and magazyn.NUCLEO==1 and pomocnicza == 1: # zamknięcie pliku .txt do logowania danych z NUCLEO
            
            text_file_1.close()
            text_file_2.close()
            pomocnicza = 0
            print("koniec logowania NUCLEO") # otwieranie/zamykanie pliku .txt
          
        if magazyn.NUCLEO == 1:  #ODCZYT DANYCH Z NUCLEO
            time.sleep(0.05)
            try:
                if magazyn.NUCLEOUsbAddress.inWaiting():
                    waiting = magazyn.NUCLEOUsbAddress.inWaiting()
                    x = magazyn.NUCLEOUsbAddress.read(waiting).decode('utf-8')
                    #x = magazyn.NUCLEOUsbAddress.readline().decode('utf-8')
                    msg = ""
                    while len(x) > 0:
                        msg = re.search('.+?(?=\n)', x)[0]
                        cut = int(len(str(msg))) + 1
                        x = x[cut:]    

                        try:
                            device = re.search('.+?(?=:)', msg)[0]
                            cut = int(len(str(device))) + 1
                            command_send = msg[cut:]

                            ####
                            try:  
                                if int(device) == 1 or int(device) == 2 or int(device) == 3:
                                    new_time = float(time_cutter(str(datetime.now())))
                                    diff = new_time-old_time
                                    old_time = new_time
                                    msg = str('<{}, {}>'.format(23, magazyn.actual_depth, ))
                                    #print(magazyn.actual_depth)
                                    magazyn.NUCLEOUsbAddress.write(msg.encode('utf-8'))  
                            except Exception as e:
                                pass
                        
                            if magazyn.logowanie_NUCLEO == 1 and pomocnicza == 1 and str(device) == "dane":
                                
                                log = "{0}\n".format(command_send)
                                text_file_2.write(str(log)) 
                            elif magazyn.logowanie_NUCLEO == 1 and pomocnicza == 1 and str(device) != "dane" and device != None: # LOGOWANIE DANYCH
                                log = command_send
                                magazyn.simulation_time = re.search('.+?(?=:)', log)[0] #odcinanie czasu i zapisywanie go do magazynu.
                                if magazyn.tryb == 0:
                                    log = "{0}:{1}:{2}\n".format(str(magazyn.thruster1),str(magazyn.thruster2),command_send)
                                    text_file_1.write(str(log))
                        
                                elif magazyn.tryb == 1:
                                    log = "{0}:{1}\n".format(str(magazyn.krokowy),command_send)
                                    text_file_1.write(str(log))
                            ####
                            print("device: " + str(device) + ",command: " + str(command_send))
                        
                        except Exception as e:
                            device = None
                            #print(e)
                            log = "{0}\n".format(command_send)
                            text_file_1.write(str(log)) 
                            text_file_2.write(str(log)) 
                        
            except Exception as e:
                #magazyn.NUCLEO =0
                pass #print(e)
        if magazyn.NUCLEO == 0:
            pass
            #ReconnectToNucleo(magazyn)
