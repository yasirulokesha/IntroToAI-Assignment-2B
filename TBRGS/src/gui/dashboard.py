import pandas as pd
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageDraw, ImageSequence
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import customtkinter


class TBRGSApp:
    def __init__(self, root, graph):
        self.root = root
        self.root.title("Traffic-Based Route Guidance System")
        self.root.geometry(self.center_window(1200, 1024))

        self.loading = False
        self.searched = False
        self.photo = None  # image holder

        self.init_variables()
        self.build_gui()
        self.create_right_frame()
        self.graph = graph
        self.paths = []
        self.current_model = None
        self.current_time = None

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
        self.model = ["LSTM","GRU", "RNN"]

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
        self.model = self.add_dropdown("Prediction Model", self.model)

        search_button = customtkinter.CTkButton(
            self.left_frame, text='Search', width=240, height=50,
            font=("Modern", 16), command=self.search_routes
        )
        search_button.pack(side="bottom", pady=20)

        # Right Panel
        self.right_frame = tk.Frame(self.root, bg="lightgray")
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
        print(f"Model: {self.model.get()}")
        print("Generating routes...")
        self.generate_routes()
        self.create_right_frame()
        
    def create_right_frame(self):
        for widget in self.right_frame.winfo_children():
            widget.destroy()
            
        if self.loading:
            # gif_path = "TBRGS/src/gui/loading_gif.gif"
            # gif_image = Image.open(gif_path)
            # gif_frames = [
            #     ImageTk.PhotoImage(frame.copy().convert("RGBA").resize((150, 150), Image.LANCZOS))
            #     for frame in ImageSequence.Iterator(gif_image)
            # ]
            # gif_label = tk.Label(self.right_frame, bg="lightgray", bd=0)
            # gif_label.place(relx=0.5, rely=0.45, anchor="center")
            # self.animate_gif(gif_label, gif_frames)

            loading_label = tk.Label(
                self.right_frame, text="Loading...",
                bg="lightgray", fg="black", font=("Modern", 16, "bold")
            )
            loading_label.place(relx=0.5, rely=0.55, anchor="center")
            
        else:
            if self.searched and self.origin.get() != None and self.destination.get() != None:
                self.show_image_panel()
            else:
                # Title
                tk.Label(
                    self.right_frame, text="SCATS Map",
                    bg="lightgray", fg="black", font=("Modern", 25, "bold")
                ).pack(pady=20)
                # Load and process image
                img = Image.open("TBRGS/src/gui/map.jpg").convert("RGBA")
                img = img.resize((900, 900), Image.LANCZOS)
                img = self.add_rounded_corners(img, radius=10)
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
        
        # Title
        tk.Label(
            scrollable_frame, text=f"Route Information",
            bg="lightgray", fg="black", font=("Modern", 20, "bold"), justify="left", anchor="w",
            padx=20, pady=10
        ).pack(padx=20, pady=(10, 1), anchor="w")
        
        tk.Label(
            scrollable_frame,
            text=f"Origin : {self.origin.get()}",
            bg="lightgray",
            fg="black",
            font=("Modern", 13),
            wraplength=400,  # Set a width for wrapping
            justify="left",     
            anchor="w",
            padx=20,
            pady=0
        ).pack(padx=20, pady=1, anchor="w")
        
        tk.Label(
            scrollable_frame,
            text=f"Destination : {self.destination.get()}",
            bg="lightgray",
            fg="black",
            font=("Modern", 13),
            wraplength=400,  # Set a width for wrapping
            justify="left",     
            anchor="w",
            padx=20,
            pady=0
        ).pack(padx=20, pady=1, anchor="w")
        
        tk.Label(
            scrollable_frame,
            text=f"Day : {self.day.get()}",
            bg="lightgray",
            fg="black",
            font=("Modern", 13),
            wraplength=400,  # Set a width for wrapping
            justify="left",     
            anchor="w",
            padx=20,
            pady=0
        ).pack(padx=20, pady=1, anchor="w")
        
        tk.Label(
            scrollable_frame,
            text=f"Time : {self.time.get()}",
            bg="lightgray",
            fg="black",
            font=("Modern", 13),
            wraplength=400,  # Set a width for wrapping
            justify="left",     
            anchor="w",
            padx=20,
            pady=0
        ).pack(padx=20, pady=1, anchor="w")
        
        tk.Label(
            scrollable_frame,
            text=f"Model : {self.model.get()}",
            bg="lightgray",
            fg="black",
            font=("Modern", 13),
            wraplength=400,  # Set a width for wrapping
            justify="left",     
            anchor="w",
            padx=20,
            pady=0
        ).pack(padx=20, pady=1, anchor="w")
        
        tk.Label(
            scrollable_frame,
            text=f"Total Routes : {len(self.paths)}",
            bg="lightgray",
            fg="black",
            font=("Modern", 13),
            wraplength=400,  # Set a width for wrapping
            justify="left",     
            anchor="w",
            padx=20,
            pady=0
        ).pack(padx=20, pady=1, anchor="w")
        
        
        
        
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
        def add_map_image(image_path, path, time_estimation):
            try:
                # Add route text
                route_text = tk.Label(scrollable_frame, text=f"Route: \n{' → '.join(map(str, map(int, path)))}", font=("Modern", 14, "bold"), wraplength=400, fg="black", bg="lightgray")
                route_text.pack(padx=10, pady=(0, 10), anchor="center")
                minutes = int(time_estimation)
                seconds = int((time_estimation - minutes) * 60)
                route_text = tk.Label(scrollable_frame, text=f"Total Time Estimation: {minutes}min {seconds}sec", font=("Modern", 14, "bold"), wraplength=400, fg="black", bg="lightgray")
                route_text.pack(padx=10, pady=(0, 5), anchor="center")
                
                img = Image.open(image_path).convert("RGBA")
                img = img.resize((650, 650), Image.LANCZOS)
                img = self.add_rounded_corners(img, radius=13)
                photo = ImageTk.PhotoImage(img)

                # Store reference to avoid GC
                if not hasattr(self, "photos"):
                    self.photos = []
                self.photos.append(photo)

                label = tk.Label(scrollable_frame, image=photo, bg="lightgray", bd=0)
                label.pack(padx=10, pady=10) 
            
                
            except FileNotFoundError:
                tk.Label(scrollable_frame, text=f"❌ {image_path} not found!", bg="lightgray", fg="red").pack(pady=30)
    
        num_of_paths = len(self.paths)
        
        if num_of_paths == 0:
            tk.Label(scrollable_frame, text="❌ No routes found!", bg="lightgray", fg="red").pack(pady=30, anchor="center")
        else:
            for i in range(num_of_paths):
                image_path = f"TBRGS/src/gui/route_maps/route_{i}.jpg"
                print(f"Adding image: {image_path}")
                add_map_image(str(image_path), self.paths[i][1], self.paths[i][0])
                    
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
        
        self.right_frame.pack_forget()
        
        # splash = loding_splash()
        # self.root.update()
        splash = tk.Toplevel()
        splash.overrideredirect(True)  # Removes title bar
        
        # gif_path = "TBRGS/src/gui/loading_gif.gif"
        # gif_image = Image.open(gif_path)
        # gif_frames = [
        #     ImageTk.PhotoImage(frame.copy().convert("RGBA").resize((150, 150), Image.LANCZOS))
        #     for frame in ImageSequence.Iterator(gif_image)
        # ]
        # gif_label = tk.Label(self.right_frame, bg="lightgray", bd=0)
        # gif_label.place(relx=0.5, rely=0.45, anchor="center")
        # self.animate_gif(gif_label, gif_frames)

        # loading_label = tk.Label(
        #     self.right_frame, text="Loading...",
        #     bg="lightgray", fg="black", font=("Modern", 16, "bold")
        # )
        # loading_label.place(relx=0.5, rely=0.55, anchor="center")
        # loading_label.pack(side="right", fill="both")
        
        from data_processing import process_scats_edges
        
        if (self.model != self.current_model or self.time != self.current_time):
            self.graph = process_scats_edges(self.graph, self.day.get(), self.time.get(), self.model.get())
            
        self.current_model = self.model.get()
        self.current_time = self.time.get()
        
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
        
            
        self.loading = False
        splash.destroy()
        # gif_label.destroy()
        # loading_label.destroy()
        self.right_frame.pack(side="right", fill="both", expand=True)
