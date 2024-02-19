import serial
import time
import threading
import re
from datetime import datetime
from serial.tools import list_ports

def MastNeopixelControl(maszt_ctrl_que, magazyn):
    ### Sprawdz czy obiekt portu istnieje - jezeli nie podlacz
    if magazyn.NANOUsbAddress == None:
        print("NANO- WYSZUKIWANIE")
        ConnectToNANO(magazyn,maszt_ctrl_que)
    
    magazyn.status = 'IDLE'
    
    t1 = threading.Thread(target=send, args=(maszt_ctrl_que, magazyn)) # wątek ciągłego wysyłania ramek do MEGA
    t1.start()

    t2 = threading.Thread(target=receive, args=(maszt_ctrl_que, magazyn)) # wątek ciągłego wysyłania ramek do MEGA
    t2.start()  
 
def ReconnectToNANO(magazyn,):
    time.sleep(1)
    device_list = list_ports.comports()
    
    for device in device_list:
        if (device.vid == magazyn.NANO_VID) and (device.pid == magazyn.NANO_PID):
            port_USB = device.device
    try:
        magazyn.NANOUsbAddress  = serial.Serial(port=port_USB, baudrate=115200, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=10, xonxoff=False, rtscts=False, write_timeout=None, dsrdtr=True, inter_byte_timeout=None, exclusive=None) # w razie problemów z komunikacją podmień na 0  
       
        connection = True
        print("NANO - reconnection OK")
    except:
        pass


def ConnectToNANO(magazyn,maszt_ctrl_que):
    connection = False
    device_list = list_ports.comports()
    
    for device in device_list:
        if (device.vid == magazyn.NANO_VID) and (device.pid == magazyn.NANO_PID):
            port_USB = device.device
            print(port_USB)
            #port_USB = '/dev/ttyUSB1'#'/dev/ttyUSB2'
    try:
        magazyn.NANOUsbAddress  = serial.Serial(port=port_USB, baudrate=115200, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=10, xonxoff=False, rtscts=False, write_timeout=None, dsrdtr=True, inter_byte_timeout=None, exclusive=None) # w razie problemów z komunikacją podmień na 0  
        connection = True
        print("NANO CONNECTED")
        time.sleep(0.5)

        
    except:
        print("No NANO")
        magazyn.NANO = 0
 
     
def send(maszt_ctrl_que, magazyn):
    if magazyn.NANOUsbAddress:
        while True:   ### Petla glowna komunikacji
            command_string = str(maszt_ctrl_que.get()).strip()
            try: # sprawdz czy zawiera dodatkową komendę
                device = re.search('.+?(?=:)', command_string)[0] # czyli przeszukaj string. od lewej bierz ile mozliwe a od prawej do znaku :
                cut = int(len(str(device))) + 1
                command_send = command_string[cut:]
                
                if str(device) == "RED": # jeżeli dodatkowa komenda ENABLE
                    msg =('<{},{}>'.format(1, int(command_send), ))
                    magazyn.NANOUsbAddress.write(msg.encode('utf-8'))
                    print(msg.encode('utf-8'))
                if str(device) == "GREEN": # jeżeli dodatkowa komenda ENABLE
                    msg = ('<{},{}>'.format(2, command_send, ))
                    magazyn.NANOUsbAddress.write(msg.encode('utf-8'))
                    print(msg.encode('utf-8'))
                if str(device) == "BLUE": # jeżeli dodatkowa komenda ENABLE
                    msg = str('<{},{}>'.format(3, command_send, ))
                    magazyn.NANOUsbAddress.write(msg.encode('utf-8'))
                    print(msg.encode('utf-8'))
                if str(device) == "WHITE": # jeżeli dodatkowa komenda ENABLE
                    msg = str('<{},{}>'.format(4, command_send, ))
                    magazyn.NANOUsbAddress.write(msg.encode('utf-8'))
                    print(msg.encode('utf-8'))
                if str(device) == "BLACK": # jeżeli dodatkowa komenda ENABLE
                    msg = str('<{},{}>'.format(5, command_send, ))
                    magazyn.NANOUsbAddress.write(msg.encode('utf-8'))
                    print(msg.encode('utf-8'))
            except: 
                print("NIE DZIALA")
        
    else:
        pass

     
def receive(maszt_ctrl_que, magazyn):
    if magazyn.NANOUsbAddress:
        old_time = 0
        while True:
            try:
                if magazyn.NANOUsbAddress.inWaiting():
                    msg = magazyn.NANOUsbAddress.readline().decode('utf-8')
                    print(msg)
            except:
                print("bledna ramka") #pass #magazyn.NANO = 0