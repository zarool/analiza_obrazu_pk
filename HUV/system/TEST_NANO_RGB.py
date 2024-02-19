import serial
import time
import threading
import re
from datetime import datetime
from serial.tools import list_ports



def ConnectToNANO():

    NANOUsbAddress = None 

    NANO_VID = 0x1a86
    NANO_PID = 0x7523

    connection = False
    device_list = list_ports.comports()
    
    for device in device_list:
        if (device.vid == NANO_VID) and (device.pid == NANO_PID):
            port_USB = device.device
            print(port_USB)
            #port_USB = '/dev/ttyUSB1'#'/dev/ttyUSB2'
    try:
        NANOUsbAddress  = serial.Serial(port=port_USB, baudrate=115200, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=0.01, xonxoff=False, rtscts=False, write_timeout=None, dsrdtr=True, inter_byte_timeout=None, exclusive=None) # w razie problemów z komunikacją podmień na 0  
        connection = True
        print("NANO CONNECTED")
        time.sleep(0.5) 

    except:
        print("No")

        
    
    msg =str('<{},{}>'.format(1, 100, ))
    NANOUsbAddress.write(msg.encode('utf-8'))
    print(msg.encode('utf-8'))
    time.sleep(1) 
    msg =str('<{},{}>'.format(2, 100, ))
    NANOUsbAddress.write(msg.encode('utf-8'))
    print(msg.encode('utf-8'))

    #if NANOUsbAddress.inWaiting():
        
    print(NANOUsbAddress.readline().decode('utf-8'))

ConnectToNANO()


