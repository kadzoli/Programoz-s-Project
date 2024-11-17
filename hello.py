import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np
import tkinter as tk
from tkinter import messagebox

# File Paths
file_path_lakasar = 'eves_lakasar_valtozas_2010_2023.xlsx'
file_path_atlagkereset = 'magyar_atlagkereset_2010_2023.xlsx'
file_path_atlagos_lakasar = 'atlagos_lakasar_2010_2023.xlsx'

# Load Data from Excel files
data_lakasar = pd.read_excel(file_path_lakasar)
data_lakasar.columns = ['Év', 'Lakásár Index']
data_lakasar_filtered = data_lakasar.dropna()

data_atlagkereset = pd.read_excel(file_path_atlagkereset)
data_atlagkereset.columns = ['Év', 'Bruttó Átlagkereset']
data_atlagkereset_filtered = data_atlagkereset.dropna()

data_atlagos_lakasar = pd.read_excel(file_path_atlagos_lakasar)
data_atlagos_lakasar.columns = ['Év', 'Átlagos négyzetméterár (Ft/m²)', 'Átlagos lakásméret (m²)', 'Átlagos lakásár (Ft)']
data_atlagos_lakasar_filtered = data_atlagos_lakasar.dropna()

# Calculate Nettó Átlagkereset
data_atlagkereset_filtered['Nettó Átlagkereset'] = data_atlagkereset_filtered['Bruttó Átlagkereset'] * (1 - 0.15 - 0.185)

# Calculate Havi Átlagkereset Arány using Nettó Átlagkereset
data_combined = pd.merge(data_atlagkereset_filtered, data_atlagos_lakasar_filtered, on='Év')
data_combined['Havi Átlagkereset Arány'] = data_combined['Átlagos lakásár (Ft)'] / data_combined['Nettó Átlagkereset']

# Calculate Percentage Change from the First Year
lakasar_base = data_lakasar_filtered['Lakásár Index'].iloc[0]
atlagkereset_base = data_atlagkereset_filtered['Bruttó Átlagkereset'].iloc[0]

data_lakasar_filtered['Lakásár Index Növekedés (%)'] = (
    (data_lakasar_filtered['Lakásár Index'] / lakasar_base - 1) * 100
)
data_atlagkereset_filtered['Átlagkereset Növekedés (%)'] = (
    (data_atlagkereset_filtered['Bruttó Átlagkereset'] / atlagkereset_base - 1) * 100
)

# Linear Regression for Lakásár
X_lakasar = data_lakasar_filtered['Év'].values.reshape(-1, 1)
y_lakasar = data_lakasar_filtered['Lakásár Index'].values
model_lakasar = LinearRegression()
model_lakasar.fit(X_lakasar, y_lakasar)

# Linear Regression for Átlagkereset
X_atlagkereset = data_atlagkereset_filtered['Év'].values.reshape(-1, 1)
y_atlagkereset = data_atlagkereset_filtered['Bruttó Átlagkereset'].values
model_atlagkereset = LinearRegression()
model_atlagkereset.fit(X_atlagkereset, y_atlagkereset)

# Define Plot Functions
def show_lakasar_scatter():
    """Show scatter plot of housing market index."""
    plt.figure(figsize=(10, 6))
    plt.plot(data_lakasar_filtered['Év'], data_lakasar_filtered['Lakásár Index'], label='Lakásár Index', marker='o')
    for x, y in zip(data_lakasar_filtered['Év'], data_lakasar_filtered['Lakásár Index']):
        plt.text(x, y, f'{y:.2f}', ha='center', va='bottom', fontsize=8)
    plt.xlabel('Év')
    plt.ylabel('Lakásár Index')
    plt.title('Lakáspiaci árindexek időbeli változása')
    plt.xticks(data_lakasar_filtered['Év'])  # Show all years
    plt.legend()
    plt.grid(visible=True, linestyle='--', alpha=0.5)
    plt.show()

def show_lakasar_regression():
    """Show regression plot for housing market index."""
    plt.figure(figsize=(10, 6))
    plt.scatter(X_lakasar, y_lakasar, color='blue', label='Eredeti adatok')
    plt.plot(X_lakasar, model_lakasar.predict(X_lakasar), color='red', label='Lineáris regresszió')
    plt.xlabel('Év')
    plt.ylabel('Lakásár Index')
    plt.title('Lineáris regresszió: Lakásár Index')
    plt.xticks(data_lakasar_filtered['Év'])  # Show all years
    plt.legend()
    plt.grid(visible=True, linestyle='--', alpha=0.5)
    plt.show()

def show_atlagkereset_scatter():
    """Show scatter plot of average income."""
    plt.figure(figsize=(10, 6))
    plt.plot(data_atlagkereset_filtered['Év'], data_atlagkereset_filtered['Bruttó Átlagkereset'], label='Bruttó Átlagkereset', marker='o')
    for x, y in zip(data_atlagkereset_filtered['Év'], data_atlagkereset_filtered['Bruttó Átlagkereset']):
        plt.text(x, y, f'{y:.2f}', ha='center', va='bottom', fontsize=8)
    plt.xlabel('Év')
    plt.ylabel('Bruttó Átlagkereset')
    plt.title('Átlagkeresetek időbeli változása')
    plt.xticks(data_atlagkereset_filtered['Év'])  # Show all years
    plt.legend()
    plt.grid(visible=True, linestyle='--', alpha=0.5)
    plt.show()

