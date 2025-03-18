import customtkinter as ctk
from tkinter import Button, PhotoImage, Toplevel,messagebox,filedialog
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
import json
import matplotlib.patches as patches




class DataFilteringPage(ctk.CTkFrame):
    def __init__(self, parent,file_path,file_name=" "):
        super().__init__(parent, corner_radius=0)

        self.parent = parent
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

        #self.add_export_send_buttons()

        # Show default segment
        self.current_segment = None
        self.change_segment("Select Filter Process")

        if self.file_path:  
            self.load_csv_columns(self.file_path)
        
        # Initial Boxplot for first column
        # if self.column_name:
        # self.plot_boxplot(self.column_name)

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
        
         # ✅ Check for column selection if in "Outlier Detection"
        if current_segment == "Outlier Detection":
            selected_columns = [
                child.cget("text") for child in self.scroll_frame.winfo_children()
                if isinstance(child, ctk.CTkCheckBox) and child.get()
            ]
            if not selected_columns:
                messagebox.showerror("Error", "You must select at least one column before proceeding!")
                return  # 🚫 Stop further execution

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

    
           # ✅ Update button visibility
        self.update_buttons_visibility()

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
        


    def plot_boxplot(self, column_name,cleaned=False):
        """Generates and embeds an interactive boxplot with UI enhancements."""
        if cleaned and hasattr(self, "cleaned_data")and isinstance(self.cleaned_data, pd.DataFrame):
            plot_data = self.cleaned_data
            print("ommala")  # Use cleaned data from response
        else:
            plot_data = self.data  # Use raw CSV data

        if column_name not in plot_data.columns:
            return

        # Clear previous widgets in the graph display area
        for widget in self.graph_display.winfo_children():
            widget.destroy()

  

        # Create Matplotlib figure
        fig, ax = plt.subplots(figsize=(7, 4))  # Slightly larger size
        fig.patch.set_facecolor("#E0E0E0")  # Match UI theme
        ax.set_facecolor("#E0E0E0")

        # Generate Boxplot with Better Formatting
        box = ax.boxplot(plot_data[column_name], vert=False, patch_artist=True, widths=0.6,
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
                        value = plot_data[column_name].median()
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

    def plot_line_graph(self, column_name, original_data, processed_data, title):
        """
        Plots a line graph for original and processed data (interpolation or smoothing).
        
        Parameters:
            column_name (str): The name of the column to plot.
            original_data (pd.Series or np.ndarray): The original data.
            processed_data (pd.Series or np.ndarray): The processed data (interpolated or smoothed).
            title (str): The title of the plot.
        """
        # Ensure data is a Pandas Series to prevent errors
        if isinstance(original_data, np.ndarray):
            original_data = pd.Series(original_data, name=column_name)

        if isinstance(processed_data, np.ndarray):
            processed_data = pd.Series(processed_data, name=column_name)

        # Clear previous widgets in the graph display area
        for widget in self.graph_display.winfo_children():
            widget.destroy()

        # Create Matplotlib figure
        fig, ax = plt.subplots(figsize=(7, 4))  # Slightly larger size
        fig.patch.set_facecolor("#E0E0E0")  # Match UI theme
        ax.set_facecolor("#E0E0E0")

        # Plot original data
        ax.plot(original_data.index, original_data, color="blue", label="Original Data")

        # Plot processed data
        ax.plot(processed_data.index, processed_data, color="red", label=title)

        # Improve readability
        ax.set_title(f"{title} for {column_name}", fontsize=13, fontweight="bold")
        ax.set_xlabel("Index", fontsize=11)
        ax.set_ylabel(column_name, fontsize=11)
        ax.legend()
        ax.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.7)

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
                    #print(response_data)
                    if process_name == "outlier_detection" and "cleaned_data" in response_data:
                        self.cleaned_data = response_data["cleaned_data"]  # Store cleaned data JSON
                        #print(self.cleaned_data)
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
        self.selected_columns = []
        for child in self.scroll_frame.winfo_children():
            if isinstance(child, ctk.CTkCheckBox) and child.get():
                self.selected_columns.append(child.cget("text"))  # Get checkbox label as column name

            #  Restriction: Ensure at least one column is selected
        if not self.selected_columns:
            messagebox.showerror("Error", "You must select at least one column before proceeding!")
            return 

        dataobject = DataObject()
        dataobject.data_filtering["filepath"] = self.file_path
        dataobject.data_filtering["Outlier Detection"]["Method"] = self.radio_var.get()
        dataobject.data_filtering["Outlier Detection"]["Parameters"]["contamination"] = float(self.slider.get())
        dataobject.data_filtering["Outlier Detection"]["Parameters"]["column_names"]= self.selected_columns
        
        json_data = {"dataobject": dataobject.to_dict()}
        #print(json_data)
        # Send request
        


        self.show_loading_message()
        self.graph_display.update_idletasks()
        response =self.send_request("outlier_detection", json_data)

        if response and "cleaned_data" in response:
            self.cleaned_data_str = response["cleaned_data"]  # Extract cleaned data as string

        try:
            # ✅ Convert JSON string to Python Dictionary
            cleaned_data_dict = json.loads(self.cleaned_data_str)

            # ✅ Convert Dictionary to DataFrame
            self.cleaned_data = pd.DataFrame.from_dict(cleaned_data_dict)
            print(self.cleaned_data)
            print(type(self.cleaned_data))

            # ✅ Ensure cleaned data is properly formatted before updating UI
            if not self.cleaned_data.empty:
                self.update_dropdown(self.selected_columns)  # Update dropdown with selected columns
                self.plot_boxplot(self.selected_columns[0], cleaned=True)  # Plot cleaned data

        except json.JSONDecodeError as e:
            print("❌ Error: Failed to parse cleaned data JSON:", e)
            self.cleaned_data = None
       

    def run_interpolation(self):
                
        if not hasattr(self, "cleaned_data"):
            messagebox.showerror("Error", "Cleaned data is missing. Please run Outlier Detection first.")
            return

        json_data = {
            "cleaned_data": self.cleaned_data_str
        }
        print("going to send request to interpolation")
        # Send request to backend
        response = self.send_request("interpolation", json_data)

        if response and "interpolated_data" in response:
            self.interpolated_data_str = response["interpolated_data"]  # Extract interpolated data as string

            try:
                # Convert JSON string to Python Dictionary
                interpolated_data_dict = json.loads(self.interpolated_data_str)

                # Convert Dictionary to DataFrame
                self.interpolated_data = pd.DataFrame.from_dict(interpolated_data_dict)
                print(self.interpolated_data)
                print(type(self.interpolated_data))

                # Ensure interpolated data is properly formatted before updating UI
                if not self.interpolated_data.empty:

                    # Plot interpolation data
                    self.update_dropdown(self.selected_columns)
                    self.plot_line_graph(
                        column_name=self.selected_columns[0],
                        original_data=self.data[self.selected_columns[0]],
                        processed_data=self.interpolated_data[self.selected_columns[0]],
                        title="Interpolated Data"
                    )

            except json.JSONDecodeError as e:
                print("❌ Error: Failed to parse interpolated data JSON:", e)
                self.interpolated_data = None
        
    def run_smoothing(self):
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
        json_data = {
            "dataobject": dataobject.to_dict(),
            "interpolated_data": self.interpolated_data_str
        }
        print("going to send request to smoothing")
        # Send request to backend
        response = self.send_request("smoothing", json_data)

        if response and "smoothed_data" in response:
            self.smoothed_data_str = response["smoothed_data"]  # Extract smoothed data as string

            try:
                # Convert JSON string to Python Dictionary
                smoothed_data_dict = json.loads(self.smoothed_data_str)

                # Convert Dictionary to DataFrame
                self.smoothed_data = pd.DataFrame.from_dict(smoothed_data_dict)
                print(self.smoothed_data)
                print(type(self.smoothed_data))

                # Ensure smoothed data is properly formatted before updating UI
                if not self.smoothed_data.empty:
                    # Plot smoothing data
                    self.update_dropdown(self.selected_columns)
                    self.plot_line_graph(
                        column_name=self.selected_columns[0],
                        original_data=self.data[self.selected_columns[0]],
                        processed_data=self.smoothed_data[self.selected_columns[0]],
                        title="Smoothed Data"
                    )

            except json.JSONDecodeError as e:
                print("❌ Error: Failed to parse smoothed data JSON:", e)
                self.smoothed_data = None

    def run_scaling_and_encoding(self):
        """Runs scaling and encoding on raw data if filtering is not done, otherwise uses smoothed data."""
        
        # Check if smoothed data exists
        if hasattr(self, "smoothed_data"):
            print("✅ Using Smoothed Data for Scaling & Encoding")
            data_str = self.smoothed_data_str  # Use stored JSON string of smoothed data
        else:
            print("⚠️ Smoothed Data Not Found. Using Raw Data for Scaling & Encoding")
            
            if not hasattr(self, "data"):
                messagebox.showerror("Error", "No raw data found! Please upload a dataset first.")
                return
            
            data_str = self.data.to_json()  # Convert raw DataFrame to JSON

        dataobject = DataObject()
        dataobject.data_filtering["Train-Test Split"]["parameters"]["test_size"] = self.test_size_slider.get()
        dataobject.data_filtering["Train-Test Split"]["parameters"]["random_state"] = int(round(self.random_state_slider.get()))

        json_data = {
            "dataobject": dataobject.to_dict(),
            "smoothed_data": data_str  # Send data for scaling and encoding
        }

        print("Sending request to backend for Scaling & Encoding...")
        response = self.send_request("scaling_encoding", json_data)

        if response and "processed_data" in response:
            processed_data = response["processed_data"]

            if not isinstance(processed_data, dict):
                print("Error: Processed data is not a valid dictionary.")
                messagebox.showerror("Error", "Invalid processed data format received.")
                return
            
            # Ensure all columns have the same length
            column_lengths = [len(v) for v in processed_data.values()]
            min_length = min(column_lengths)

            # Trim or pad columns to match the minimum length
            cleaned_data = {k: list(v)[:min_length] for k, v in processed_data.items()}  # ✅ Ensure v is a list
            
            print(type(cleaned_data))

            # Convert to DataFrame
            self.scaled_encoded_data = pd.DataFrame(cleaned_data)

            print("✅ Scaled & Encoded Data received:")
            print(self.scaled_encoded_data)

            # Show preview of the scaled and encoded data
            self.preview_scaled_encoded_data()

        else:
            print("❌ Error: No processed data received from backend.")
            messagebox.showerror("Error", "Failed to retrieve scaled and encoded data.")



    def preview_scaled_encoded_data(self):
        """Opens a new popup window to display the scaled and encoded data."""
        if not hasattr(self, "scaled_encoded_data") or self.scaled_encoded_data.empty:
            messagebox.showerror("Error", "No scaled and encoded data available!")
            return

        # Create a new popup window
        preview_window = ctk.CTkToplevel(self)
        preview_window.title("Scaled and Encoded Data Preview")
        preview_window.geometry("900x500")
        preview_window.grab_set()
    
        # Create a frame for the Treeview
        frame = tk.Frame(preview_window)
        frame.pack(fill="both", expand=True)

        # Treeview (table) widget
        tree = ttk.Treeview(frame, columns=list(self.scaled_encoded_data.columns), show="headings")

        # Add column headers
        for col in self.scaled_encoded_data.columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)  # Adjust column width

        # Insert rows (limit to first 50 rows to avoid UI lag)
        for index, row in self.scaled_encoded_data.head(50).iterrows():
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

        print("✅ Scaled & Encoded Data preview displayed successfully!")

    
    def update_dropdown(self, selected_columns):
        """Update the dropdown with selected columns and dynamically set the callback function."""
        if hasattr(self, "dropdown"):
            self.dropdown.destroy()  # Remove the old dropdown

        # Determine the current process
        current_segment = self.segmented_frame.get()

        # Set appropriate callback function for dropdown
        if current_segment == "Outlier Detection":
            command = lambda col: self.plot_boxplot(col, cleaned=True)

        elif current_segment == "Interpolation":
            command = lambda col: self.plot_line_graph(
                column_name=col,
                original_data=self.data[col],  # Ensure Pandas Series
                processed_data=self.interpolated_data[col],  # Ensure Pandas Series
                title="Interpolated Data"
            ) if col in self.interpolated_data.columns else None

        elif current_segment == "Smoothing":
            command = lambda col: self.plot_line_graph(
                column_name=col,
                original_data=self.data[col],  # Ensure Pandas Series
                processed_data=self.smoothed_data[col],  # Ensure Pandas Series
                title="Smoothed Data"
            ) if col in self.smoothed_data.columns else None

        elif current_segment == "Scaling & Encoding":
            self.preview_scaled_encoded_data()  # Show preview for Scaling & Encoding
            return  # No need to update dropdown

        else:
            command = lambda col: self.plot_boxplot(col)

        # Create the updated dropdown with correct command
        self.dropdown = ctk.CTkComboBox(
            self.graph_frame,
            values=selected_columns,
            command=command,  # Dynamic function assignment
            width=280,
            justify="center"
        )
        self.dropdown.grid(row=0, column=0, padx=10, pady=20, sticky="n")
        self.dropdown.set(selected_columns[0] if selected_columns else "Select Column")

   

    def export_data(self):
        """Exports the processed data based on the latest completed step."""
        if self.segment_completion.get("Scaling & Encoding", False):
            data_to_export = self.scaled_encoded_data
            message = None  # No message box for final export
        elif self.segment_completion.get("Smoothing", False):
            data_to_export = self.smoothed_data
            message = "Only Smoothed data available for export."
        elif self.segment_completion.get("Interpolation", False):
            data_to_export = self.interpolated_data
            message = "Only Interpolated data available for export."
        elif self.segment_completion.get("Outlier Detection", False):
            data_to_export = self.cleaned_data
            message = "Only Outlier Cleaned data available for export."
        else:
            messagebox.showerror("Error", "No processed data available for export!")
            return

        # ✅ Show message box before file dialog
        if message:
            messagebox.showinfo("Export Data", message)

        # ✅ Open file dialog after message box
        file_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                                filetypes=[("CSV files", "*.csv"), ("All Files", "*.*")],
                                                title="Save Processed Data")

        if file_path:
            data_to_export.to_csv(file_path, index=False)
            messagebox.showinfo("Success", "Data successfully exported!")


    def open_send_popup(self):
        """Opens a popup for selecting the destination page after Scaling & Encoding is completed."""
        if not hasattr(self, "scaled_encoded_data"):
            messagebox.showerror("Error", "Scaling & Encoding must be completed before sending the file.")
            return

        # Create Popup Window
        popup = ctk.CTkToplevel(self)
        popup.title("Select Destination")
        popup.geometry("400x200")
        popup.grab_set()

        ctk.CTkLabel(popup, text="Choose the Process :", font=("Inter", 14, "bold")).pack(pady=20)

        # Dropdown Menu
        process_var = ctk.StringVar(value="Regression & Classification")  # Default Value
        process_dropdown = ctk.CTkComboBox(popup, values=["Regression & Classification", "AI Model"], variable=process_var ,width=250)
        process_dropdown.pack(pady=10)

        def send_file():
            """Handles file sending based on the selected process."""
            selected_process = process_var.get()
            popup.destroy()  # Close popup

            # Navigate to the respective page with the file argument
            if selected_process == "Regression & Classification":
                self.parent.show_page("RegressionClassificationPage", file_data=self.scaled_encoded_data,file_name="Preprocessed_Data")
            else:
                self.parent.show_page("AIModelPage", file_data=self.scaled_encoded_data,file_name="Preprocessed_Data")

        ctk.CTkButton(popup, text="Proceed", command=send_file).pack(pady=10)

    def update_buttons_visibility(self):
    
        # ✅ Ensure Export Button is only created & visible after Outlier Detection is submitted
        if self.segment_completion.get("Outlier Detection", False) or self.segment_completion.get("Scaling & Encoding", False):
            self.add_export_send_buttons()  # ✅ Call button creation only after Outlier Detection

            # ✅ Show Export button after Outlier Detection is completed
        if hasattr(self, "cleaned_data"):
            self.export_button.grid()
            self.compare_button.grid()  # ✅ Compare button visible after outlier detection

        # ✅ Show Export button after Interpolation is completed
        if hasattr(self, "interpolated_data"):
            self.export_button.grid()
            self.compare_button.grid()

        # ✅ Show Export button after Smoothing is completed
        if hasattr(self, "smoothed_data"):
            self.export_button.grid()
            self.compare_button.grid()

        # ✅ Show Export button after Scaling & Encoding is completed and replace Compare with Send
        if hasattr(self, "scaled_encoded_data"):
            self.export_button.grid()
            self.compare_button.grid_remove()  # ✅ Hide Compare Button after Scaling & Encoding
            self.send_button.grid()  # ✅ Show Send Button



    def add_export_send_buttons(self):
        """Adds Export, Compare, and Send buttons to the main UI at the bottom-right corner below the right frame."""
        
        # ✅ Ensure button frame is added below the right frame
        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")  
        self.button_frame.grid(row=2, column=1, padx=10, pady=10, sticky="se")  # Bottom-right below right frame

        # ✅ Export Button (Initially Hidden)
        self.export_button = ctk.CTkButton(
            self.button_frame, text="Export", fg_color="transparent", border_width=2, border_color="black",
            text_color="black", command=self.export_data
        )
        self.export_button.grid(row=0, column=0, pady=5, padx=10, sticky="ew")
        self.export_button.grid_remove()  # Initially hidden

        # ✅ Compare Button (Initially Hidden, shown after Outlier Detection)
        self.compare_button = ctk.CTkButton(
            self.button_frame, text="Compare", fg_color="transparent", border_width=2, border_color="black",
            text_color="black", command=self.open_comparison_popup
        )
        self.compare_button.grid(row=0, column=1, pady=5, padx=10, sticky="ew")
        self.compare_button.grid_remove()  # Initially hidden

                # ✅ Send Button (Initially Hidden, shown after Scaling & Encoding)
        self.send_button = ctk.CTkButton(
            self.button_frame, text="Send", fg_color="transparent", border_width=2, border_color="black",
            text_color="black", command=self.open_send_popup
        )
        self.send_button.grid(row=0, column=1, pady=5, padx=10, sticky="ew")
        self.send_button.grid_remove()  # Initially hidden

    def open_comparison_popup(self):
        """Opens a popup window for comparing different stages of data processing."""
        
        # Create Popup Window
        self.compare_popup = ctk.CTkToplevel(self)
        self.compare_popup.title("Compare Data")
        self.compare_popup.geometry("900x500")
        self.compare_popup.grab_set()

        # Create Two Frames (Left & Right)
        left_frame = ctk.CTkFrame(self.compare_popup, fg_color="#E0E0E0", corner_radius=10)
        left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        right_frame = ctk.CTkFrame(self.compare_popup, fg_color="#E0E0E0", corner_radius=10)
        right_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # ✅ Dropdown for Selecting Graph or Data
        self.compare_type = ctk.StringVar(value="Graph")
        compare_dropdown = ctk.CTkComboBox(
            right_frame, values=["Graph", "Data"], variable=self.compare_type, width=150
        )
        compare_dropdown.grid(row=0, column=1, padx=10, pady=10, sticky="e")

        # ✅ Left Data Selection Dropdown
        left_options = ["Raw Data"]
        #if hasattr(self, "cleaned_data"): left_options.append("Outlier Cleaned Data")
        if hasattr(self, "interpolated_data"): left_options.append("Outlier Cleaned Data")
        if hasattr(self, "smoothed_data"): left_options.append("Interpolated Data")

        self.left_selection = ctk.StringVar(value=left_options[0])
        left_dropdown = ctk.CTkComboBox(
            left_frame, values=left_options, variable=self.left_selection, width=200
        )
        left_dropdown.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        # ✅ Right Data Selection Dropdown
        right_options = []
        if hasattr(self, "cleaned_data"): right_options.append("Outlier Cleaned Data")
        if hasattr(self, "interpolated_data"): (right_options.append("Interpolated Data") , right_options.remove("Outlier Cleaned Data"))
        if hasattr(self, "smoothed_data"): right_options.append("Smoothed Data"), right_options.remove("Interpolated Data")

        self.right_selection = ctk.StringVar(value=right_options[0] if right_options else "")
        right_dropdown = ctk.CTkComboBox(
            right_frame, values=right_options, variable=self.right_selection, width=200
        )
        right_dropdown.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        # ✅ Column Selection Dropdown
        self.column_selection = ctk.StringVar(value=self.selected_columns[0])
        column_dropdown = ctk.CTkComboBox(
            self.compare_popup, values=self.selected_columns, variable=self.column_selection, width=200
        )
        column_dropdown.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

            # ✅ Compare Button (Triggers Graph/Data Display)
        compare_button = ctk.CTkButton(
            right_frame, text="Compare", command=self.update_comparison_view, 
            fg_color="transparent", border_width=2, border_color="black", text_color="black"
        )
        compare_button.grid(row=0, column=2, pady=10, sticky="ew")

    def show_comparison_data(self, left_data, right_data, column_name):
        """Displays a side-by-side comparison of selected datasets in a table format, highlighting differences."""
        
        # Get the corresponding DataFrames
        left_df = self.get_data_by_name(left_data)
        right_df = self.get_data_by_name(right_data)

        if left_df is None or right_df is None:
            messagebox.showerror("Error", "Invalid Data Selection!")
            return

        # Extract the selected column
        if column_name not in left_df.columns or column_name not in right_df.columns:
            messagebox.showerror("Error", f"Column '{column_name}' not found in selected datasets!")
            return

        left_values = left_df[column_name].astype(str).tolist()  # Convert to list for comparison
        right_values = right_df[column_name].astype(str).tolist()

        # ✅ Create Comparison Popup Window
        compare_table_popup = ctk.CTkToplevel(self)
        compare_table_popup.title("Data Comparison")
        compare_table_popup.geometry("900x500")
        compare_table_popup.grab_set()

        # ✅ Create a frame to hold the Treeview (Table)
        frame = tk.Frame(compare_table_popup)
        frame.pack(fill="both", expand=True)

        # ✅ Treeview Widget for Side-by-Side Data Comparison
        tree = ttk.Treeview(frame, columns=("Index", "Left Data", "Right Data"), show="headings")

        # ✅ Add column headers
        tree.heading("Index", text="Index", anchor="center")
        tree.heading("Left Data", text=f"{left_data} ({column_name})", anchor="center")
        tree.heading("Right Data", text=f"{right_data} ({column_name})", anchor="center")

        tree.column("Index", width=50, anchor="center")
        tree.column("Left Data", width=200, anchor="center")
        tree.column("Right Data", width=200, anchor="center")

        # ✅ Insert rows with differences highlighted
        for i in range(min(len(left_values), len(right_values))):
            left_value = left_values[i]
            right_value = right_values[i]

            # Highlight changes in red
            tag = "changed" if left_value != right_value else ""

            tree.insert("", "end", values=(i, left_value, right_value), tags=(tag,))

        # ✅ Define a tag for changed values (Red color)
        tree.tag_configure("changed", background="lightcoral")

        # ✅ Add Scrollbars
        v_scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        h_scrollbar = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)
        tree.configure(yscroll=v_scrollbar.set, xscroll=h_scrollbar.set)

        # ✅ Pack elements
        tree.pack(side="top", fill="both", expand=True)
        v_scrollbar.pack(side="right", fill="y")
        h_scrollbar.pack(side="bottom", fill="x")



    def update_comparison_view(self):
        
        """Updates the comparison popup based on user selections."""
        compare_type = self.compare_type.get()
        left_data = self.left_selection.get()
        right_data = self.right_selection.get()
        column_name = self.column_selection.get()

        if compare_type == "Graph":
            self.plot_comparison_graph(left_data, right_data, column_name)
        else:
            self.show_comparison_data(left_data, right_data, column_name)

    def plot_comparison_graph(self, left_data, right_data, column_name):
        """Generates comparison graphs for selected datasets."""
        
        # Retrieve the corresponding DataFrames
        left_df = self.get_data_by_name(left_data)
        right_df = self.get_data_by_name(right_data)

        if left_df is None or right_df is None:
            messagebox.showerror("Error", "Invalid Data Selection!")
            return

        # Ensure column exists in both datasets
        if column_name not in left_df.columns or column_name not in right_df.columns:
            messagebox.showerror("Error", f"Column '{column_name}' not found in selected datasets!")
            return

        # ✅ Clear previous widgets in the compare popup
        for widget in self.compare_popup.winfo_children():
            if isinstance(widget, tk.Canvas):  
                widget.destroy()

        # ✅ Create Matplotlib Figure with Two Subplots (Side-by-Side)
        fig, axes = plt.subplots(1, 2, figsize=(10, 4))  # 2 side-by-side plots
        fig.patch.set_facecolor("#E0E0E0")  # Match UI Theme

        # ✅ Left Graph
        if left_data in ["Raw Data", "Outlier Cleaned Data"]:
            axes[0].boxplot(left_df[column_name], vert=False, patch_artist=True, 
                            boxprops=dict(facecolor='lightblue', edgecolor='black'),
                            medianprops=dict(color='red'))
            axes[0].set_title(f"{left_data} - Box Plot", fontsize=11)
        else:
            axes[0].plot(left_df[column_name], color="blue", label=left_data)
            axes[0].set_title(f"{left_data} - Line Graph", fontsize=11)

        # ✅ Right Graph
        if right_data in ["Raw Data", "Outlier Cleaned Data"]:
            axes[1].boxplot(right_df[column_name], vert=False, patch_artist=True, 
                            boxprops=dict(facecolor='lightcoral', edgecolor='black'),
                            medianprops=dict(color='red'))
            axes[1].set_title(f"{right_data} - Box Plot", fontsize=11)
        else:
            axes[1].plot(right_df[column_name], color="red", label=right_data)
            axes[1].set_title(f"{right_data} - Line Graph", fontsize=11)

        # ✅ Improve Layout
        for ax in axes:
            ax.grid(True, linestyle="--", alpha=0.5)

        # ✅ Embed the Matplotlib Figure inside Tkinter Frame
        canvas = FigureCanvasTkAgg(fig, master=self.compare_popup)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.grid(row=2, column=0, columnspan=2, pady=10, sticky="nsew")
        canvas.draw()

    def get_data_by_name(self, name):
        """Returns the corresponding DataFrame for the given name."""
        if name == "Raw Data":
            return self.data
        elif name == "Outlier Cleaned Data":
            return self.cleaned_data
        elif name == "Interpolated Data":
            return self.interpolated_data
        elif name == "Smoothed Data":
            return self.smoothed_data
        return None