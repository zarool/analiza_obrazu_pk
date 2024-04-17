# Analiza obrazu - kod masztu

Generalnie kod opiewa na modulacji obrazem wejściowym, tak, aby ustawić odpowiednie kontury, jasność, kolor aby przy
poszukiwanym obiekcie powstały kontury a algorytm opencv2 był w stanie wychwycić ten kontur i podał jego współrzędne -
następnie rysowany jest kwadrat wokół tego konturu, co pozwala na późniejsze wyszukanie koloru. Program uruchamiany był
przy użyciu NVIDIA Jetson Nano z kamerą IMX219. Jednak poprzez użycie biblioteki JetCam nie powinno być problemu z
innymi typami kamer. <br>
W trakcie pracy jest dodawanie sieci neurowonych i trenowanie własnego modelu rozpoznawania obrazu, tak, aby mógł
automatycznie przechwycić poszukiwany obiekt.

![Zrzut ekranu działającego programu](https://github.com/zarool/analiza_obrazu_pk/blob/main/dokumentacja/images-output-old/out0.png?raw=true)

### Spis treści

1. [ Pliki ](#files)
2. [Potrzebne biblioteki](#dependencies)
3. [ Uruchomienie ](#usage)
4. [Hardware](#hw)
5. [Opis funkcji w programie](#functions)
6. [Wykorzystanie programu jako modułu](https://github.com/zarool/analiza_obrazu_pk/blob/class/README.md)

<a name="files"></a>

## Pliki

Niezbędne pliki do uruchomienia samej analizy obrazu (bez sieci neuronowych)

|             | Opis                                                                                                                                                                                                                                          |                
|-------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `main.py`   | Główny plik programu, na starcie ustawia kluczowe globalne zmienne - te podane z terminala oraz ustawione przez cv2 do odczytu obrazu z kamery. Zawiera skrypt do wygenerowania prostego GUI ze sliderami do przetwarzania uchwyconego obrazu |
| `utils.py`  | Plik do modulacji obrazem, zawiera same funkcje, zwraca obraz z konturami                                                                                                                                                                     |
| `system.py` | Przyjmuje parametry z terminala (mają defaultowe wartości, nie są niezbędne) oraz zbiera informacje na temat tego, czy zewnętrzna kamera występuje - jeżeli nie, to wychwyci obraz z kamerki z laptopa                                        |
| `jetcam/`   | Folder z opensourcową biblioteką do obsługi kamer CSI oraz wbudowanych kamer                                                                                                                                                                  |

<a name="dependencies"></a>

## Biblioteki

|           | Wersja                                                                                                                                        |
|-----------|-----------------------------------------------------------------------------------------------------------------------------------------------|
| Python3   | Każdy interpeter od wersji `>=3.8` nie powinien wywoływać problemu                                                                            |
| opencv2 	 | `>= 4.0.0`- im nowsza tym lepiej, kluczowa do odbioru obrazu z kamery - konieczne jest zainstalowanie OpenCV2 ze wsparciem modułu GSTSTREAMER |
| numpy     | 	Zawarta w interpreterze                                                                                                                      |
| JetCam    | Znajduje się w folderze jetcam, nic nie trzeba zmieniać                                                                                       |

<a name="usage"></a>

## Uruchomienie skryptu

`python3 main.py` - standardowe uruchomienie programu, wyświetli się obraz oraz osobne okienko ze sliderami

Dodatkowe parametry jakie można użyć podczas uruchamiania programu (szczegółowy opis po użyciu parametru `--help, -h`:

| Paremtr do uruchomienia | Domyślna wartość | Opis                                                                                                                                                                            |
|-------------------------|------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `camera`                | `1`              | zmiana odczytu obrazu z kamery (wartość 1) lub ze zdjęć (wartość 0)                                                                                                             |
| `contour, c`            | `0`              | wyświetlenie się dodatkowego okna z efektem dilation (gdy ustawimy wartość 1) - używane do lepszej modulacji obrazem                                                            |
| `detect, d`             | `1`              | pokazuje prostokąty znalezionych obiektów (ustawienie 0 wyłącza te funkcje)                                                                                                     |
| `info, i`               | `1`              | pomocniczne zmienne pod każdym z odnalezionych kwadratów (kolor, wielkość)                                                                                                      |
| `image`                 | `-`              | do użycia, jeżeli wpisujemy `--camera 0 ` - odczytuje zdjęcie z folderu `/images/camX.jpg`- w repo nie ma tego folderu (na ten moment), lepiej nie używać - tylko do debuggingu |
| `flip`                  | `0`              | przy ustawieniu parametru `2` - obrót widoku kamery o 180 stopni                                                                                                                |
| `width`                 | `-`              | Ustawienie szerokości wyświetlanego obrazu w oknie opencv2                                                                                                                      |
| `height`                | `-`              | Ustawienie wysokości wyświetlanego obrazu w oknie opencv2                                                                                                                       |
| `mode, m`               | `0`              | Zmiana trybu pracy kamery (rozdzielczość oraz ilość odbieranych klatek), opisane w tabeli poniżej                                                                               |

<a name="hw"></a>

## Hardware

Tryby działania kamery IMX219 użytej w programie

| Indeks | Szerokość [px] | Wysokość [px] | FPS |
|--------|----------------|---------------|-----|
| 0      | 3264           | 2454          | 21  |
| 1      | 3264           | 1848          | 28  |
| 2      | 1920           | 1090          | 30  |
| 3      | 1640           | 1232          | 30  |
| 4      | 1280           | 720           | 60  |
| 5      | 1280           | 720           | 120 |

<a name="functions"></a>

## Opis funkcji w programie

* Sterowanie programem:
    - `q` - zamyka program
    - `n` oraz `b` służą do przechodzenia pomiedzy zdjęciami

 <br>  

* `main.py`

| Nazwa funkcji          | Opis                                                                                                                                                                                                             |
|------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `set_exposure(valuse)` | Zmiana ekspozycji kamery, wymaga restartu, dlatego znajduje się w głównym programie                                                                                                                              |
| `recognition()`        | Główna pętla programu, uruchamiana zaraz po ustawieniu parametrów, sprawdza na początku czy jest odczyt z kamery, odczytuje wartości ze sliderów a następnie wykonuje algorytm z modyfikacją obrazu (`utils.py`) |

<br>

* `utils.py`

| Nazwa funkcji                                                                            | Opis                                                                                                                                                                                                                                                   |
|------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `masking(img, lower, upper)`                                                             | Maskowanie obrazu zgodnie z paletą HSV, w zależności od tego jak ustawimy slidery, możemy uzyskać wychwytywanie tylko konkretnego koloru z obrazu                                                                                                      |
| `get_contours(img, c_thr, contrast, brightness, draw=True)`                              | Algorytm opencv2, z podanego obrazu funkcja zwraca nam potrzebne kontury do dalszej analizy (w funkcji są wykomentowane poszczególne etapy)                                                                                                            |
| `detect_square(model_image, final_image,` <br> `min_area, max_area, object_w, object_l)` | Z podanych konutr wyznacza kwadrat (algorytm opencv2) i obrysowuje obiekt, zwraca obraz z naniesionymi konturami                                                                                                                                       |
| `display_info(final_image, contour, ...)`                                                | Nanosi na wyświetlany obraz dodatkowe informacje                                                                                                                                                                                                       |
| `approx_length(rect, object_w, object_l)`                                                | Wyliczenie długości oraz szerokości odnalezionego obiektu, jeszcze w trakcie pracy, należy przeprowadzić kilka testów                                                                                                                                  |
| `approx_color(image, x, y, w, h)`                                                        | Algorytm szacujący kolor na podstawie prostokąta podanego w parametrach funkcji - oblicza średnią z kolorów każdego z pikseli a następnie dopasowuje najbliższy z podanej tablicy `colors = {"black", "red", "green", "blue"}` - dalej w trakcie pracy |

<br>

* `system.py`

| Nazwa funkcji     | Opis                                                                              |
|-------------------|-----------------------------------------------------------------------------------|
| `set_camera`      | Uruchamia odczyt obrazu z kamery przy użyciu biblioteki JetCam                    |
| `prepare_devices` | Sprawdza czy odczyt z kamery jest możliwy - jeżeli nie, odczytuje obraz z laptopa |
| `arguments`       | Przypisuje zmienne z terminala do globalnych ustawień programu                    |

