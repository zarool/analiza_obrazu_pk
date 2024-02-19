import serial
import time


def Thruster(Number,Thruster_que, magazyn,nucleo_que):
    while True:   ### Petla glowna komunikacji
        value = float(Thruster_que.get())
        try:
            msg = str('<{}, {}>'.format(Number, int(value), ))
            nucleo_que.put(msg)
            #print(msg.encode('utf-8'))
        except:
            pass
          
