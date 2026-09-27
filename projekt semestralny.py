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
# PANEL FILTROWANIA
# -------------------------

panel_filtr = ttk.LabelFrame(
    root,
    text=" Filtrowanie danych ",
    padding=15
)
panel_filtr.pack(fill="x", padx=30, pady=10)


# ----- FILTR 1 -----

ttk.Label(
    panel_filtr,
    text="Filtr 1:"
).grid(row=0, column=0, padx=10, pady=5)

wybrany_filtr = tk.StringVar()

lista_filtrow = ttk.Combobox(
    panel_filtr,
    textvariable=wybrany_filtr,
    values=["Brak filtra"] + wspolne_zmienne,
    state="readonly",
    width=22
)

lista_filtrow.grid(
    row=0,
    column=1,
    padx=10,
    pady=5
)

lista_filtrow.current(0)


ttk.Label(
    panel_filtr,
    text="Wartość:"
).grid(row=0, column=2, padx=10, pady=5)

wybrana_wartosc_filtra = tk.StringVar()

lista_wartosci_filtra = ttk.Combobox(
    panel_filtr,
    textvariable=wybrana_wartosc_filtra,
    state="readonly",
    width=22
)

lista_wartosci_filtra.grid(
    row=0,
    column=3,
    padx=10,
    pady=5
)


# ----- FILTR 2 -----

ttk.Label(
    panel_filtr,
    text="Filtr 2:"
).grid(row=1, column=0, padx=10, pady=5)

wybrany_filtr2 = tk.StringVar()

lista_filtrow2 = ttk.Combobox(
    panel_filtr,
    textvariable=wybrany_filtr2,
    values=["Brak filtra"] + wspolne_zmienne,
    state="readonly",
    width=22
)

lista_filtrow2.grid(
    row=1,
    column=1,
    padx=10,
    pady=5
)

lista_filtrow2.current(0)


ttk.Label(
    panel_filtr,
    text="Wartość:"
).grid(row=1, column=2, padx=10, pady=5)

wybrana_wartosc_filtra2 = tk.StringVar()

lista_wartosci_filtra2 = ttk.Combobox(
    panel_filtr,
    textvariable=wybrana_wartosc_filtra2,
    state="readonly",
    width=22
)

lista_wartosci_filtra2.grid(
    row=1,
    column=3,
    padx=10,
    pady=5
)

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

    df_filtr = pobierz_przefiltrowane_dane()

    mapa_etykiet = pobierz_mape_etykiet(zmienna)

    dane = df_filtr[zmienna].copy()

    if mapa_etykiet:
        dane = dane.map(mapa_etykiet).fillna(dane)

    wyniki.delete("1.0", tk.END)

    wyniki.insert(
        tk.END,
        f"Liczba rekordów po filtrowaniu: {len(df_filtr)}\n\n"
    )

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

    df_filtr = pobierz_przefiltrowane_dane()

    mapa_etykiet = pobierz_mape_etykiet(zmienna)

    dane = df_filtr[zmienna].copy()

    if mapa_etykiet:
        dane = dane.map(mapa_etykiet).fillna(dane)

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

    # Pobieramy dane po zastosowaniu obu filtrów
    df_filtr = pobierz_przefiltrowane_dane()

    # Pobieramy wybraną zmienną tylko z przefiltrowanych danych
    dane = df_filtr[zmienna].copy()

    # Zamiana kodów na etykiety ze słownika
    mapa_etykiet = pobierz_mape_etykiet(zmienna)

    if mapa_etykiet:
        dane = dane.map(mapa_etykiet).fillna(dane)

    # Liczebności kategorii
    liczebnosci = dane.value_counts()

    plt.figure(figsize=(9, 5))

    ax = liczebnosci.plot(
        kind="bar"
    )

    for kontener in ax.containers:
        ax.bar_label(
            kontener,
            padding=3,
            fontsize=10
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

def wyczysc_filtry():
    lista_filtrow.current(0)
    lista_filtrow2.current(0)

    wybrana_wartosc_filtra.set("")
    wybrana_wartosc_filtra2.set("")

    lista_wartosci_filtra["values"] = []
    lista_wartosci_filtra2["values"] = []

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

ttk.Button(
    przyciski,
    text="Wyczyść filtry",
    command=wyczysc_filtry,
    width=18
).grid(
    row=0,
    column=3,
    padx=8
)

def aktualizuj_filtr(zmienna_var, lista_wartosci, wartosc_var):

    zmienna = zmienna_var.get()

    if zmienna == "Brak filtra" or not zmienna:
        lista_wartosci["values"] = []
        wartosc_var.set("")
        return

    dane_opisane = pobierz_dane_opisane(zmienna)

    wartosci = (
        dane_opisane
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    wartosci = sorted(wartosci)

    lista_wartosci["values"] = wartosci

    if wartosci:
        lista_wartosci.current(0)


def aktualizuj_filtr1(event=None):
    aktualizuj_filtr(
        wybrany_filtr,
        lista_wartosci_filtra,
        wybrana_wartosc_filtra
    )


def aktualizuj_filtr2(event=None):
    aktualizuj_filtr(
        wybrany_filtr2,
        lista_wartosci_filtra2,
        wybrana_wartosc_filtra2
    )


lista_filtrow.bind(
    "<<ComboboxSelected>>",
    aktualizuj_filtr1
)

lista_filtrow2.bind(
    "<<ComboboxSelected>>",
    aktualizuj_filtr2
)

def pobierz_przefiltrowane_dane():

    df_filtr = df.copy()

    # ----------------
    # FILTR 1
    # ----------------

    filtr1 = wybrany_filtr.get()
    wartosc1 = wybrana_wartosc_filtra.get()

    if filtr1 != "Brak filtra" and filtr1 and wartosc1:

        dane_opisane1 = pobierz_dane_opisane(filtr1)

        maska1 = (
            dane_opisane1.astype(str)
            == str(wartosc1)
        )

        df_filtr = df_filtr[maska1]


    # ----------------
    # FILTR 2
    # ----------------

    filtr2 = wybrany_filtr2.get()
    wartosc2 = wybrana_wartosc_filtra2.get()

    if filtr2 != "Brak filtra" and filtr2 and wartosc2:

        mapa2 = pobierz_mape_etykiet(filtr2)

        dane2 = df_filtr[filtr2].copy()

        if mapa2:
            dane2 = dane2.map(mapa2).fillna(dane2)

        maska2 = (
            dane2.astype(str)
            == str(wartosc2)
        )

        df_filtr = df_filtr[maska2]

    return df_filtr.copy()
    # Pobieramy wersję z Label
    dane_opisane = pobierz_dane_opisane(filtr)

    # Porównujemy etykietę wybraną w GUI
    maska = dane_opisane.astype(str) == str(wartosc)

    return df[maska].copy()

def wyczysc_filtry():

    lista_filtrow.current(0)
    lista_filtrow2.current(0)

    wybrana_wartosc_filtra.set("")
    wybrana_wartosc_filtra2.set("")

    lista_wartosci_filtra["values"] = []
    lista_wartosci_filtra2["values"] = []

root.mainloop()