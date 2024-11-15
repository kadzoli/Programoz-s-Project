import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np
import tkinter as tk
from tkinter import messagebox

# File Path
file_path = r"C:\Users\judit\Desktop\GDE\Programozás\project\stadat-lak0013-18.1.1.13-hu.xlsx"  # Modify this to your file path
data = pd.read_excel(file_path, skiprows=2)

# Rename Columns
years = [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023]
data.columns = ['Típus'] + years

# Filter Rows
data_filtered = data.dropna(subset=years, how='all')

# Linear Regression Data for "tiszta árváltozás"
tiszta_arvaltozas = data_filtered[data_filtered['Típus'] == 'tiszta árváltozás'].iloc[0, 1:].values
X = np.array(years).reshape(-1, 1)
y = tiszta_arvaltozas

# Regression Model
model = LinearRegression()
model.fit(X, y)

# Define Plot Functions
def show_scatter():
    """Show scatter plot of all housing market types."""
    plt.figure(figsize=(10, 6))
    for típus in data_filtered['Típus'].unique():
        plt.plot(years, data_filtered[data_filtered['Típus'] == típus].iloc[0, 1:], label=típus)
    plt.xlabel('Év')
    plt.ylabel('Árindex')
    plt.title('Lakáspiaci árindexek időbeli változása')
    plt.legend()
    plt.grid(visible=True, linestyle='--', alpha=0.5)
    plt.show()

def show_regression():
    """Show regression plot for 'tiszta árváltozás'."""
    plt.figure(figsize=(10, 6))
    plt.scatter(X, y, color='blue', label='Eredeti adatok')
    plt.plot(X, model.predict(X), color='red', label='Lineáris regresszió')
    plt.xlabel('Év')
    plt.ylabel('Tiszta árváltozás index')
    plt.title('Lineáris regresszió: Tiszta árváltozás index')
    plt.legend()
    plt.grid(visible=True, linestyle='--', alpha=0.5)
    plt.show()

# Tkinter GUI Setup
root = tk.Tk()
root.title("Interactive Graph Viewer")

# Scatter Plot Button
scatter_button = tk.Button(root, text="Vonaldiagram", command=show_scatter)
scatter_button.pack(pady=5)

# Regression Plot Button
regression_button = tk.Button(root, text="Lineáris Regresszió", command=show_regression)
regression_button.pack(pady=5)

# Exit Button
exit_button = tk.Button(root, text="Kilépés", command=root.quit)
exit_button.pack(pady=5)

# Run Tkinter Event Loop
root.mainloop()
