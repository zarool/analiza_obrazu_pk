import socket
import threading
import time
import re
from datetime import datetime

# UWAGA! DOPISZ KOD, który w ClientEth będzie usuwał i dodawał siebie w liście dostępnych klientów. tego jeszcze nie ma.....

'''

Biblioteka obsługująca server i komunikację z wszystkimi pojazdami (clientami), które zgłoszą się do servera.

Posiada 3 główne elementy: ClientEth, ethernet_server_function i send_message_to_client.

Class ClientEth:
To klasa odpowiedzialna za realizację komunikacji z pojazdem, który zgłasza się do servera. Każdy nowy pojazd dostaje 
swój obiekt klasy ClientEth. Klasa ta posiada metody do wysyłania danych do swojego pojazdu, oraz metody do sprawdzania 
łącza. Client przyjmowany jest przez server raz, natomiast metody: timer, check_send i check_receive sprawdzają łączność. 
Co 0.04s każdy obiekt ClientEth wysyła do swojego pojazdu ramkę "życia" HUV:1 i mierzy czas odpowiedzi przez pojazd. 
Pojazd gdy tylko otrzyma ramkę życia odpowiada od razu taką samą ramką życia. Jeżeli czas przyjścia odpowiedzi przekroczy 0.3s 
to znaczy, że pojazd jest pod wodą lub za daleko i nie odebrał ramki życia. Wtedy obiekt ClientEth co chwilę próbuje 
znów wysłać ramkę życia, gdyby pojazd wrócił do zasiegu ale jednocześnie usuwa swój pojazd z listy dostępnych pojazdów,
do momentu gdy znów odzyska z nim komunikację. Wtedy znów go do tej listy dodaje.

Function ethernet_server_function:
Jest to główna funkcja biblioteki tworząca server i oczekująca w pętli nieskończonej na pojawienie się nowych 
pojazdów-clientów. Jeżeli taki nowy pojazd zgłosi się do servera, to funkcja ta tworzy mu nowy obiekt klasy ClientEth 
i odpala mu metody check_send, check_receive i timer.

Function send_message_to_client:
To funkcja wywoływana z funkcji ethernet_server_function. Jest to funkcja działająca w pętli nieskończonej, która 
przyjmuje ramki danych z eth_que i  wysyła je do wybranego pojazdu z listy dostępnych pojazdów. Komendą "ZMIEN" 
zmieniamy pojazd z którym chcemy się komunikować na następny z listy dostępnych pojazdów. Lista ta jest aktualizowana 
automatycznie przez obiekty ClientEth, także w każdej chwili lista ma pojazdy, z którymi możemy się łączyć. Jeżeli 
jakiś pojazd zniknął z zasięgu, to automatycznie jest usuwany z tej listy natomiast jeżeli ponownie się pojawił to 
zostaje automatycznie na tą listę dodany. Dzięki temu, od strony użytkownika, interesuje nas tylko ta lista. 

UWAGA! każda ramka, która jest wysyłana do pojazdu jest uzupełniana spacjami, jeżeli posiada mniej niż 50 znaków.
Oznacza to ze każda ramka niezaleznie od tego co się w niej znajduje ma 50 znaków i to jest przyjęty standard. 

UWAGA! powyżej zdefiniowane czasy mogą zostać zmienione na inne. 0.3s i 0.04s zostały przyjęte na oko

'''


def time_cutter(time_):  # funkcja pomocnicza, wycinająca z datetime.now() tylko sekundy
    device = re.search('.+?(?=:)', time_)[0]
    cut = int(len(str(device))) + 1
    command_send = time_[cut:]
    device = re.search('.+?(?=:)', command_send)[0]
    cut = int(len(str(device))) + 1
    device = command_send[cut:]
    return device


