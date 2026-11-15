import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def save_graph(location="Amazon", north_path=None, east_path=None):
    # Default to the location folder if custom paths aren't provided
    path_north = north_path or f"../data/{location}/north_vel_850hpa.csv"
    path_east  = east_path  or f"../data/Sahara/east_vel_850hpa.csv"
    
    # Ensure the output directory exists
    os.makedirs("../graphs", exist_ok=True)

    print(f"\n--- Processing: {location} ---")
    print(f"North file: {path_north}")
    print(f"East file:  {path_east}")

    # 1. Load Data
    df_n = pd.read_csv(path_north)
    df_e = pd.read_csv(path_east)

    # Normalize column names (lowercase, strip spaces)
    df_n.columns = df_n.columns.str.strip().str.lower()
    df_e.columns = df_e.columns.str.strip().str.lower()

    # 2. Parse Time and Merge
    df_n['time'] = pd.to_datetime(df_n['time'], errors='coerce')
    df_e['time'] = pd.to_datetime(df_e['time'], errors='coerce')
    
    # Drop rows where time failed to parse
    df_n = df_n.dropna(subset=['time'])
    df_e = df_e.dropna(subset=['time'])

    df = pd.merge(df_n[['time', 'v850']], df_e[['time', 'u850']], on="time", how="inner")
    print(f"Rows after merge: {len(df)}")

    if len(df) == 0:
        print("ERROR: Merge resulted in 0 rows. Time formats likely don't match.")
        return

    # 3. Force Numeric and Drop NaNs (The Critical Fix)
    df['v850'] = pd.to_numeric(df['v850'], errors='coerce')
    df['u850'] = pd.to_numeric(df['u850'], errors='coerce')
    df = df.dropna(subset=['v850', 'u850'])
    
    print(f"Rows after dropping NaNs: {len(df)}")
    if len(df) == 0:
        print("ERROR: All rows contained invalid/NaN velocity data.")
        return

    # 4. Calculate Wind Speed
    df['vel'] = np.sqrt(df['v850'] ** 2 + df['u850'] ** 2)
    print(f"Velocity stats: min={df['vel'].min():.2f}, max={df['vel'].max():.2f}")

    # 5. Create the Plot
    fig, ax = plt.subplots(figsize=(12, 6))
    
    ax.plot(df['time'], df['vel'], label='Wind Speed (m/s)', color='teal', linewidth=2)
    ax.scatter(df['time'], df['vel'], color='teal', s=15, zorder=3) # Adds dots for visibility

    ax.set_xlabel('Date')
    ax.set_ylabel('Wind Velocity (m/s)')
    ax.set_title(f'{location} - 850 hPa Wind Speed')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Format X-axis dates nicely
    fig.autofmt_xdate()

    # 6. Save and Close (Order matters here!)
    fig.tight_layout()
    output_path = f"../graphs/{location}_WS.png"
    fig.savefig(output_path, dpi=300)
    plt.close(fig)
    
    print(f"✅ Successfully saved: {output_path}")


if __name__ == "__main__":
    areas = ["Amazon", "Amazon_NE", "Amazon_SW", "Sahara", "Atlantic"]
    
    """for area in areas:
        save_graph(area)"""

    save_graph()

    # If you specifically need to mix Amazon and Sahara data, uncomment below:
    # save_graph("Amazon_Mixed", 
    #            north_path="../data/Amazon/north_vel_850hpa.csv", 
    #            east_path="../data/Sahara/east_vel_850hpa.csv")