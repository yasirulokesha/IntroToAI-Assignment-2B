import pandas as pd
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Sample SCATS site list (40 dummy site numbers)
# scats_sites = [str(site_id) for site_id in range(970, 1010)]


# Read only specific columns
df = pd.read_csv("TBRGS/data/processed/map_data.csv", usecols=["SCATS Number", "Location"])

# Combine the two columns into a single string and store in a list
scats_sites = [f"{int(row['SCATS Number'])} - {row['Location']}" for _, row in df.iterrows()]


# Generate time options (00:00 to 23:45 in 15 min intervals)
time_options = [f"{h:02}:{m:02}" for h in range(24) for m in (0, 15, 30, 45)]

# Initialize main window
root = tk.Tk()
root.title("TBRGS")
root.geometry("1200x700")

# Frames: Left 30%, Right 70%
left_frame = tk.Frame(root, width=480, bg="white", padx=20, pady=20)
left_frame.pack(side="left", fill="y")

right_frame = tk.Frame(root, bg="lightgray")
right_frame.pack(side="right", fill="both", expand=True)

# ----- LEFT PANEL -----
# Left Panel Header
tk.Label(left_frame, text="TBRGS", font=("Helvetica", 20, "bold"), fg="black", bg="white").pack(pady=(0, 20))

# Dropdown field generator
def add_dropdown(label, options):
    tk.Label(left_frame, text=label, bg="white").pack(anchor="w")
    cb = ttk.Combobox(left_frame, values=options, state="readonly")
    cb.current(0)
    cb.pack(fill="x", pady=(0, 10))
    return cb

# Dropdowns
orig_cb = add_dropdown("ORIGINATION", scats_sites)
dest_cb = add_dropdown("DESTINATION", scats_sites)
day_cb = add_dropdown("DAY", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
time_cb = add_dropdown("TIME", time_options)
model_cb = add_dropdown("MODEL", ["LSTM", "GRU"])
 
# Search Button
tk.Button(left_frame, text="SEARCH", width=20).pack(pady=30)

# ----- RIGHT PANEL: Add Route Blocks -----
# Function to add route block to right frame
def add_route(route_number, route_path):
    frame = tk.Frame(right_frame, bg="white", padx=10, pady=10)
    frame.pack(fill="x", padx=20, pady=15)

    tk.Label(frame, text=f"ROUTE {route_number}", font=("Helvetica", 12, "bold"), bg="white").pack(anchor="w")
    tk.Label(frame, text=route_path, bg="white").pack(anchor="w", pady=(0, 10))

    # Dummy matplotlib plot
    fig, ax = plt.subplots(figsize=(6, 2))
    ax.plot([0, 1, 2], [0, 1, 0], marker='o')
    ax.set_title(f"Route {route_number} Visualization")
    ax.axis('off')
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

# Example routes
add_route(1, "970 -> 2000 -> 5261")
add_route(2, "970 -> 3685 -> 5261")
add_route(3, "970 -> 3685 -> 2000 -> 5261")

root.mainloop()
