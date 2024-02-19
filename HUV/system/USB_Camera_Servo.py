import serial
import time

def CameraControl(Number, camera_ctrl_que, magazyn,nucleo_que):
    

    ### Petla glowna komunikacji   
    while True:
        try:
            value = int(camera_ctrl_que.get())
        except:
            print('Bledna ramka dla  {}'.format(Number))
        msg = str('<{}, {}>'.format(Number, value, ))
        nucleo_que.put(msg)
