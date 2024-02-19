import socket
import os
import threading
from time import sleep
from datetime import datetime

import re
# utwórz dużą funkcję komunikacja i utwórz obiekt. w funkcji komunikacja twórz nowy obiekt i temu obiektowi wywołaj wątki.
class Klient:
    def __init__(self,connection,magazyn,eth_que_to_HUV,eth_que_to_PC):
        self.eth_que = eth_que_to_HUV
        self.client = connection
        self.receive_flag = False
        self.recv_time = 0
        self.new_time = 0
        self.difference = 0
        self.run = True
    def vehicle_stop(self): # funkcja zatrzymująca pędniki i silnik krokowy.
        self.eth_que.put("THRUSTER:1:1500")
        print("THRUSTER:1:1500")
        self.eth_que.put("THRUSTER:2:1500")
        print("THRUSTER:2:1500")
        self.eth_que.put("KROKOWY:0")
        print("KROKOWY:0")
        
    def parameter_send(self,eth_que_to_PC,magazyn):
        while True:
            if magazyn.connected:
                sleep(0.25)
                msg = '{:<50}'.format(str(magazyn.NUCLEO) + ":" + str(magazyn.IMU) + ":" + str(magazyn.GPS)+ ":" + str(magazyn.Bar02)+ ":" + str(magazyn.Leakage) + ":"  + str(magazyn.tryb)+ ":"+ str(magazyn.thruster_enable)  +":" + str(magazyn.thruster1) + ":" + str(magazyn.thruster2)+":" +str(magazyn.mast) + ":" +str(magazyn.actual_depth) +":" + str(magazyn.fin_angle) + ":")
                eth_que_to_PC.put(msg)
                #print(msg)
                
            
    def send_function(self, eth_que_to_PC, magazyn):
        while True:
            if magazyn.connected:
                try:
                    message = eth_que_to_PC.get()
                    msg = '{:<50}'.format(message)
                    self.client.send(msg.encode())
                except:
                    pass
        
    def recv_function(self, eth_que_to_HUV,eth_que_to_PC,magazyn):
       
        while magazyn.connected:
            try:
                command_string = str(self.client.recv(50).decode())# odbieraj tylko 50 bajtow. To jest max ilosc bajtow na ramke danych ethernet
                #print(command_string)
                if not magazyn.connected:
                    magazyn.connected = True
                    print("reconnection succesfull 2")
                device = re.search('.+?(?=:)', command_string)[0]

                if str(device) == "HUV":
                    magazyn.receive_flag = True
                    magazyn.connected = True
                    
                    try:
                        message ="HUV:1"
                        eth_que_to_PC.put(message)
                    except socket.error:
                        pass
                elif str(device) == "DYNAMIXEL":
                    magazyn.scenerio_mode = 0
                    eth_que_to_HUV.put(command_string)
                    print(command_string)
                else:
                    eth_que_to_HUV.put(command_string)
                    print(command_string)
            except:
                magazyn.connected = False
                print("blad odbioru")
                self.vehicle_stop()
                self.client.close()
                self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                while not magazyn.connected:
                    try: 
                        self.client.connect( magazyn.ADDR )   
                        print( "re-connection successful" )
                        magazyn.connected = True
                    except:
                         sleep(3)
                

                
    def t_watchdog(self,eth_que_to_HUV,magazyn):  # Oblicza czas od ostatniej przybyłej ramki. jeżeli wiekszy niż 0.3s to usuwa klienta
        self.recv_time = 0
        while True:
            sleep(0.04)
            self.new_time = float(time_cutter(str(datetime.now())))
            if magazyn.receive_flag:                 # jeżeli true (czyli przyszła ramka danych) to recv_time=aktualny czas
                
                self.recv_time = float(time_cutter(str(datetime.now())))
                magazyn.receive_flag = False

            self.difference = self.new_time - self.recv_time  # obliczenie czasu, który upłynął od ostatniej ramki danych
            if self.difference > 1 and self.recv_time != 0 and magazyn.connected == True: # jeżeli różnica >0.3 i przyszła już jakas ramka (recv_time !=)
                magazyn.connected = False
                print( "connection lost... reconnecting" )
                self.vehicle_stop()
                self.client.close()
                self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                while not magazyn.connected:
                    try: 
                        self.client.connect( magazyn.ADDR )   
                        print( "re-connection successful2" )
                        magazyn.connected = True
                    except:
                         sleep(3)  
            
def time_cutter(time_): # funkcja wycinająca z datetime.now() tylko sekundy
        device = re.search('.+?(?=:)', time_)[0]
        cut = int(len(str(device))) + 1
        command_send = time_[cut:]
        device = re.search('.+?(?=:)', command_send)[0]
        cut = int(len(str(device))) + 1
        device = command_send[cut:]
        return device

  

def HUV_PC_communication(eth_que_to_HUV,eth_que_to_PC,magazyn):
    # tutaj duża funkcja która tworzy nowy obiekt klient i wywołuje jego wewnętrzne funkcje odpowiedzialne za połączenie z
    # komputerem i sprawdzanie przychodzenia ramek.
    
    SERVER =  '192.168.124.170'#'192.168.0.105'#'192.168.43.13'#'192.168.1.1'
    PORT = 12350
    ADDR = (SERVER, PORT)
    magazyn.ADDR = (SERVER, PORT)
    print(magazyn.receive_flag)
    print("connecting to server....")
    name = " "
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 
    
    while not magazyn.connected:  # attempt to first connection, otherwise sleep for 1 seconds
    
        if magazyn.connected == False:
            try:  
                client.connect( magazyn.ADDR )  
                magazyn.connected = True  
                print( "connection successful" )
                print(" ")
                klient_polaczenie = Klient(client,magazyn,eth_que_to_HUV,eth_que_to_PC)
            except socket.error:  
                sleep(1)

            t1 = threading.Thread(target=klient_polaczenie.recv_function,args=(eth_que_to_HUV,eth_que_to_PC,magazyn))
            t1.start()
            t2 = threading.Thread(target=klient_polaczenie.t_watchdog,args=(eth_que_to_HUV,magazyn))
            t2.start()
            t4 = threading.Thread(target=klient_polaczenie.parameter_send,args=(eth_que_to_PC,magazyn))
            t4.start()
            t3 = threading.Thread(target=klient_polaczenie.send_function,args=(eth_que_to_PC,magazyn))
            t3.start()