import serial
import time
import re
from serial.tools import list_ports

def IMUcommunication(magazyn):
    print("IMU - WYSZUKIWANIE")

    device_list = list_ports.comports()

    for device in device_list:
        if (device.vid == magazyn.VN100_VID) and (device.pid == magazyn.VN100_PID):
            port_USB = device.device
            print(port_USB)
    try:
        port = serial.Serial(port=port_USB, baudrate=115200, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=0.1, xonxoff=False, rtscts=False, write_timeout=None, dsrdtr=True, inter_byte_timeout=None, exclusive=None) # w razie problemów z komunikacją podmień na 0  
        magazyn.IMUUsbAddress = port
        if magazyn.IMU != 1:
            magazyn.IMU = 1
        magazyn.status = 'IDLE'
    except:
        print("No IMU")
        magazyn.IMU = 0
        magazyn.status = 'IDLE'
    

    
    while True: # ODCZYT RAMKI DANYCH Z IMU I ZAPISANIE
        try:
            if magazyn.IMUUsbAddress.inWaiting():
                x = magazyn.IMUUsbAddress.readline().decode('utf-8')
                if magazyn.IMU != 1:
                    magazyn.IMU = 1
                #print(x)
                device = re.search('.+?(?=,)', x)[0]   
                cut = int(len(str(device))) + 1
                command_send = x[cut:] 
                #print(device) # tytul
                device = re.search('.+?(?=,)', command_send)[0]
                cut = int(len(str(device))) + 1
                command_send= command_send[cut:]
                magazyn.HUV_roll = device                    # ZAPISYWANIE roll
                #print(device) # roll
                device = re.search('.+?(?=,)', command_send)[0]
                cut = int(len(str(device))) + 1
                command_send= command_send[cut:]
                magazyn.HUV_pitch = device                    # ZAPISYWANIE pitch
                #print(device) # pitch
                device = re.search('.+?(?=,)', command_send)[0]
                cut = int(len(str(device))) + 1
                command_send= command_send[cut:]
                magazyn.HUV_yaw = device                      # ZAPISYWANIE yaw
                #print(device) # yaw
                #print(x)
        except:
            #print("bledna ramka IMU")
            pass