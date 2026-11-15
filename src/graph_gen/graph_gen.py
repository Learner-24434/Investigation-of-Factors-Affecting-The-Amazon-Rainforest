import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import stats
import csv
import datetime as dt


"""
ratio/speed
ratio


"""

files = {
    "ratio" : "../data/dust_ratio.csv",
    "surface_velocity" : "../data/Sahara/speed_10.csv",
    "dust_density_sahara" : "../data/Sahara/dust_density.csv",
    "dust_density_atlantic" : "../data/Atlantic/dust_density.csv",
    "850hpa velocity" : "../data/Atlantic/speed_850hpa.csv",
    "NVDI_A" : "../data/Amazon/ndvi_evi_amazon.csv",
    "EVI_A" : "../data/Amazon/ndvi_evi_amazon.csv",
    "time" : "",
}


def regression_plot(x, y, x_label="x", y_label="y", filename="regression.png"):
    """Takes two sets of values, do a linear regression, save a PNG with the
    data, the fitted line and the p value. Returns the p value."""
    x = np.asarray(x, dtype=(int))
    y = np.asarray(y, dtype=(float))

    # linear regression
    r = stats.linregress(x, y)
    xs = np.linspace(x.min(), x.max(), 156)
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
    fig.savefig(filename, dpi=200)
    plt.close(fig)

    print(f"p value = {r.pvalue:.3g}")
    return r.pvalue


for var_x in files.keys():
    for var_y in files.keys():
        if var_x == var_y : continue

with open("../../data/dust_ratio.csv") as file:
    reader = csv.DictReader(file)
    x_var = []
    y_var = []
    for line in reader:

        try:
            y_var.append(float(line["total_dep_g_m2"])/float(line["emission_g_m2"]))
            x_var.append(int(line['date'].split("-")[0]))
        except:
            continue

regression_plot(x_var, y_var, "Time", "Ratio of Dust Deposition over Dust Emission", "ratio.png")