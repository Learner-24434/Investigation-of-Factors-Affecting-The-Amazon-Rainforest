import pandas as pd
import matplotlib.pyplot as plt
import sys

location = sys.argv[1]  # e.g. "asw"
df = pd.read_csv(f"evindvi_{location}.csv", parse_dates=["time"])

fig, ax = plt.subplots(figsize=(12, 5))

ax.plot(df["time"], df["ndvi"], label="NDVI", color="#2E7D32", linewidth=1.5)
ax.plot(df["time"], df["evi"],  label="EVI",  color="#F9A825", linewidth=1.5)

ax.set_xlabel("Time")
ax.set_ylabel("Index value")
ax.set_title(f"NDVI vs EVI — {location.upper()} (Amazon)")
ax.legend(loc="best")          # the "key"
ax.grid(True, alpha=0.3)

fig.autofmt_xdate()            # rotate date labels so they don't overlap
fig.tight_layout()
fig.savefig(f"ndvi_evi_{location}.png", dpi=150)
plt.show()