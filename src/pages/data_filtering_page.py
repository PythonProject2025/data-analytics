import customtkinter as ctk
from tkinter import Button, PhotoImage, Toplevel,messagebox
from src.assets_management import assets_manage, load_image
import pandas as pd
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import threading
from src.models.data_object_class import DataObject
import requests
from matplotlib.backend_bases import MouseEvent
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
import matplotlib.patches as patches



class DataFilteringPage(ctk.CTkFrame):
    def __init__(self, parent,file_path,file_name=" "):
        super().__init__(parent, corner_radius=0)

        self.file_name = file_name
        self.file_path=file_path
        self.current_segment_index = 0
        window_height = self.winfo_screenheight()  # Get the total screen height
        right_frame_height = int(0.8 * window_height)  # 60% of the screen height

        self.segment_completion = {
                                    "Select Filter Process": False,
                                    "Outlier Detection": False,
                                    "Interpolation": False,
                                    "Smoothing": False,
                                    "Scaling & Encoding": False
                                  }
        self.visible_segments = ["Select Filter Process"]
        self.data = pd.read_csv(self.file_path)  # Load CSV data
        self.column_names = list(self.data.columns)[1:]  # Exclude first column (Date)
        self.column_name = self.column_names[0] if self.column_names else None



        # Configure grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=8)  
        self.grid_columnconfigure(1, weight=2)  

         # Left Side Frame
        self.left_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.left_frame.grid(row=0, column=0, sticky="nsew", padx=50, pady=10)
        self.left_frame.grid_columnconfigure(0, weight=2)

        # First Frame (Text Box with Cancel Button)
        self.label_frame = ctk.CTkFrame(self.left_frame, fg_color="#E0E0E0", corner_radius=10,height=50)
        self.label_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.left_frame.grid_rowconfigure(0, weight=0)
        self.label = ctk.CTkLabel(self.label_frame, text=self.file_name, font=("Inter", 16, "bold"))
        self.label.place(relx=0.5, rely=0.5, anchor="center")
        self.preview_label = ctk.CTkLabel(self.label_frame, text="Preview", font=("Inter", 12, "bold"),
                                  text_color="blue", cursor="hand2")
        self.preview_label.place(relx=0.9, rely=0.5, anchor="center")  # Adjusted position
        self.preview_label.bind("<Button-1>", lambda event: self.preview_csv())
        self.cancel_button = ctk.CTkButton(self.left_frame, text="X", width=30, height=25, command=lambda: parent.show_page("file_upload"))
        self.cancel_button.grid(row=0, column=1, padx=10, pady=10)

        # Second Frame (Dropdown & Graph Display) - Increased Size
        self.graph_frame = ctk.CTkFrame(self.left_frame, fg_color="#E0E0E0", corner_radius=10, height=350)  # Increased Height
        self.graph_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.left_frame.grid_rowconfigure(1, weight=1)  # Keep left frame standard but allow graph frame to take space

        # Configure Graph Frame Grid
        self.graph_frame.grid_rowconfigure(0, weight=1)  # Center the dropdown
        self.graph_frame.grid_rowconfigure(1, weight=4)  # Allow graph display to expand
        self.graph_frame.grid_columnconfigure(0, weight=1)

          # `sticky="n"` keeps it at the top

        # Graph Display Area (Expanded)
        self.graph_display = ctk.CTkFrame(self.graph_frame, fg_color="#D1D1D1", height=250, corner_radius=10)  # Increased Size
        self.graph_display.grid(row=1, column=0, padx=0, pady=10, sticky="nsew")  # Expands to fill space


        self.Info_button_image = PhotoImage(file=assets_manage("info_B.png"))

        # Right Side Frame (Segmented Buttons)
        self.right_frame = ctk.CTkScrollableFrame(self, fg_color="#171821", width=300 , height= right_frame_height)
        self.right_frame.grid(row=0, column=1, sticky="en", padx=10, pady=10)
        self.right_frame.grid_columnconfigure(0, weight=1)
      

        # Segmented Button Frame
        self.segmented_frame = ctk.CTkSegmentedButton(self.right_frame, values=self.visible_segments,
                                                      command=self.change_segment)
        self.segmented_frame.grid(row=0, column=0, padx=10, pady=10)
        self.segmented_frame.set("Outlier Detection")

        # Frame that holds all segment contents
        self.segment_container = ctk.CTkFrame(self.right_frame, fg_color="transparent")
        self.segment_container.grid(row=1, column=0, sticky="s", padx=10, pady=10)

        # Define ordered segment list
        self.segment_order = ["Select Filter Process","Outlier Detection", "Interpolation", "Smoothing"]
        self.scaling_segment = "Scaling & Encoding"

        # Create segment frames
        self.segments = {
            "Select Filter Process": self.create_process_selection_frame(),
            "Outlier Detection": self.create_segment_frame(),
            "Interpolation": self.create_interpolation_frame(),
            "Smoothing": self.create_smoothing_frame(),
            
        }

        # Submit Button
        self.submit_button = ctk.CTkButton(self.right_frame, text="Submit", command=self.submit_action)
        self.submit_button.grid(row=2, column=0, pady=10)

        # Show default segment
        self.current_segment = None
        self.change_segment("Select Filter Process")

        if self.file_path:  
            self.load_csv_columns(self.file_path)
        
        # Initial Boxplot for first column
        if self.column_name:
            self.plot_boxplot(self.column_name)

    def create_process_selection_frame(self):
        """Creates the initial process selection frame."""
        frame = ctk.CTkFrame(self.segment_container, fg_color="#E0E0E0", corner_radius=10)
        frame.grid_columnconfigure(0, weight=1)
        radio_frame = ctk.CTkFrame(frame, fg_color="#D1D1D1", corner_radius=10)
        radio_frame.grid(row=1, column=0, padx=10, pady=15, sticky="new")

        self.process_radio_var = ctk.StringVar(value="Filtering Method")  # Default

        ctk.CTkRadioButton(radio_frame, text="Filtering Method", variable=self.process_radio_var,
                           value="Filtering Method").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        ctk.CTkRadioButton(radio_frame, text="Scaling & Encoding", variable=self.process_radio_var,
                           value="Scaling & Encoding").grid(row=1, column=0, padx=10, pady=10, sticky="w")

        return frame
        
    
    def create_segment_frame(self):
        """Creates a frame for each segment."""
        frame = ctk.CTkFrame(self.segment_container, fg_color="#E0E0E0", corner_radius=10)
        frame.grid_columnconfigure(0, weight=1)

        def create_info_button(parent, text):
            button = Button(parent, text="", image=self.Info_button_image, width=8, height=8, command=lambda: self.show_info_dialog(text))
            button.grid(row=0, column=1, padx=5, sticky="w")

        # Radio Button FrameS
        radio_frame = ctk.CTkFrame(frame, fg_color="#D1D1D1", corner_radius=10)
        radio_frame.grid(row=1, column=0, padx=10, pady=15, sticky="new")
        radio_label = ctk.CTkLabel(radio_frame, text="Select Method", font=("Inter", 12, "bold"), fg_color="#A0A0A0")
        radio_label.grid(row=0, column=0, sticky="nesw")
        create_info_button(radio_frame, "Information about options")
        self.radio_var = ctk.StringVar(value="Isolation Forest")
        ctk.CTkRadioButton(radio_frame, text="Isolation Forest", variable=self.radio_var, value="Isolation Forest", command=lambda: self.toggle_slider(frame, True)).grid(row=1, column=0, padx=10,pady=5,sticky="w")
        ctk.CTkRadioButton(radio_frame, text="IQR", variable=self.radio_var, value="IQR", command=lambda: self.toggle_slider(frame, False)).grid(row=1, column=1, padx=10,pady=5, sticky="w")

        # Slider Frame
        slider_frame = ctk.CTkFrame(frame, fg_color="#D1D1D1", corner_radius=10)
        slider_frame.grid(row=2, column=0, padx=10, pady=15, sticky="nsew")
        slider_label = ctk.CTkLabel(slider_frame, text="Contamination Value", font=("Inter", 12, "bold"), fg_color="#A0A0A0")
        slider_label.grid(row=0, column=0, sticky="new")
        create_info_button(slider_frame, "Information about slider")
        value_label = ctk.CTkLabel(slider_frame, text="Value: 0.00", font=("Inter", 12))
        value_label.grid(row=1, column=0, pady=5)

        def update_value(value):
            value_label.configure(text=f"Value: {float(value):.2f}")

        self.slider = ctk.CTkSlider(slider_frame, from_=0.00, to=0.50, number_of_steps=20,command= update_value)
        self.slider.grid(row=2, column=0, padx=10, sticky="ew")

        # Scrollable Frame with Checkboxes
        self.scroll_frame = ctk.CTkScrollableFrame(frame, fg_color="#D1D1D1", label_text="Columns", corner_radius=10)
        self.scroll_frame.grid(row=0, column=0, padx=10, pady=15, sticky="nsew")
        scroll_label = ctk.CTkLabel(self.scroll_frame, text="Choose Columns", font=("Inter", 12, "bold"), fg_color="#A0A0A0")
        scroll_label.grid(row=0, column=0, sticky="new")
        create_info_button(self.scroll_frame, "Information about checkboxes")
          

        frame.slider_frame = slider_frame  # Store reference for toggling

        return frame

    def create_interpolation_frame(self):


        frame = ctk.CTkFrame(self.segment_container, fg_color="#E0E0E0", corner_radius=10)
        frame.grid_columnconfigure(0, weight=1)

        def create_info_button(parent, text):
            button = Button(parent, text="", image=self.Info_button_image, width=8, height=8, command=lambda: self.show_info_dialog(text))
            button.grid(row=0, column=1, padx=5, sticky="w")

        radio_frame = ctk.CTkFrame(frame, fg_color="#D1D1D1", corner_radius=10)
        radio_frame.grid(row=0, column=1, padx=10, pady=15, sticky="ew")
        radio_label = ctk.CTkLabel(radio_frame, text="Select Method", font=("Inter", 12, "bold"), fg_color="#A0A0A0")
        radio_label.grid(row=0, column=0, sticky="nesw")
        create_info_button(radio_frame, "Information about options")
        self.interpolation_radio_var = ctk.StringVar(value="Spline")
        ctk.CTkRadioButton(radio_frame, text="Spline", variable=self.interpolation_radio_var, value="Spline").grid(row=1, column=0, padx=30, pady=5, sticky="w")
        ctk.CTkRadioButton(radio_frame, text="Kriging", variable=self.interpolation_radio_var, value="Kriging").grid(row=2, column=0, padx=30, pady=5, sticky="w")
        return frame

    def create_smoothing_frame(self):
        frame = ctk.CTkFrame(self.segment_container, fg_color="#E0E0E0", corner_radius=10)
        frame.grid_columnconfigure(0, weight=1)

        def create_info_button(parent, text, row, column):
            button = Button(parent, text="", image=self.Info_button_image, width=8, height=8, command=lambda: self.show_info_dialog(text))
            button.grid(row=0, column=1, padx=5, sticky="w")

        # Radio Button Frame
        radio_frame = ctk.CTkFrame(frame, fg_color="#D1D1D1", corner_radius=10)
        radio_frame.grid(row=0, column=0, padx=10, pady=15, sticky="ew")
        radio_frame.grid_columnconfigure(0, weight=1)

        radio_label = ctk.CTkLabel(radio_frame, text="Select Method", font=("Inter", 12, "bold"), fg_color="#A0A0A0")
        radio_label.grid(row=0, column=0, sticky="nesw")
        create_info_button(radio_frame, "Information about smoothing methods", row=0, column=1)

        self.smoothing_radio_var = ctk.StringVar(value="SMA")

        ctk.CTkRadioButton(radio_frame, text="SMA", variable=self.smoothing_radio_var, value="SMA",
                        command=lambda: self.toggle_smoothing_options(frame, "SMA")).grid(row=1, column=0, padx=10, pady=5, sticky="w")
        ctk.CTkRadioButton(radio_frame, text="TES", variable=self.smoothing_radio_var, value="TES",
                        command=lambda: self.toggle_smoothing_options(frame, "TES")).grid(row=1, column=1, padx=10, pady=5, sticky="w")

        # SMA Slider Frame (Default Visible)
        sma_slider_frame = ctk.CTkFrame(frame, fg_color="#D1D1D1", corner_radius=10)
        sma_slider_frame.grid(row=1, column=0, padx=10, pady=15, sticky="ew")

        sma_label = ctk.CTkLabel(sma_slider_frame, text="Window Size", font=("Inter", 12, "bold"), fg_color="#A0A0A0")
        sma_label.grid(row=0, column=0, sticky="nesw")
        create_info_button(sma_slider_frame, "Information about SMA window size", row=0, column=1)

        sma_value_label = ctk.CTkLabel(sma_slider_frame, text="Value: 5", font=("Inter", 12))
        sma_value_label.grid(row=1, column=0, pady=5)
        self.sma_slider = ctk.CTkSlider(sma_slider_frame, from_=5, to=100,
                                command=lambda value: sma_value_label.configure(text=f"Value: {int(value)}"))
        self.sma_slider.grid(row=2, column=0, padx=10, sticky="ew")

        # TES Frame (Default Hidden)
        self.tes_params = {}
        tes_frame =ctk.CTkFrame(frame, fg_color="#D1D1D1")
        tes_frame.grid(row=1, column=0, padx=10, pady=0, sticky="ew")
        tes_frame.grid_remove()  # Hidden initially

        # TES Parameters with Grid Layout
        def add_tes_parameter(parent, label_text, widget_type="slider", from_=0, to=1, row_index=0):
            param_frame = ctk.CTkFrame(parent, fg_color="#E0E0E0", corner_radius=10)
            param_frame.grid(row=row_index, column=0, padx=10, pady=10, sticky="nesw")

            # # Header Frame (Holds Label + Info Button)
            # header_frame = ctk.CTkFrame(param_frame, fg_color="transparent")
            # header_frame.grid(row=0, column=0, sticky="new")  # Keep everything left-aligned

            # Label for the parameter
            param_label = ctk.CTkLabel(param_frame, text=label_text, font=("Inter", 12, "bold"), fg_color="#A0A0A0")
            param_label.grid(row=0, column=0, sticky="nesw")  # Left-aligned with slight padding

            # Information Button (Immediately after Label, Not Right-Aligned)
            info_button = Button(
                param_frame, text=" ",image=self.Info_button_image, width=8, height=8,
                command=lambda: self.show_info_dialog(f"Information about {label_text}")
            )
            info_button.grid(row=0, column=1, padx=(4, 5), sticky="w")  # Right next to the label

            if widget_type == "slider":
                # Value label below header
                value_label = ctk.CTkLabel(param_frame, text="0.00", font=("Inter", 12))
                value_label.grid(row=1, column=0, padx=10, sticky="ew")

                # Slider below value label
                slider = ctk.CTkSlider(
                    param_frame, from_=from_, to=to,
                    command=lambda value: value_label.configure(text=f"{float(value):.2f}")
                )
                slider.grid(row=2, column=0, padx=10, sticky="ew")

                self.tes_params[label_text] = slider


            else:  # If widget_type is "entry"
                entry = ctk.CTkEntry(param_frame)
                entry.grid(row=1, column=0, padx=10, pady=10, sticky="ew")  # Below header frame
                self.tes_params[label_text] = entry
        # Placed below label

        add_tes_parameter(tes_frame, "Seasonal Periods", "slider", 1, 12, row_index=0)
        add_tes_parameter(tes_frame, "Trend", "entry", row_index=1)
        add_tes_parameter(tes_frame, "Seasonal", "entry", row_index=2)
        add_tes_parameter(tes_frame, "Smoothing Level", "slider", 0, 1, row_index=3)
        add_tes_parameter(tes_frame, "Smoothing Trend", "slider", 0, 1, row_index=4)
        add_tes_parameter(tes_frame, "Smoothing Seasonal", "slider", 0, 1, row_index=5)

        frame.sma_slider_frame = sma_slider_frame
        frame.tes_frame = tes_frame

        return frame
    
    def create_scaling_encoding_frame(self):
        
        """Creates Scaling & Encoding tab with sliders."""
        frame = ctk.CTkFrame(self.segment_container, fg_color="#E0E0E0", corner_radius=10)
        frame.grid_columnconfigure(0, weight=1)

        def create_info_button(parent, text, row, column):
            """Creates an inline info button next to the label."""
            button = Button(parent, text="", image=self.Info_button_image, width=8, height=8,
                            command=lambda: self.show_info_dialog(text))
            button.grid(row=row, column=column, padx=5, sticky="w")

        # 🔹 Test Size Slider
        test_size_frame = ctk.CTkFrame(frame, fg_color="#D1D1D1", corner_radius=10)
        test_size_frame.grid(row=0, column=0, padx=10, pady=15, sticky="nsew")

        test_size_label = ctk.CTkLabel(test_size_frame, text="Test Size", font=("Inter", 12, "bold"), fg_color="#A0A0A0")
        test_size_label.grid(row=0, column=0, sticky="nesw")
        create_info_button(test_size_frame, "Defines the proportion of the dataset used for testing.", row=0, column=1)

        test_size_value_label = ctk.CTkLabel(test_size_frame, text="Value: 0.2", font=("Inter", 12))
        test_size_value_label.grid(row=1, column=0, pady=5)

        self.test_size_slider = ctk.CTkSlider(test_size_frame, from_=0.0, to=1.0,
                                            command=lambda value: test_size_value_label.configure(text=f"Value: {float(value):.2f}"))
        self.test_size_slider.set(0.2)
        self.test_size_slider.grid(row=2, column=0, padx=10, sticky="ew")

        # 🔹 Random State Slider
        random_state_frame = ctk.CTkFrame(frame, fg_color="#D1D1D1", corner_radius=10)
        random_state_frame.grid(row=1, column=0, padx=10, pady=15, sticky="nsew")

        random_state_label = ctk.CTkLabel(random_state_frame, text="Random State", font=("Inter", 12, "bold"), fg_color="#A0A0A0")
        random_state_label.grid(row=0, column=0, sticky="nesw")
        create_info_button(random_state_frame, "Seed value for reproducibility in data splitting.", row=0, column=1)

        random_state_value_label = ctk.CTkLabel(random_state_frame, text="Value: 42", font=("Inter", 12))
        random_state_value_label.grid(row=1, column=0, pady=5)

        self.random_state_slider = ctk.CTkSlider(random_state_frame, from_=0, to=100,
                                                command=lambda value: random_state_value_label.configure(text=f"Value: {int(value)}"))
        self.random_state_slider.set(42)
        self.random_state_slider.grid(row=2, column=0, padx=10, sticky="ew")

        return frame


    def toggle_smoothing_options(self, frame, method):
        """Toggles between SMA and TES parameters using grid layout."""
        if method == "SMA":
            frame.sma_slider_frame.grid()
            frame.tes_frame.grid_remove()
        else:
            frame.sma_slider_frame.grid_remove()
            frame.tes_frame.configure(height=250)
            frame.tes_frame.grid()



    def toggle_slider(self, frame, show):
        """Shows or hides the slider based on radio button selection."""
        if show:
            frame.slider_frame.grid()
        else:
            frame.slider_frame.grid_remove()

    def show_info_dialog(self, text):
        """Displays an information dialog box."""
        dialog = ctk.CTkToplevel(self)
        dialog.title("Information")
        dialog.geometry("300x150")
        dialog.grab_set()
        ctk.CTkLabel(dialog, text=text, font=("Inter", 12)).pack(pady=20)
        ctk.CTkButton(dialog, text="OK", command=dialog.destroy).pack()

    def load_csv_columns(self, file_path):
        """Loads column names from the uploaded CSV file and updates dropdown & checkboxes."""
        try:
            df = pd.read_csv(file_path)
            column_names = df.columns.tolist()[1:]  # Extract column names

            # Dropdown ComboBox (Centered)
            self.dropdown = ctk.CTkComboBox(self.graph_frame, values=column_names,command=self.update_boxplot,width=280,justify="center")
            self.dropdown.grid(row=0, column=0, padx=10, pady=20, sticky="n")
            self.dropdown.set(column_names[0] if column_names else "Select Column")

            for widget in self.scroll_frame.winfo_children():
                widget.destroy()  # Clear previous checkboxes

            for col in column_names:
                checkbox = ctk.CTkCheckBox(self.scroll_frame, text=col)
                checkbox.grid(sticky="w", padx=5, pady=2)

          

        except Exception as e:
            print("Error loading CSV:", str(e))


    


    def change_segment(self, segment_name):
        """Switch between segment frames while controlling access."""
        segment_order = ["Select Filter Process", "Outlier Detection", "Interpolation", "Smoothing"]
        
        # Ensure all previous segments are completed before allowing the switch
        if segment_name in segment_order:
            selected_index = segment_order.index(segment_name)
            for i in range(selected_index):
                if not self.segment_completion[segment_order[i]]:
                    return  # Prevent access if a previous segment is incomplete

        # If allowed, switch segment
        if self.current_segment:
            self.current_segment.grid_forget()

        # ✅ Show correct frame when Scaling & Encoding is selected directly
        if segment_name == "Scaling & Encoding":
            self.current_segment = self.create_scaling_encoding_frame()
            self.segmented_frame.configure(values=["Scaling & Encoding"])  # Only show this tab
        else:
            self.current_segment = self.segments[segment_name]
            self.segmented_frame.configure(values=self.visible_segments)  # Maintain available tabs

        self.current_segment.grid(row=1, column=0, sticky="nsew")
        self.segmented_frame.set(segment_name)


    def submit_action(self):
        """Handles segment transitions and submission logic."""
        current_segment = self.segmented_frame.get()  # Get the active segment

        # If already completed, move to the next segment instead of re-submitting
        if self.segment_completion[current_segment]:
            self.move_to_next_segment()
            return

        self.segment_completion[current_segment] = True  # Mark as completed
        print(f"{current_segment} completed!")

        # Lock the completed segment
        if current_segment in self.segments:
            self.lock_segment(self.segments[current_segment])

        # Print parameter values based on segment
        if current_segment == "Outlier Detection":
            print(self.radio_var.get())
            print(self.slider.get())
            self.run_outlier_detection()

        elif current_segment == "Interpolation":
            print(self.interpolation_radio_var.get())
            self.run_interpolation()

        elif current_segment == "Smoothing":
            print(self.smoothing_radio_var.get())
            print(self.sma_slider.get())
            self.run_smoothing()

            # ✅ Print TES Parameters if TES is selected
            if self.smoothing_radio_var.get() == "TES":
                print("\n--- TES Parameters ---")
                for key, widget in self.tes_params.items():
                    if isinstance(widget, ctk.CTkSlider):
                        print(f"{key}: {widget.get()}")
                    elif isinstance(widget, ctk.CTkEntry):
                        print(f"{key}: {widget.get()}")

        elif current_segment == "Scaling & Encoding":
            print("\n--- Scaling & Encoding Parameters ---")
            print(f"Test Size: {self.test_size_slider.get()}")
            print(f"Random State: {self.random_state_slider.get()}")
            self.run_scaling_and_encoding()

        # ✅ Remove Filtering Segments After Smoothing Completion
        if current_segment == "Smoothing":
            self.visible_segments = ["Scaling & Encoding"]

        # Enable the next segment in the segmented frame
        self.move_to_next_segment()


    def move_to_next_segment(self):
        """Move to the next available segment after submission."""
        segment_order = ["Select Filter Process", "Outlier Detection", "Interpolation", "Smoothing"]
        current_segment = self.segmented_frame.get()
        
        # Check the index of the current segment
        if current_segment == "Select Filter Process":
            selected_process = self.process_radio_var.get()
            if selected_process == "Filtering Method":
                self.visible_segments = ["Outlier Detection"]
            else:
                self.visible_segments = ["Scaling & Encoding"]
                self.change_segment("Scaling & Encoding")
                return  # Prevent unnecessary switching

        elif current_segment == "Outlier Detection":
            self.visible_segments.append("Interpolation")

        elif current_segment == "Interpolation":
            self.visible_segments.append("Smoothing")

        elif current_segment == "Smoothing":
            # ✅ Remove previous tabs & show only Scaling & Encoding
            self.visible_segments = ["Scaling & Encoding"]

        elif current_segment == "Scaling & Encoding":
            # ✅ Hide submit button once Scaling & Encoding is completed
            self.submit_button.configure(state="disabled")
            return

        self.segmented_frame.configure(values=self.visible_segments)
        self.change_segment(self.visible_segments[-1])

    def lock_segment(self, frame):
        """Disable all widgets in the given segment."""
        for child in frame.winfo_children():
            if isinstance(child, (ctk.CTkRadioButton, ctk.CTkSlider, ctk.CTkEntry, ctk.CTkCheckBox, ctk.CTkComboBox)):
                child.configure(state="disabled")

    def preview_csv(self):
        """Opens a new popup window to display the CSV file with scrollbars."""
        if not self.file_path:
            messagebox.showerror("Error", "No CSV file selected!")
            return

        # Read the CSV file
        try:
            df = pd.read_csv(self.file_path)  # Load CSV
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open CSV: {e}")
            return

        # Create a new popup window
        preview_window = ctk.CTkToplevel(self)
        preview_window.title("CSV Preview")
        preview_window.geometry("900x500")
        preview_window.grab_set()

        # Create a frame for the Treeview
        frame = tk.Frame(preview_window)
        frame.pack(fill="both", expand=True)

        # Treeview (table) widget
        tree = ttk.Treeview(frame, columns=list(df.columns), show="headings")

        # Add column headers
        for col in df.columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)  # Adjust column width

        # Insert rows (limit to first 50 rows to avoid UI lag)
        for index, row in df.head(50).iterrows():
            tree.insert("", "end", values=list(row))

        # Add vertical scrollbar
        v_scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscroll=v_scrollbar.set)

        # Add horizontal scrollbar
        h_scrollbar = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)
        tree.configure(xscroll=h_scrollbar.set)

        # Pack elements
        tree.pack(side="top", fill="both", expand=True)
        v_scrollbar.pack(side="right", fill="y")
        h_scrollbar.pack(side="bottom", fill="x")

    def update_boxplot(self, column_name):
        """Triggered when a new column is selected in the dropdown."""
        self.column_name = column_name

        # Show loading text
        self.show_loading_message()

        # Generate plot asynchronously to prevent UI freezing
        threading.Thread(target=lambda: self.plot_boxplot(column_name), daemon=True).start()

    def show_loading_message(self):
        """Displays a loading message in the graph display area."""
        for widget in self.graph_display.winfo_children():
            widget.destroy()

        loading_label = ctk.CTkLabel(self.graph_display, text="Loading...", font=("Inter", 14, "bold"))
        loading_label.place(relx=0.5, rely=0.5, anchor="center")





    def plot_boxplot(self, column_name):
        """Generates and embeds an interactive boxplot with UI enhancements."""
        if column_name not in self.data.columns:
            return

        # Clear previous widgets in the graph display area
        for widget in self.graph_display.winfo_children():
            widget.destroy()

        # Create Matplotlib figure
        fig, ax = plt.subplots(figsize=(7, 4))  # Slightly larger size
        fig.patch.set_facecolor("#E0E0E0")  # Match UI theme
        ax.set_facecolor("#E0E0E0")

        # Generate Boxplot with Better Formatting
        box = ax.boxplot(self.data[column_name], vert=False, patch_artist=True, widths=0.6,
                        boxprops=dict(facecolor='lightblue', edgecolor='black', linewidth=1.2),
                        medianprops=dict(color='red', linewidth=1.5),
                        whiskerprops=dict(color='black', linewidth=1.2, linestyle="--"))

        # Improve readability
        ax.set_title(f"Box Plot of {column_name}", fontsize=13, fontweight="bold")
        ax.set_xlabel(column_name, fontsize=11)
        ax.tick_params(axis="x", labelsize=10)
        ax.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.7)

        # Enable Zooming and Panning with Scroll Wheel
        def on_scroll(event):
            """Handles zooming on mouse scroll."""
            base_scale = 1.1
            scale_factor = base_scale if event.step > 0 else 1 / base_scale

            xlim = ax.get_xlim()
            x_range = (xlim[1] - xlim[0]) * scale_factor
            ax.set_xlim([xlim[0] + x_range * 0.1, xlim[1] - x_range * 0.1])
            fig.canvas.draw()

        # Show data values on hover
        tooltip = ax.annotate("", xy=(0, 0), xytext=(15, 15),
                            textcoords="offset points",
                            bbox=dict(boxstyle="round,pad=0.3", fc="lightgray", ec="black", lw=1),
                            arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=0.2"),
                            fontsize=9, visible=False)

        def on_hover(event):
            """Displays value tooltips when hovering over the boxplot."""
            if event.inaxes == ax:
                for i, line in enumerate(box["medians"]):
                    if line.contains(event)[0]:
                        value = self.data[column_name].median()
                        tooltip.set_text(f"Median: {value:.2f}")
                        tooltip.set_position((event.xdata, event.ydata))
                        tooltip.set_visible(True)
                        fig.canvas.draw_idle()
                        return
            tooltip.set_visible(False)
            fig.canvas.draw_idle()

        # Connect the scroll and hover events
        fig.canvas.mpl_connect("scroll_event", on_scroll)
        fig.canvas.mpl_connect("motion_notify_event", on_hover)

        # Embed Matplotlib Figure inside Tkinter Frame
        canvas = FigureCanvasTkAgg(fig, master=self.graph_display)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill="both", expand=True)

        # Add Toolbar for Navigation (Zoom, Pan, Save)
        toolbar_frame = ctk.CTkFrame(self.graph_display, fg_color="#E0E0E0")  # Match toolbar bg color
        toolbar_frame.pack(side="top", fill="x")

        toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)
        toolbar.config(background="#E0E0E0")  # Set toolbar background
        for child in toolbar.winfo_children():
            child.config(bg="#E0E0E0")  # Change toolbar button backgrounds

        toolbar.update()

        # Render the plot
        canvas.draw()




    def send_request(self, process_name, json_data):
        """Send the request to the Django backend and return the response."""
 
        try:
           
            response = requests.post(
                    f"http://127.0.0.1:8000/api/{process_name}/",
                    json=json_data
            )
 
            if response.status_code == 200:
                    response_data = response.json()
                    print(response_data)
                    if process_name == "outlier_detection" and "cleaned_data" in response_data:
                        self.cleaned_data = response_data["cleaned_data"]  # Store cleaned data JSON
                    elif process_name == "interpolation" and "interpolated_data" in response_data:
                        self.interpolated_data = response_data["interpolated_data"]  # Store interpolated data JSON
                    elif process_name == "smoothing" and "smoothed_data" in response_data:
                        self.smoothed_data = response_data["smoothed_data"]  # Store smoothed data JSON
                    return response_data
            else:
                    messagebox.showerror(
                        "Error", response.json().get('error', 'File upload failed.')
                    )
        except Exception as e:
                messagebox.showerror("Error", str(e))
 
    def run_outlier_detection(self):
        """Runs outlier detection and updates the data object."""
        selected_columns = []
        for child in self.scroll_frame.winfo_children():
            if isinstance(child, ctk.CTkCheckBox) and child.get():
                selected_columns.append(child.cget("text"))  # Get checkbox label as column name
        dataobject = DataObject()
        dataobject.data_filtering["filepath"] = self.file_path
        dataobject.data_filtering["Outlier Detection"]["Method"] = self.radio_var.get()
        dataobject.data_filtering["Outlier Detection"]["Parameters"]["contamination"] = float(self.slider.get())
        dataobject.data_filtering["Outlier Detection"]["Parameters"]["column_names"]= selected_columns
        
        # Convert DataObject to JSON
        json_data = {"dataobject": dataobject.to_dict()}
        print(json_data)
        # Send request
        self.send_request("outlier_detection", json_data)

    def run_interpolation(self):
        """Runs interpolation and updates the data object."""
        if not hasattr(self, "cleaned_data"):
            messagebox.showerror("Error", "Cleaned data is missing. Please run Outlier Detection first.")
            return
        
        json_data = {
            "cleaned_data": self.cleaned_data  
        }
        print(type(self.cleaned_data))
        # Send request to backend
        self.send_request("interpolation", json_data)
        
    def run_smoothing(self):
        """Runs smoothing and updates the data object."""
        if not hasattr(self, "interpolated_data"):
            messagebox.showerror("Error", "Interpolated data is missing. Please run Outlier Detection first and then Interpolation.")
            return
        dataobject = DataObject()
        dataobject.data_filtering["Smoothing"]["Method"] = self.smoothing_radio_var.get()
        
        # If SMA is selected, store window size
        if self.smoothing_radio_var.get() == "SMA":
            dataobject.data_filtering["Smoothing"]["parameters"]["window_size"] = int(round(self.sma_slider.get()))
    
        # If TES is selected, store TES parameters
        elif self.smoothing_radio_var.get() == "TES":
            tes_params = {}
            for key, widget in self.tes_params.items():
                if isinstance(widget, ctk.CTkSlider):
                    tes_params[key] = float(widget.get())  # Get float value from sliders
                elif isinstance(widget, ctk.CTkEntry):
                    tes_params[key] = widget.get()  # Get text value from entries

        # Store TES parameters in DataObject
        dataobject.data_filtering["Smoothing"]["parameters"].update(tes_params)
        
        # Convert DataObject to JSON
        json_data = {"dataobject": dataobject.to_dict()}
        print(json_data)
        json_data = {
            "dataobject": dataobject.to_dict(),
            "interpolated_data": self.interpolated_data 
        }
        print("going to send request to smoothing")
        # Send request to backend
        self.send_request("smoothing", json_data)
        
    def run_scaling_and_encoding(self):
        """Runs scaling and encoding and updates the data object."""
        if not hasattr(self, "smoothed_data"):
            messagebox.showerror("Error", "Smoothed data is missing. Please run Outlier Detection, Interpolation and Smoothing.")
            return
        dataobject = DataObject()
        # to be edited need to add the user given test-size and random state
        dataobject.data_filtering["Train-Test Split"]["parameters"]["test_size"] = int(round(self.test_size_slider.get()))
        dataobject.data_filtering["Train-Test Split"]["parameters"]["random_state"] = int(round(self.random_state_slider.get()))
        
        # Convert DataObject to JSON
        json_data = {"dataobject": dataobject.to_dict()}
        print(self.smoothed_data)
        json_data = {
            "dataobject": dataobject.to_dict(),
            "smoothed_data": self.smoothed_data 
        }
        print("going to send request to scaling")
        # Send request to backend
        self.send_request("scaling_encoding", json_data)