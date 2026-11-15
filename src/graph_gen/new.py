import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import stats

VARIABLE = ["ndvi", "evi"]
AREAS = ["NE", "savanna", "amazon", "SW"]

def plot(series, color, title, ylab, fname, label):
    fig, ax = plt.subplots(figsize=(11, 5))
    ax.plot(series.index, series, color=color, alpha=.35, lw=1, label="Monthly")
    ax.plot(series.index, series.rolling(12, center=True).mean(), color=color, lw=2.5, label=label)
    ax.set_title(title, fontsize=13, weight="bold")
    ax.set_xlabel("Time"); ax.set_ylabel(ylab)
    ax.set_xlim(pd.Timestamp("2013-01-01"), pd.Timestamp("2025-12-31"))
    ax.grid(alpha=.3); ax.legend(frameon=False)
    fig.tight_layout(); fig.savefig(os.path.join(OUTDIR, fname), dpi=160); plt.close(fig)

def regression_plot(x_dates, y, x_label="Year", y_label="Dust speed", filename="Sahara_Dust_speed_Regression.png"):
    x = np.asarray(x_dates.year + (x_dates.dayofyear - 1) / 365.25, dtype=float)
    y = np.asarray(y, dtype=float)

    r = stats.linregress(x, y)
    xs = np.linspace(x.min(), x.max(), len(x))

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.scatter(x, y, s=22, alpha=.65, color="#1f77b4", label=f"Data (n = {len(x)})")
    ax.plot(xs, r.intercept + r.slope * xs, color="crimson", lw=2.2,
            label=f"y = {r.slope:.3g}x + {r.intercept:.3g}\n"
                f"R² = {r.rvalue**2:.3f}\n"
                f"p = {r.pvalue:.3g}")
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_title(f"{y_label} vs {x_label}")
    ax.grid(alpha=.3)
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(f"../../graphs/{filename}", dpi=200)
    plt.close(fig)

    return r.pvalue


for var in VARIABLE:
    for area in AREAS:
        CSV = fr"../../data/Amazon/ndvi_evi_{area}.csv"
        OUTDIR = os.path.dirname(CSV)

        d = pd.read_csv(CSV)
        d["date"] = pd.to_datetime(d["date"], format="%Y-%m-%d")
        d = d[(d.date >= "2013-01-01") & (d.date <= "2025-12-31")]

        x = d.set_index("date")[var].dropna()

        plot(x, "#7b3fa0", f"{var.upper()} in Amazon",
            var.upper(), f"{area}_{var.upper()}.png", "12-month mean")

        print(area, var, regression_plot(x.index, x, y_label=var.upper(), filename = f"{area}_{var.upper()}.png"))
