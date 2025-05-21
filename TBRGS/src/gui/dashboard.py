import pandas as pd
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import customtkinter
from PIL import Image, ImageTk, ImageDraw, ImageFilter


from route_generator import plot_route_map

# plot_route_map([]).savefig("TBRGS/src/gui/map.jpg", dpi=300, bbox_inches='tight')

loading = False

def search_routes():
    global loading
    loading = not loading
    create_right_frame()
    print('button pressed')

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
root.geometry("1100x768")

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




button = customtkinter.CTkButton(left_frame, text='Search', width=240, height=50, font=("Helvetica", 16), command=search_routes)
button.pack(side="bottom", pady=20)


def add_rounded_corners(image, radius):
    # Create mask
    mask = Image.new("L", image.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0, image.size[0], image.size[1]), radius=radius, fill=255)
    image.putalpha(mask)
    return image

# ----- RIGHT PANEL -----
def create_right_frame():
    global loading_label, title_label, image_label
    title_label.destroy() if 'title_label' in globals() else None
    image_label.destroy() if 'image_label' in globals() else None
    loading_label.destroy() if 'loading_label' in globals() else None
    try:
        if loading:
            # Loading animation
            loading_label = tk.Label(right_frame, text="Loading...", bg="lightgray", fg="black", font=("Helvetica", 16, "bold"))
            loading_label.pack(pady=(10, 5))
        else:
        # Title text
            title_label = tk.Label(right_frame, text="SCATS Map", bg="lightgray", fg="black", font=("Helvetica", 16, "bold"))
            title_label.pack(pady=(10, 5))

            # Load and process image
            image = Image.open("TBRGS/src/gui/map.jpg").convert("RGBA")
            image = image.resize((700, 700), Image.LANCZOS)
            image = add_rounded_corners(image, radius=13)
            photo = ImageTk.PhotoImage(image)

            # Image label
            image_label = tk.Label(right_frame, image=photo, bg="lightgray", bd=0)
            image_label.image = photo  # prevent garbage collection
            image_label.pack(pady=10, expand=True)
    except FileNotFoundError:
        print("Error: Image file not found.")
        root.destroy()
        exit()

create_right_frame()
# scroll_container = tk.Frame(root)
# scroll_container.pack(fill="both", side="right", expand=True)

# canvas = tk.Canvas(right_frame, bg="lightgray")
# scrollbar = tk.Scrollbar(right_frame, orient="vertical", command=canvas.yview)

# scrollable_frame = tk.Frame(canvas)

# scrollable_frame.bind(
#     "<Configure>",
#     lambda e: canvas.configure(
#         scrollregion=canvas.bbox("all")
#     )
# )

# canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
# canvas.configure(yscrollcommand=scrollbar.set)

# right_frame.pack(side="right", fill="both", expand=True)
# # scrollbar.pack(side="right", fill="y")
# fig = plot_route_map([])  # Get the matplotlib Figure

# # Embed it into Tkinter
# canvas = FigureCanvasTkAgg(fig, master=right_frame)
# canvas.draw()
# canvas.get_tk_widget().pack(fill="both", expand=True)

# --- Function to add plots dynamically ---
# def add_route_plot(route_list):
#     fig = plot_route_map(route_list)
#     frame = tk.Frame(scrollable_frame, bg="white", pady=10)
#     frame.pack(fill="x", padx=10, pady=10)

#     label = tk.Label(frame, text=f"Route: {' → '.join(map(str, route_list))}", font=("Helvetica", 12, "bold"), bg="white")
#     label.pack(anchor="w")

#     canvas_plot = FigureCanvasTkAgg(fig, master=frame)
#     canvas_plot.draw()
#     canvas_plot.get_tk_widget().pack(fill="both", expand=True)

# # --- Example routes ---
# routes = [
#     [970, 3685, 2000, 4043],
#     [970, 2000, 5261],
#     [3685, 4043, 2000] 
# ]

# for route in routes:
#     add_route_plot(route)


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

