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

print("\n=== SPRAWDZAMY SŁOWNIK ===")

print("Nazwy kolumn:")
print(slownik.columns.tolist())

print("\nPierwsze 10 wierszy:")
print(slownik.head(10).to_string())

print("\n=== KONIEC TESTU ===")

print("\nNazwy kolumn w słowniku:")
print(slownik.columns.tolist())

print("\nPierwsze 10 wierszy:")
print(slownik.head(10).to_string())

print("Dane zostały poprawnie wczytane!")

print("\nWymiary zbioru:")
print(df.shape)

print("\nPierwsze 5 rekordów:")
print(df.head())

print("\nInformacje o danych:")
df.info()

print("\nSłownik zmiennych:")
print(slownik.shape)

print("\nPierwsze wiersze słownika:")
print(slownik.head())

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