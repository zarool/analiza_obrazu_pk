# Analiza obrazu - kod masztu - wersja OOP

[Lepszy opis działania programu.](https://github.com/zarool/analiza_obrazu_pk/blob/main/README.md)

Krótki spis treści

1. [ Pliki ](#files)
2. [Potrzebne biblioteki](#dependencies)
3. [ Uruchomienie ](#usage)
4. [Opis funkcji w programie](#functions)

<a name="files"></a>

## Pliki

Niezbędne pliki do uruchomienia samej analizy obrazu (bez sieci neuronowych)

|           | Opis                                                                         |
|-----------|------------------------------------------------------------------------------|
| main.py   | Przykładowy plik pokazujący wykorzystanie modułu analizy obrazu jako obiektu |
| Maszt.py  | Główna klasa, moduł importuje pozostałe potrzebne biblioteki                 |
| Utils.py  | Klasa zawierająca głównie funkcje statyczne, przetwarza i zwraca obraz       |
| Camera.py | Moduł uruchamiający kamerę, nagranie bądź odczytuje zdjęcia                  |
| Window.py | Utworzenie dwóch okienek z obrazem oraz pomocnicznymi suwakami               |

<a name="dependencies"></a>

## Biblioteki

|                 | Wersja                                                                |
|-----------------|-----------------------------------------------------------------------|
| opencv2		       | `>= 4.0.0`- im nowsza tym lepiej, kluczowa do odbioru obrazu z kamery |
| numpy        	  | 	Zawarta w interpreterze                                              |
| JetCam          | Znajduje się w folderze jetcam, nic nie trzeba zmieniać               |

<a name="usage"></a>

## Uruchomienie skryptu

`from Maszt import Maszt` - zaimportowanie biblioteki

`analiza = Maszt()` - utworzenie nowego obiektu

`analiza.start()` - uruchomienie analizy obrazu oraz potrzebnych okienek do działania

`analiza.close()` - zamknięcie programu

Dodatkowe parametry podczas inicjalizacji obiektu (`analiza = Maszt(---)`):

| Paremtr do uruchomienia | Domyślna wartość | Opis                                                                                                                                             |
|-------------------------|------------------|--------------------------------------------------------------------------------------------------------------------------------------------------|
| `cam_disp=`             | `1`              | zmiana odczytu obrazu z kamery (wartość 1) lub ze zdjęć (wartość 0)                                                                              |
| `contour=`              | `0`              | wyświetlenie się dodatkowego okna z efektem dilation (gdy ustawimy wartość 1) - używane do lepszej modulacji obrazem                             |
| `detect=`               | `1`              | pokazuje prostokąty znalezionych obiektów (ustawienie 0 wyłącza te funkcje)                                                                      |
| `info=`                 | `1`              | pomocniczne zmienne pod każdym z odnalezionych kwadratów (kolor, wielkość)                                                                       |
| `current=`              | `X`              | do użycia, jeżeli `cam_disp=0` - wpisujemy `current=X` - odczytuje zdjęcie z folderu `/images/camX.jpg`, lepiej nie używać - tylko do debuggingu |
| `flip=`                 | `0`              | przy ustawieniu parametru `2` - obrót widoku kamery o 180 stopni                                                                                 |
| `mode=`                 | `0`              | ustawienie rozdzielczości oraz ilości klatek w jakiej ma pracować kamera, dokładny opis [poniżej](#camera_modes)                                 |
| `object_w=`             | `4` [cm]         | szerokość szukanego obiektu, do obliczenia odległości - na ten moment nie działa poprawnie                                                       |
| `object_l=`             | `15` [cm]        | długość (wysokość) szukanego obiektu, do obliczenia odległości - na ten moment nie działa poprawnie                                              |


<a name="camera_modes"></a>
### Tryby działania kamery

| Indeks | Szerokość [px] | Wysokość [px] | FPS |
|--------|----------------|---------------|-----|
| 0      | 3264           | 2454          | 21  |
| 1      | 3264           | 1848          | 28  |
| 2      | 1920           | 1090          | 30  |
| 3      | 1640           | 1232          | 30  |
| 4      | 1280           | 720           | 60  |
| 5      | 1280           | 720           | 120 |

<a name="functions"></a>

### Opis podstawowych funkcji w programie

Samo działanie funkcji jest opisane w poprzednim pliku. W razie jakiś błędów czekam na kontakt. 

W przyszłości będzie dodana funkcjonalność zwracania obrazu jako zmiennej w celu jeszcze późniejszej analizy, bądź do wykorzystania w kolejnym planowanym module do serwo kamery - podążanie kamerą za wykrytym obiektem.
