

class Magazyn():
    def __init__(self):
        self.clients_table = []
        self.clients_table_name = []  # '192.168.0.101', '192.168.0.104', '192.168.0.103', '192.168.0.102'
        self.wybor_HUV = 0  # licznik zmiany lienta
        self.parameter_magazyn = [1, 1, 1, 1, 1, 0, 0, 1500, 1500,0,0,0]
        self.parameter_id_magazyn = ['NUCLEO', 'IMU', 'GPS', 'Bar02', 'Leakage', 'tryb', 'thruster enable', 'T200_1', 'T200_2', 'mast', 'actual depth', 'fin angle']
        self.number_of_parameters = 12
        self.ograniczenie = 20