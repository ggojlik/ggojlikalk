# Analiza danych medycznych – reakcja na stres SECPT-G

## 1. Opis projektu

Projekt semestralny z języka Python przedstawia aplikację z graficznym interfejsem użytkownika (GUI), służącą do analizy danych dotyczących reakcji organizmu na stres wywołany procedurą SECPT-G (Socially Evaluated Cold Pressor Test for Groups).

Aplikacja umożliwia wczytywanie danych, przeglądanie wyników, filtrowanie obserwacji, wykonywanie analiz statystycznych oraz prezentowanie wyników na wykresach.

Projekt wykorzystuje **syntetyczny zbiór danych zawierający 500 rekordów**. Wyniki mają charakter edukacyjny i nie służą do diagnozy medycznej.

## 2. Lista funkcji aplikacji

- Wczytywanie danych z pliku CSV.
- Korzystanie ze słownika zmiennych zapisanego w pliku Excel.
- Wyświetlanie danych wybranych zmiennych.
- Filtrowanie danych według dwóch kryteriów.
- Wyświetlanie liczebności i procentów.
- Obliczanie średniej, mediany, minimum, maksimum i odchylenia standardowego.
- Porównywanie poziomu kortyzolu w grupach według płci.
- Wykonywanie testu t-Studenta dla prób zależnych.
- Prezentowanie wykresów słupkowych, histogramów, wykresu rozrzutu oraz wykresu reakcji kortyzolowej.
- Eksportowanie przefiltrowanych danych do pliku CSV.
- Kopiowanie danych do schowka w celu wklejenia do programu Excel.
- Wyświetlanie podsumowania wyników i krótkich wniosków.


## 3. Instalacja

Do uruchomienia projektu potrzebny jest Python 3.10 lub zgodna wersja Pythona z obsługą Tkinter.

Pobierz repozytorium z GitHub:

https://github.com/ggojlik/ggojlikalk

Następnie otwórz folder projektu w PyCharmie lub innym środowisku obsługującym Python.

Zainstaluj wymagane biblioteki poleceniem:

```bash
python -m pip install -r requirements.txt
```

## 4. Uruchomienie aplikacji

W folderze projektu uruchom:

```bash
python "projekt semestralny.py"
```

W tym samym folderze powinny znajdować się pliki:

- `projekt semestralny.py` – kod aplikacji
- `dane_syntetyczne_500_rekordow.csv` – przykładowe dane
- `zmienne.xlsx` – słownik zmiennych
- `foka.jpeg` – grafika używana w oknie informacyjnym
- `requirements.txt` – lista bibliotek

Aplikacja automatycznie wczytuje dane podczas uruchamiania.


## 5. Zrzuty ekranu

W tej sekcji zostaną umieszczone zrzuty ekranu prezentujące:

- Główne okno aplikacji.
- Statystyki opisowe.
- Histogram kortyzolu.
- Wykres rozrzutu.
- Wyniki analizy statystycznej.

## 6. Wykorzystanie sztucznej inteligencji

Podczas realizacji projektu korzystano z ChatGPT jako narzędzia wspomagającego naukę i programowanie.

AI pomagała w planowaniu struktury aplikacji, przygotowywaniu i poprawianiu fragmentów kodu Python, wyjaśnianiu komunikatów błędów, implementacji analiz statystycznych, tworzeniu wykresów oraz opracowywaniu dokumentacji.

Kod był uruchamiany, testowany i poprawiany w środowisku PyCharm. Poszczególne etapy pracy dokumentowano w repozytorium GitHub za pomocą kolejnych commitów.
