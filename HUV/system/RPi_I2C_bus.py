import RPi_I2C_ms5837
import time

def I2C_bus_communication(nie_potrzebne,magazyn):
    sensor = RPi_I2C_ms5837.MS5837_02BA() # Default I2C bus is 1 (Raspberry Pi 3)
    print("Bar02 - WYSZUKIWANIE")
    # We must initialize the sensor before reading it
    try:
        sensor.init()
        print("Bar02 - OK\n")
        magazyn.Bar02 = 1
    except:
        magazyn.Bar02 = 0
        

    # Print readings
    while True:
        try:
            sensor.read()
            magazyn.actual_depth = -round(sensor.depth(),2)

               
        except:
            magazyn.Bar02 = 0
            print("No Bar02")
            while magazyn.Bar02 == 0: 
                try:
                
                    sensor.init()
                    magazyn.Bar02=1
                    print("Bar02 - OK\n")
                    sleep(1)
                except:
                    pass
