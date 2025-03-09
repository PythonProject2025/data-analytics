import customtkinter as ctk
from tkinter import Button, PhotoImage, Toplevel
from src.assets_management import assets_manage, load_image


class DataFilteringPage(ctk.CTkFrame):
    def __init__(self, parent,file_name=" "):
        super().__init__(parent, corner_radius=0)

        self.file_name = file_name

        # Configure grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=9)  # Left side (70%)
        self.grid_columnconfigure(1, weight=1)  # Right side (30%)

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

        # Dropdown ComboBox (Centered)
        self.dropdown = ctk.CTkComboBox(self.graph_frame, values=["Option 1", "Option 2", "Option 3"])
        self.dropdown.grid(row=0, column=0, padx=10, pady=10, sticky="n")  # `sticky="n"` keeps it at the top

        # Graph Display Area (Expanded)
        self.graph_display = ctk.CTkFrame(self.graph_frame, fg_color="#D1D1D1", height=250, corner_radius=10)  # Increased Size
        self.graph_display.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")  # Expands to fill space


        self.Info_button_image = PhotoImage(file=assets_manage("info_B.png"))

        # Right Side Frame (Segmented Buttons)
        self.right_frame = ctk.CTkFrame(self, fg_color="#171821")
        self.right_frame.grid(row=0, column=1, sticky="en", padx=10, pady=10)
        self.right_frame.grid_columnconfigure(0, weight=1)

        # Segmented Button Frame
        self.segmented_frame = ctk.CTkSegmentedButton(self.right_frame, values=["Outlier Detection", "Interpolation", "Smoothning","Scaling & Encoding"],
                                                      command=self.change_segment)
        self.segmented_frame.grid(row=0, column=0, padx=10, pady=10)
        self.segmented_frame.set("Outlier Detection")

        # Frame that holds all segment contents
        self.segment_container = ctk.CTkFrame(self.right_frame, fg_color="transparent")
        self.segment_container.grid(row=1, column=0, sticky="s", padx=20, pady=10)

        # Create segment frames
        self.segments = {
            "Outlier Detection": self.create_segment_frame(),
            "Interpolation": self.create_interpolation_frame(),
            "Smoothning": self.create_smoothing_frame(),
           "Scaling & Encoding" : self.create_smoothing_frame()
        }

        # Submit Button
        self.submit_button = ctk.CTkButton(self.right_frame, text="Submit", command=self.submit_action)
        self.submit_button.grid(row=2, column=0, pady=10)

        # Show default segment
        self.current_segment = None
        self.change_segment("Outlier Detection")

    def clear_text(self):
        """Clears the text entry field."""
        self.text_entry.delete(0, 'end')



    def create_segment_frame(self):
        """Creates a frame for each segment."""
        frame = ctk.CTkFrame(self.segment_container, fg_color="#E0E0E0", corner_radius=10)
        frame.grid_columnconfigure(0, weight=1)

        def create_info_button(parent, text):
            button = Button(parent, text="", image=self.Info_button_image, width=8, height=8, command=lambda: self.show_info_dialog(text))
            button.grid(row=0, column=1, padx=5, sticky="e")

        # Radio Button FrameS
        radio_frame = ctk.CTkFrame(frame, fg_color="#D1D1D1", corner_radius=10)
        radio_frame.grid(row=0, column=0, padx=10, pady=15, sticky="new")
        radio_label = ctk.CTkLabel(radio_frame, text="Select Method", font=("Inter", 12, "bold"), fg_color="#A0A0A0")
        radio_label.grid(row=0, column=0, sticky="nesw")
        create_info_button(radio_frame, "Information about options")
        radio_var = ctk.StringVar(value="Option 1")
        ctk.CTkRadioButton(radio_frame, text="Isolation Forest", variable=radio_var, value="Isolation Forest", command=lambda: self.toggle_slider(frame, True)).grid(row=1, column=0, padx=10,pady=5,sticky="w")
        ctk.CTkRadioButton(radio_frame, text="IQR", variable=radio_var, value="IQR", command=lambda: self.toggle_slider(frame, False)).grid(row=1, column=1, padx=10,pady=5, sticky="w")

        # Slider Frame
        slider_frame = ctk.CTkFrame(frame, fg_color="#D1D1D1", corner_radius=10)
        slider_frame.grid(row=1, column=0, padx=10, pady=15, sticky="nsew")
        slider_label = ctk.CTkLabel(slider_frame, text="Contamination Value", font=("Inter", 12, "bold"), fg_color="#A0A0A0")
        slider_label.grid(row=0, column=0, sticky="new")
        create_info_button(slider_frame, "Information about slider")
        value_label = ctk.CTkLabel(slider_frame, text="Value: 0.00", font=("Inter", 12))
        value_label.grid(row=1, column=0, pady=5)

        def update_value(value):
            value_label.configure(text=f"Value: {float(value):.2f}")

        slider = ctk.CTkSlider(slider_frame, from_=0.00, to=0.50, number_of_steps=20,command= update_value)
        slider.grid(row=2, column=0, padx=10, sticky="ew")

        # Scrollable Frame with Checkboxes
        scroll_frame = ctk.CTkScrollableFrame(frame, fg_color="#D1D1D1", label_text="Columns", corner_radius=10)
        scroll_frame.grid(row=2, column=0, padx=10, pady=15, sticky="nsew")
        scroll_label = ctk.CTkLabel(scroll_frame, text="Choose Columns", font=("Inter", 12, "bold"), fg_color="#A0A0A0")
        scroll_label.grid(row=0, column=0, sticky="new")
        create_info_button(scroll_frame, "Information about checkboxes")
        for i in range(20):
            checkbox = ctk.CTkCheckBox(scroll_frame, text=f"Column {i}")
            checkbox.grid(row=i + 1, column=0, sticky="w", pady=2)

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
        radio_var = ctk.StringVar(value="Spline")
        ctk.CTkRadioButton(radio_frame, text="Spline", variable=radio_var, value="Spline").grid(row=1, column=0, padx=30, pady=5, sticky="w")
        ctk.CTkRadioButton(radio_frame, text="Kriging", variable=radio_var, value="Kriging").grid(row=2, column=0, padx=30, pady=5, sticky="w")
        return frame

    def create_smoothing_frame(self):
        frame = ctk.CTkFrame(self.segment_container, fg_color="#E0E0E0", corner_radius=10)
        frame.grid_columnconfigure(0, weight=1)

        def create_info_button(parent, text, row, column):
            button = Button(parent, text="", image=self.Info_button_image, width=8, height=8, command=lambda: self.show_info_dialog(text))
            button.grid(row=0, column=1, padx=5, sticky="e")

        # Radio Button Frame
        radio_frame = ctk.CTkFrame(frame, fg_color="#D1D1D1", corner_radius=10)
        radio_frame.grid(row=0, column=0, padx=10, pady=15, sticky="ew")
        radio_frame.grid_columnconfigure(0, weight=1)

        radio_label = ctk.CTkLabel(radio_frame, text="Select Method", font=("Inter", 12, "bold"), fg_color="#A0A0A0")
        radio_label.grid(row=0, column=0, sticky="nesw")
        create_info_button(radio_frame, "Information about smoothing methods", row=0, column=1)

        radio_var = ctk.StringVar(value="SMA")

        ctk.CTkRadioButton(radio_frame, text="SMA", variable=radio_var, value="SMA",
                        command=lambda: self.toggle_smoothing_options(frame, "SMA")).grid(row=1, column=0, padx=10, pady=5, sticky="w")
        ctk.CTkRadioButton(radio_frame, text="TES", variable=radio_var, value="TES",
                        command=lambda: self.toggle_smoothing_options(frame, "TES")).grid(row=1, column=1, padx=10, pady=5, sticky="w")

        # SMA Slider Frame (Default Visible)
        sma_slider_frame = ctk.CTkFrame(frame, fg_color="#D1D1D1", corner_radius=10)
        sma_slider_frame.grid(row=1, column=0, padx=10, pady=15, sticky="ew")

        sma_label = ctk.CTkLabel(sma_slider_frame, text="Window Size", font=("Inter", 12, "bold"), fg_color="#A0A0A0")
        sma_label.grid(row=0, column=0, sticky="nesw")
        create_info_button(sma_slider_frame, "Information about SMA window size", row=0, column=1)

        sma_value_label = ctk.CTkLabel(sma_slider_frame, text="Value: 5", font=("Inter", 12))
        sma_value_label.grid(row=1, column=0, pady=5)
        sma_slider = ctk.CTkSlider(sma_slider_frame, from_=5, to=100,
                                command=lambda value: sma_value_label.configure(text=f"Value: {int(value)}"))
        sma_slider.grid(row=2, column=0, padx=10, sticky="ew")

        # TES Scrollable Frame (Default Hidden)
        tes_frame = ctk.CTkScrollableFrame(frame, fg_color="#D1D1D1", label_text="TES Parameters", corner_radius=10)
        tes_frame.grid(row=1, column=0, padx=10, pady=0, sticky="ew",ipady=50)
        tes_frame.grid_remove()  # Hidden initially

        # TES Parameters with Grid Layout
        def add_tes_parameter(parent, label_text, widget_type="slider", from_=0, to=1, row_index=0):
            param_frame = ctk.CTkFrame(parent, fg_color="#E0E0E0", corner_radius=10)
            param_frame.grid(row=row_index, column=0, padx=10, pady=10, sticky="nesw")

            # Header Frame (Holds Label + Info Button)
            header_frame = ctk.CTkFrame(param_frame, fg_color="transparent")
            header_frame.grid(row=0, column=0, sticky="new")  # Keep everything left-aligned

            # Label for the parameter
            param_label = ctk.CTkLabel(header_frame, text=label_text, font=("Inter", 12, "bold"), fg_color="#A0A0A0")
            param_label.grid(row=0, column=0, padx=(5, 2), sticky="nesw")  # Left-aligned with slight padding

            # Information Button (Immediately after Label, Not Right-Aligned)
            info_button = Button(
                header_frame, text=" ",image=self.Info_button_image, width=8, height=8,
                command=lambda: self.show_info_dialog(f"Information about {label_text}")
            )
            info_button.grid(row=0, column=1, padx=(4, 5), sticky="ew")  # Right next to the label

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

            else:  # If widget_type is "entry"
                entry = ctk.CTkEntry(param_frame)
                entry.grid(row=1, column=0, padx=10, pady=10, sticky="ew")  # Below header frame
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
        """Switch between segment frames."""
        if self.current_segment:
            self.current_segment.grid_forget()
        self.current_segment = self.segments[segment_name]
        self.current_segment.grid(row=1, column=0, sticky="nsew")

    def submit_action(self):
        """Submit button action placeholder."""
        print("Submitted!")
