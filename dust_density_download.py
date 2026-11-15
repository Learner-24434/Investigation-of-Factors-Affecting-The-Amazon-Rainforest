import earthaccess
import xarray as xr
import pandas as pd
import numpy as np
import os
import time
from requests.exceptions import RequestException
import sys

# 1. Login (it is recommended to use netrc or interactive mode)

location = sys.argv[1]

if location == "amazon":
    box = (-75, -10, -50, 5)
elif location == "atlantic":
    box = (-45, 0, -25, 20)
else:
    exit()

try:
    earthaccess.login(strategy="netrc")
except Exception:
    earthaccess.login(strategy="interactive")

# 2. Search for data
print("Searching for MERRA-2 monthly aerosol data...")
results = earthaccess.search_data(
    short_name="M2TMNXAER",
    temporal=("2013-01", "2025-12"),
    bounding_box=box,  # Adjust to your target area as needed
)

if not results:
    print("No data found. Please check your search criteria.")
    exit()

# 3. Download files one by one to local storage (with retry)
local_files = []
download_dir = f"./merra2_data/{location}"
os.makedirs(download_dir, exist_ok=True)

for i, granule in enumerate(results):
    # Get the direct download link for the file
    # earthaccess results usually contain data_links(), we take the first https link
    try:
        urls = granule.data_links()
        if not urls:
            continue
        url = urls[0]  # Usually the .nc4 file link
        filename = os.path.join(download_dir, os.path.basename(url))
        
        # If the file already exists locally and is not empty, skip it
        if os.path.exists(filename) and os.path.getsize(filename) > 0:
            print(f"[{i+1}] Already exists: {filename}")
            local_files.append(filename)
            continue

        print(f"[{i+1}] Downloading: {url}")
        
        # Key point: download using earthaccess.download with built-in retry
        # earthaccess.download supports retries and can download to a specified directory
        # To avoid 502 errors, we call it individually here and add a manual delay
        max_retries = 3
        for attempt in range(max_retries):
            try:
                # Only download one file at a time
                downloaded = earthaccess.download([granule], local_path=download_dir)
                if downloaded:
                    local_files.append(downloaded[0])
                    print(f"    Success: {downloaded[0]}")
                    break
            except Exception as e:
                print(f"    Attempt {attempt+1} failed: {e}")
                if attempt == max_retries - 1:
                    print(f"    Giving up on this file.")
                else:
                    time.sleep(5 * (attempt + 1))  # Wait longer each time
                    
    except Exception as e:
        print(f"Error processing granule {i}: {e}")

if not local_files:
    print("No files were downloaded successfully.")
    exit()

# 4. Read local files and merge them
print("Opening local files...")
ds = xr.open_mfdataset(local_files, combine='by_coords')

# 5. Extract DUCMASS and calculate area average
# Note: DUCMASS is the dust column mass density, with units kg m^-2
dust_mass_ts = ds["DUCMASS"].mean(dim=["lat", "lon"], skipna=True)

# 6. Convert to DataFrame and save
df = dust_mass_ts.to_dataframe(name="massdensity").reset_index()
df = df[["time", "massdensity"]]
# Ensure time is in a readable format
df['time'] = pd.to_datetime(df['time'])
df.to_csv(f"dust_column_mass_density_{location}.csv", index=False)

print(df.head())
print(f"Saved {len(df)} records to dust_column_mass_density.csv")