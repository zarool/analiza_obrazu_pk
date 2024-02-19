import re

def commands_parser_to_HUV(ethernet_que_to_HUV, dynamixel_que, thruster_que_1, thruster_que_2,krokowy_que, balast_que, camera_que, maszt_que, scenerio_que, nucleo_que, rozpoznawianie_que, magazyn):
    ##### Take item from Joystick Queue pars and put into Ethernet Queue ###########
    while True:
        try:
            command_string = str(ethernet_que_to_HUV.get())
            device = re.search('.+?(?=:)', command_string)[0] # czyli przeszukaj string. od lewej bierz ile mozliwe a od prawej do znaku :
            cut = int(len(str(device))) + 1
            command_send = command_string[cut:]
        except:
            print('Bledna Komenda - parser')
       

        if str(device) == "DYNAMIXEL":
            dynamixel_que.put(command_send)
            
        elif str(device) == "THRUSTER":
            id = re.search('.+?(?=:)', command_send)[0]
            id = str(id)
            command_send = command_send[::-1]
            value = re.search('.+?(?=:)', command_send)[0]
            value = value[::-1]
            if id == '1':
                magazyn.thruster1=float(value)
                thruster_que_1.put(value.encode('utf-8'))
            elif id == '2':
                magazyn.thruster2=float(value)
                thruster_que_2.put(value.encode('utf-8'))
                
        elif str(device) == "KROKOWY":
            krokowy_que.put(command_send)
           
        elif str(device) == "BALAST":
            balast_que.put(command_send)
            
        elif str(device) == "BREAK": # no
            break
        
        elif str(device) == "CAMERA": #no 
            camera_que.put(command_send.replace(" ", ""))
            
        elif str(device) == "MASZT": #no
            maszt_que.put(command_send)
        
        elif str(device) == "NUCLEORESET":
            msg = str('<{}, {}>'.format(26,int(command_send), )) # start pomiaru zanurzenia
            nucleo_que.put(msg)
        elif str(device) == "SCENERIO": 
            scenerio_que.put(command_send)
            
        elif str(device) == "BATERYMODULE":

            msg = str('<{}, {}>'.format(18,int(command_send), )) # start pomiaru zanurzenia
            nucleo_que.put(msg)
        elif str(device) == "BATERYBALAST": 
            msg = str('<{}, {}>'.format(19,int(command_send), )) # start pomiaru zanurzenia
            nucleo_que.put(msg)
        elif str(device) == "NUCLEOON":
            msg = str('<{}, {}>'.format(5,int(command_send), )) # start pomiaru zanurzenia
            nucleo_que.put(msg)          
        elif str(device) == "NUCLEOLOG":
            magazyn.logowanie_NUCLEO = int(command_send)
            
        elif str(device) == 'ROZPOZNAWANIE':
            rozpoznawianie_que.put(command_send)
            
        elif str(device) == "TRYB":
            if magazyn.tryb == 0:
                magazyn.tryb = 1
                msg = str('<{}, {}>'.format(15, 1, ))
                nucleo_que.put(msg)
                print(msg)
            elif magazyn.tryb == 1:
                magazyn.tryb = 0
                msg = str('<{}, {}>'.format(15, 1, ))
                nucleo_que.put(msg)
                print(msg)
            print("zmiana trybu napedu" + str(magazyn.tryb))
        elif str(device) == "THRUSTERENABLE":
            if magazyn.thruster_enable == 0:
                magazyn.thruster_enable = 1
            elif magazyn.thruster_enable == 1:
                magazyn.thruster_enable = 0
            print("zmiana thruster enable" + str(magazyn.thruster_enable))
            
        else:
            print('Bledna komenda2: ' + str(device))