import serial
import time
import re
from serial.tools import list_ports
from datetime import datetime

device_list = list_ports.comports()

NUCLEO_VID = 0x0483
NUCLEO_PID = 0x374b

connection = False

def time_cutter(time_): # funkcja wycinająca z datetime.now() tylko sekundy
        device = re.search('.+?(?=:)', time_)[0]
        cut = int(len(str(device))) + 1
        command_send = time_[cut:]
        device = re.search('.+?(?=:)', command_send)[0]
        cut = int(len(str(device))) + 1
        device = command_send[cut:]
        return device

for device in device_list:
    print(device)
    if (device.vid == NUCLEO_VID) and (device.pid == NUCLEO_PID):
        port_USB = device.device
        print(port_USB)
            #port_USB = '/dev/ttyUSB1'#'/dev/ttyUSB2'
        try:
            NUCLEOUsbAddress = serial.Serial(port=port_USB, baudrate=230400)# parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=0.1, xonxoff=False, rtscts=False, write_timeout=None, dsrdtr=True, inter_byte_timeout=None, exclusive=None) # w razie problemów z komunikacją podmień na 0  
            connection = True
            
        except:
            print("No NUCLEO")

old_time = 0
time.sleep(1)
msg = str('<{}, {}>'.format(5, 1, )) # start wysylania ramek
NUCLEOUsbAddress.write(msg.encode('utf-8'))
print("go")
while connection:
   
    if NUCLEOUsbAddress.inWaiting():

        try: # przyjecie ramki z NUCLEO i dekodowanie.  format:   type:value1:value2:value3
            x = NUCLEOUsbAddress.read(25).decode('utf-8')
            print(x)
            try:
                device = re.search('.+?(?=:)', x)[0]
                cut = int(len(str(device))) + 1
                command_send = x[cut:]
            except:
                device = "None"

            if device == "1" or device == "2" or device == "3":
                msg = str('<{}, {}>'.format(23, 0.2, ))
                NUCLEOUsbAddress.write(msg.encode('utf-8'))
                new_time = float(time_cutter(str(datetime.now())))
                print(new_time-old_time)
                old_time = new_time
            
                      
            
        except:
            print("error !!!!!!!!!!!!!!!!!!!!!")
        