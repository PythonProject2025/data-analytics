import customtkinter as ctk
from tkinter import Button, PhotoImage, Toplevel,messagebox
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
import pandas as pd
import requests
from src.models.data_object_class import DataObject
from sklearn.metrics import ConfusionMatrixDisplay
from src.assets_management import assets_manage, load_image
import re
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from src.utils.ui_element_manager import UIElementManager
from src.utils.ui_style_manager import StyleManager
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class RegressionClassificationPage(ctk.CTkFrame):
    def __init__(self, parent,file_path=None,file_name=None,data=None,**page_state):
        super().__init__(parent, corner_radius=0)
        self.parent_widget = parent

        self.Info_button_image = load_image("info_B.png", size=(16, 16))  
        self.ui = UIElementManager(
        info_icon_light=parent.info_icon_light,
        info_icon_dark=parent.info_icon_dark,
        parent_widget=self
        )
        self.parent=parent
        self.file_data=data
        self.file_name = file_name
        print(self.file_name)
        self.sliders = {}
        self.dropdowns = {}
        self.textboxes = {}

         # Check if data is available
        if self.file_data is not None:
            print(f" Received Preprocessed Data: {self.file_name}")
            print(self.file_data.head())  # Display first few rows for verification

        # Configure grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=9)  
        self.grid_columnconfigure(1, weight=1) 
        right_frame_height = int(0.8 * self.winfo_screenheight())  # Get the total screen height



         # Left Side Frame
        self.left_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.left_frame.grid(row=0, column=0, sticky="nsew", padx=50, pady=10)
        self.left_frame.grid_columnconfigure(0, weight=2)

        # First Frame (Text Box with Cancel Button)
        self.label_frame = ctk.CTkFrame(self.left_frame, fg_color=StyleManager.COLORS.get("Default Mode"), corner_radius=10,height=50)
        self.label_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.left_frame.grid_rowconfigure(0, weight=0)
        self.label = ctk.CTkLabel(self.label_frame, text=self.file_name, font=("Inter", 16, "bold"))
        self.label.place(relx=0.5, rely=0.5, anchor="center")
        self.preview_label = ctk.CTkLabel(self.label_frame, text="Preview", font=("Inter", 12, "bold"),
                                  text_color="red", cursor="hand2")
        self.preview_label.place(relx=0.9, rely=0.5, anchor="center")  # Adjusted position
        self.preview_label.bind("<Button-1>", lambda event: self.preview_data())
        self.cancel_button = ctk.CTkButton(self.left_frame, text="X", width=30, height=25, command=lambda: self.cancel_file())
        self.cancel_button.grid(row=0, column=1, padx=10, pady=10)

        # Second Frame (Dropdown & Graph Display)
        self.graph_frame = ctk.CTkFrame(self.left_frame, fg_color=StyleManager.COLORS.get("Default Mode"), corner_radius=10, height=350)  # Increased Height
        self.graph_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.left_frame.grid_rowconfigure(1, weight=1)  # Keep left frame standard but allow graph frame to take space

        # Configure Graph Frame Grid
        self.graph_frame.grid_rowconfigure(0, weight=1)  # Center the dropdown
        self.graph_frame.grid_rowconfigure(1, weight=4)  # Allow graph display to expand
        self.graph_frame.grid_columnconfigure(0, weight=1)

       
        # Graph Display Area (Expanded)
        self.graph_display = ctk.CTkFrame(self.graph_frame, fg_color=StyleManager.COLORS.get("Default Mode"), height=250, corner_radius=10)  # Increased Size
        self.graph_display.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")  # Expands to fill space


        
        # Right Side Frame (Segmented Buttons for AI Model)
        self.right_frame = ctk.CTkScrollableFrame(self, fg_color=StyleManager.COLORS.get("Default Mode"), width=300 , height= right_frame_height)
        self.right_frame.grid(row=0, column=1, sticky="en", padx=10, pady=10)
        self.right_frame.grid_columnconfigure(0, weight=1)

       # **Tabs for Regression & Classification**
        self.segmented_frame = ctk.CTkSegmentedButton(self.right_frame, values=["Regression", "Classification"],
                                                      command=self.change_segment)
        self.segmented_frame.grid(row=0, column=0, padx=10, pady=10)
        self.segmented_frame.set("Regression")

        # **Container for Segment Content**
        self.segment_container = ctk.CTkFrame(self.right_frame, fg_color=StyleManager.COLORS.get("Default Mode"))
        self.segment_container.grid(row=1, column=0, sticky="s", padx=10, pady=10)

        # **Create segment frames**
        self.segments = {
            "Regression": self.create_regression_frame(),
            "Classification": self.create_classification_frame()
        }

        # **Submit Button**
        self.submit_button = ctk.CTkButton(self.right_frame, text="Submit", command=self.submit_action)
        self.submit_button.grid(row=2, column=0, pady=10)

        # Show default segment
        self.current_segment = None
        self.change_segment("Regression")

  


    def create_regression_frame(self):
        """Creates the Regression segment frame with dynamic parameters."""
        frame = ctk.CTkFrame(self.segment_container, fg_color=StyleManager.COLORS.get("Default Mode"), corner_radius=10)
        frame.grid_columnconfigure(0, weight=1)

        # **Regression Model Selection (Radio Buttons)**
        radio_frame = ctk.CTkFrame(frame, fg_color=StyleManager.COLORS.get("accent"), corner_radius=10)
        radio_frame.grid(row=0, column=0, padx=10, pady=15, sticky="new")

        self.regression_radio_var = ctk.StringVar(value="Linear Regression")  # Default
        ctk.CTkRadioButton(radio_frame, text="Linear Regression", variable=self.regression_radio_var,
                           value="Linear Regression", command=self.toggle_regression_options).grid(row=0, column=0, padx=10, pady=5, sticky="w")
        ctk.CTkRadioButton(radio_frame, text="Polynomial Regression", variable=self.regression_radio_var,
                           value="Polynomial Regression", command=self.toggle_regression_options).grid(row=1, column=0, padx=10, pady=5, sticky="w")
        ctk.CTkRadioButton(radio_frame, text="Ridge Regression", variable=self.regression_radio_var,
                           value="Ridge Regression", command=self.toggle_regression_options).grid(row=2, column=0, padx=10, pady=5, sticky="w")
        ctk.CTkRadioButton(radio_frame, text="Lasso Regression", variable=self.regression_radio_var,
                           value="Lasso Regression", command=self.toggle_regression_options).grid(row=3, column=0, padx=10, pady=5, sticky="w")

        self.regression_options_frame = ctk.CTkFrame(frame, fg_color=StyleManager.COLORS.get("accent"))
        self.regression_options_frame.grid(row=1, column=0, padx=10, pady=15, sticky="new")
        
           
        self.toggle_regression_options()

        return frame


    

    def create_classification_frame(self):
        """Creates the Classification segment frame with dynamic parameters."""
        frame = ctk.CTkFrame(self.segment_container, fg_color=StyleManager.COLORS.get("Default Mode"), corner_radius=10)
        frame.grid_columnconfigure(0, weight=1)

        # **Classification Model Selection (Radio Buttons)**
        radio_frame = ctk.CTkFrame(frame, fg_color=StyleManager.COLORS.get("accent"), corner_radius=10)
        radio_frame.grid(row=0, column=0, padx=10, pady=15, sticky="new")

        self.classification_radio_var = ctk.StringVar(value="RandomForest")  # Default
        ctk.CTkRadioButton(radio_frame, text="RandomForest", variable=self.classification_radio_var,
                           value="RandomForest", command=self.toggle_classification_options).grid(row=0, column=0, padx=10, pady=5, sticky="w")
        ctk.CTkRadioButton(radio_frame, text="SVC", variable=self.classification_radio_var,
                           value="SVC", command=self.toggle_classification_options).grid(row=1, column=0, padx=10, pady=5, sticky="w")
        ctk.CTkRadioButton(radio_frame, text="KNN", variable=self.classification_radio_var,
                           value="KNN", command=self.toggle_classification_options).grid(row=2, column=0, padx=10, pady=5, sticky="w")

        self.classification_options_frame = ctk.CTkFrame(frame, fg_color="transparent")
        self.classification_options_frame.grid(row=1, column=0, padx=10, pady=15, sticky="new")

        self.toggle_classification_options()



        return frame

    def toggle_regression_options(self):
        """Updates the Regression options dynamically based on selection."""
        model = self.regression_radio_var.get()
        self.clear_frame(self.regression_options_frame)
           
        if model == "Polynomial Regression":
            self.create_textbox(self.regression_options_frame, "Polynomial Degree","polynomial")
            # self.create_textbox(self.regression_options_frame, "X_Label", "xlabel")
        

        elif model == "Ridge Regression":
            self.create_textbox(self.regression_options_frame, "Polynomial Degree (Ridge)", "polynomial")
            self.create_textbox(self.regression_options_frame, "Alpha Values (Ridge)", "alpha")
        elif model == "Lasso Regression":
            self.create_textbox(self.regression_options_frame, "Polynomial Degree (Lasso)", "polynomial")
            self.create_textbox(self.regression_options_frame, "Alpha Values (Lasso)", "alpha")
            
            

    def toggle_classification_options(self):
        """Updates the Classification options dynamically based on selection."""
        model = self.classification_radio_var.get()
        self.clear_frame(self.classification_options_frame)

        if model == "RandomForest":
            self.create_slider(self.classification_options_frame, "n_estimators", 50, 150, 100)
            self.create_slider(self.classification_options_frame, "max_depth", 5, 20, 10)

        elif model == "SVC":
            self.create_slider(self.classification_options_frame, "C", 0.1, 10, 1)
            self.create_dropdown(self.classification_options_frame, "Kernel", ["linear", "rbf"])
            self.create_dropdown(self.classification_options_frame, "Gamma", ["scale", "auto"])

        elif model == "KNN":
            self.create_slider(self.classification_options_frame, "n_neighbors", 3, 7, 5)
            self.create_dropdown(self.classification_options_frame, "Weights", ["uniform", "distance"])
            self.create_slider(self.classification_options_frame, "P", 1, 2, 1)

    def change_segment(self, segment_name):
        """Handles switching between Regression and Classification."""
        if self.current_segment:
            self.current_segment.grid_forget()
        self.current_segment = self.segments[segment_name]
        self.current_segment.grid(row=1, column=0, sticky="nsew")

    def clear_frame(self, frame):
        """Clears the contents of a frame."""
        for widget in frame.winfo_children():
            widget.destroy()

    

    def create_slider(self, parent, label_text, min_val, max_val, default):
        """Creates a labeled slider with info button and cleaner layout."""

        # Outer container
        frame = ctk.CTkFrame(
            parent,
            fg_color=StyleManager.COLORS.get("accent"),
            corner_radius=10
        )
        frame.grid(row=len(parent.winfo_children()), column=0, padx=10, pady=10, sticky="nsew")

        # Label row (label + info icon)
        label_frame = ctk.CTkFrame(frame, fg_color="transparent")
        label_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=(5, 0))
        label_frame.grid_columnconfigure(0, weight=1)

        label = ctk.CTkLabel(
            label_frame,
            text=label_text,
            font=StyleManager.get_font("label"),
            fg_color="transparent",
            text_color=StyleManager.get_color("Text Color")
        )
        label.grid(row=0, column=0, sticky="w")

        self.create_info_button(label_frame, f"Information about {label_text}", row=0, column=1)

        # Value label
        value_label = ctk.CTkLabel(
            frame,
            text=f"Value: {default}",
            font=StyleManager.get_font("normal"),
            text_color=StyleManager.get_color("Text Color")
        )
        value_label.grid(row=1, column=0, padx=10, pady=(5, 0), sticky="w")

        # Slider itself
        def update_value(value):
            formatted = f"{float(value):.0f}" if isinstance(value, float) else f"{int(value)}"
            value_label.configure(text=f"Value: {formatted}")

        slider = ctk.CTkSlider(
            frame,
            from_=min_val,
            to=max_val,
            command=update_value,
            button_color=StyleManager.get_color("primary"),
            progress_color=StyleManager.get_color("primary")
        )
        slider.set(default)
        slider.grid(row=2, column=0, padx=10, pady=(5, 10), sticky="ew")

        self.sliders[label_text] = slider


    def create_dropdown(self, parent, label_text, options):
        """Creates a labeled dropdown menu with info button and styled layout."""

        # Outer rounded frame
        frame = ctk.CTkFrame(
            parent,
            fg_color=StyleManager.get_color("accent"),
            corner_radius=10
        )
        frame.grid(row=len(parent.winfo_children()), column=0, padx=10, pady=10, sticky="nsew")

        # Label row frame: Label + Info Button
        label_frame = ctk.CTkFrame(frame, fg_color="transparent")
        label_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=(5, 0))
        label_frame.grid_columnconfigure(0, weight=1)

        label = ctk.CTkLabel(
            label_frame,
            text=label_text,
            font=StyleManager.get_font("label"),
            text_color=StyleManager.get_color("Text Color"),
            fg_color="transparent"
        )
        label.grid(row=0, column=0, sticky="w")

        self.create_info_button(label_frame, f"Information about {label_text}", row=0, column=1)

        # Dropdown (ComboBox)
        combobox = ctk.CTkComboBox(
            frame,
            values=options,
            fg_color=StyleManager.get_color("secondary"),
            text_color=StyleManager.get_color("Text Color"),
            dropdown_fg_color=StyleManager.get_color("secondary"),
            dropdown_text_color=StyleManager.get_color("Text Color"),
            font=StyleManager.get_font("normal")
        )
        combobox.set(options[0])
        combobox.grid(row=1, column=0, padx=10, pady=(5, 10), sticky="ew")

        self.dropdowns[label_text] = combobox  # Store reference



    def create_textbox(self, parent, label_text, mode):
        """
        Creates a labeled textbox with validation.

        mode:
            - "polynomial": Allows 1-5 single-digit numbers (0-9), separated by commas.
            - "alpha": Allows 1-5 float values (0-1) with at least 4 decimal places, separated by commas.
            - "xlabel": Allows only strings and special characters (No numbers allowed).
        """
        # Outer container with rounded corners
        frame = ctk.CTkFrame(
            parent,
            fg_color=StyleManager.get_color("accent"),
            corner_radius=10
        )
        frame.grid(row=len(parent.winfo_children()), column=0, padx=10, pady=10, sticky="nsew")

        # Create a nested frame for the label + info icon
        label_frame = ctk.CTkFrame(frame, fg_color="transparent")
        label_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=(5, 0))
        label_frame.grid_columnconfigure(0, weight=1)

        # Label
        label = ctk.CTkLabel(
            label_frame,
            text=label_text,
            font=StyleManager.get_font("label"),
            fg_color="transparent",
            text_color=StyleManager.get_color("Text Color")
        )
        label.grid(row=0, column=0, sticky="w")

        # Info Button
        self.create_info_button(label_frame, f"Information about {label_text}", row=0, column=1)

        # Entry wrapper to get clean border radius
        entry_wrapper = ctk.CTkFrame(frame, fg_color=StyleManager.get_color("accent"), corner_radius=8)
        entry_wrapper.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        entry_var = tk.StringVar()
        entry = ctk.CTkEntry(entry_wrapper, textvariable=entry_var, border_width=0)
        entry.pack(fill="x", padx=8, pady=6)

        # Add Validation
        if mode == "xlabel":
            entry.bind("<KeyRelease>", self.validate_x_label)

        self.textboxes[label_text] = entry_var  # Store for validation on submit



    def validate_x_label(self, event):
        """Ensures X_Label only contains strings and special characters (No numbers)."""
        self.X_Label_data = self.textboxes["X_Label"].get()

        if any(char.isdigit() for char in self.X_Label_data):
            self.textboxes["X_Label"].set(re.sub(r'\d+', '', self.X_Label_data))  # Remove numbers
            messagebox.showwarning("Invalid Input", "X_Label cannot contain numbers!")


    def show_info_dialog(self, text):
        # The popup window
        dialog = ctk.CTkToplevel(self.parent_widget)
        dialog.title("Information")

        # --- dimensions ---
        dialog_width = 350
        dialog_height = 180

        # --- Center the dialog on the screen ---
        screen_width = dialog.winfo_screenwidth()
        screen_height = dialog.winfo_screenheight()
        x = int((screen_width / 2) - (dialog_width / 2))
        y = int((screen_height / 2) - (dialog_height / 2))
        dialog.geometry(f"{dialog_width}x{dialog_height}+{x}+{y}")

        # --- Make it modal ---
        dialog.grab_set()

        # --- Wrapped Label ---
        ctk.CTkLabel(
            dialog,
            text=text,
            font=self.font_normal,
            wraplength=300,
            justify="center"
        ).pack(padx=20, pady=(20, 10), expand=True)


        # --- OK Button ---
        ctk.CTkButton(
            dialog,
            text="OK",
            command=dialog.destroy
        ).pack(pady=(0, 20))

    def create_info_button(self, parent, text, row=0, column=1):
            button = ctk.CTkButton(
                parent,
                text="",  
                image=self.Info_button_image,  # CTkImage
                width=24,  
                height=24,
                fg_color="transparent",  # Make button background transparent
                hover_color="#d3d3d3",  # hover effect
                command=lambda: self.show_info_dialog(text)
            )
            button.grid(row=row, column=column, padx=5, sticky="w")

    def submit_action(self):
        """Handles submission and prints selected model parameters."""
        dataobject = DataObject()
        current_segment = self.segmented_frame.get()
        
        # Store the preprocessed data from file_data
        if self.file_data is not None:
            split_data = self.file_data  # Assuming file_data contains the split dataset
            for key, value in split_data.items():
                if isinstance(value, pd.DataFrame):
                    dataobject.data_filtering["Train-Test Split"]["split_data"][key] = value.to_dict(orient="records")
                elif isinstance(value, pd.Series):
                    dataobject.data_filtering["Train-Test Split"]["split_data"][key] = value.tolist()  # Convert to list

        if current_segment == "Regression":
            model = self.regression_radio_var.get()
            dataobject.regression["Selected Model"]= model
            errors = []
            
            if model == "Linear Regression":
                
                # Convert DataObject to JSON
                json_data = {"dataobject": dataobject.to_dict()}
                # Send request
                self.send_request_regression(json_data)
            
            elif model == "Polynomial Regression":

                polynomial_degree = self.textboxes["Polynomial Degree"].get()
                 
                if not re.fullmatch(r"^(\d{1})(,\d{1}){0,4}$", polynomial_degree):
                    errors.append("Polynomial Degree: Enter up to 5 single-digit numbers (0-9) separated by commas.")
                if errors:
                    messagebox.showerror("Input Error", "\n".join(errors))
                else:
                     polynomial_degree_list = [int(x) for x in polynomial_degree.split(",")]
                     dataobject.regression["Model_Selection"]["Polynomial Regression"]["polynomial_degree"]=polynomial_degree_list
                # Convert DataObject to JSON
                json_data = {"dataobject": dataobject.to_dict()}
                # Send request
                self.send_request_regression(json_data)


            elif model == "Ridge Regression":

                polynomial_degree = self.textboxes["Polynomial Degree (Ridge)"].get()
                if not re.fullmatch(r"^(\d{1})(,\d{1}){0,4}$", polynomial_degree):
                    errors.append("Polynomial Degree: Enter up to 5 single-digit numbers (0-9) separated by commas.")
                alpha_value = self.textboxes["Alpha Values (Ridge)"].get()  # Example for Ridge
                if not re.fullmatch(r"^(0\.\d{1,4}|1\.0{0,3})(,(0\.\d{1,4}|1\.0{0,3})){0,4}$", alpha_value):
                    errors.append("Alpha Values: Enter up to 5 values between 0-1 with at least 4 decimal places, separated by commas.")

                if errors:
                    messagebox.showerror("Input Error", "\n".join(errors))
                else:
                    polynomial_degree_ridge_list = [int(x) for x in polynomial_degree.split(",")]
                    alpha_values_ridge_list = [float(x) for x in alpha_value.split(",")]
                    dataobject.regression["Model_Selection"]["Ridge Regression"]["polynomial_degree_ridge"]=polynomial_degree_ridge_list
                    dataobject.regression["Model_Selection"]["Ridge Regression"]["alpha_values_ridge"]=alpha_values_ridge_list
                # Convert DataObject to JSON
                json_data = {"dataobject": dataobject.to_dict()}
                # Send request
                self.send_request_regression(json_data)

            elif model == "Lasso Regression":

                polynomial_degree = self.textboxes["Polynomial Degree (Lasso)"].get()
                if not re.fullmatch(r"^(\d{1})(,\d{1}){0,4}$", polynomial_degree):
                    errors.append("Polynomial Degree: Enter up to 5 single-digit numbers (0-9) separated by commas.")
                alpha_value = self.textboxes["Alpha Values (Lasso)"].get()  # Example for Ridge
                if not re.fullmatch(r"^(0\.\d{1,4}|1\.0{0,3})(,(0\.\d{1,4}|1\.0{0,3})){0,4}$", alpha_value):
                    errors.append("Alpha Values: Enter up to 5 values between 0-1 with at least 4 decimal places, separated by commas.")

                if errors:
                    messagebox.showerror("Input Error", "\n".join(errors))
                else:

                    polynomial_degree_Lasso_list = [int(x) for x in polynomial_degree.split(",")]
                    alpha_values_Lasso_list = [float(x) for x in alpha_value.split(",")]

                    dataobject.regression["Model_Selection"]["Lasso Regression"]["polynomial_degree_lasso"]=polynomial_degree_Lasso_list
                    dataobject.regression["Model_Selection"]["Lasso Regression"]["alpha_values_lasso"]=alpha_values_Lasso_list
                # Convert DataObject to JSON
                json_data = {"dataobject": dataobject.to_dict()}
                # Send request
                self.send_request_regression(json_data)

            print("\nSubmission Successful!\n")


        elif current_segment == "Classification":
             model = self.classification_radio_var.get()
             print(f"Selected Classification Model: {model}")
             dataobject.classification["Model_Selection"]= model
             if model == "RandomForest":
                 
                dataobject.classification["RandomForest"]["n_estimators"]= int(self.sliders['n_estimators'].get())
                dataobject.classification["RandomForest"]["max_depth"]=int(self.sliders['max_depth'].get())
                # Convert DataObject to JSON
                json_data = {"dataobject": dataobject.to_dict()}
                # Send request
                self.send_request_classification(json_data)

             elif model == "SVC":
                dataobject.classification["SVC"]["C"]= float(self.sliders['C'].get())
                dataobject.classification["SVC"]["kernel"]= self.dropdowns['Kernel'].get()
                dataobject.classification["SVC"]["gamma"]= self.dropdowns['Gamma'].get()
                dataobject.classification["SVC"]["kernel"]
                # Convert DataObject to JSON
                json_data = {"dataobject": dataobject.to_dict()}
                # Send request
                self.send_request_classification(json_data)

             elif model == "KNN":
                dataobject.classification["KNN"]["n_neighbours"]= int(self.sliders['n_neighbors'].get())
                dataobject.classification["KNN"]["weights"]=self.dropdowns['Weights'].get()
                dataobject.classification["KNN"]["p"]=int(self.sliders['P'].get())
                print(dataobject.classification["KNN"]["weights"])               
                # Convert DataObject to JSON
                json_data = {"dataobject": dataobject.to_dict()}
                # Send request
                self.send_request_classification(json_data)


        if hasattr(self, "submit_button"):
            self.submit_button.configure(state="disabled")  # Hide the submit button
       

    def preview_data(self):
        """Opens a new popup window to display the scaled and encoded data."""
        
        if not hasattr(self, "file_data") or self.file_data is None or self.file_data.empty:
            messagebox.showerror("Error", "No processed data available for preview!")
            return

        #  Create a new popup window
        preview_window = ctk.CTkToplevel(self)
        preview_window.title("Processed Data Preview")
        preview_window.geometry("900x500")
        preview_window.grab_set()

        #  Create a frame for the Treeview
        frame = tk.Frame(preview_window)
        frame.pack(fill="both", expand=True)

        #  Treeview (Table) widget
        tree = ttk.Treeview(frame, columns=list(self.file_data.columns), show="headings")

        #  Add column headers
        for col in self.file_data.columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)  # Adjust column width

        #  Insert rows (limit to first 50 rows to avoid UI lag)
        for index, row in self.file_data.head(50).iterrows():
            tree.insert("", "end", values=list(row))

        #  Add vertical scrollbar
        v_scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscroll=v_scrollbar.set)

        #  Add horizontal scrollbar
        h_scrollbar = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)
        tree.configure(xscroll=h_scrollbar.set)

        #  Pack elements
        tree.pack(side="top", fill="both", expand=True)
        v_scrollbar.pack(side="right", fill="y")
        h_scrollbar.pack(side="bottom", fill="x")
        
    def send_request_regression(self, json_data):
        """Send the request to the Django backend and return the response."""
        print("sending to backend")
        try:
           
            response = requests.post(
                    "http://127.0.0.1:8000/api/regression/",
                    json=json_data
            )
 
            if response.status_code == 200:
                    response_data = response.json()
                    self.display_regression_results(response_data)
                    # Check if Lasso Regression data is present
                    if "Lasso_Regression" in response_data:
                        # Extracting values for Lasso Regression
                        r2_score_lasso = response_data["r2_score_lasso"]
                        best_degree_lasso = response_data["best_degree_lasso"]
                        best_alpha_lasso = response_data["best_alpha_lasso"]
                        results_lasso = response_data["results_lasso"]
                        Lasso_Regression = response_data["Lasso_Regression"]

                        # Generate Lasso Regression Plot
                        self.lasso_plot(results_lasso, Lasso_Regression)

                    # Check if Ridge Regression data is present
                    elif "Ridge_Regression" in response_data:
                        # Extracting values for Ridge Regression
                        r2_score_ridge = response_data["r2_score_ridge"]
                        best_degree_ridge = response_data["best_degree_ridge"]
                        best_alpha_ridge = response_data["best_alpha_ridge"]
                        results_ridge = response_data["results_ridge"]
                        Ridge_Regression = response_data["Ridge_Regression"]

                        # Generate Ridge Regression Plot
                        self.ridge_plot(results_ridge, Ridge_Regression)  
                        
                    elif "best_polynomial_degree" in response_data:
                        r2_score_polynomial = response_data["r2_score_polynomial"]
                        y_pred = response_data["y_pred"]
                        best_polynomial_degree = response_data["best_polynomial_degree"]
                        #x_data = response_data["x_data"]
                        y_test = response_data["y_test"]
                        x_label = response_data["x_label"]
                        y_label = response_data["y_label"]
                        
                    # Create dummy x-axis if not provided
                        x_data = np.arange(len(y_test))
                    
                        self.polynomial_plot(x_data, y_test, y_pred, x_label, y_label, best_polynomial_degree)
                    elif "r2_score_linear" in response_data:
                        # Extract values
                        r2_score_linear = response_data["r2_score_linear"]
                        y_pred = response_data["y_pred"]
                        y_test = response_data["y_test"]
                        x_label = response_data["x_label"]
                        y_label = response_data["y_label"]

                        #  Create a Tkinter Toplevel window
                        popup = ctk.CTkToplevel(self)
                        popup.title("Linear Regression & Residual Plot")
                        popup.geometry("1000x500")
                        popup.grab_set()

                        #  Create the matplotlib figure with 2 subplots
                        from matplotlib.figure import Figure
                        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

                        fig = Figure(figsize=(12, 5), dpi=100)
                        ax1 = fig.add_subplot(121)
                        ax2 = fig.add_subplot(122)

                        #  Call your existing functions, passing subplot axes
                        self.regression_plot(y_test, y_pred, x_label, y_label, ax=ax1)
                        self.residual_plot(y_test, y_pred, ax=ax2)

                        #  Embed the figure in the popup window
                        canvas = FigureCanvasTkAgg(fig, master=popup)
                        canvas.draw()
                        canvas.get_tk_widget().pack(fill="both", expand=True)


                   
            else:
                    messagebox.showerror(
                        "Error", response.json().get('error', 'File upload failed.')
                    )
        except Exception as e:
                messagebox.showerror("Error", str(e))

    def display_regression_results(self, response_data):
        """Displays regression results dynamically based on the selected model above the graph frame."""
        
        #  Clear Previous Results if Any
        for widget in self.graph_frame.winfo_children():
            if isinstance(widget, ctk.CTkLabel):
                widget.destroy()

        #  Extract Regression Results Based on the Model
        result_text = ""
        
        if "r2_score_lasso" in response_data:
            result_text = (
                f"R2 Score: {float(response_data['r2_score_lasso']):.4f}\n"
                f"Best Polynomial Degree: {response_data['best_degree_lasso']}\n"
                f"Best Alpha: {float(response_data['best_alpha_lasso']):.4f}"
            )

        elif "r2_score_ridge" in response_data:
            result_text = (
                f"R2 Score: {float(response_data['r2_score_ridge']):.4f}\n"
                f"Best Polynomial Degree: {response_data['best_degree_ridge']}\n"
                f"Best Alpha: {float(response_data['best_alpha_ridge']):.4f}"
            )

        elif "best_polynomial_degree" in response_data:
            result_text = (
                f"R2 Score: {float(response_data['r2_score_polynomial']):.4f}\n"
                f"Best Polynomial Degree: {response_data['best_polynomial_degree']}"
            )

        elif "r2_score_linear" in response_data:
            result_text = f"R2 Score: {float(response_data['r2_score_linear']):.4f}"


        # Display Results as a Label Above Graph
        if result_text:
            result_label = ctk.CTkLabel(
                self.graph_frame, text=result_text, 
                font=("Inter", 15, "bold"), fg_color="#D1D1D1", text_color="black",
                height=50, width=500, corner_radius=8, padx=5, pady=5
            )
            result_label.grid(row=0, column=0, padx=10, pady=5, sticky="new")  # Placed above graph display

                
        
    def send_request_classification(self, json_data):
        """Send the request to the Django backend and render confusion matrix and metrics."""
     

        try:
            response = requests.post(
                "http://127.0.0.1:8000/api/classification/",
                json=json_data
            )

            if response.status_code == 200:
                response_data = response.json()
                self.display_classification_results(response_data)

                cm_data = response_data.get("cm")
                if cm_data:
                    self.display_confusion_matrix(cm_data)
                else:
                    messagebox.showerror("Error", "Confusion Matrix data not received.")

            else:
                messagebox.showerror(
                    "Error", response.json().get('error', 'Classification request failed.')
                )

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def display_classification_results(self, response_data):
        """Displays classification results (accuracy, MSE) above the graph frame."""
        
        # Clear previous result labels
        for widget in self.graph_frame.winfo_children():
            if isinstance(widget, ctk.CTkLabel):
                widget.destroy()

        result_text = ""

        if "accuracy" in response_data and "mse" in response_data:
            result_text = (
                f"Accuracy: {float(response_data['accuracy']):.4f}\n"
                f"MSE: {float(response_data['mse']):.4f}"
            )

        if result_text:
            result_label = ctk.CTkLabel(
                self.graph_frame, text=result_text,
                font=("Inter", 15, "bold"), fg_color="#D1D1D1", text_color="black",
                height=50, width=500, corner_radius=8, padx=5, pady=5
            )
            result_label.grid(row=0, column=0, padx=10, pady=5, sticky="new")


    def cancel_file(self):
        """Handles file cancellation and resets only this page."""
        
        page_name = self.__class__.__name__  # Get the page's class name

        self.parent.file_paths[page_name] = None
        self.parent.file_names[page_name] = None
        self.parent.page_data[page_name] = None
        self.parent.update_sidebar_buttons(page_name, action="remove")

        if hasattr(self.parent, f"{page_name}_instance"):
            delattr(self.parent, f"{page_name}_instance")

        self.parent.show_page("file_upload")

    def render_plot_to_frame(self, fig):
            for widget in self.graph_display.winfo_children():
                widget.destroy()

            canvas = FigureCanvasTkAgg(fig, master=self.graph_display)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)
        
    
    
    def lasso_plot(self,results_lasso,best_params):
        plt.close('all')
        
        best_degree_mask = (np.array(results_lasso['param_polynomial_features__degree']) == best_params['best_degree_lasso'])
        alphas = list(np.array(results_lasso['param_lasso_regression__alpha'])[best_degree_mask])
        mean_scores = list(np.array(results_lasso['mean_test_score'])[best_degree_mask])

        # Set the figure size and style
        fig=plt.figure(figsize=(9, 5), dpi=100)
        sns.set_theme(style="whitegrid")  # Clean background with gridlines
        
        # Plot the lineplot
        sns.lineplot(
            x=alphas, y=mean_scores,
            marker='o', linestyle='-', color='#e74c3c',  # Line color and marker style
            label=f'Best Degree = {best_params["best_degree_lasso"]}\nBest Alpha = {best_params["best_alpha_lasso"]}', 
            linewidth=2.5, markersize=8
        )
        
        # Add labels and title with improved styling
        plt.xlabel('Alpha (Regularization Strength)', fontsize=14, weight='bold', labelpad=15)
        plt.ylabel('Cross-Validation Score (R2 Score)', fontsize=14, weight='bold', labelpad=15)
        plt.title('Alpha vs Model Performance (Lasso Regression)', fontsize=16, weight='bold', pad=20)
        
        #plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
        #plt.gca().yaxis.get_offset_text().set_visible(False)
        
        # Instead, ensure the y-axis is in plain format
        plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:.3f}'))
    
        # Set y-axis limits to better reflect the R² range (optional, adjust as needed)
        plt.ylim(min(mean_scores) - 0.01, max(mean_scores) + 0.01)  # Add some padding
        
        # Customize the legend to remove the line
        plt.legend(
            fontsize=12, loc='upper right', frameon=True, fancybox=True, shadow=True, borderpad=1, handlelength=0
        )
        
        # Add gridlines and customize tick params
        plt.grid(which='major', linestyle='--', linewidth=0.7, color='gray', alpha=0.7)
        plt.minorticks_on()
        plt.tick_params(
            which='both', direction='in', length=6, width=1, colors='black', grid_alpha=0.5
        )
        
        # Remove top and right spines for a clean look
        sns.despine(top=True, right=True)
        
        # Ensure the plot looks neat with tight layout
        plt.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master= self.graph_display)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
    
    def ridge_plot(self,results_ridge,best_params):
        plt.close('all')

    #    results = data.results_ridge
        best_degree_mask = (np.array(results_ridge['param_polynomial_features__degree']) == best_params['best_degree_ridge'])
        alphas = np.array(results_ridge['param_ridge_regression__alpha'])[best_degree_mask]
        mean_scores = np.array(results_ridge['mean_test_score'])[best_degree_mask]
        # Set the figure size and style
        fig=plt.figure(figsize=(9, 5), dpi=120)
        sns.set_theme(style="whitegrid")  # Clean background with gridlines
        
        # Plot the lineplot
        sns.lineplot(
        x=alphas, y=mean_scores,
        marker='o', linestyle='-', color='#1f77b4',  # Line color and marker style
        label=f'Best Degree = {best_params["best_degree_ridge"]}\nBest Alpha = {best_params["best_alpha_ridge"]}', 
        linewidth=2.5, markersize=8
    )
        
        # Add labels and title with improved styling
        plt.xlabel('Alpha (Regularization Strength)', fontsize=14, weight='bold', labelpad=15)
        plt.ylabel('Cross-Validation Score (R2 Score)', fontsize=14, weight='bold', labelpad=8)
        plt.title('Alpha vs Model Performance (Ridge Regression)', fontsize=16, weight='bold', pad=20)
        plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:.3f}'))
    
        # Set y-axis limits to better reflect the R² range (optional, adjust as needed)
        plt.ylim(min(mean_scores) - 0.01, max(mean_scores) + 0.01)  # Add some padding
        
        # Customize the legend
        plt.legend(
            fontsize=12, loc='upper right', frameon=True, fancybox=True, shadow=True, borderpad=1
        )
        
        # Add gridlines and customize tick params
        plt.grid(which='major', linestyle='--', linewidth=0.7, color='gray', alpha=0.7)
        plt.minorticks_on()
        plt.tick_params(
            which='both', direction='in', length=6, width=1, colors='black', grid_alpha=0.5
        )
        
        # Remove top and right spines for a clean look
        sns.despine(top=True, right=True)
        
        # Ensure the plot looks neat with tight layout
        plt.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master= self.graph_display)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        
    def polynomial_plot(self, x_scatter, y_scatter, y_poly, x_label, y_label, degree):
        plt.close('all')
        """Generates and displays the Polynomial Regression plot."""
        try:
            if isinstance(y_scatter, dict):
                y_scatter = np.array(list(y_scatter.values()))

            x_scatter = np.array(x_scatter).flatten() if not isinstance(x_scatter, np.ndarray) else x_scatter.flatten()
            y_scatter = np.array(y_scatter).flatten() if not isinstance(y_scatter, np.ndarray) else y_scatter.flatten()
            y_poly = np.array(y_poly).flatten() if not isinstance(y_poly, np.ndarray) else y_poly.flatten()

            if len(x_scatter) != len(y_scatter) or len(x_scatter) != len(y_poly):
                expected_length = len(y_scatter)
                if len(x_scatter) == 1:  # If x_scatter is a single value like [0]
                    x_scatter = np.arange(expected_length)  # e.g., [0, 1, 2, 3, 4]
                else:
                    raise ValueError(
                        f"Array length mismatch: x_scatter ({len(x_scatter)}), y_scatter ({len(y_scatter)}), y_poly ({len(y_poly)}). All arrays must be the same length."
                    )
            
            #  Sort the data by x_scatter to ensure a smooth line plot
            sorted_indices = np.argsort(x_scatter)
            x_scatter = x_scatter[sorted_indices]
            y_scatter = y_scatter[sorted_indices]
            y_poly = y_poly[sorted_indices]
            
            # Set figure size and seaborn style
            fig=plt.figure(figsize=(10, 5), dpi=120)
            sns.set_theme(style="ticks")

            # Scatter plot for actual data
            sns.scatterplot(
                x=x_scatter, y=y_scatter,
                color='#1f77b4',
                label='Actual Data', s=50, alpha=0.5,
                edgecolor='black', linewidth=0.3
            )

            # Line plot for polynomial regression
            sns.lineplot(
                x=x_scatter, y=y_poly,
                color='#ff5733',
                label='Polynomial Regression Line',
                linewidth=2.5, alpha=0.7
            )

            # Add labels and title with better styling
            plt.xlabel(x_label, fontsize=14, weight='semibold', labelpad=12)
            plt.ylabel(y_label, fontsize=14, weight='semibold', labelpad=12)
            plt.title(
                f'Polynomial Regression Fit (Degree: {degree})', fontsize=16, weight='bold', pad=20, loc='center',
                color='#333333'
            )

            # Legend styling - fixed at lower left corner
            plt.legend(
                fontsize=12, loc='lower left', frameon=True, shadow=False,
                fancybox=True, borderpad=1, framealpha=0.9
            )

            # Customize the grid and spines
            plt.grid(
                which='major', linestyle='--', linewidth=0.6, color='gray', alpha=0.7
            )
            plt.minorticks_on()
            plt.tick_params(
                which='both', direction='in', length=6, width=1, colors='black',
                grid_alpha=0.5
            )
            sns.despine(top=True, right=True)

            # Tight layout for better spacing
            plt.tight_layout()
            
            #  Embed in the Tkinter frame
            canvas = FigureCanvasTkAgg(fig, master= self.graph_display)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)

        except Exception as e:
            print("ERROR in polynomial_plot:", str(e))
            messagebox.showerror("Plot Error", str(e))
            
    def regression_plot(self,x, y, x_label, y_label, data=None, ax=None):
       # plt.close('all')
        if isinstance(x, dict):  
            x = np.array(list(x.values()))  # Convert dictionary to array
        elif isinstance(x, list):
            x = np.array(x)  # Convert list to NumPy array

        if isinstance(y, dict):  
            y = np.array(list(y.values()))
        elif isinstance(y, list):
            y = np.array(y)
        if ax is None:
            ax = plt.gca()
            plt.figure(figsize=(10, 6), dpi=600)  # Adjust size and set DPI
        sns.regplot(
            x=x, y=y, data=None, ax=ax,
            scatter_kws={"s": 60, "alpha": 0.8},  # Customize scatter points
            line_kws={"color": "crimson", "lw": 2},  # Customize regression line
        )
        for patch in ax.collections:
            patch.set_alpha(0.5)  # Darkens the shaded portion
        ax.set_xlabel(x_label, fontsize=12, weight='bold')
        ax.set_ylabel(y_label, fontsize=12, weight='bold')
        ax.set_title('Linear Regression Fit', fontsize=14, weight='bold') 
        ax.grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.7)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)    
        #plt.show()
        
    def residual_plot(self,x, y, ax=None):
        if isinstance(x, dict):  
            x = np.array(list(x.values()))  
        elif isinstance(x, list):
            x = np.array(x)  

        if isinstance(y, dict):  
            y = np.array(list(y.values()))
        elif isinstance(y, list):
            y = np.array(y)
        if ax is None:
            ax = plt.gca()
            fig =plt.figure(figsize=(10, 6), dpi=600)  # Adjust size and set DPI
        sns.residplot(
            x=x, y=y, scatter_kws={"s": 60, "alpha": 0.8}, ax=ax,
            color="teal"
        )
        ax.set_title('Residual Plot', fontsize=14, weight='bold')
        ax.set_xlabel('Predicted Values', fontsize=12, weight='bold')
        ax.grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.7)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        #plt.show()
    
    def display_confusion_matrix(self, cm):
        
        
        #  Clear previous plots inside graph_display
        for widget in self.graph_display.winfo_children():
            widget.destroy()

        #  Compute percent matrix
        cm = np.array(cm)
        cm_percent = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis] * 100

        #  Create a matplotlib Figure
        fig = Figure(figsize=(4, 5), dpi=100)
        ax = fig.add_subplot(111)

        #  Plot the matrix
        disp = ConfusionMatrixDisplay(confusion_matrix=cm_percent)
        disp.plot(cmap="Blues", values_format=".1f", ax=ax, colorbar=False)

        #  Add percent signs to annotations
        for text in disp.text_.flatten():
            text.set_text(text.get_text() + '%')

        ax.set_title("Confusion Matrix (%)")

        #  Embed in the Tkinter frame
        canvas = FigureCanvasTkAgg(fig, master= self.graph_display)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)