class ClientEth:  # klasa klient, każdy HUV po podłączeniu do servera dostaje swój obiekt który obsługuje komunikację

    def __init__(self, connection, magazyn, name):              # ta metoda jest wywoływana ilekroć tworzy się obiekt tej klasy.
        self.HUV_name = name
        self.klient_name = None                     # zapisanie nazwy obiektu, tak aby obiekt mógł sam się usunąć z listy dostępnych klientów

        # ----- zmienne do komunikacji (ethernet live-bit) ------
        # wykorzystywane przez funkcje: timer(), check_send(), check_receive()
        self.conn = connection                      # socket tego nowo utworzonego obiektu-clienta
        self.receive_flag = False                   # flaga otrzymania nowej wiadomości
        self.reconecting = False                    # flaga próby ponownego połączenia (po utracie z zasięgu)
        self.run = True                             # flaga działania metod obiektu (w przypadku zamknięcia komunikacji ze strony klienta)
        self.stop = False                           # flaga do symulacji utraty łączności (nie pozwala wysłać ramki życia do pojazdu)
        self.new_time = 0                           # aktualny czas ( do odmierzania czasu przyjścia ramek życia)
        self.recv_time = 0                          # czas przyjścia ( do odmierzania czasu przyjścia ramek życia)
        self.difference = 0                         # różnica new-recv ( do odmierzania czasu przyjścia ramek życia)
        # -------------------------------------------------------

        # ----- zmienne przechowujące aktualne parametry pojazdu --------
        # wykorzystywane przez funkcje: HUV_package_decode()
        self.message = ''
        self.parameter_magazyn = [-1,-1,-1,-1,0,0,0,0,0,0,0,0]  # tablica przechowująca zmienne
        self.number_of_parameters =12
        # parameters:
        # 1.  NUCLEO            - [flag]
        # 2.  IMU               - [flag]
        # 3.  GPS               - [flag]
        # 4.  Bar02             - [flag]
        # 5.  Leakage           - [flag]
        # 6.  tryb              - [flag]
        # 7.  thruster enable   - [flag]
        # 8.  Thruster_1        - [%]
        # 9.  Thruster_2        - [%]
        # 10.  mast             - [int]
        # 11.  actual depth     -[m]
        # 12.  RX24f_ID5        - [deg]
        # ---------------------------------------------------------------

    def timer(self, name, magazyn):  # Oblicza czas od ostatniej przybyłej ramki. jeżeli wiekszy niż 0.3s to ustawia flagę reconecting na True
        time.sleep(1)
        while self.run:     # pętla nieskończona, dopuki run=True
            time.sleep(0.1)
            self.new_time = float(time_cutter(str(datetime.now())))    # mierzy new_time ilekroć powtarza while
            if self.receive_flag:                 # jeżeli przyszła odpowiedz od pojazdu (flaga receive jest True), to zapisz czas receive
                self.recv_time = float(time_cutter(str(datetime.now())))
                self.receive_flag = False
            self.difference = self.new_time - self.recv_time  # obliczenie czasu, który upłynął od ostatniej odpowiedzi pojazdu
            if self.difference >= 0.8 and self.recv_time != 0:  # jeżeli różnica >0.3, to wystaw flagę reconecting na True
                if not self.reconecting:
                    magazyn.clients_table.remove(self.klient_name)
                    magazyn.clients_table_name.remove(self.HUV_name)
                    print("name: " + str(magazyn.clients_table_name))
                    print("throw out 1")
                    self.run = False
                    self.reconecting = True
            '''if self.reconecting and self.difference <= 0.5:
                if  self.klient_name not in magazyn.clients_table and self.HUV_name not in magazyn.clients_table_name:
                    magazyn.clients_table.append(self.klient_name)
                    magazyn.clients_table_name.append(self.HUV_name)
                    print("name: " + str(magazyn.clients_table_name))
                    print("throw out 2")
                    self.reconecting = False'''

    def get_conn(self):  # nie wykorzystywana funkcja (w przyszłości będzie)
        return self.conn

    def send2(self, message):   # funkcja odpowiedzialna za wysyłanie wiadomości do swojego pojazdu
        print(message)
        msg = '{:<50}'.format(message)  # KAŻDA WIADOMOSC WYSYLANA MA 50 BAJTÓW. JAK NIE TO UZUPELNIJ SPACJAMI
        self.conn.send(msg.encode())   # wyślij na socket conn

    def check_send(self, name, magazyn):   # jeżeli nie da się wysłać, to usuń klienta całkowicie z pamięci, ponieważ on sam zakończył komunikację z serverem.
        msg2 = '{:<50}'.format("HUV:1")  # ramka życia
        while self.run:
            try:
                self.conn.send(msg2.encode())   # wyślij ramkę życia do klienta
                    #print(msg2)
            except socket.error:                # jeżeli błąd, czyli klient zamknął z nami łącze
                print("blad wysylania")
                self.run = False  # zakończ pracę metod tego klienta
                self.conn.close()  # zamknij z nim komunikację
                self.reconecting = True
                self.receive_flag = False
                self.difference = 1
               
                try:
                    magazyn.clients_table.remove(self.klient_name)
                    magazyn.clients_table_name.remove(self.HUV_name)
                    time.sleep(1)
                    print("name: " + str(magazyn.clients_table_name))
                    print("adres: " + str(magazyn.clients_table))
                    print("throw out 3")
                except:
                    pass
            time.sleep(0.1)  # bardzo ważne, żeby nie zapchać komunikacji!

    def check_receive(self, name, magazyn):    # jeżeli nie da się odebrać, to usuń klienta całkowicie z pamięci, ponieważ on sam zakończył komunikację z serverem.
        time.sleep(0.1)
        while self.run:
            try:
                msg = str(self.conn.recv(50).decode())  # tu kod się zatrzymuje i oczekuje na przyjście ramki od klienta

                if "HUV" in str(msg):  # jeżeli przyszła ramka i jest ona równa HUV:1
                    self.receive_flag = True

                elif len(msg) > 5:  # jeżeli przyszła jakaś inna ramka niż HUV:1


                    self.HUV_package_decode(msg)  # dekodowanie ramki i zapisywanie parametrów pojazdu do listy

            except socket.error:

                try:  #if self.klient_name in magazyn.clients_table:  # jeżeli błąd, czyli klient zamknął z nami łącze
                    magazyn.clients_table.remove(self.klient_name)
                    magazyn.clients_table_name.remove(self.HUV_name)
                    print("name 2: " + str(magazyn.clients_table_name))
                    print("adres 2: " + str(magazyn.clients_table))
                except:
                    pass
            #self.run = False                            # zakończ pracę metod tego klienta
            #self.conn.close()                           # zamknij z nim komunikację
            #if self.klient_name in magazyn_clients_table:  # jeżeli błąd, czyli klient zamknął z nami łącze
            #    magazyn_clients_table.remove(self.klient_name)
            #    magazyn_clients_table_name.remove(self.HUV_name)
            #print("blad odbioru")
            #print("name: " + str(magazyn_clients_table_name))
            #print("adres: " + str(magazyn_clients_table))

    def HUV_package_decode(self, message):

        # package format: parameter_1:parameter_2:parameter_3:parameter_4...
        i=0
        #print(message)
        while i < self.number_of_parameters:
            try:
                parameter = re.search('.+?(?=:)', message)[0]  # czyli przeszukaj string. od lewej bierz ile mozliwe a od prawej do znaku :
                cut = int(len(str(parameter))) + 1
                self.parameter_magazyn[i] = parameter
                #print(parameter)
                message = message[cut:]

                i +=1
            except:
                pass
                #print("wrong package decode")
        #self.parameter_magazyn[i] = parameter
        #print(parameter)

