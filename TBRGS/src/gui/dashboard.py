import pandas as pd
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import customtkinter

from route_generator import plot_route_map

# Read only specific columns
df = pd.read_csv("TBRGS/data/processed/map_data.csv", usecols=["SCATS Number", "Location"])

# Combine the two columns into a single string and store in a list
scats_sites = [f"{int(row['SCATS Number'])} - {(row['Location'])}" for _, row in df.iterrows()]

# Generate time options (00:00 to 23:45 in 15 min intervals)
time_options = [f"{h:02}:{m:02}" for h in range(24) for m in (0, 15, 30, 45)]

date_options = [ 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday' ]

# Initialize main window
root = tk.Tk()
root.title("Traffic-Based Route Guidance System")
root.geometry("1500x768")

# Frames: Left 30%, Right 70%
left_frame = tk.Frame(root, width=480, bg="white", padx=20, pady=20)
left_frame.pack(side="left", fill="y")

right_frame = tk.Frame(root, bg="lightgray")
right_frame.pack(side="right", fill="both", expand=True)

# ----- LEFT PANEL -----
# Left Panel Header
tk.Label(left_frame, text="Traffic-Based Route Guidance System", font=("Helvetica", 20, "bold"), fg="black", bg="white", wraplength=200, justify="center").pack(pady=(20, 50))

# Dropdown field generator
def add_dropdown(label, options):
    label = customtkinter.CTkLabel(left_frame, text=label, width=40, height=30, fg_color='transparent', text_color='black', font=("Helvetica", 16, "bold"))
    label.pack(anchor="w", pady=(2))
    combobox_var = customtkinter.StringVar(value='Select an option')
    combobox = customtkinter.CTkComboBox(left_frame, values=options, width=240, height=30, variable=combobox_var)
    combobox.pack(pady=(0, 40))
    
    return combobox_var

add_dropdown("Origin", scats_sites)
add_dropdown("Destination", scats_sites)
add_dropdown("Day", date_options)
add_dropdown("Time Slot", time_options)


def button_event():
    print('button pressed')

button = customtkinter.CTkButton(left_frame, text='Search', width=240, height=50, font=("Helvetica", 16))
button.pack(side="bottom", pady=20)


# ----- RIGHT PANEL -----

fig, ax = plt.subplots(figsize=(6, 2))

canvas = FigureCanvasTkAgg(fig, master=right_frame)
canvas.get_tk_widget().pack(fill="both", expand=True)

root.mainloop()

# Function to add route block to right frame
# def add_route(route_number, route_path):
#     frame = tk.Frame(right_frame, bg="white", padx=10, pady=10)
#     frame.pack(fill="x", padx=20, pady=15)

#     tk.Label(frame, text=f"ROUTE {route_number}", font=("Helvetica", 12, "bold"), bg="white").pack(anchor="w")
#     tk.Label(frame, text=route_path, bg="white").pack(anchor="w", pady=(0, 10))

#     # Dummy matplotlib plot
#     fig, ax = plt.subplots(figsize=(6, 2))
#     ax.plot([0, 1, 2], [0, 1, 0], marker='o')
#     ax.set_title(f"Route {route_number} Visualization")
#     ax.axis('off')
#     canvas = FigureCanvasTkAgg(fig, master=frame)
#     canvas.draw()
#     canvas.get_tk_widget().pack()

# Example routes
# add_route(1, "970 -> 2000 -> 5261")
# add_route(2, "970 -> 3685 -> 5261")
# add_route(3, "970 -> 3685 -> 2000 -> 5261")

