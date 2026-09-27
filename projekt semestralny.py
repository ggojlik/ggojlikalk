import pandas as pd
from pathlib import Path

# Lokalizacja projektu
BASE_DIR = Path(__file__).resolve().parent

# Lokalizacja pliku CSV
file_path = BASE_DIR / "dane_syntetyczne_500_rekordow.csv"

# Wczytanie danych głównych
df = pd.read_csv(
    file_path,
    sep=";",
    decimal=","
)

# Wczytanie słownika zmiennych
slownik = pd.read_excel(
    BASE_DIR / "zmienne.xlsx",
    header=3
)

# Czyszczenie nazw kolumn
slownik.columns = slownik.columns.str.strip()

# NAJPIERW uzupełniamy puste nazwy zmiennych
slownik["Variable"] = slownik["Variable"].ffill()

# DOPIERO POTEM zamieniamy na tekst i czyścimy spacje
slownik["Variable"] = slownik["Variable"].astype(str).str.strip()

print("\nKontrola słownika:")
print(slownik.head(10))

# Nazwy zmiennych w danych głównych
zmienne_dane = set(df.columns)

# Nazwy zmiennych w słowniku
zmienne_slownik = set(slownik["Variable"].dropna())

# Sprawdzenie zgodności
brakujace_opisy = zmienne_dane - zmienne_slownik

print("\nZmienne bez opisu w słowniku:")
print(brakujace_opisy)

print(slownik.columns.tolist())
print(slownik.head(10).to_string())

# Ujednolicenie nazw zmiennych w słowniku
slownik["Variable"] = slownik["Variable"].astype(str).str.strip()

# Mapa: nazwa małymi literami -> prawdziwa nazwa kolumny w danych
mapa_kolumn = {
    col.strip().lower(): col
    for col in df.columns
}

# Tylko zmienne występujące jednocześnie
# w danych i w słowniku
wspolne_zmienne = []

for zmienna in slownik["Variable"].dropna().unique():
    nazwa = zmienna.lower()

    if nazwa in mapa_kolumn:
        wspolne_zmienne.append(mapa_kolumn[nazwa])

# Kontrola
print("\nZmienne dostępne w GUI:")
print(wspolne_zmienne)
print("Liczba:", len(wspolne_zmienne))

def pobierz_mape_etykiet(zmienna):
    """
    Zwraca słownik:
    wartość z danych -> opis (Label)
    """

    # Znajdujemy nazwę zmiennej w słowniku
    fragment = slownik[
        slownik["Variable"].str.lower() == zmienna.lower()
    ].copy()

    # Usuwamy wiersze bez Value lub Label
    fragment = fragment.dropna(subset=["Value", "Label"])

    return dict(zip(fragment["Value"], fragment["Label"]))

import tkinter as tk
from tkinter import ttk


# Utworzenie okna
root = tk.Tk()

root.title("Projekt semestralny - Analiza danych")

root.geometry("850x600")


# Nagłówek
naglowek = tk.Label(
    root,
    text="Analiza danych - 500 rekordów",
    font=("Arial", 18, "bold")
)

naglowek.pack(pady=20)


# Informacja o liczbie rekordów
informacja = tk.Label(
    root,
    text=f"Liczba rekordów: {len(df)} | Liczba dostępnych zmiennych: {len(wspolne_zmienne)}",
    font=("Arial", 11)
)

informacja.pack(pady=10)


# Wybór zmiennej
etykieta = tk.Label(
    root,
    text="Wybierz zmienną do analizy:",
    font=("Arial", 12)
)

etykieta.pack(pady=10)


wybrana_zmienna = tk.StringVar()

lista_zmiennych = ttk.Combobox(
    root,
    textvariable=wybrana_zmienna,
    values=wspolne_zmienne,
    state="readonly",
    width=40
)

lista_zmiennych.pack(pady=10)


# Pole wyświetlania wyników
wyniki = tk.Text(
    root,
    height=18,
    width=90
)

wyniki.pack(pady=20)


# Funkcja wyświetlająca dane
def pokaz_dane():
    zmienna = wybrana_zmienna.get()

    if not zmienna:
        return

    wyniki.delete("1.0", tk.END)

    # Pobieramy mapowanie kod -> opis
    mapa_etykiet = pobierz_mape_etykiet(zmienna)

    # Kopia wybranej kolumny
    dane = df[zmienna].copy()

    # Jeśli dla zmiennej istnieją etykiety,
    # zamieniamy kody na opisy
    if mapa_etykiet:
        dane_opisane = dane.map(mapa_etykiet).fillna(dane)
    else:
        dane_opisane = dane

    wyniki.insert(
        tk.END,
        f"Wybrana zmienna: {zmienna}\n\n"
    )

    wyniki.insert(
        tk.END,
        "Pierwsze 20 rekordów:\n\n"
    )

    wyniki.insert(
        tk.END,
        dane_opisane.head(20).to_string()
    )


# Przycisk
przycisk = tk.Button(
    root,
    text="Pokaż dane",
    command=pokaz_dane,
    font=("Arial", 11),
    width=20
)

przycisk.pack(pady=10)


# Uruchomienie aplikacji
root.mainloop()

print(slownik.head(10))