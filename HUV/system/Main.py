### PROGRAM GLOWNY DLA KOMUNIKACJI PO ETHERNET ######

############ import ###############
import _thread
import threading
import time
import queue
import socket

##### Create indywidual magazine for each HUV vehicle #####
print(socket.gethostname())
if socket.gethostname() == "HUV1":
    from Storage_HUV1 import Magazyn
    magazyn = Magazyn()
elif socket.gethostname() == "HUV2":
    from Storage_HUV2 import Magazyn
    magazyn = Magazyn()
elif socket.gethostname() == "HUV3":
    from Storage_HUV3 import Magazyn
    magazyn = Magazyn()
elif socket.gethostname() == "HUV4":
    from Storage_HUV4 import Magazyn
    magazyn = Magazyn()
elif socket.gethostname() == "huv1-desktop":
    from Storage_HUV1 import Magazyn
    magazyn = Magazyn()
elif socket.gethostname() == "huv2-desktop":
    from Storage_HUV2 import Magazyn
    magazyn = Magazyn()
elif socket.gethostname() == "huv3-desktop":
    from Storage_HUV3 import Magazyn
    magazyn = Magazyn()
elif socket.gethostname() == "huv4-desktop":
    from Storage_HUV4 import Magazyn
    magazyn = Magazyn()
elif socket.gethostname() == "tt-desktop":
    from Storage_HUV1 import Magazyn
    magazyn = Magazyn()
    
###### Support functions ######
def WAIT(magazyn):
    while (magazyn.status != 'IDLE'):
        time.sleep(0.3)
        
###### Queues for the system ######
ethernet_que_to_PC  = queue.Queue()     #queue HUV -> PC 
ethernet_que_to_HUV = queue.Queue()     #queue PC -> HUV

dynamixel_que     = queue.Queue()       #queue Rasp -> Nucleo -> RS485 -> dynamixel
thruster_que_1    = queue.Queue()       #queue Rasp -> Nucleo -> PWM -> thruster 1
thruster_que_2    = queue.Queue()       #queue Rasp -> Nucleo -> PWM -> thruster 2
krokowy_que       = queue.Queue()       #queue Rasp -> Nucleo -> pulse -> krokowy
balast_que        = queue.Queue()       #queue Rasp -> Nucleo -> PWM -> balast
radio_que         = queue.Queue()       #queue not used
camera_ctrl_que   = queue.Queue()       #queue Rasp -> Nucleo -> PWM -> camera rotation servo
maszt_ctrl_que    = queue.Queue()       #queue Rasp -> 1wire -> RGBW programable strips
scenerio_exe_que  = queue.Queue()       #queue mission.txt -> Rasp 
nucleo_que        = queue.Queue()       #queue Rasp -> Nucleo
rozpoznawanie_que = queue.Queue()       #queue Rasp -> modul of image analysis OpenCV

###### Main threads ######

##### Ethernet loop #####
from Client_Ethernet_class import HUV_PC_communication
Eth = threading.Thread(target=HUV_PC_communication, args=(ethernet_que_to_HUV,ethernet_que_to_PC,magazyn))
Eth.start()

##### NUCLEO loop #####
magazyn.status = 'PROCESS' ### wystaw flage ze procesuje operacje
from USB_NUCLEO import communicationNUCLEO
Nucleo_comm = threading.Thread(target=communicationNUCLEO, args=(nucleo_que, magazyn))
Nucleo_comm.start()
WAIT(magazyn) ### Zaczekaj dopuki nie zainicjalizuje

##### IMU Loop ##### #ok
#magazyn.status = 'PROCESS' ### wystaw flage ze procesuje operacje
#from USB_VN100 import IMUcommunication
#IMU_USB = threading.Thread(target=IMUcommunication, args=(magazyn, ))
#IMU_USB.start()
#WAIT(magazyn) ### Zaczekaj dopuki nie zainicjalizuje

##### GPS Loop #####
from USB_GPS import GPS_communication
GPS_Ctrl = threading.Thread(target=GPS_communication, args=(krokowy_que, magazyn))
GPS_Ctrl.start()

