import customtkinter as ctk
from tkinter import Button, PhotoImage, Toplevel
from src.assets_management import assets_manage, load_image


class RegressionClassificationpage(ctk.CTkFrame):
    def __init__(self, parent,file_name=" "):
        super().__init__(parent, corner_radius=0)

        self.file_name = file_name

        # Configure grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=9)  
        self.grid_columnconfigure(1, weight=1)  

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

        # Right Side Frame (Segmented Buttons for AI Model)
        self.right_frame = ctk.CTkFrame(self, fg_color="#171821")
        self.right_frame.grid(row=0, column=1, sticky="en", padx=10, pady=10)
        self.right_frame.grid_columnconfigure(0, weight=1)

        # Segmented Button for AI Model
        self.segmented_frame = ctk.CTkSegmentedButton(self.right_frame, values=["Random Forest", "CatBoost", "ANN", "XGBoost"],
                                                    command=self.change_segment)
        self.segmented_frame.grid(row=0, column=0, padx=10, pady=10)
        self.segmented_frame.set("Random Forest")  # Default Segment

        # Frame that holds AI Model settings
        self.segment_container = ctk.CTkFrame(self.right_frame, fg_color="transparent")
        self.segment_container.grid(row=1, column=0, sticky="s", padx=20, pady=10)

        # Create segment frames
        self.segments = {
            "Random Forest": self.create_rf_frame(),
            "CatBoost": self.create_cb_frame(),
            "ANN": self.create_ann_frame(),
            "XGBoost": self.create_xgb_frame()
        }

        # Submit Button
        self.submit_button = ctk.CTkButton(self.right_frame, text="Submit", command=self.submit_action)
        self.submit_button.grid(row=2, column=0, pady=10)

        # Show default segment
        self.current_segment = None
        self.change_segment("Random Forest")


    def create_rf_frame(self):
        """Creates a frame for Random Forest parameters."""
        frame = ctk.CTkFrame(self.segment_container, fg_color="#E0E0E0", corner_radius=10)
        frame.grid_columnconfigure(0, weight=1)

        # Sliders for Random Forest
        self.create_slider_frame(frame, "n_estimators", 10, 500, 200, row=0)
        self.create_slider_frame(frame, "max_depth", 3, 50, 20, row=1)
        self.create_slider_frame(frame, "min_samples_split", 4, 10, 5, row=2)
        self.create_slider_frame(frame, "min_samples_leaf", 1, 10, 1, row=3)

        return frame


    def create_cb_frame(self):
        """Creates a frame for CatBoost parameters."""
        frame = ctk.CTkFrame(self.segment_container, fg_color="#E0E0E0", corner_radius=10)
        frame.grid_columnconfigure(0, weight=1)

        # Sliders for CatBoost
        self.create_slider_frame(frame, "n_estimators", 100, 1000, 500, row=0)
        self.create_slider_frame(frame, "learning_rate", 0.01, 0.1, 0.03, row=1)
        self.create_slider_frame(frame, "max_depth", 4, 10, 6, row=2)
        self.create_slider_frame(frame, "reg_lambda", 1, 10, 3, row=3)

        return frame


    def create_ann_frame(self):
        """Creates a frame for Artificial Neural Network parameters."""
        frame = ctk.CTkFrame(self.segment_container, fg_color="#E0E0E0", corner_radius=10)
        frame.grid_columnconfigure(0, weight=1)

        # Sliders for ANN
        self.create_slider_frame(frame, "Layer Number", 1, 6, 3, row=0)
        self.create_slider_frame(frame, "Units", 1, 256, 128, row=1)
        
        # Activation Function Dropdown
        self.create_combobox_frame(frame, "Activation Function", ["relu", "sigmoid", "tanh", "softmax"], "relu", row=2)
        
        # Optimizer Dropdown
        self.create_combobox_frame(frame, "Optimizer", ["adam", "sgd", "rmsprop"], "adam", row=3)
        
        # Sliders for ANN
        self.create_slider_frame(frame, "Batch Size", 16, 128, 30, row=4)
        self.create_slider_frame(frame, "Epochs", 10, 300, 100, row=5)

        return frame


    def create_xgb_frame(self):
        """Creates a frame for XGBoost parameters."""
        frame = ctk.CTkFrame(self.segment_container, fg_color="#E0E0E0", corner_radius=10)
        frame.grid_columnconfigure(0, weight=1)

        # Sliders for XGBoost
        self.create_slider_frame(frame, "n_estimators", 100, 1000, 200, row=0)
        self.create_slider_frame(frame, "learning_rate", 0.01, 0.3, 0.3, row=1)
        self.create_slider_frame(frame, "min_split_loss", 3, 10, 10, row=2)
        self.create_slider_frame(frame, "max_depth", 0, 10, 6, row=3)

        return frame
    

    def create_slider_frame(self, parent, label_text, from_, to, default, row):
        """Creates a frame with a slider."""
        frame = ctk.CTkFrame(parent, fg_color="#D1D1D1", corner_radius=10)
        frame.grid(row=row, column=0, padx=10, pady=10, sticky="nsew")

        label = ctk.CTkLabel(frame, text=label_text, font=("Inter", 12, "bold"), fg_color="#A0A0A0")
        label.grid(row=0, column=0, sticky="nesw")

        self.create_info_button(frame, f"Information about {label_text}")

        value_label = ctk.CTkLabel(frame, text=f"Value: {default}", font=("Inter", 12))
        value_label.grid(row=1, column=0, pady=5)

        def update_value(value):
            value_label.configure(text=f"Value: {float(value):.2f}")

        slider = ctk.CTkSlider(frame, from_=from_, to=to, command=update_value)
        slider.set(default)
        slider.grid(row=2, column=0, padx=10, sticky="ew")


    def create_combobox_frame(self, parent, label_text, options, default, row):
        """Creates a frame with a dropdown combobox."""
        frame = ctk.CTkFrame(parent, fg_color="#D1D1D1", corner_radius=10)
        frame.grid(row=row, column=0, padx=10, pady=10, sticky="nsew")

        label = ctk.CTkLabel(frame, text=label_text, font=("Inter", 12, "bold"), fg_color="#A0A0A0")
        label.grid(row=0, column=0, sticky="nesw")

        self.create_info_button(frame, f"Information about {label_text}")

        combobox = ctk.CTkComboBox(frame, values=options)
        combobox.set(default)
        combobox.grid(row=1, column=0, padx=10, pady=5, sticky="ew")


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

    def create_info_button(self,parent, text):
            """Creates an inline info button next to the label."""
            button = Button(parent, text="", image=self.Info_button_image, width=8, height=8, command=lambda: self.show_info_dialog(text))
            button.grid(row=0, column=1, padx=5, sticky="w") 

    def submit_action(self):
        """Submit button action placeholder."""
        print("Submitted!")
