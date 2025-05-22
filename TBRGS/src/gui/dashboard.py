# import pandas as pd
# import tkinter as tk
# from tkinter import ttk
# import matplotlib.pyplot as plt
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# import customtkinter
# from PIL import Image, ImageTk, ImageDraw, ImageSequence


# from route_generator import plot_route_map

# # plot_route_map([]).savefig("TBRGS/src/gui/map.jpg", dpi=300, bbox_inches='tight')

# loading = False
# searched = False

# origin = None
# destination = None
# day = None
# time = None

# def search_routes():
#     global loading, origin, destination, day, time, searched
    
#     if not searched:
#         searched = True
        
#     if not loading:
#         loading = not loading
        
#     create_right_frame()
#     print('button pressed')
#     print(f"Origin: {origin.get()}")
#     print(f"Destination: {destination.get()}")
#     print(f"Day: {day.get()}")
#     print(f"Time: {time.get()}")
    
# def add_rounded_corners(image, radius):
#     # Create mask
#     mask = Image.new("L", image.size, 0)
#     draw = ImageDraw.Draw(mask)
#     draw.rounded_rectangle((0, 0, image.size[0], image.size[1]), radius=radius, fill=255)
#     image.putalpha(mask)
#     return image

# def animate_gif(label, frames, delay=35, index=0):
#     frame = frames[index]
#     label.configure(image=frame)
#     label.image = frame
#     next_index = (index + 1) % len(frames)
#     label.after(delay, lambda: animate_gif(label, frames, delay, next_index))

# # Read only specific columns
# df = pd.read_csv("TBRGS/data/processed/map_data.csv", usecols=["SCATS Number", "Location"])

# # Combine the two columns into a single string and store in a list
# scats_sites = [f"{int(row['SCATS Number'])} - {(row['Location'])}" for _, row in df.iterrows()]

# # Generate time options (00:00 to 23:45 in 15 min intervals)
# time_options = [f"{h:02}:{m:02}" for h in range(24) for m in (0, 15, 30, 45)]

# date_options = [ 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday' ]


# # Initialize main window
# root = tk.Tk()

# # Set window dimensions
# window_width = 1000
# window_height = 768

# screen_width = root.winfo_screenwidth()
# screen_height = root.winfo_screenheight()

# # Find the center point
# x = int((screen_width / 2) - (window_width / 2))
# y = int((screen_height / 2) - (window_height / 2))

# root.title("Traffic-Based Route Guidance System")
# root.geometry(f"{window_width}x{window_height}+{x}+{y}")

# # Frames: Left 30%, Right 70%
# left_frame = tk.Frame(root, width=480, bg="white", padx=20, pady=20)
# left_frame.pack(side="left", fill="y")

# right_frame = tk.Frame(root, bg="lightgray")
# right_frame.pack(side="right", fill="both", expand=True)

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

# # Load and process image
# image = Image.open("TBRGS/src/gui/map.jpg").convert("RGBA")
# image = image.resize((700, 700), Image.LANCZOS)
# image = add_rounded_corners(image, radius=13)
# photo = ImageTk.PhotoImage(image)

# # Add image inside the scrollable frame
# image_label = tk.Label(scrollable_frame, image=photo, bg="lightgray", bd=0)
# image_label.image = photo  # prevent garbage collection
# image_label.pack(pady=10, expand=True)

# # ----- LEFT PANEL -----
# # Left Panel Header
# tk.Label(left_frame, text="Traffic-Based Route Guidance System", font=("Modern", 20, "bold"), fg="black", bg="white", wraplength=200, justify="center").pack(pady=(20, 50))

# # Dropdown field generator
# def add_dropdown(label, options):
#     label = customtkinter.CTkLabel(left_frame, text=label, width=40, height=30, fg_color='transparent', text_color='black', font=("Modern", 16, "bold"))
#     label.pack(anchor="w", pady=(2))
#     combobox_var = customtkinter.StringVar(value='Select an option')
#     combobox = customtkinter.CTkComboBox(left_frame, values=options, width=240, height=30, variable=combobox_var)
#     combobox.pack(pady=(0, 40))
    
#     return combobox_var

# origin = add_dropdown("Origin", scats_sites)
# destination = add_dropdown("Destination", scats_sites)
# day = add_dropdown("Day", date_options)
# time = add_dropdown("Time Slot", time_options)

# button = customtkinter.CTkButton(left_frame, text='Search', width=240, height=50, font=("Modern", 16), command=search_routes)
# button.pack(side="bottom", pady=20)

# # ----- RIGHT PANEL -----
# def create_right_frame():
#     global loading_label, title_label, image_label
#     title_label.destroy() if 'title_label' in globals() else None
#     image_label.destroy() if 'image_label' in globals() else None
#     loading_label.destroy() if 'loading_label' in globals() else None
#     try:
#         if loading:
#             gif_path = "TBRGS/src/gui/loading_gif.gif"  # 🔁 Change to your gif path
#             gif_image = Image.open(gif_path)

