
import sys
import os
import subprocess
import pandas as pd

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QComboBox, QPushButton, QTableWidget, QTableWidgetItem,
    QLabel, QSlider, QGroupBox, QMessageBox
)

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


# =========================
# PLIKI
# =========================

KATALOG = os.path.dirname(os.path.abspath(__file__))
SCIEZKA_PLIKU = os.path.join(KATALOG, "dane_50_fikcyjnych_pacjentow.xlsx")
SCIEZKA_WYNIKI = os.path.join(KATALOG, "wyniki_gui.xlsx")


# =========================
# DANE
# =========================

dane = pd.read_excel(SCIEZKA_PLIKU)

for kolumna in ["BMI", "Temperatura (°C)", "Wiek"]:
    dane[kolumna] = pd.to_numeric(dane[kolumna], errors="coerce")

dane["Grupa wiekowa"] = pd.cut(
    dane["Wiek"],
    bins=[0, 18, 40, 60, 80, 120],
    labels=["0-18", "19-40", "41-60", "61-80", "81+"],
    include_lowest=True
)

goraczka = dane[
    dane["Gorączka"].astype(str).str.strip().str.lower() == "tak"
].copy()

goraczka["Czy brał(a) leki"] = (
    goraczka["Czy brał(a) leki"]
    .astype(str)
    .str.strip()
    .str.lower()
    .map({"tak": "Tak", "nie": "Nie"})
)


# =========================
# OKNO
# =========================

