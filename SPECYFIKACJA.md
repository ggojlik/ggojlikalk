# Specyfikacja aplikacji – analiza danych medycznych SECPT-G

## 1. Cel aplikacji

Celem projektu jest stworzenie aplikacji desktopowej z graficznym interfejsem użytkownika (GUI), umożliwiającej analizę danych dotyczących reakcji organizmu na stres w procedurze SECPT-G (Socially Evaluated Cold Pressor Test for Groups).

Aplikacja została przygotowana w języku Python na potrzeby projektu semestralnego. Wykorzystuje syntetyczny zbiór danych zawierający 500 rekordów.

## 2. Interfejs użytkownika (GUI)

Interfejs aplikacji został wykonany z wykorzystaniem biblioteki Tkinter.

Główne okno zawiera:

- Listę rozwijaną umożliwiającą wybór zmiennej.
- Przyciski uruchamiające dostępne funkcje analityczne.
- Pola umożliwiające ustawienie dwóch kryteriów filtrowania.
- Obszar tekstowy prezentujący dane, statystyki i wyniki.
- Dodatkowe okna z wykresami i wynikami analiz.

Obsługa programu odbywa się za pomocą myszy, bez konieczności wpisywania poleceń w terminalu.

## 3. Dane wejściowe

Aplikacja korzysta z następujących plików:

- `dane_syntetyczne_500_rekordow.csv` – syntetyczny zbiór danych.
- `zmienne.xlsx` – słownik zmiennych i ich wartości.

Zbiór zawiera dane uczestników oraz pomiary związane z reakcją na stres.

Do analiz kortyzolu wykorzystywane są między innymi zmienne:

- `cort_s0` – pomiar kortyzolu przed stresorem.
- `cort_s1` – kolejny pomiar kortyzolu.
- `cort_s2` – późniejszy pomiar kortyzolu.
- `sex` – zmienna określająca płeć uczestnika.

W danych mogą występować specjalne kody braków danych, takie jak `-99` i `-77`, które są pomijane w odpowiednich obliczeniach statystycznych.

## 4. Funkcje aplikacji

### 4.1. Wczytywanie i wyświetlanie danych

Program umożliwia wczytanie zbioru danych CSV oraz wyświetlanie informacji dotyczących wybranej zmiennej.

Użytkownik wybiera zmienną z listy rozwijanej, a wyniki prezentowane są w obszarze tekstowym.

### 4.2. Filtrowanie danych

Aplikacja umożliwia zastosowanie dwóch kryteriów filtrowania danych.

Filtry pozwalają ograniczyć analizowany zbiór do obserwacji spełniających wybrane warunki. Dostępna jest również funkcja usuwania filtrów i powrotu do pełnego zbioru.

### 4.3. Statystyki opisowe

Dla wybranych zmiennych liczbowych program oblicza:

- Liczbę poprawnych obserwacji.
- Średnią arytmetyczną.
- Medianę.
- Wartość minimalną i maksymalną.
- Odchylenie standardowe.

Dla danych jakościowych możliwe jest wyświetlanie liczebności oraz udziałów procentowych poszczególnych wartości.

### 4.4. Porównywanie grup

Program umożliwia porównanie podstawowego poziomu kortyzolu (`cort_s0`) między grupami określonymi przez zmienną `sex`.

Prezentowane są liczebności grup, średnie, mediany i odchylenia standardowe.

### 4.5. Analiza statystyczna

Aplikacja wykonuje test t-Studenta dla prób zależnych, porównujący pomiary kortyzolu `cort_s0` i `cort_s2`.

Wynik analizy obejmuje:

- Liczbę analizowanych par pomiarów.
- Średnie wartości w obu pomiarach.
- Średnią różnicę między pomiarami.
- Wartość statystyki t.
- Wartość p.
- Krótką interpretację wyniku.

### 4.6. Wizualizacja danych

Aplikacja generuje wykresy za pomocą biblioteki Matplotlib.

Dostępne są między innymi:

- Wykresy przedstawiające częstości wartości.
- Histogram rozkładu kortyzolu.
- Wykres reakcji kortyzolowej w kolejnych pomiarach.
- Wykres rozrzutu porównujący `cort_s0` i `cort_s2`.

Wykresy otwierane są w osobnych oknach.

### 4.7. Eksport danych

Użytkownik może wyeksportować aktualnie przefiltrowane dane do pliku CSV.

Aplikacja umożliwia również skopiowanie danych do schowka w formacie ułatwiającym ich wklejenie do arkusza Excel.

## 5. Przebieg działania programu

1. Użytkownik uruchamia aplikację.
2. Program udostępnia dane i listę zmiennych.
3. Użytkownik wybiera zmienną oraz opcjonalnie ustawia filtry.
4. Uruchamia wybraną funkcję, np. statystyki, wykres lub analizę kortyzolu.
5. Wyniki pojawiają się w głównym oknie albo w dodatkowym oknie.
6. Użytkownik może wykonać kolejne analizy, usunąć filtry lub wyeksportować dane.

## 6. Wymagania techniczne

- Python 3.10 lub zgodna wersja.
- System z obsługą graficznego interfejsu Tkinter.
- Biblioteki wymienione w pliku `requirements.txt`.

Główny plik programu: `projekt semestralny.py`.

## 7. Ograniczenia aplikacji

- Program wykorzystuje dane syntetyczne.
- Wyniki nie stanowią diagnozy ani porady medycznej.
- Analizy statystyczne mają charakter edukacyjny.
- Eksport CSV obejmuje dane, a nie pełny raport zawierający wszystkie wykresy i wyniki testów.

## 8. Podsumowanie

Aplikacja łączy funkcje przeglądania i filtrowania danych, obliczeń statystycznych, porównywania grup, testowania hipotez oraz wizualizacji wyników.

Projekt demonstruje praktyczne zastosowanie języka Python do analizy danych medycznych z wykorzystaniem graficznego interfejsu użytkownika.