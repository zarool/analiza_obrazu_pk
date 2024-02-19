import re

def JoyParser (joystick_que,ethernet_que):
###### Get Button from the Joystick and execute proper procedure to code the message
###### Every button have it's  unique scenario what will happen
###### Axis are described as button +20, we have 4 axis so 20-23
###### Hat is described as button +30, we have 1 hat i don't know how to solve this
    # Thruster state - remember state of the thruster ON(1)/OFF(0)
    thruster_state = 0
    m = -1
    ograniczenie = 20
    korektaprawa = 0
    korektalewa = 0
    zbiornikstan = 'stop'
    korteka = 'stop'
    polozenielewyrx = 0
    polozenieprawyex = 0
    kierunek = 'zero'
    predkoscpletw = 0
    camera = 74
    maszt = 0
    while True:

        command = joystick_que.get().replace(" ", "")
        value = re.search('(?<=:)[\w+.-]+', command)[0]
        button = re.search('.+?(?=:)', command)[0].strip()
        #print(button)
        ### Korekcja ciagu lewego pednika!!!!
        if button == "0" and m != 0:
            m = 0
            print('Pletwy ON')
            command = str('DYNAMIXEL:WHEELSTART:1:{}'.format(int(predkoscpletw), ))
            ethernet_que.put(command)
            print('Predkosc ruchu pletw: {}'.format(predkoscpletw))
        ### Pedniki tyl
        elif button == "1" and m != 1:
        # Ustaw pletwy do tylu - kierunek plyniecia tyl
        # Ustaw Lewa na przod
            ethernet_que.put('[DYNAMIXEL:SETPOSITION:4:90]')
            polozenielewyrx = 90
            # Ustaw prawa na przod
            ethernet_que.put('[DYNAMIXEL:SETPOSITION:5:-90]')
            polozenieprawyex = -90
            m = 1
            print('Ustaw pletwy do przodu')
            kierunek = 'tyl'
        ### Korekcja ciagu prawego pednika
        elif button == "2" and m != 2:
            print("Pletwy OFF")
            value = '10'
            command = str('DYNAMIXEL:WHEELSTOP:1:{}'.format(int(value), ))
            ethernet_que.put(command)
            m = 2
        ### Pedniki przod
        elif button == "3" and m != 3:
            # Ustaw pletwy do tylu - kierunek plyniecia przod
            # Ustaw Lewa na tyl
            ethernet_que.put('[DYNAMIXEL:SETPOSITION:4:-90]')
            polozenielewyrx = -90
            # Ustaw prawa na tyl
            ethernet_que.put('[DYNAMIXEL:SETPOSITION:5:90]')
            polozenieprawyex = 90
            kierunek = 'przod'
            m = 3
        ### Korekcja ujemna
        elif button == "4" and m != 4:
           m = 4
           predkoscpletw = predkoscpletw - 15
           print("Predkość pletw {}".format(predkoscpletw))
        ### Korekcja dodatnia
        elif button == "5" and m != 5:
            m = 5
            predkoscpletw = predkoscpletw + 15
            print("Predkość pletw {}".format(predkoscpletw))
        ### Oproznianie zbiornika
        elif button == "6" and m != 6:
            if zbiornikstan != 'out':
                # Pednik lewy start
                right = 1500 + ograniczenie
                ethernet_que.put('1[THRUSTER:2:{}]'.format(right))
                zbiornikstan = 'out'
            elif zbiornikstan == 'out':
                # Lewy Stop
                right = 1500
                ethernet_que.put('1[THRUSTER:2:{}]'.format(right))
                zbiornikstan = 'stop'
            m = 6
        ### Napelnianie zbiornika
        elif button == "7" and m != 7:
        # Zacznij napełniać zbiornik
            m = 7
            if zbiornikstan != 'take':
                # Pednik lewy Start z predkoscia nastawiona
                left = 1500 + ograniczenie
                ethernet_que.put('1[THRUSTER:1:{}]'.format(left))
                zbiornikstan = 'take'
                print('Napelnianie zbiornika balastowego!')
            elif zbiornikstan == 'take':
                # Zatrzymaj pednik lewy
                left = 1500
                ethernet_que.put('1[THRUSTER:1:{}]'.format(left))
                zbiornikstan = 'stop'
                print('Zbiornik balastowy stop!')
        ### Restart Dynamixli
        elif button == "8" and m != 8:
            # Restart procedure for Dynamixel
            ethernet_que.put('[DYNAMIXEL:RESTART:0:0]')
            print('Dynamixel restart do pozycji starowych!')
            polozenielewyrx = 0
            polozenieprawyex = 0
            kierunek = 'stop'
            m = 8
        ### Restart pednikow
        elif button == "9" and m != 9:
            ethernet_que.put('THRUSTER:1:64')
            ethernet_que.put('THRUSTER:2:64')
        # Pędniki Start/Stop
            if thruster_state == 0:
                print('Pedniki Kierunke przod!')
                ograniczenie = abs(ograniczenie)
                thruster_state = 1
            elif thruster_state == 1:
                print('Pedniki Kierunke tyl!')
                ograniczenie = abs(ograniczenie)*-1
                thruster_state = 0
            m = 9
        ### Ogranicznik predkosci zmniejsz
        elif button == "10" and m != 10:
            if ograniczenie < 500:
                ograniczenie = ograniczenie + 2
            print('Ograniczenie zakresu pednikow wynosi: {}'.format(ograniczenie))
            m = 10
        ### Ogranicznik zwieksz
        elif button == "11" and m != 11:
            if ograniczenie > 0:
                ograniczenie = ograniczenie - 2
            m = 11
            print('Ograniczenie zakresu pednikow wynosi: {}'.format(ograniczenie))
        ### Puszczono przycisk
        elif button == "99":
            m = 99
        ######## Galki  ANALOGOWE STEROWANIE!!!!  ############
        ### Sterowanie Dynamixlem
        elif button == "20":
            empty = 0
            #Dynamixel
            # NewValue = (((OldValue - OldMin) * (NewMax - NewMin)) / (OldMax - OldMin)) + NewMin
            # Kontrola predkosci dynamixla - tryb wolny
            #value = (((int(value) - (-100)) * (1023 - (-1023))) / (100 - (-100))) + (-1023)
            #command = str('DYNAMIXEL:SPEED:1:{}'.format(int(value), ))
            #ethernet_que.put(command)
            #print('Predkosc ruchu pletw: {}'.format(value))
        ### Sterowanie pednikami
        elif button == "21":
            #Thrusters
            #print(command)
            cut = 3
            command = command[cut:]
            #### Umiesic w dobrym zakresie
            # NewValue = (((OldValue - OldMin) * (NewMax - NewMin)) / (OldMax - OldMin)) + NewMin
            left = re.search('.+?(?=:)', command)[0].strip()
            left = (((float(left) - (-100)) * ((118-ograniczenie+korektalewa) - (68+ograniczenie+korektalewa)) / (100 - (-100))) + (68+ograniczenie+korektalewa))
            right = re.search('(?<=:)[\w+.-]+', command)[0]
            right = (((float(right) - (-100)) * ((118-ograniczenie+korektaprawa) - (68+ograniczenie+korektaprawa)) / (100 - (-100))) + (68+ograniczenie+korektaprawa))
            #### wysłac komende
            ethernet_que.put('THRUSTER:1:{}'.format(left))
            ethernet_que.put('THRUSTER:2:{}'.format(right))
            #print('Predkosc pednikow - Lewy {}  Prawy {}'.format(left,right))
        ####### Kapelusz ##########
        ### Niewykorzystany
        elif button == "30":
            if value == '1':
                if kierunek == 'przod':
                    # Podnies o 5 stopni
                    polozenielewyrx = polozenielewyrx + 5
                    polozenieprawyex = polozenieprawyex - 5
                elif kierunek == 'tyl':
                    polozenielewyrx = polozenielewyrx - 5
                    polozenieprawyex = polozenieprawyex + 5
                command = str('DYNAMIXEL:SETPOSITION:5:{}'.format(int(polozenieprawyex), ))
                print(command)
                ethernet_que.put(command)
                command = str('DYNAMIXEL:SETPOSITION:4:{}'.format(int(polozenielewyrx), ))
                print(command)
                ethernet_que.put(command)
            elif value == '0':
                # Obniz o 5 stopni
                if kierunek == 'przod':
                    # Podnies o 5 stopni
                    polozenielewyrx = polozenielewyrx - 5
                    polozenieprawyex = polozenieprawyex + 5
                elif kierunek == 'tyl':
                    polozenielewyrx = polozenielewyrx + 5
                    polozenieprawyex = polozenieprawyex - 5
                command = str('DYNAMIXEL:SETPOSITION:5:{}'.format(int(polozenieprawyex), ))
                ethernet_que.put(command)
                print(command)
                command = str('DYNAMIXEL:SETPOSITION:4:{}'.format(int(polozenielewyrx), ))
                ethernet_que.put(command)
                print(command)
        elif button == "31":
            if value == '1':
                # camera = camera + 5
                # if camera > 180:
                #    camera = 0
                # command = str('CAMERA:{}'.format(camera, ))
                # print(command)
                # ethernet_que.put(command)
                ethernet_que.put('THRUSTER:1:58')
                right = '1540'
                ethernet_que.put('THRUSTER:2:70')
            elif value == '0':
                # maszt = maszt + 1
                # if maszt > 10:
                #    maszt = 0
                # command = str('MASZT:{}'.format(maszt, ))
                # print(command)
                # ethernet_que.put(command)
                left = 1550
                ethernet_que.put('THRUSTER:1:70')
                right = '1540'
                ethernet_que.put('THRUSTER:2:58')
        elif button == "32":
            print(value)
            print(button)
        elif button == "33":
            print(value)
            print(button)