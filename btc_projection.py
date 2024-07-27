import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import seaborn as sns
import requests
from tkinter import Tk, Frame, Button, Label, Entry
from tkinter.messagebox import showerror
from datetime import datetime
import signal
import sys
import mplcyberpunk

# Initial investment in BTC
initial_investment_btc = 0.08

# Default trajectories (percentage)
DEFAULT_ARR_BEAR = 0.21
DEFAULT_ARR_BASE = 0.29
DEFAULT_ARR_BULL = 0.37

def fetch_current_btc_price():
    url = "https://api.coindesk.com/v1/bpi/currentprice/USD.json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['bpi']['USD']['rate_float']
    else:
        raise ValueError("Failed to fetch BTC data")

class BTCProjectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("BTC Projection")

        # Handle Ctrl+C
        signal.signal(signal.SIGINT, self.exit_gracefully)

        # Setup UI
        self.frame = Frame(root)
        self.frame.pack(padx=10, pady=10)

        self.label_bear = Label(self.frame, text="Bear Case (%/year):")
        self.label_bear.pack()
        self.entry_bear = Entry(self.frame)
        self.entry_bear.insert(0, str(DEFAULT_ARR_BEAR * 100))
        self.entry_bear.pack()

        self.label_base = Label(self.frame, text="Base Case (%/year):")
        self.label_base.pack()
        self.entry_base = Entry(self.frame)
        self.entry_base.insert(0, str(DEFAULT_ARR_BASE * 100))
        self.entry_base.pack()

        self.label_bull = Label(self.frame, text="Bull Case (%/year):")
        self.label_bull.pack()
        self.entry_bull = Entry(self.frame)
        self.entry_bull.insert(0, str(DEFAULT_ARR_BULL * 100))
        self.entry_bull.pack()

        self.load_button = Button(self.frame, text="Fetch Data", command=self.load_data)
        self.load_button.pack(pady=5)

        self.plot_button = Button(self.frame, text="Plot Projections", command=self.plot_projections, state="disabled")
        self.plot_button.pack(pady=5)

        self.status_label = Label(self.frame, text="Fetch BTC data to start", fg="blue")
        self.status_label.pack(pady=5)

    def exit_gracefully(self, signum, frame):
        self.root.quit()
        sys.exit(0)

    def load_data(self):
        try:
            self.current_price = fetch_current_btc_price()
            self.status_label.config(text="Data successfully fetched", fg="green")
            self.plot_button.config(state="normal")
        except Exception as e:
            showerror("Error", f"Failed to fetch data: {e}")
            self.status_label.config(text="Failed to fetch data", fg="red")

    def plot_projections(self):
        try:
            arr_bear = float(self.entry_bear.get()) / 100
            arr_base = float(self.entry_base.get()) / 100
            arr_bull = float(self.entry_bull.get()) / 100
        except ValueError:
            showerror("Error", "Please enter valid percentages")
            return

        current_year = datetime.now().year
        years = np.arange(current_year, current_year + 22)
        base_case = [self.current_price * ((1 + arr_base) ** i) for i in range(22)]
        bear_case = [self.current_price * ((1 + arr_bear) ** i) for i in range(22)]
        bull_case = [self.current_price * ((1 + arr_bull) ** i) for i in range(22)]

        plt.style.use("cyberpunk")

        plt.figure(figsize=(12, 6))
        plt.plot(years, base_case, label='Base Case (29%/year)', color='#F7931A', linewidth=2)
        plt.fill_between(years, bear_case, bull_case, color='#A9DFBF', alpha=0.5, label='Cone of Uncertainty')

        # Add dots and annotations every four years
        for i in range(0, len(years), 4):
            plt.scatter(years[i], base_case[i], color='#F7931A', s=50)
            plt.text(years[i], base_case[i], f'{base_case[i]:,.0f} USD', fontsize=10, ha='center', color='#F7931A', verticalalignment='bottom')

        # Add a dot and annotation at the end of the data
        end_year = years[-1]
        end_value = base_case[-1]
        plt.scatter(end_year, end_value, color='#F7931A', s=40, label='Value every 4th year')
        plt.text(end_year, end_value, f'{end_value:,.0f} USD', fontsize=10, ha='center', color='#F7931A', verticalalignment='bottom')

        plt.xlabel('Year')

        satoshis = convert2satoshi(initial_investment_btc)
        satoshis_formatted = format_for_presentation(satoshis)
        plt.ylabel('Bitcoin Value (USD)')
        plt.title(f'''
                          Bitcoin in your organization
           Bitcoin has enormous potential to help your organization grow.
           Here is a possible development of just {satoshis_formatted} Satoshis ({initial_investment_btc} BTC)!''')

        # Function to add thousands separators
        def thousands_formatter(x, pos):
            return f'{int(x):,}'

        # Format y-axis with thousands separator
        plt.gca().yaxis.set_major_formatter(FuncFormatter(thousands_formatter))

        plt.legend()
        plt.grid(True, linestyle='--', alpha=0.7)
        mplcyberpunk.add_glow_effects()
        plt.show()

def convert2satoshi(btc):
    return int(btc * 100_000_000)

def format_for_presentation(satoshis):
    return f'{satoshis:,}'

if __name__ == "__main__":
    root = Tk()
    app = BTCProjectionApp(root)
    root.mainloop()