# ======================================================================================================================


def send_message_to_client(eth_queue_to_HUV, magazyn):  # funkcja zmienia HUV do którego chcemy wysyłać dane lub wysyła dane
    while True:

        message = eth_queue_to_HUV.get()        # pobierz wiadomość z kolejki

        if message == "ZMIEN":                  # jeżeli wiadomość to "ZMIEN", to zmień na kolejny pojazd z listy
            if magazyn.wybor_HUV >= (len(magazyn.clients_table_name) -1):  # lista przekroczona?
                magazyn.wybor_HUV = 0                           # wróc do elementu zero
                print(magazyn.wybor_HUV)


            else:

                magazyn.wybor_HUV = magazyn.wybor_HUV + 1                       # nie przekroczona? to przeskocz na następny
                print(magazyn.wybor_HUV)
        else:                                   # jeżeli wiadomość to nie "ZMIEN" i nie "STOP", to wyślij ją do pojazdu
            try:
                if len(magazyn.clients_table_name) == 0:    # jeżeli nie ma klientów w liście dostępnych klientów
                    no_client = True
                    while no_client:            # czekaj w pętli dopuki nie pojawi się jakiś klient w liście dostępnych klientów
                        if len(magazyn.clients_table_name) > 0:
                            no_client = False
                elif magazyn.wybor_HUV > len(magazyn.clients_table_name)-1:    # lista przekroczona? wróc do elementu zero
                    magazyn.wybor_HUV = 0
                    print("lista przekroczona")
                else:
                    pass
                    try:
                        magazyn.clients_table[magazyn.wybor_HUV].send2(str(message))  # wyślij wiadomość do klienta (send2 to funkcja obiektu klient)
                    except:
                        pass
            except socket.error:                # jeżeli błąd, to tylko poinformuj, że client lost.
                '''
                nie ma innej obsługi tej sytuacji, ponieważ takowa jeszcze się nie trafiła i pojawi się dopiero w testach
                komunikacji z rzeczywistym pojazdem w wodzie, lub nie pojawi się, bo pojazd będzie dobrze działał i
                obsługa tej sytuacji nie jest potrzebna. To sie dopiero okaże
                '''
                print("brak klientow")
                pass


