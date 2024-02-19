import time
import RPi.GPIO as GPIO


connected = 0
try:
    GPIO.setmode(GPIO.BOARD) # tryb nazywania piów. to ustawienie teraz daje nam 1,2,3,4, itd. czyli czytamiy na łytce jak nazwany jest pin i tak go wprowadzamy do programu.p
    GPIO.setup(7,GPIO.IN)
    connected = 1
    print("Leakage detection - OK")
    magazyn.Leakage = 1
except:
    magazyn.Leakage = -1
    print("GPIO in use, cannot proceed LEAKAGE DETECTION - restart JETSON NANO")


 while connected:
    time.sleep(1)
    if(GPIO.input(7) == 1):
            print("PRZECIEK!")
            time.sleep(0.5)