##### Leakage Loop #####
from RPi_GPIO_Leakage import Leakage_loop
Leakage_Ctrl = threading.Thread(target=Leakage_loop, args=(krokowy_que, magazyn))
Leakage_Ctrl.start()

##### Dynamixel Loop ##### #ok
from USB_Dynamixel import RX_24F
Dynamixel = threading.Thread(target=RX_24F, args=(dynamixel_que, magazyn, nucleo_que))  # z magazynu pobiera port USB arduino MEGA
Dynamixel.start()

##### Thrusters Loops ##### #ok
from USB_Thruster import Thruster
Thruster_1 = threading.Thread(target=Thruster, args=(13, thruster_que_1, magazyn, nucleo_que))
Thruster_1.start()
Thruster_2 = threading.Thread(target=Thruster, args=(12, thruster_que_2, magazyn, nucleo_que))
Thruster_2.start()

##### Camera Control Loop ##### #no
from USB_Camera_Servo import CameraControl
Camera_Ctrl = threading.Thread(target=CameraControl, args=(17, camera_ctrl_que, magazyn, nucleo_que))
Camera_Ctrl.start()

##### Run Krokowy Loop ##### #no
from USB_Krokowy import Krokowy
Krokowy_Ctrl = threading.Thread(target=Krokowy, args=(krokowy_que, magazyn, nucleo_que))
Krokowy_Ctrl.start()

##### Run Balast Loop ##### #no
from USB_Balast import Balast
Balast_Ctrl = threading.Thread(target=Balast, args=(balast_que, magazyn, nucleo_que))
Balast_Ctrl.start()

##### I2C BUS Loop #####
from RPi_I2C_bus import I2C_bus_communication
I2C_Ctrl = threading.Thread(target=I2C_bus_communication, args=(krokowy_que, magazyn))
I2C_Ctrl.start()

##### Neopixel Mast Loop ##### PRZERZUCIC NA USB DO ARDUINO NANO
magazyn.status = 'PROCESS' 
from USB_Maszt_RGB import MastNeopixelControl
Maszt_Ctrl = threading.Thread(target=MastNeopixelControl, args=(maszt_ctrl_que, magazyn))
Maszt_Ctrl.start()

##### Ethernet commands parser loop #####
from Commands_Parser_to_HUV import commands_parser_to_HUV
Commands_Parser = _thread.start_new_thread(commands_parser_to_HUV,(ethernet_que_to_HUV, dynamixel_que,thruster_que_1, thruster_que_2, krokowy_que, balast_que, camera_ctrl_que, maszt_ctrl_que, scenerio_exe_que, nucleo_que, rozpoznawanie_que, magazyn))

##### Radio commands parser loop ###### 
#from Commands_Parser_Radio import commands_parser
#Commands_Parser = _thread.start_new_thread(commands_parser,(radio_que, dynamixel_que,thruster_que_1, thruster_que_2, balast_que, camera_ctrl_que, maszt_ctrl_que, scenerio_exe_que, arduino_mega_que))

##### Radio Loop #####
#from Radio_Def_New import Radio
#Radio_1 = threading.Thread(target=Radio, args=(radio_que, ))
#Radio_1.start()

##### Scenerio Executore loop #####
from RPi_Scenerio_Executore import Scenerio
Scenerio_Executore = threading.Thread(target=Scenerio, args=(scenerio_exe_que, ethernet_que_to_HUV,magazyn))
Scenerio_Executore.start()

##### Rozpoznawanie Loop #####
#flag = False
from RPi_Analiza_obrazu import main_program
Wykrywanie = threading.Thread(target=main_program, args=((ethernet_que_to_HUV, rozpoznawanie_que,camera_ctrl_que, lambda: flag, magazyn)))
Wykrywanie.start()

print('Pojazd Gotowy')
while True:
    command = input("COMMAND: ")
    ethernet_que_to_HUV.put(str(command))
    #radio_que.put(str(command))

