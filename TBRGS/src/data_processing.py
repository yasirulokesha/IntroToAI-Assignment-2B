import pandas as pd

traffic_csv_path = "Scats Data October 2006.csv"
coords_csv_path = "Traffic_Count_Locations_with_LONG_LAT.csv"

def load_and_process_traffic_data(traffic_csv_path, coords_csv_path):
    # Load traffic volume data (skip first row with V labels)
    df_raw = pd.read_csv(traffic_csv_path, skiprows=1)

    # Create time mapping for V00–V95 (15-minute intervals)
    time_labels = [f"{h:02}:{m:02}:00" for h in range(24) for m in range(0, 60, 15)]
    v_columns = [f"V{str(i).zfill(2)}" for i in range(96)]
    time_map = dict(zip(v_columns, time_labels))

    # Melt the V columns into long format
    df_melted = df_raw.melt(
        id_vars=["SCATS Number", "Location", "Date"],
        value_vars=v_columns,
        var_name="time_code",
        value_name="volume"
    )

    # Map time codes to actual time strings
    df_melted['time_str'] = df_melted['time_code'].map(time_map)

    # Combine Date and Time into a full timestamp
    df_melted['timestamp'] = pd.to_datetime(df_melted['Date'] + ' ' + df_melted['time_str'], dayfirst=True)

    # Rename columns for clarity
    df_melted = df_melted.rename(columns={
        "SCATS Number": "site_id",
        "Location": "location"
    })

    # Select and reorder important columns
    df_traffic = df_melted[["site_id", "location", "timestamp", "volume"]].dropna()

    # Load site coordinate data
    df_coords = pd.read_csv(coords_csv_path)
    df_coords = df_coords.rename(columns={
        "TFM_ID": "site_id",
        "X": "longitude",
        "Y": "latitude"
    })

    # Merge coordinates into traffic data
    df_combined = df_traffic.merge(df_coords[["site_id", "latitude", "longitude"]], on="site_id", how="left")

    return df_combined

# Load cleaned data
df = load_and_process_traffic_data(traffic_csv_path, coords_csv_path)

# Preview
print(df.head())