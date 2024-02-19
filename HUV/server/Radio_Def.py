import serial
import time
import threading
import re
port = serial.Serial(port='COM15', baudrate=115200, timeout=0.1)

pednik_lewy = 64
pednik_prawy = 64
pletwy_glowny = 64
pletwy_glowny_onoff = 20
pletwa_lewy = 0
pletwa_prawy = 0

def KreatorWiadomosci(Radio_que ):

    global pednik_lewy
    global pednik_prawy
    global pletwy_glowny
    global pletwy_glowny_onoff
    global pletwa_lewy
    global pletwa_prawy

    pednik_lewy = 92
    pednik_prawy = 92
    pletwy_glowny = 64
    pletwy_glowny_onoff = 20
    pletwa_lewy = 64
    pletwa_prawy = 64

    while True:

        command = Radio_que.get()
        device = re.search('.+?(?=:)', command)[0]
        cut = int(len(str(device))) + 1
        command_send = command[cut:]
        if str(device) == "DYNAMIXEL":

            len_ = int(len(command_send))
            func = re.search('.+?(?=:)', command_send)[0]
            func = str(func)
            id = re.search('(?<=\:)(.*?)(?=\:)', command_send)[0]
            command = command_send[::-1]
            value = re.search('.+?(?=:)', command)[0]
            value = value[::-1]
            if func == "WHEELSTART":
                print('Uruchom oscylacyjny')
                value = (((float(value) - (-100)) * ((128) - (0)) / (100 - (-100))) + (0))
                pletwy_glowny = int(value)
                # Ruch obrotowy
                pletwy_glowny_onoff = 50
            elif func == "WHEELSTOP":
                # Ruch obrotowy Stop
                print('Zatrzymaj oscylacyjny')
                pletwy_glowny_onoff = 20
                pletwy_glowny = 64
            elif func == "SPEED":
                print('Ustaw predkosc')
                value = (((float(value) - (-100)) * ((128) - (0)) / (100 - (-100))) + (0))
                pletwy_glowny = value
            elif func == "SETPOSITION":
                if int(id) == 4:
                    # NewValue = (((OldValue - OldMin) * (NewMax - NewMin)) / (OldMax - OldMin)) + NewMin
                    value = (((float(value) - (-150)) * ((128) - (0)) / (150 - (-150))) + (0))
                    pletwa_lewy = int(value)
                    print(value)
                if int(id) == 5:
                    # NewValue = (((OldValue - OldMin) * (NewMax - NewMin)) / (OldMax - OldMin)) + NewMin
                    value = (((float(value) - (-150)) * ((128) - (0)) / (150 - (-150))) + (0))
                    pletwa_prawy = int(value)
                    print(value)


        elif str(device) == "THRUSTER":
            id = re.search('.+?(?=:)', command_send)[0]
            id = str(id)
            command_send = command_send[::-1]
            value = re.search('.+?(?=:)', command_send)[0]
            value = value[::-1]
            if id == '1':
                pednik_lewy = value
            elif id == '2':
                pednik_prawy = value

#def RadioThread(pednik_lewy, pednik_prawy, pletwy_glowny):
def RadioThread():
    global pednik_lewy
    global pednik_prawy
    global pletwy_glowny
    global pletwy_glowny_onoff
    global pletwa_lewy
    global pletwa_prawy
    while True:
        pednik_lewy_ch = chr(int(float(pednik_lewy)))
        pednik_prawy_ch = chr(int(float(pednik_prawy)))
        pletwy_glowny_onoff_ch = chr(int(float(pletwy_glowny_onoff)))
        pletwy_glowny_ch = chr(int(float(pletwy_glowny)))
        pletwa_lewy_ch = chr(int(float(pletwa_lewy)))
        pletwa_prawy_ch = chr(int(float(pletwa_prawy)))

        znaki = [pednik_lewy_ch, pednik_prawy_ch, pletwy_glowny_onoff_ch, pletwy_glowny_ch, pletwa_lewy_ch, pletwa_prawy_ch]
        msg = ''.join(znaki)
        print(msg)
        #msg = Radio_que.get()
        if len(msg) == 6:
            port.write(msg.encode('utf-8'))
        #port.write(msg.encode())
        time.sleep(0.2)

def Radio(Radio_que):

    KreatorWiadomosci_T = threading.Thread(target=KreatorWiadomosci, args=(Radio_que, ))
    KreatorWiadomosci_T.start()
    RadioThread_T = threading.Thread(target=RadioThread, args=())
    RadioThread_T.start()

    KreatorWiadomosci_T.join()
    RadioThread_T.join()