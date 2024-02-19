import re
import time
from datetime import datetime


def time_cutter(time_): # funkcja wycinająca z datetime.now() tylko sekundy
        device = re.search('.+?(?=:)', time_)[0]
        cut = int(len(str(device))) + 1
        command_send = time_[cut:]
        device = re.search('.+?(?=:)', command_send)[0]
        cut = int(len(str(device))) + 1
        device = command_send[cut:]
        return device

def Scenerio(Scenerio_que, Ethernet_que,magazyn ):
    print("Started Scenerio Executore")
    while True:
        infile = ""
        sce_num = Scenerio_que.get()
      
        
        magazyn.scenerio_mode=1
        magazyn.simulation_time=0  
        infile = "{0}".format(sce_num.rstrip())#.rstrip()
        try:
            with open(infile) as fin:
                for line in fin:
                    if magazyn.scenerio_mode > 0:
                
                    #print(str(line))
                        command = re.search('.+?(?=:)', line)[0]
                        if command == 'TIME':
                            cut = int(len(str(command))) + 1
                            command_send = line[cut:]
                            #print(command_send)
                            time_start = 0
                            magazyn.simulation_time2 = 0
                            time_start = time.time()
                        
                        
                            while (magazyn.simulation_time2  <= float(command_send)):
                                time.sleep(0.1)
                            
                                magazyn.simulation_time2 = time.time() - time_start
                            #print(magazyn.simulation_time2)
                                if magazyn.scenerio_mode == 0:
                                    break
                        
                            #print(magazyn.simulation_time)
                            #print(magazyn.simulation_time)
                        elif command == 'KP': # BEZPOŚREDNIO WYSYŁA DO MEGA. NIE PRZECHODZI PRZEZ PARSER.
                            cut = int(len(str(command))) + 1
                            command_send = line[cut:]
                            msg = str('<{},{}>'.format(12, float(command_send), ))
                            magazyn.NUCLEOUsbAddress.write(msg.encode('utf-8'))
                        #print(msg)

                        elif command == 'KI': # BEZPOŚREDNIO WYSYŁA DO MEGA. NIE PRZECHODZI PRZEZ PARSER.
                            put = int(len(str(command))) + 1
                            command_send = line[cut:]
                            msg = str('<{},{}>'.format(13, float(command_send), ))
                            magazyn.NUCLEOUsbAddress.write(msg.encode('utf-8'))
                    
                        elif command == 'KD': # BEZPOŚREDNIO WYSYŁA DO MEGA. NIE PRZECHODZI PRZEZ PARSER.
                            put = int(len(str(command))) + 1
                            command_send = line[cut:]
                            msg = str('<{},{}>'.format(14, float(command_send), ))
                            magazyn.NUCLEOUsbAddress.write(msg.encode('utf-8'))    
                        
                            #print(magazyn.simulation_time)
                        else:
                        
                            Ethernet_que.put(line)
        #Ethernet_que.put("MEGALOG:0")
            magazyn.scenerio_mode=1
            print("End scenerio executore")
        except:
            print("nie ma takiego scenariusza w katalogu")