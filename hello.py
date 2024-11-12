import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np

# Fájl beolvasása
file_path = '/Users/kadzoli/projects/test/stadat-lak0013-18.1.1.13-hu.xlsx'  # Ide az elérési útvonalat írd be ahol a táblázat van
data = pd.read_excel(file_path, skiprows=2)

# Oszlopok átnevezése
years = [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023]
data.columns = ['Típus'] + years

# Csak a releváns sorok megtartása
data_filtered = data.dropna(subset=years, how='all')

# Lineáris regresszió a "tiszta árváltozás" adatokra
tiszta_arvaltozas = data_filtered[data_filtered['Típus'] == 'tiszta árváltozás'].iloc[0, 1:].values
X = np.array(years).reshape(-1, 1)
y = tiszta_arvaltozas

# Regresszió modell
model = LinearRegression()
model.fit(X, y)

# Két diagram együttes megjelenítése
fig, axs = plt.subplots(1, 2, figsize=(16, 6))  # 1 sor, 2 oszlop elrendezés

# Vonaldiagram
for típus in data_filtered['Típus'].unique():
    axs[0].plot(years, data_filtered[data_filtered['Típus'] == típus].iloc[0, 1:], label=típus)
axs[0].set_xlabel('Év')
axs[0].set_ylabel('Árindex')
axs[0].set_title('Lakáspiaci árindexek időbeli változása')
axs[0].legend()
axs[0].grid(visible=True, linestyle='--', alpha=0.5)

# Lineáris regresszió diagram
axs[1].scatter(X, y, color='blue', label='Eredeti adatok')
axs[1].plot(X, model.predict(X), color='red', label='Lineáris regresszió')
axs[1].set_xlabel('Év')
axs[1].set_ylabel('Tiszta árváltozás index')
axs[1].set_title('Lineáris regresszió: Tiszta árváltozás index')
axs[1].legend()
axs[1].grid(visible=True, linestyle='--', alpha=0.5)

plt.tight_layout()
plt.show()