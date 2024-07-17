#!/usr/bin/env python3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load data from CSV
df = pd.read_csv('bitcoin_forecast.csv')

# Calculate Min and Max values based on the percentage
df['Min value'] = df['Average'] * (1 - df['Percentage'] / 100)
df['Max value'] = df['Average'] * (1 + df['Percentage'] / 100)

# Plotting
years = np.array(df["Year"], dtype=float)
average = np.array(df["Average"], dtype=float)
min_value = np.array(df["Min value"], dtype=float)
max_value = np.array(df["Max value"], dtype=float)

plt.figure(figsize=(12, 6))
plt.plot(years, average, label='Average', color='blue', linewidth=2)
plt.fill_between(years, min_value, max_value, color='orange', alpha=0.3, label='Cone of Uncertainty')
plt.xlabel('Year')
plt.ylabel('Bitcoin Value (SEK)')
plt.title('''Bitcoin Potential Development with Cone of Uncertainty
            Potential future value of 800 000 Satoshis (0.008 BTC)''')
plt.legend()
plt.grid(True)
plt.show()
