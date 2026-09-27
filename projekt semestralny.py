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
import matplotlib.pyplot as plt


root = tk.Tk()
root.title("Analiza danych")
root.geometry("950x700")
root.minsize(800, 600)


# -------------------------
# NAGŁÓWEK
# -------------------------

naglowek = ttk.Label(
    root,
    text="Analiza danych",
    font=("Arial", 22, "bold")
)
naglowek.pack(pady=(20, 5))

informacja = ttk.Label(
    root,
    text=f"Liczba rekordów: {len(df)}   |   "
         f"Liczba dostępnych zmiennych: {len(wspolne_zmienne)}",
    font=("Arial", 11)
)
informacja.pack(pady=(0, 20))


# -------------------------
# PANEL WYBORU ZMIENNEJ
# -------------------------

panel = ttk.LabelFrame(
    root,
    text=" Wybór zmiennej ",
    padding=15
)
panel.pack(fill="x", padx=30, pady=10)

ttk.Label(
    panel,
    text="Zmienna:",
    font=("Arial", 11)
).grid(row=0, column=0, padx=10, pady=5)

wybrana_zmienna = tk.StringVar()

lista_zmiennych = ttk.Combobox(
    panel,
    textvariable=wybrana_zmienna,
    values=wspolne_zmienne,
    state="readonly",
    width=35
)
lista_zmiennych.grid(row=0, column=1, padx=10, pady=5)

if wspolne_zmienne:
    lista_zmiennych.current(0)


# -------------------------
# POLE WYNIKÓW
# -------------------------

ramka_wyniki = ttk.LabelFrame(
    root,
    text=" Wyniki analizy ",
    padding=10
)
ramka_wyniki.pack(
    fill="both",
    expand=True,
    padx=30,
    pady=15
)

wyniki = tk.Text(
    ramka_wyniki,
    height=20,
    width=90,
    font=("Consolas", 10),
    wrap="none"
)

scroll_y = ttk.Scrollbar(
    ramka_wyniki,
    orient="vertical",
    command=wyniki.yview
)

wyniki.configure(yscrollcommand=scroll_y.set)

wyniki.pack(
    side="left",
    fill="both",
    expand=True
)

scroll_y.pack(
    side="right",
    fill="y"
)


# -------------------------
# FUNKCJE
# -------------------------

def pobierz_dane_opisane(zmienna):

    mapa_etykiet = pobierz_mape_etykiet(zmienna)

    dane = df[zmienna].copy()

    if mapa_etykiet:
        return dane.map(mapa_etykiet).fillna(dane)

    return dane


def pokaz_dane():

    zmienna = wybrana_zmienna.get()

    if not zmienna:
        return

    dane = pobierz_dane_opisane(zmienna)

    wyniki.delete("1.0", tk.END)

    wyniki.insert(
        tk.END,
        f"ZMIENNA: {zmienna}\n"
        + "=" * 60
        + "\n\n"
    )

    wyniki.insert(
        tk.END,
        "Pierwsze 20 rekordów:\n\n"
    )

    wyniki.insert(
        tk.END,
        dane.head(20).to_string()
    )


def pokaz_statystyki():

    zmienna = wybrana_zmienna.get()

    if not zmienna:
        return

    dane = pobierz_dane_opisane(zmienna)

    liczebnosci = dane.value_counts(dropna=False)
    procenty = dane.value_counts(
        normalize=True,
        dropna=False
    ) * 100

    tabela = pd.DataFrame({
        "Liczebność": liczebnosci,
        "Procent [%]": procenty.round(2)
    })

    wyniki.delete("1.0", tk.END)

    wyniki.insert(
        tk.END,
        f"STATYSTYKI: {zmienna}\n"
        + "=" * 60
        + "\n\n"
    )

    wyniki.insert(
        tk.END,
        tabela.to_string()
    )


def pokaz_wykres():

    zmienna = wybrana_zmienna.get()

    if not zmienna:
        return

    dane = pobierz_dane_opisane(zmienna)

    liczebnosci = dane.value_counts()

    plt.figure(figsize=(9, 5))

    liczebnosci.plot(
        kind="bar"
    )

    plt.title(
        f"Rozkład zmiennej: {zmienna}"
    )

    plt.xlabel(zmienna)
    plt.ylabel("Liczebność")

    plt.xticks(
        rotation=45,
        ha="right"
    )

    plt.tight_layout()
    plt.show()


# -------------------------
# PRZYCISKI
# -------------------------

przyciski = ttk.Frame(root)
przyciski.pack(pady=(0, 20))

ttk.Button(
    przyciski,
    text="Pokaż dane",
    command=pokaz_dane,
    width=18
).grid(
    row=0,
    column=0,
    padx=8
)

ttk.Button(
    przyciski,
    text="Statystyki",
    command=pokaz_statystyki,
    width=18
).grid(
    row=0,
    column=1,
    padx=8
)

ttk.Button(
    przyciski,
    text="Wykres",
    command=pokaz_wykres,
    width=18
).grid(
    row=0,
    column=2,
    padx=8
)


root.mainloop()