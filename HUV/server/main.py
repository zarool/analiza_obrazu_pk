############ import ###################
import _thread
import threading
import queue

from Storage import Magazyn
magazyn = Magazyn()


magazyn_clients_table = []
magazyn_clients_table_name = [] # '192.168.0.101', '192.168.0.104', '192.168.0.103', '192.168.0.102'
wybor_HUV = 0   # licznik zmiany lienta
###### Queue for Ethernet communication ######
ethernet_queue_to_HUV = queue.Queue()

### - Queue for joystick - joystick will put items in this queue
joystick_que = queue.Queue()

### - Queue for joystick - joystick will put items in this queue
radio_que = queue.Queue()

###### Run Server Loop #########
#from Server_Ethernet import start
#t1 = threading.Thread(target=start, args=(ethernet_queue_to_HUV,))      # startujemy całą komunikację ethernet
#t1.start()
#


from Server_Ethernet_class import ethernet_server_function
t2 = threading.Thread(target=ethernet_server_function, args=(ethernet_queue_to_HUV,magazyn))      # startujemy całą komunikację ethernet
t2.start()

#t2 = _thread.start_new(ethernet_server_function,(ethernet_queue_to_HUV,))

###### Run Joystick Loop ########
from Pygame_Window import Joystick
Joy = _thread.start_new(Joystick,(joystick_que,ethernet_queue_to_HUV,magazyn))

##### Run Joystick Parser Loop ########## ETHERNET #####
from JoystickCommands_Parser import JoyParser
Parser = _thread.start_new(JoyParser,(joystick_que,ethernet_queue_to_HUV,magazyn ))

##### Run Joystick Parser Loop ########## RADIO ######
#from JoystickCommands_Parser_Radio import JoyParser
#Parser = _thread.start_new(JoyParser,(joystick_que,radio_que, ))

##### Run Radio if needed - turn off Ethernet LooP
#from Radio_Def import Radio
#Radio = _thread.start_new(Radio,(radio_que, ))


while True:
    message = str(input())
    ethernet_queue_to_HUV.put(message)
    # radio_que.put(str) # comment out if radio needed

