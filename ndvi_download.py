import earthaccess
import xarray as xr
import pandas as pd
import numpy as np
import os
import time
import sys
from pathlib import Path
from pyhdf.SD import SD, SDC

# ---------- 1. Parse location ----------
location = sys.argv[1]
match location:
    case "ane":
        box = (-60, -5, -50, 5)
    case "asw":
        box = (-75, -12, -65, -3)
    case "savanna":
        box = (-52, -18, -42, -8)
    case "amazon":
        box = (-75, -10, -50, 5)
    case _:
        raise ValueError(f"Unknown location: {location}")

# ---------- 2. Login ----------
try:
    earthaccess.login(strategy="netrc")
except Exception:
    earthaccess.login(strategy="interactive")

# ---------- 3. Search ----------
print(f"Searching MOD13A3 for {location}...")
results = earthaccess.search_data(
    short_name="MOD13A3",
    temporal=("2013-01", "2025-12"),
    bounding_box=box,
    # count removed — we want all monthly granules
)
print(f"Found {len(results)} granules")
if not results:
    sys.exit("No data found.")

# ---------- 4. Download (one by one, with retry) ----------
download_dir = f"./mod13a3_data/{location}"
os.makedirs(download_dir, exist_ok=True)
local_files = []

for i, granule in enumerate(results):
    try:
        max_retries = 3
        for attempt in range(max_retries):
            try:
                downloaded = earthaccess.download([granule], local_path=download_dir)
                if downloaded:
                    local_files.append(downloaded[0])
                    print(f"[{i+1}/{len(results)}] OK: {os.path.basename(downloaded[0])}")
                    break
            except Exception as e:
                print(f"    Attempt {attempt+1} failed: {e}")
                if attempt == max_retries - 1:
                    print("    Giving up.")
                else:
                    time.sleep(5 * (attempt + 1))
    except Exception as e:
        print(f"Error on granule {i}: {e}")

if not local_files:
    sys.exit("No files downloaded.")

# ---------- 5. Open & combine ----------
print("Opening files...")
from pyhdf.SD import SD, SDC

FILL = -3000
SCALE = 0.0001
records = []

for f in local_files:

    f = Path(f).as_posix()
    try:
        hdf = SD(f, SDC.READ)
    except Exception as e:
        print(f"Skipping {f}: {e}")
        continue


    # Read variables
    ndvi_raw = hdf.select("1 km monthly NDVI")[:].astype(np.float32)
    evi_raw  = hdf.select("1 km monthly EVI")[:].astype(np.float32)
    qa       = hdf.select("1 km monthly pixel reliability")[:]

    # Fill -> NaN, then scale
    ndvi = np.where(ndvi_raw == FILL, np.nan, ndvi_raw) * SCALE
    evi  = np.where(evi_raw  == FILL, np.nan, evi_raw)  * SCALE

    # Quality mask: keep 0 (good) and 1 (marginal)
    mask = (qa == 0) | (qa == 1)
    ndvi = np.where(mask, ndvi, np.nan)
    evi  = np.where(mask, evi,  np.nan)

    # Extract time from filename: MOD13A3.AYYYYDDD.hXXvYY...
    base = os.path.basename(f)
    yyyyddd = base.split(".")[1]  # A2013001
    year  = int(yyyyddd[1:5])
    doy   = int(yyyyddd[5:8])
    t = pd.Timestamp(year=year, month=1, day=1) + pd.Timedelta(days=doy - 1)

    records.append({
        "time": t,
        "ndvi": float(np.nanmean(ndvi)),
        "evi":  float(np.nanmean(evi)),
    })

    hdf.end()

df = pd.DataFrame(records).sort_values("time").reset_index(drop=True)
df.to_csv(f"evindvi_{location}.csv", index=False)
print(df.head())
print(f"Saved {len(df)} records to evindvi_{location}.csv")