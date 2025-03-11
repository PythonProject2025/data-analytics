import customtkinter as ctk
from tkinter import Button, PhotoImage, Toplevel, messagebox
import requests
from src.models.data_object_class import DataObject
from src.assets_management import assets_manage, load_image
import pandas as pd



class DataFilteringPage(ctk.CTkFrame):
    def __init__(self, parent,file_path,file_name=" "):
        super().__init__(parent, corner_radius=0)

        self.file_name = file_name
        self.file_path=file_path
        self.current_segment_index = 0
        window_height = self.winfo_screenheight()  # Get the total screen height
        right_frame_height = int(0.8 * window_height)  # 60% of the screen height

        self.segment_completion = {
                                    "Outlier Detection": False,
                                    "Interpolation": False,
                                    "Smoothing": False
                                  }
        self.visible_segments = ["Outlier Detection"]



        # Configure grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=8)  # Left side (70%)
        self.grid_columnconfigure(1, weight=2)  # Right side (30%)

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
        self.graph_display.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")  # Expands to fill space


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
        self.segment_order = ["Outlier Detection", "Interpolation", "Smoothing"]

        # Create segment frames
        self.segments = {
            "Outlier Detection": self.create_segment_frame(),
            "Interpolation": self.create_interpolation_frame(),
            "Smoothing": self.create_smoothing_frame(),
        }

        # Submit Button
        self.submit_button = ctk.CTkButton(self.right_frame, text="Submit", command=self.submit_action)
        self.submit_button.grid(row=2, column=0, pady=10)

        # Show default segment
        self.current_segment = None
        self.change_segment("Outlier Detection")

        if self.file_path:  
            self.load_csv_columns(self.file_path)
        
    



    def create_segment_frame(self):
        """Creates a frame for each segment."""
        frame = ctk.CTkFrame(self.segment_container, fg_color="#E0E0E0", corner_radius=10)
        frame.grid_columnconfigure(0, weight=1)

        def create_info_button(parent, text):
            button = Button(parent, text="", image=self.Info_button_image, width=8, height=8, command=lambda: self.show_info_dialog(text))
            button.grid(row=0, column=1, padx=5, sticky="e")

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
            button.grid(row=0, column=1, padx=5, sticky="e")

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

    def change_segment(self, segment_name):
        """Switch between segment frames while controlling access."""
        segment_order = ["Outlier Detection", "Interpolation", "Smoothing"]

        # Ensure all previous segments are completed before allowing the switch
        selected_index = segment_order.index(segment_name)
        for i in range(selected_index):
            if not self.segment_completion[segment_order[i]]:
                return  # Prevent access if a previous segment is incomplete

        # If allowed, switch segment
        if self.current_segment:
            self.current_segment.grid_forget()
        
        self.current_segment = self.segments[segment_name]
        self.current_segment.grid(row=1, column=0, sticky="nsew")
        self.segmented_frame.set(segment_name)  # Ensure correct highlighting

    def load_csv_columns(self, file_path):
        """Loads column names from the uploaded CSV file and updates dropdown & checkboxes."""
        try:
            df = pd.read_csv(file_path)
            column_names = df.columns.tolist()[1:]  # Extract column names

            # Dropdown ComboBox (Centered)
            self.dropdown = ctk.CTkComboBox(self.graph_frame, values=column_names)
            self.dropdown.grid(row=0, column=0, padx=10, pady=10, sticky="n")
            self.dropdown.set(column_names[0] if column_names else "Select Column")

            for widget in self.scroll_frame.winfo_children():
                widget.destroy()  # Clear previous checkboxes

            for col in column_names:
                checkbox = ctk.CTkCheckBox(self.scroll_frame, text=col)
                checkbox.grid(sticky="w", padx=5, pady=2)

          

        except Exception as e:
            print("Error loading CSV:", str(e))



    def submit_action(self):
        current_segment = self.segmented_frame.get()  # Get the active segment
        
        # If already completed, move to the next segment instead of re-submitting
        if self.segment_completion[current_segment]:
            self.move_to_next_segment()
            return

        self.segment_completion[current_segment] = True  # Mark as completed
        print(f"{current_segment} completed!")

        # Lock the completed segment
        self.lock_segment(self.segments[current_segment])

        # Enable the next segment in the segmented frame
        self.move_to_next_segment()
        if current_segment == "Outlier Detection":
            self.run_outlier_detection()
        elif current_segment == "Interpolation":
            print (self.interpolation_radio_var.get())

        elif current_segment == "Smoothing":
            print (self.smoothing_radio_var.get())
            print (self.sma_slider.get())
        # ✅ Print TES Parameters if TES is selected
        if self.smoothing_radio_var.get() == "TES":
            print("\n--- TES Parameters ---")
            for key, widget in self.tes_params.items():
                if isinstance(widget, ctk.CTkSlider):
                    print(f"{key}: {widget.get()}")
                elif isinstance(widget, ctk.CTkEntry):
                    print(f"{key}: {widget.get()}")

    def move_to_next_segment(self):
        """Move to the next available segment after submission."""
        segment_order = ["Outlier Detection", "Interpolation", "Smoothing"]
        current_segment = self.segmented_frame.get()
        current_index = segment_order.index(current_segment)

        # Unlock the next segment and update the header
        if current_index + 1 < len(segment_order):
            next_segment = segment_order[current_index + 1]
            if next_segment not in self.visible_segments:
                self.visible_segments.append(next_segment)  # Unlock the next process
                self.segmented_frame.configure(values=self.visible_segments)  # Update segment tab
            self.change_segment(next_segment)  # Move to next tab

        # Disable submit button if all processes are completed
        if all(self.segment_completion.values()):
            self.submit_button.configure(state="disabled")

    def lock_segment(self, frame):
        """Disable all widgets in the given segment."""
        for child in frame.winfo_children():
            if isinstance(child, (ctk.CTkRadioButton, ctk.CTkSlider, ctk.CTkEntry, ctk.CTkCheckBox, ctk.CTkComboBox)):
                child.configure(state="disabled")
                
    def send_request(self, process_name, json_data):
        """Send the request to the Django backend and return the response."""
 
        try:
           
            response = requests.post(
                    'http://127.0.0.1:8000/api/outlier_detection/',
                    json=json_data
            )
 
            if response.status_code == 200:
                    response_data = response.json()
                    print(response_data)
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
        
