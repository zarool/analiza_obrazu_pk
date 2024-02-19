class Magazyn():
    frame = []
    USBPorts = [] # Lista portów USB
    def __init__(self):
        #self.frame = []
        
        
        self.colours = {}  # Lista, list z danymi o kolorach
        self.messages = {} # Wiadomosci do odczytania
        
        self.status = 'IDLE' # zakladam ze ta flaga bedzie synchronizowac start
        
        # Do komunikacji USB
        self.IMUUsbAddress = None
        self.NUCLEOUsbAddress = None # Zapisany adres portu USB arduino UNO
        self.NANOUsbAddress = None 
        self.GPSUsbAddress = None
        
        self.NUCLEO_VID = 0x0483
        self.NUCLEO_PID = 0x374b
        
        self.NANO_VID = 0x1a86
        self.NANO_PID = 0x7523

        self.GPS_VID = 0x10c4
        self.GPS_PID = 0xea60
        
        self.VN100_VID = 0x1a86
        self.VN100_PID =0x7523
        
        # IMU data
        self.HUV_roll = 0
        self.HUV_pitch = 0
        self.HUV_yaw = 0
        self.HUV_roll_v = 0
        self.HUV_pitch_v = 0
        self.HUV_yaw_v = 0
        
        self.thrust_force = 0
        
        #Pozycja neutralna płetw
        self.polozeniezeroRxId4 = 85 
        self.polozeniezeroRxId5 = 75
        
  
        
        # Kontrolery
        self.set_static_depth = -1             # wartość z zakresu -0.4 do 2m uruchamia regulator statycznego (zbiornik balastowy). Wartość -1 to regulator wyłączony
        self.set_dynamic_depth = -1            # wartość z zakresu -0.4 do 2m uruchamia regulator zanurzania dynamicznego (płetwy). Wartość -1 to regulator wyłączony
        self.set_dynamic_pitch = -100          # wartość z zakresu -15  do 15 uruchamia regulator przegłębienia dynamicznego (płetwy). Wartość -100 to regulator wyłączony
        self.set_rozpoznawanie_bearing = 0     # nie wykorzystane jeszcze!
        self.set_rozpoznawanie_distance = 1.0  # wartosc z zakresu  0.5 do 10 (regulacja uruchamiana przez moduł Kontroler)
        self.set_rozpoznawanie_speed = 1       # wartość z zakresu  0   do 5  (wykorzystywana tylko przez moduł  Kontroler)
        
        self.rozpoznawanie_speed_Kp = 100
        self.rozpoznawanie_speed_Ki = 0
        self.rozpoznawanie_speed_Kd = 0
        # Ethernet connection
        self.connected = False
        self.ADDR = None
        self.client = None
        
        # Ethernet live package
        self.receive_flag = False
        self.receive_time = 0
        
        # Dynamixel - chyba nie potrzebne.
        self.RX_oscylatory_movement_mode = 0#flaga uruchamiająca tryb oscylacji RX.
        self.RX_frequency = 0
        self.RX_amplitude = 0
        
        # Scenerio executore
        self.scenerio_mode = 0
        self.simulation_time = 0
        self.simulation_time2 = 0
        
        # Logowanie pomiarów z MEGA do pliku .txt
        self.logowanie_NUCLEO = 0 # logowanie daych z NUCLEO. 1 - działa, 0 - nie działa
        self.thruster1_megalog = 0 # pomocnicza do synchronizacji czasu logowania danych z mega i rasp
        self.thruster2_megalog = 0 # pomocnicza do synchronizacji czasu logowania danych z mega i rasp
        
        # Pakiet informacji do Servera
        self.NUCLEO = -1
        self.IMU = -1
        self.GPS = -1
        self.Bar02 = -1
        self.Leakage = -1
        self.tryb = 0 # false = śrubowy, true = biomimetyczny
        self.thruster_enable = 0
        self.thruster1=1500
        self.thruster2=1500
        self.actual_depth = 0
        self.fin_angle = 0
        self.mast=0
        
        self.krokowy=1000

        
        
    ###### Zapisywanie klatki z kamery i odczyt #####
    def getframe(self):
        return Magazyn.frame
    def setframe(self, frame_new):
        Magazyn.frame = frame_new
    ###### Zapisywanie portów USB i odczyt #####
    def getUSBPorts(self):
        return Magazyn.USBPorts
    def setUSBPorts(self, Ports):
        Magazyn.USBPorts = Ports
