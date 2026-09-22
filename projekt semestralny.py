import pandas as pd
from pathlib import Path

# Lokalizacja projektu
BASE_DIR = Path(__file__).resolve().parent

# Lokalizacja pliku CSV
file_path = BASE_DIR / "dane_syntetyczne_500_rekordow.csv"

# Wczytanie danych
df = pd.read_csv(
    file_path,
    sep=";",
    decimal=","
)

print("Dane zostały poprawnie wczytane!")

print("\nWymiary zbioru:")
print(df.shape)

print("\nPierwsze 5 rekordów:")
print(df.head())

print("\nInformacje o danych:")
df.info()