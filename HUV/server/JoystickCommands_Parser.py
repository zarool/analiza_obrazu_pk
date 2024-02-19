import re
import time
import decimal


def JoyParser(joystick_que, ethernet_que,magazyn):
    ###### Get Button from the Joystick and execute proper procedure to code the message
    ###### Every button have it's  unique scenario what will happen
    ###### Axis are described as button +20, we have 4 axis so 20-23
    ###### Hat is described as button +30, we have 1 hat i don't know how to solve this
    # Thruster state - remember state of the thruster ON(1)/OFF(0)
    thruster_state = 0
    m = -1

    korektaprawa = 0
    korektalewa = 0
    zbiornikstan = 'stop'
    korteka = 'stop'
    polozenieRxId5 = 0
    polozenieRxId4 = 0

    kierunek = 'zero'
    predkoscpletw = 0
    camera = 74
    maszt = 0
    while True:

        command = joystick_que.get().replace(" ", "")
        value = re.search('(?<=:)[\w+.-]+', command)[0]
        button = re.search('.+?(?=:)', command)[0].strip()
        # print(button)


        ### Korekcja ciagu lewego pednika!!!!
        if button == "0" and m != 0:
            m = 0

        elif button == "1" and m != 1:
            m = 1

        elif button == "2" and m != 2:
            m = 2


        elif button == "3" and m != 3:  ### PLETWY W PRZOD - ZEROWANIE ###
            print("pletwy w przod - zerowanie")
            ethernet_que.put('DYNAMIXEL:SETPOSITIONZERO:4:0')
            polozenielewyrx = -90
            ethernet_que.put('DYNAMIXEL:SETPOSITIONZERO:5:0')
            polozenieprawyex = 90
            kierunek = 'przod'
            m = 3

        ###
        elif button == "4" and m != 4:
            m = 4
        ###
        elif button == "5" and m != 5:
            m = 5
        ###
        elif button == "6" and m != 6:
            m = 6

        ###
        elif button == "7" and m != 7:
            m = 7

        ### tryb pracy
        elif button == "8" and m != 8:
            ethernet_que.put('TRYB:')
            m = 8

        ### funkcja zmiany pojazdów "ZMIEN"
        elif button == "9" and m != 9:
            ethernet_que.put('ZMIEN')
            m = 9

        ### Ogranicznik predkosci zmniejsz
        elif button == "10" and m != 10:
            if magazyn.ograniczenie < 25:
                magazyn.ograniczenie = magazyn.ograniczenie + 5
            print('Ograniczenie zakresu pednikow wynosi: {}'.format(magazyn.ograniczenie))
            m = 10

        ### Ogranicznik prędkości zwieksz
        elif button == "11" and m != 11:
            if magazyn.ograniczenie > 0:
                magazyn.ograniczenie = magazyn.ograniczenie - 5
            m = 11
            print('Ograniczenie zakresu pednikow wynosi: {}'.format(magazyn.ograniczenie))

        ### Puszczono przycisk
        elif button == "99":
            m = 99

        ### Sterowanie Dynamixlem
        elif button == "20":

            cut = 3
            command = command[cut:]
            left2 = re.search('.+?(?=:)', command)[0].strip()
            left2 = int((float(left2) / 2))
            right2 = re.search('(?<=:)[\w+.-]+', command)[0]
            right2 = int((float(right2) / 2))
            right3 = 'DYNAMIXEL:SETPOSITIONJOY:4:{}'.format(-right2)
            left3 = 'DYNAMIXEL:SETPOSITIONJOY:5:{}'.format(-left2)
            ethernet_que.put('{:<50}'.format(left3))
            ethernet_que.put('{:<50}'.format(right3))

        ### Sterowanie pednikami
        elif button == "21":  # Axis 3
            # Thrusters
            cut = 3
            command = command[cut:]
            left = re.search('.+?(?=:)', command)[0].strip()
            left = int(1500 - (25 - magazyn.ograniczenie) * float(left) / 5)

            right = re.search('(?<=:)[\w+.-]+', command)[0]
            right = int(1500 - (25 - magazyn.ograniczenie) * float(right) / 5)

            #### wysłac komende
            left1 = 'THRUSTER:1:{}'.format(left)
            right1 = 'THRUSTER:2:{}'.format(right)
            ethernet_que.put('{:<40}'.format(left1))
            ethernet_que.put('{:<40}'.format(right1))

        elif button == "19":  # Axis 3
            pass
        elif button == "22":  # krokowy
            cut = 3
            command = command[cut:]
            left = re.search('.+?(?=:)', command)[0].strip()
            left1 = 'KROKOWY:{}'.format(left)
            ethernet_que.put('{:<40}'.format(left1))
        ######### Kapelusz ##########
        elif button == "30":  # HAT - góra dół - sterowanie połozeniem płetw
            if value == '1':  # value wynika z joistick_def. Jak walue 1 to podnieś, jak 0 to opuśc płetwy.
                if kierunek == 'przod':
                    # Podnies o 5 stopni
                    polozenieRxId5 = 5
                    polozenieRxId4 = -5
                elif kierunek == 'tyl':
                    polozenieRxId5 = -5
                    polozenieRxId4 = 5
                command = str('DYNAMIXEL:SETPOSITIONHAT:5:{}'.format(polozenieRxId5, ))
                print(command)
                ethernet_que.put(command)
                command = str('DYNAMIXEL:SETPOSITIONHAT:4:{}'.format(polozenieRxId4, ))
                print(command)
                ethernet_que.put(command)
            elif value == '0':
                if kierunek == 'przod':
                    # Podnies o 5 stopn
                    polozenieRxId5 = -5
                    polozenieRxId4 = 5
                elif kierunek == 'tyl':
                    polozenieRxId5 = 5
                    polozenieRxId4 = -5

                command = str('DYNAMIXEL:SETPOSITIONHAT:5:{}'.format(polozenieRxId5, ))
                print(command)
                ethernet_que.put(command)
                command = str('DYNAMIXEL:SETPOSITIONHAT:4:{}'.format(polozenieRxId4, ))
                print(command)
                ethernet_que.put(command)

        elif button == "31":
            if value == '1':

                print(button)
                print(value)

            elif value == '0':

                print(button)
                print(value)

        elif button == "32":
            print(value)
            print(button)
        elif button == "33":
            print(value)
            print(button)
