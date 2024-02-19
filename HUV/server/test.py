import matplotlib.pyplot as plt
import time

# Inicjalizacja list przechowujących dane
times = []
values = []

# Utworzenie nowego okna wykresu
fig, ax = plt.subplots()

# Inicjalizacja pustej linii wykresu
line, = ax.plot(times, values)

# Ustawienie etykiet osi i tytułu wykresu
ax.set_xlabel('Czas')
ax.set_ylabel('Wartość')
ax.set_title('Dynamiczny wykres')

# Uruchomienie pętli w tle
plt.ion()

while True:
    # Przyjęcie nowej wartości i czasu
    new_value = 0.1  # Tutaj podstaw kod, który przyjmuje nową wartość
    new_time = time.time()

    # Dodanie wartości i czasu do list
    values.append(new_value)
    times.append(new_time)

    # Ograniczenie list wartości i czasu do ostatnich 100 elementów (opcjonalnie)
    values = values[-100:]
    times = times[-100:]

    # Uaktualnienie danych na wykresie
    line.set_data(times, values)

    # Dopasowanie osi x do zakresu czasu
    ax.relim()
    ax.autoscale_view()

    # Odświeżenie wykresu
    plt.draw()
    plt.pause(0.1)  # Czas pauzy między odświeżeniami wykresu


