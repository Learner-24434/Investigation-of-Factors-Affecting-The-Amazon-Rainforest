import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import sys

csv_path = sys.argv[1]  # e.g. "dust_column_mass_density.csv"
df = pd.read_csv(csv_path, parse_dates=["time"])

fig, ax = plt.subplots(figsize=(12, 5))

ax.plot(df["time"], df["massdensity"], label="Dust column mass density",
        color="#8D6E63", linewidth=1.5)

ax.set_xlabel("Time")
ax.set_ylabel("Mass density (kg m⁻²)")
ax.set_title("Dust Column Mass Density over Time")
ax.legend(loc="best")          # the "key"
ax.grid(True, alpha=0.3)

# Yearly ticks + readable date labels
ax.xaxis.set_major_locator(mdates.YearLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
fig.autofmt_xdate()

fig.tight_layout()
fig.savefig("dust_mass_density.png", dpi=150)
plt.show()