def ethernet_server_function(eth_queue_to_HUV, magazyn):  # główna funkcja biblioteki. Obsługuje całą komunikację ethernet

    print("start servera")

    PORT = 12350  # na tym porcie (sockecie) stanie server
    SERVER = socket.gethostbyname(socket.gethostname())  # uzyskiwanie IP servera (tego komputera PC) w sieci WiFi
    print(SERVER)
    ADDR = (SERVER, PORT)  # łączymy nasz adres ip z socketem

    server = socket.socket()  # stawiamy socket servera oczekujący na IPV4 adresy
    server.bind(ADDR)  # łączymy ten socket do tego adresu,

    server.listen(4)  # oczekuje maksymalnie na 4 klientów. Więcej nowych klientów nie przyjmie. zmien gdy pojawi się więcej pojazdów w sieci

    ip_list = ['192.168.0.101', '192.168.0.102', '192.168.0.103', '192.168.0.104', '192.168.124.25', '192.168.1.3', '192.168.124.233']  # możliwe pojazdy


    t3 = threading.Thread(target=send_message_to_client, args=(eth_queue_to_HUV, magazyn))
    t3.start()  # uruchomienie funkcji odpowiedzialnej za zmianę pojazdu i wysylanie do niego komend
    name = ''

    while True:  # PĘTLA DODAWANIA NOWEGO KLIENTA, stoi na .accept() dopuki nie pojawi się nowy klient
        conne, addr = server.accept()  # jeżeli jest nowy klient
        print(addr)
        for ip in ip_list:

            if ip in str(conne):
                magazyn.clients_table_name.append(ip)
                name = ip


        klient = ClientEth(conne, magazyn, name)  # utwórz obiekt dla tego klienta i zapisz mu conne (adres) tego klienta
        klient.klient_name = klient     # zapisz mu swoją nazwę, tak, żeby potem mógł sam siebie usunąć z listy klientów
        magazyn.clients_table.append(klient)
        name = "HUV"
        t13 = threading.Thread(target=klient.check_receive, args=(name, magazyn))
        t13.start()  # wystartuj funkcję check_receive tego konkretnego klienta (obiektu), którego dodano do listy
        t11 = threading.Thread(target=klient.check_send, args=(name, magazyn))
        t11.start()  # wystartuj funkcję check_send tego konkretnego klienta (obiektu), którego dodano do listy
        t12 = threading.Thread(target=klient.timer, args=(name, magazyn))
        t12.start()  # wystartuj funkcję timer tego konkretnego klienta (obiektu), którego dodano do listy


        print("name: " + str(magazyn.clients_table_name))
        print("adres: " + str(magazyn.clients_table))
        print("add 1")