#             gif_frames = [ImageTk.PhotoImage(frame.copy().convert("RGBA").resize((150, 150), Image.LANCZOS) ) for frame in ImageSequence.Iterator(gif_image)]

#             gif_label = tk.Label(right_frame, bg="lightgray", bd=0)
#             gif_label.place(relx=0.5, rely=0.45, anchor="center")  # slightly below text
            
#             animate_gif(gif_label, gif_frames)
            
#             # Loading animation
#             loading_label = tk.Label(right_frame, text="Loading...", bg="lightgray", highlightthickness=0, fg="black", font=("Modern", 16, "bold"))
#             loading_label.place(relx=0.5, rely=0.55, anchor="center")
#         else:
#             # Title text
#             title_label = tk.Label(right_frame, text="SCATS Map", bg="lightgray", fg="black", font=("Modern", 16, "bold"))
#             title_label.pack(pady=(10, 5))

#             # Load and process image
#             image = Image.open("TBRGS/src/gui/map.jpg").convert("RGBA")
#             image = image.resize((700, 700), Image.LANCZOS)
#             image = add_rounded_corners(image, radius=13)
#             photo = ImageTk.PhotoImage(image)

#             # Image label
#             image_label = tk.Label(right_frame, image=photo, bg="lightgray", bd=0)
#             image_label.image = photo  # prevent garbage collection
#             image_label.pack(pady=10, expand=True)  
            
#     except FileNotFoundError:
#         print("Error: Image file not found.")
#         root.destroy()
#         exit()

# create_right_frame()
# # scroll_container = tk.Frame(root)
# # scroll_container.pack(fill="both", side="right", expand=True)

# # canvas = tk.Canvas(right_frame, bg="lightgray")
# # scrollbar = tk.Scrollbar(right_frame, orient="vertical", command=canvas.yview)

# # scrollable_frame = tk.Frame(canvas)

# # scrollable_frame.bind(
# #     "<Configure>",
# #     lambda e: canvas.configure(
# #         scrollregion=canvas.bbox("all")
# #     )
# # )

# # canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
# # canvas.configure(yscrollcommand=scrollbar.set)

# # right_frame.pack(side="right", fill="both", expand=True)
# # # scrollbar.pack(side="right", fill="y")
# # fig = plot_route_map([])  # Get the matplotlib Figure

# # # Embed it into Tkinter
# # canvas = FigureCanvasTkAgg(fig, master=right_frame)
# # canvas.draw()
# # canvas.get_tk_widget().pack(fill="both", expand=True)

# # --- Function to add plots dynamically ---
# # def add_route_plot(route_list):
# #     fig = plot_route_map(route_list)
# #     frame = tk.Frame(scrollable_frame, bg="white", pady=10)
# #     frame.pack(fill="x", padx=10, pady=10)

# #     label = tk.Label(frame, text=f"Route: {' → '.join(map(str, route_list))}", font=("Modern", 12, "bold"), bg="white")
# #     label.pack(anchor="w")

# #     canvas_plot = FigureCanvasTkAgg(fig, master=frame)
# #     canvas_plot.draw()
# #     canvas_plot.get_tk_widget().pack(fill="both", expand=True)

# # # --- Example routes ---
# # routes = [
# #     [970, 3685, 2000, 4043],
# #     [970, 2000, 5261],
# #     [3685, 4043, 2000] 
# # ]

# # for route in routes:
# #     add_route_plot(route)


# root.mainloop()

# # Function to add route block to right frame
# # def add_route(route_number, route_path):
# #     frame = tk.Frame(right_frame, bg="white", padx=10, pady=10)
# #     frame.pack(fill="x", padx=20, pady=15)

# #     tk.Label(frame, text=f"ROUTE {route_number}", font=("Modern", 12, "bold"), bg="white").pack(anchor="w")
# #     tk.Label(frame, text=route_path, bg="white").pack(anchor="w", pady=(0, 10))

# #     # Dummy matplotlib plot
# #     fig, ax = plt.subplots(figsize=(6, 2))
# #     ax.plot([0, 1, 2], [0, 1, 0], marker='o')
# #     ax.set_title(f"Route {route_number} Visualization")
# #     ax.axis('off')
# #     canvas = FigureCanvasTkAgg(fig, master=frame)
# #     canvas.draw()
# #     canvas.get_tk_widget().pack()

# # Example routes
# # add_route(1, "970 -> 2000 -> 5261")
# # add_route(2, "970 -> 3685 -> 5261")
# # add_route(3, "970 -> 3685 -> 2000 -> 5261")


import pandas as pd
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageDraw, ImageSequence
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import customtkinter
# from route_generator import plot_route_map