class Okno(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("System analizy pacjentów z gorączką")
        self.resize(1400, 900)

        layout = QVBoxLayout(self)

        # Tytuł
        tytul = QLabel("ANALIZA PACJENTÓW Z GORĄCZKĄ")
        tytul.setStyleSheet(
            "font-size:24px; font-weight:bold; padding:10px;"
        )
        layout.addWidget(tytul)

        # =====================
        # FILTRY
        # =====================

        grupa = QGroupBox("Filtry")
        filtry = QVBoxLayout(grupa)

        # Filtr leków
        wiersz = QHBoxLayout()
        wiersz.addWidget(QLabel("Leki:"))

        self.filtr = QComboBox()
        self.filtr.addItems([
            "Wszyscy z gorączką",
            "Tylko biorący leki",
            "Tylko niebiorący leków"
        ])

        leki = goraczka.loc[
            goraczka["Czy brał(a) leki"] == "Tak",
            "Jakie leki"
        ].dropna().unique()

        self.filtr.addItems(map(str, leki))
        wiersz.addWidget(self.filtr)
        filtry.addLayout(wiersz)

        # Suwaki
        self.label_wiek, self.suwak_wiek_min, self.suwak_wiek_max = \
            self.dodaj_suwaki(filtry, "Wiek", 0, 100, 0, 100)

        self.label_bmi, self.suwak_bmi_min, self.suwak_bmi_max = \
            self.dodaj_suwaki(filtry, "BMI", 150, 400, 150, 400)

        self.label_temp, self.suwak_temp_min, self.suwak_temp_max = \
            self.dodaj_suwaki(filtry, "Temperatura", 360, 420, 360, 420)

        # Przyciski
        przyciski = QHBoxLayout()

        self.przycisk = QPushButton("🔎 Pokaż dane")
        self.przycisk.clicked.connect(self.aktualizuj)

        self.przycisk_excel = QPushButton("📊 Zapisz wyniki do Excel")
        self.przycisk_excel.clicked.connect(self.eksport_do_excel)

        przyciski.addWidget(self.przycisk)
        przyciski.addWidget(self.przycisk_excel)
        filtry.addLayout(przyciski)

        layout.addWidget(grupa)

        # Liczba pacjentów
        self.informacja = QLabel("Znaleziono pacjentów: 0")
        self.informacja.setStyleSheet(
            "font-size:16px; font-weight:bold; padding:5px;"
        )
        layout.addWidget(self.informacja)

        # =====================
        # WYKRES
        # =====================

        self.figure = Figure(figsize=(10, 5))
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        # =====================
        # TABELA
        # =====================

        self.kolumny = [
            "Imię (dane fikcyjne)",
            "Płeć",
            "Wiek",
            "Temperatura (°C)",
            "Czy brał(a) leki",
            "Jakie leki",
            "Ciśnienie (mmHg)",
            "BMI"
        ]

        self.tabela = QTableWidget()
        self.tabela.setColumnCount(len(self.kolumny))
        self.tabela.setHorizontalHeaderLabels([
            "Imię", "Płeć", "Wiek", "Temperatura",
            "Leki", "Jakie leki", "Ciśnienie", "BMI"
        ])

        layout.addWidget(self.tabela)

        self.aktualizuj()

    # =========================
    # TWORZENIE SUWAKA
    # =========================

    def dodaj_suwaki(self, layout, nazwa, minimum, maksimum,
                     wartosc_min, wartosc_max):

        label = QLabel()
        suwak_min = QSlider(Qt.Orientation.Horizontal)
        suwak_max = QSlider(Qt.Orientation.Horizontal)

        for suwak, wartosc in [
            (suwak_min, wartosc_min),
            (suwak_max, wartosc_max)
        ]:
            suwak.setRange(minimum, maksimum)
            suwak.setValue(wartosc)
            suwak.valueChanged.connect(self.zmien_etykiete)

        layout.addWidget(label)
        layout.addWidget(suwak_min)
        layout.addWidget(suwak_max)

        return label, suwak_min, suwak_max

    # =========================
    # ETYKIETY SUWAKÓW
    # =========================

    def zmien_etykiete(self):

        self.label_wiek.setText(
            f"Wiek: {self.suwak_wiek_min.value()} - "
            f"{self.suwak_wiek_max.value()} lat"
        )

        self.label_bmi.setText(
            f"BMI: {self.suwak_bmi_min.value()/10:.1f} - "
            f"{self.suwak_bmi_max.value()/10:.1f}"
        )

        self.label_temp.setText(
            f"Temperatura: {self.suwak_temp_min.value()/10:.1f} - "
            f"{self.suwak_temp_max.value()/10:.1f} °C"
        )

    # =========================
    # FILTROWANIE
    # =========================

    def pobierz_przefiltrowane_dane(self):

        wybor = self.filtr.currentText()
        df = goraczka.copy()

        if wybor == "Tylko biorący leki":
            df = df[df["Czy brał(a) leki"] == "Tak"]

        elif wybor == "Tylko niebiorący leków":
            df = df[df["Czy brał(a) leki"] == "Nie"]

        elif wybor != "Wszyscy z gorączką":
            df = df[
                df["Jakie leki"].astype(str).str.contains(
                    wybor, case=False, na=False
                )
            ]

        wiek_min, wiek_max = sorted([
            self.suwak_wiek_min.value(),
            self.suwak_wiek_max.value()
        ])

        bmi_min, bmi_max = sorted([
            self.suwak_bmi_min.value() / 10,
            self.suwak_bmi_max.value() / 10
        ])

        temp_min, temp_max = sorted([
            self.suwak_temp_min.value() / 10,
            self.suwak_temp_max.value() / 10
        ])

        df = df[
            df["Wiek"].between(wiek_min, wiek_max) &
            df["BMI"].between(bmi_min, bmi_max) &
            df["Temperatura (°C)"].between(temp_min, temp_max)
        ]

        return df

    # =========================
    # AKTUALIZACJA GUI
    # =========================

    def aktualizuj(self):

        df = self.pobierz_przefiltrowane_dane()

        self.zmien_etykiete()

        self.informacja.setText(
            f"Znaleziono pacjentów: {len(df)} / {len(goraczka)}"
        )

        # Tabela
        self.tabela.setRowCount(len(df))

        for wiersz, (_, pacjent) in enumerate(df.iterrows()):

            for kolumna, nazwa in enumerate(self.kolumny):

                wartosc = pacjent[nazwa]

                if pd.isna(wartosc):
                    wartosc = ""

                self.tabela.setItem(
                    wiersz,
                    kolumna,
                    QTableWidgetItem(str(wartosc))
                )

        # Wykres
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        if not df.empty:

            wynik = pd.crosstab(
                [df["Grupa wiekowa"], df["Płeć"]],
                df["Czy brał(a) leki"]
            )

            wynik.plot(kind="bar", ax=ax)

            ax.set_title(
                "Pacjenci z gorączką według wieku,\n"
                "płci i przyjmowania leków"
            )
            ax.set_xlabel("Grupa wiekowa i płeć")
            ax.set_ylabel("Liczba pacjentów")
            ax.tick_params(axis="x", rotation=45)
            ax.legend(title="Czy brał(a) leki")

            for kontener in ax.containers:
                ax.bar_label(kontener, fmt="%d", padding=3)

        else:
            ax.text(
                0.5, 0.5,
                "Brak pacjentów spełniających kryteria",
                ha="center",
                va="center",
                fontsize=14
            )
            ax.set_axis_off()

        self.figure.tight_layout()
        self.canvas.draw()

    # =========================
    # EKSPORT DO EXCELA
    # =========================

    def eksport_do_excel(self):

        df = self.pobierz_przefiltrowane_dane().copy()

        try:

            with pd.ExcelWriter(
                SCIEZKA_WYNIKI,
                engine="openpyxl"
            ) as writer:

                dane.to_excel(
                    writer,
                    sheet_name="Dane źródłowe",
                    index=False
                )

                df.to_excel(
                    writer,
                    sheet_name="Plik GUI",
                    index=False
                )

            # Otwórz plik
            if sys.platform.startswith("win"):
                os.startfile(SCIEZKA_WYNIKI)

            elif sys.platform == "darwin":
                subprocess.Popen(["open", SCIEZKA_WYNIKI])

            else:
                subprocess.Popen(["xdg-open", SCIEZKA_WYNIKI])

            QMessageBox.information(
                self,
                "Zapisano",
                f"Utworzono plik:\n"
                f"wyniki_gui.xlsx\n\n"
                f"Zakładki:\n"
                f"1. Dane źródłowe\n"
                f"2. Plik GUI\n\n"
                f"Dane źródłowe: {len(dane)} pacjentów\n"
                f"Po filtrach GUI: {len(df)} pacjentów"
            )

        except PermissionError:

            QMessageBox.warning(
                self,
                "Błąd zapisu",
                "Nie można zapisać pliku.\n\n"
                "Plik 'wyniki_gui.xlsx' jest prawdopodobnie "
                "otwarty w Excelu.\n\n"
                "Zamknij go i spróbuj ponownie."
            )

        except Exception as e:

            QMessageBox.critical(
                self,
                "Błąd",
                f"Wystąpił problem podczas tworzenia "
                f"pliku Excel:\n\n{e}"
            )


# =========================
# START PROGRAMU
# =========================

app = QApplication(sys.argv)
okno = Okno()
okno.show()
sys.exit(app.exec())
