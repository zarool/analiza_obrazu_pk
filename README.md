# Analiza obrazu - kod masztu

Generalnie kod opiewa na modulacji obrazem wejściowym, tak, aby ustawić odpowiednie kontury, jasność, kolor aby przy poszukiwanym obiekcie powstały kontury a algorytm opencv2 był w stanie wychwycić ten kontur i podał jego współrzędne - następnie rysowany jest kwadrat wokół tego konturu, co pozwala na późniejsze wyszukanie koloru.
W trakcie pracy jest dodawanie sieci neurowonych i trenowanie własnego modelu rozpoznawania obrazu, tak, aby mógł przechwycić poszukiwany obiekt.

```
![Zrzut ekranu działającego programu](```
https://github.com/zarool/analiza_obrazu_pk/blob/main/dokumentacja/new-cam-out.png?raw=true
```)
```

Krótki spis treści
1. [ Pliki ](#files)  
2. [Potrzebne biblioteki](#dependencies)
3. [ Uruchomienie ](#usage)
4. [Opis funkcji w programie](#functions)
   
<a name="files"></a>
## Pliki
Niezbędne pliki do uruchomienia samej analizy obrazu (bez sieci neuronowych)
|                |Opis                          
|----------------|------------------------------
|main.py				 | Główny plik programu, na starcie ustawia kluczowe globalne zmienne - te podane z terminala oraz ustawione przez cv2 do odczytu obrazu z kamery. Zawiera skrypt do wygenerowania prostego GUI ze sliderami do przetwarzania uchwyconego obrazu          
|utils.py        | Plik do modulacji obrazem, zawiera same funkcje, zwraca obraz z konturami            
|system.py       | Przyjmuje parametry z terminala (mają defaultowe wartości, nie są niezbędne) oraz zbiera informacje na temat tego, czy zewnętrzna kamera występuje - jeżeli nie, to wychwyci obraz z kamerki z laptopa

<a name="dependencies"></a>
## Biblioteki
|                |Wersja                          
|----------------|------------------------------
|opencv2				 | `>= 4.0.0`- im nowsza tym lepiej, kluczowa do odbioru obrazu z kamery           
|numpy        	 |	Zawarta w interpreterze           
|JetCam          | Znajduje się w folderze jetcam, nic nie trzeba zmieniać


<a name="usage"></a>
## Uruchomienie skryptu

`python3 main.py` - standardowe uruchomienie programu, wyświetli się obraz oraz osobne okienko ze sliderami

Dodatkowe parametry jakie można użyć w kodzie:
| Paremtr do uruchomienia | Domyślna wartość | Opis
| - | - | -
|`--camera` | `1` | zmiana odczytu obrazu z kamery (wartość 1) lub ze zdjęć (wartość 0)
|`--contour` <br> `-c` | `0` | wyświetlenie się dodatkowego okna z efektem dilation (gdy ustawimy wartość 1) - używane do lepszej modulacji obrazem
|`--detect` <br> `-d` | `1` | pokazuje prostokąty znalezionych obiektów (ustawienie 0 wyłącza te funkcje)
|`--info` <br> `-i` | `1` | pomocniczne zmienne pod każdym z odnalezionych kwadratów (kolor, wielkość)
|`--image` | `X` | do użycia, jeżeli wpisujemy `--camera 0 ` - odczytuje zdjęcie z folderu `/images/camX.jpg`- w repo nie ma tego folderu (na ten moment), lepiej nie używać - tylko do debuggingu 
|`--flip` | `0` | przy ustawieniu parametru `2` - obrót widoku kamery o 180 stopni