class TBRGSApp:
    def __init__(self, root, graph):
        self.root = root
        self.root.title("Traffic-Based Route Guidance System")
        self.root.geometry(self.center_window(1000, 768))

        self.loading = False
        self.searched = False
        self.photo = None  # image holder

        self.init_variables()
        self.build_gui()
        self.create_right_frame()
        self.graph = graph
        self.paths = []

    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        return f"{width}x{height}+{x}+{y}"

    def init_variables(self):
        df = pd.read_csv("TBRGS/data/processed/map_data.csv", usecols=["SCATS Number", "Location"])
        self.scats_sites = [f"{int(row['SCATS Number'])} - {row['Location']}" for _, row in df.iterrows()]
        self.time_options = [f"{h:02}:{m:02}" for h in range(24) for m in (0, 15, 30, 45)]
        self.date_options = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        self.origin = self.destination = self.day = self.time = None

    def build_gui(self):
        # Left Panel
        self.left_frame = tk.Frame(self.root, width=480, bg="white", padx=20, pady=20)
        self.left_frame.pack(side="left", fill="y")

        tk.Label(
            self.left_frame, text="Traffic-Based Route Guidance System",
            font=("Modern", 20, "bold"), fg="black", bg="white", wraplength=200, justify="center"
        ).pack(pady=(20, 50))

        self.origin = self.add_dropdown("Origin", self.scats_sites)
        self.destination = self.add_dropdown("Destination", self.scats_sites)
        self.day = self.add_dropdown("Day", self.date_options)
        self.time = self.add_dropdown("Time Slot", self.time_options)

        search_button = customtkinter.CTkButton(
            self.left_frame, text='Search', width=240, height=50,
            font=("Modern", 16), command=self.search_routes
        )
        search_button.pack(side="bottom", pady=20)

        # Right Panel
        self.right_frame = tk.Frame(self.root, bg="lightgray")
        # self.right_frame.pack(side="right", fill="both", expand=True)
        self.right_frame.pack(side="right", fill="both", expand=True)

    def add_dropdown(self, label_text, options):
        label = customtkinter.CTkLabel(self.left_frame, text=label_text, width=40, height=30, fg_color='transparent', text_color='black', font=("Modern", 14, "bold"))
        label.pack(anchor="w", pady=(2))
        var = customtkinter.StringVar(value="Select an option")
        dropdown = customtkinter.CTkComboBox(self.left_frame, values=options, width=240, height=30, variable=var)
        dropdown.pack(pady=(0, 40))
        return var

    def search_routes(self):
        self.loading = True
        self.searched = True
        self.create_right_frame()
        self.root.update()  # Update the GUI immediately
        print("Search triggered")
        print(f"Origin: {self.origin.get()}")
        print(f"Destination: {self.destination.get()}")
        print(f"Day: {self.day.get()}")
        print(f"Time: {self.time.get()}")
        self.generate_routes()
        self.create_right_frame()
        
    def create_right_frame(self):
        for widget in self.right_frame.winfo_children():
            widget.destroy()
            
        if self.loading:
            gif_path = "TBRGS/src/gui/loading_gif.gif"
            gif_image = Image.open(gif_path)
            gif_frames = [
                ImageTk.PhotoImage(frame.copy().convert("RGBA").resize((150, 150), Image.LANCZOS))
                for frame in ImageSequence.Iterator(gif_image)
            ]
            gif_label = tk.Label(self.right_frame, bg="lightgray", bd=0)
            gif_label.place(relx=0.5, rely=0.45, anchor="center")
            self.animate_gif(gif_label, gif_frames)

            loading_label = tk.Label(
                self.right_frame, text="Loading...",
                bg="lightgray", fg="black", font=("Modern", 16, "bold")
            )
            loading_label.place(relx=0.5, rely=0.55, anchor="center")

            # simulate loading complete
            self.root.after(1500, self.show_image_panel)
        else:
            if self.searched and self.origin.get() != None and self.destination.get() != None:
                self.show_image_panel()
            else:
                # Title
                tk.Label(
                    self.right_frame, text="SCATS Map",
                    bg="lightgray", fg="black", font=("Modern", 20, "bold")
                ).pack(pady=(10, 5))
                # Load and process image
                img = Image.open("TBRGS/src/gui/map.jpg").convert("RGBA")
                img = img.resize((700, 700), Image.LANCZOS)
                img = self.add_rounded_corners(img, radius=13)
                photo = ImageTk.PhotoImage(img)

                # Store reference to avoid GC
                if not hasattr(self, "photos"):
                    self.photos = []
                self.photos.append(photo)

                label = tk.Label(self.right_frame, image=photo, bg="lightgray", bd=0)
                label.pack(padx=10, pady=10)  # ✅ FIXED: no expand=True
        
    def show_image_panel(self):
        self.loading = True

        for widget in self.right_frame.winfo_children():
            widget.destroy()

        # Title
        tk.Label(
            self.right_frame, text=f"Shortest Routes\n\nOrigin : {self.origin.get()} \nDestination : {self.destination.get()} \nDay : {self.day.get()}, \nTime : {self.time.get()}",
            bg="lightgray", fg="black", font=("Modern", 16, "bold"), justify="left", anchor="w"
        ).pack(padx=10, pady=(10, 5), anchor="w")

        # Scrollable Canvas Setup
        canvas = tk.Canvas(self.right_frame, bg="lightgray", highlightthickness=0)
        scrollbar = tk.Scrollbar(self.right_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="lightgray")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        # Embed scrollable frame
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", tags="frame")
        canvas.bind("<Configure>", lambda e: canvas.itemconfig("frame", width=e.width))

        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # ✅ Enable mousewheel / touchpad scroll gestures
        def _on_mousewheel(event):
            if event.num == 4 or event.delta > 0:
                canvas.yview_scroll(-1, "units")
            elif event.num == 5 or event.delta < 0:
                canvas.yview_scroll(1, "units")

        # Windows/macOS
        self.root.bind_all("<MouseWheel>", _on_mousewheel)

        # Linux (legacy X11)
        self.root.bind_all("<Button-4>", _on_mousewheel)
        self.root.bind_all("<Button-5>", _on_mousewheel)

        # Helper function to load and display a map image
        def add_map_image(image_path, path):
            try:
                img = Image.open(image_path).convert("RGBA")
                img = img.resize((500, 500), Image.LANCZOS)
                img = self.add_rounded_corners(img, radius=13)
                photo = ImageTk.PhotoImage(img)

                # Store reference to avoid GC
                if not hasattr(self, "photos"):
                    self.photos = []
                self.photos.append(photo)

                label = tk.Label(scrollable_frame, image=photo, bg="lightgray", bd=0)
                label.pack(padx=10, pady=10)  # ✅ FIXED: no expand=True
                
                # # Add route text
                # route_text = tk.Label(scrollable_frame, text=f"Route: {' → '.join(map(str, path))}", font=("Modern", 12, "bold"), bg="lightgray")
                # route_text.pack(anchor="w", padx=10, pady=(0, 10))
                
            except FileNotFoundError:
                tk.Label(scrollable_frame, text=f"❌ {image_path} not found!", bg="lightgray", fg="red").pack(pady=30)
                
        # Add two map
        # for i, path in enumerate(paths):
        #     image_path = f"TBRGS/src/gui/route_maps/route_{i}.jpg"
        #     print(f"Adding image: {image_path}")
        #     add_map_image(str(image_path), path)
        
        num_of_paths = len(self.paths)
        
        if num_of_paths == 0:
            tk.Label(scrollable_frame, text="❌ No routes found!", bg="lightgray", fg="red").pack(pady=30, anchor="center")
        else:
            for i in range(num_of_paths):
                image_path = f"TBRGS/src/gui/route_maps/route_{i}.jpg"
                print(f"Adding image: {image_path}")
                add_map_image(str(image_path), self.paths[i][1])
                    
        self.loading = False

    def add_rounded_corners(self, image, radius):
        mask = Image.new("L", image.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle((0, 0, *image.size), radius=radius, fill=255)
        image.putalpha(mask)
        return image

    def animate_gif(self, label, frames, delay=35, index=0):
        frame = frames[index]
        label.configure(image=frame)
        label.image = frame
        next_index = (index + 1) % len(frames)
        label.after(delay, lambda: self.animate_gif(label, frames, delay, next_index))

    def generate_routes(self):
        self.loading = True
        
        from .route_generator import plot_route_map  # import here to avoid circular issue
        from algorithms.yens_algorithm import find_k_shortest_routes
        
        origin_value = self.origin.get().split(" - ")[0].strip()
        destination_value = self.destination.get().split(" - ")[0].strip()
        
        paths = find_k_shortest_routes(self.graph, int(origin_value), int(destination_value), k=5)
        
        self.paths = paths  # Store paths for later use
        
        plots = []
        
        # print(paths, "\n")
        for path in paths:
            print(path[0], ":", path[1])
            print("Total cost:", path[0])
            print("Path:", " -> ".join(map(str, path[1])))
            print()
            plots.append(plot_route_map(path[1]))
        
        # Save each plot
        for i, plot in enumerate(plots):
            plot.savefig(f"TBRGS/src/gui/route_maps/route_{i}.jpg", dpi=100, bbox_inches='tight')
            plot.close()
        
        self.show_image_panel()  # refresh GUI with new image

# if __name__ == "__main__":
#     root = tk.Tk()
#     app = TBRGSApp(root)
#     root.mainloop()