def show_atlagkereset_regression():
    """Show regression plot for average income."""
    plt.figure(figsize=(10, 6))
    plt.scatter(X_atlagkereset, y_atlagkereset, color='blue', label='Eredeti adatok')
    plt.plot(X_atlagkereset, model_atlagkereset.predict(X_atlagkereset), color='red', label='Lineáris regresszió')
    plt.xlabel('Év')
    plt.ylabel('Bruttó Átlagkereset')
    plt.title('Lineáris regresszió: Átlagkereset')
    plt.xticks(data_atlagkereset_filtered['Év'])  # Show all years
    plt.legend()
    plt.grid(visible=True, linestyle='--', alpha=0.5)
    plt.show()

def show_comparison():
    """Show bar plot of Havi Átlagkereset Arány using Nettó Átlagkereset."""
    plt.figure(figsize=(12, 6))
    plt.bar(data_combined['Év'], data_combined['Havi Átlagkereset Arány'], color='green')
    for x, y in zip(data_combined['Év'], data_combined['Havi Átlagkereset Arány']):
        plt.text(x, y, f'{y:.2f}', ha='center', va='bottom', fontsize=8)
    plt.xlabel('Év')
    plt.ylabel('Havi Átlagkereset Arány')
    plt.title('Hány Havi Nettó Átlagkereset Kell Egy Átlagos Lakás Megvásárlásához')
    plt.xticks(data_combined['Év'])  # Show all years
    plt.grid(visible=True, linestyle='--', alpha=0.5)
    plt.show()

def show_analysis():
    """Show analysis of trends and future expectations."""
    analysis_text = (
       "Elemzés:\n"
        "Az elemzés alapján látható, hogy az elmúlt évtizedben az átlagos lakásár és a nettó átlagkereset közötti arány "
        "jelentős változásokon ment keresztül. 2010-ben még körülbelül 121 havi nettó átlagkeresetre volt szükség egy "
        "átlagos lakás megvásárlásához. Az arány 2013-ra fokozatosan csökkent, ami azt mutatta, hogy a lakhatás relatíve "
        "megfizethetőbbé vált. Ez azonban nem tartott sokáig.\n\n"
        "2016-tól kezdve újra emelkedni kezdett az arány, és 2020-ra megközelítette a korábbi csúcsokat, elérve a 117 havi "
        "nettó keresetet. Az ezt követő években az arány viszonylag stabil maradt, de továbbra is magas szinten, 115-117 "
        "hónap között mozgott. Csak 2023-ban láthatunk némi enyhülést, amikor az arány 98 hónapra csökkent.\n\n"
        "Fontos megjegyezni, hogy ezek az adatok országos átlagokat tükröznek. Egyes régiókban, például Budapesten vagy más "
        "nagyobb városokban, a lakásárak és a vásárlóerő közötti különbségek sokkal jelentősebbek lehetnek. Ez azt jelenti, "
        "hogy a fővárosban akár több hónappal több nettó keresetre is szükség lehet egy átlagos lakás megvásárlásához, mint "
        "vidéken. Az ingatlanpiac regionális különbségei tehát nagyban befolyásolják a lakhatás megfizethetőségét.\n\n"
        "Ez az adat arra utal, hogy az elmúlt években a lakásárak növekedése és a bérek emelkedése közötti különbség komoly "
        "terhet rótt a lakásvásárlókra. Bár a bérek is növekedtek, a lakásárak gyorsabb ütemben emelkedtek, ami megnehezítette "
        "a lakásvásárlást. Az ingatlanpiac stabilizációja és a lakhatás megfizethetőségének javulása továbbra is kulcsfontosságú "
        "marad, különösen, ha a gazdasági környezet és az inflációs nyomás tovább változik."
    )
    messagebox.showinfo("Elemzés", analysis_text)

# Tkinter GUI Setup
root = tk.Tk()
root.title("Interactive Graph Viewer")

# Scatter Plot Buttons
lakasar_button = tk.Button(root, text="Lakásár Vonaldiagram", command=show_lakasar_scatter)
lakasar_button.pack(pady=5)

lakasar_regression_button = tk.Button(root, text="Lakásár Regresszió", command=show_lakasar_regression)
lakasar_regression_button.pack(pady=5)

atlagkereset_button = tk.Button(root, text="Átlagkereset Vonaldiagram", command=show_atlagkereset_scatter)
atlagkereset_button.pack(pady=5)

atlagkereset_regression_button = tk.Button(root, text="Átlagkereset Regresszió", command=show_atlagkereset_regression)
atlagkereset_regression_button.pack(pady=5)

# Comparison and Analysis Buttons
comparison_button = tk.Button(root, text="Vásárlóerő változásai", command=show_comparison)
comparison_button.pack(pady=5)

analysis_button = tk.Button(root, text="Elemzés", command=show_analysis)
analysis_button.pack(pady=5)

# Exit Button
exit_button = tk.Button(root, text="Kilépés", command=root.quit)
exit_button.pack(pady=5)

# Run Tkinter Event Loop
root.mainloop()