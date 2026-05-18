import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# -------------------------
# Download historical data
# -------------------------

start_date = "2016-01-01"
end_date = "2026-01-01"

tickers = ["^GSPC", "^VIX"]  # S&P 500 index and VIX index

data = yf.download(tickers, start=start_date, end=end_date, auto_adjust=False)["Close"]

# Rename columns for clarity
data = data.rename(columns={
    "^GSPC": "SP500",
    "^VIX": "VIX"})

# Remove missing values
data = data.dropna()

# ---------------------------------
# Construct downside equity stress
# ---------------------------------

# Daily log-return of the S&P 500
data["SP500_return"] = np.log(data["SP500"]) - np.log(data["SP500"].shift(1))

# Downside stress: positive only when the S&P 500 falls
data["Downside_stress"] = np.maximum(-data["SP500_return"], 0)

# Remove the first row, since return is undefined there
data = data.dropna()

# ------------------------------------
# Plot VIX and downside equity stress
# ------------------------------------

fig, ax1 = plt.subplots(figsize=(12, 6))

# Plot VIX
ax1.plot(
    data.index,
    data["VIX"],
    label="VIX",
    linewidth=1.5)

ax1.set_xlabel("Date", fontsize=13)
ax1.set_ylabel("VIX", fontsize=13)
ax1.tick_params(axis="both", labelsize=11)

# Create a second y-axis for downside stress
ax2 = ax1.twinx()

ax2.bar(
    data.index,
    data["Downside_stress"],
    label="Downside S&P 500 stress",
    alpha=0.3,
    width=1.0)

ax2.set_ylabel("Downside S&P 500 stress", fontsize=13)
ax2.tick_params(axis="y", labelsize=11)

# Title
plt.title("VIX and Downside S&P 500 Stress", fontsize=15)

# Combine legends from both axes
lines_1, labels_1 = ax1.get_legend_handles_labels()
lines_2, labels_2 = ax2.get_legend_handles_labels()

ax1.legend(
    lines_1 + lines_2,
    labels_1 + labels_2,
    loc="upper left",
    fontsize=11)

plt.tight_layout()
plt.show()