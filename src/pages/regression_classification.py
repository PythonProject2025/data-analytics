import customtkinter as ctk
from tkinter import Button, PhotoImage, Toplevel,messagebox
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
import pandas as pd
import requests
from src.models.data_object_class import DataObject
from src.assets_management import assets_manage, load_image
import re
import tkinter as tk
from tkinter import ttk


class RegressionClassificationPage(ctk.CTkFrame):
    def __init__(self, parent,file_path=None,file_name=None,data=None,**page_state):
        super().__init__(parent, corner_radius=0)

        self.parent=parent
        self.file_data=data
        self.file_name = file_name
        print(self.file_name)

         # ✅ Check if data is available
        if self.file_data is not None:
            print(f"✅ Received Preprocessed Data: {self.file_name}")
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
        self.label_frame = ctk.CTkFrame(self.left_frame, fg_color="#E0E0E0", corner_radius=10,height=50)
        self.label_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.left_frame.grid_rowconfigure(0, weight=0)
        self.label = ctk.CTkLabel(self.label_frame, text=self.file_name, font=("Inter", 16, "bold"))
        self.label.place(relx=0.5, rely=0.5, anchor="center")
        self.preview_label = ctk.CTkLabel(self.label_frame, text="Preview", font=("Inter", 12, "bold"),
                                  text_color="blue", cursor="hand2")
        self.preview_label.place(relx=0.9, rely=0.5, anchor="center")  # Adjusted position
        self.preview_label.bind("<Button-1>", lambda event: self.preview_data())
        self.cancel_button = ctk.CTkButton(self.left_frame, text="X", width=30, height=25, command=lambda: self.cancel_file())
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
        self.right_frame = ctk.CTkScrollableFrame(self, fg_color="#171821", width=300 , height= right_frame_height)
        self.right_frame.grid(row=0, column=1, sticky="en", padx=10, pady=10)
        self.right_frame.grid_columnconfigure(0, weight=1)

       # **Tabs for Regression & Classification**
        self.segmented_frame = ctk.CTkSegmentedButton(self.right_frame, values=["Regression", "Classification"],
                                                      command=self.change_segment)
        self.segmented_frame.grid(row=0, column=0, padx=10, pady=10)
        self.segmented_frame.set("Regression")

        # **Container for Segment Content**
        self.segment_container = ctk.CTkFrame(self.right_frame, fg_color="transparent")
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

        self.sliders = {}
        self.dropdowns = {}
        self.textboxes = {}


    def create_regression_frame(self):
        """Creates the Regression segment frame with dynamic parameters."""
        frame = ctk.CTkFrame(self.segment_container, fg_color="#E0E0E0", corner_radius=10)
        frame.grid_columnconfigure(0, weight=1)

        # **Regression Model Selection (Radio Buttons)**
        radio_frame = ctk.CTkFrame(frame, fg_color="#D1D1D1", corner_radius=10)
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

        self.regression_options_frame = ctk.CTkFrame(frame, fg_color="transparent")
        self.regression_options_frame.grid(row=1, column=0, padx=10, pady=15, sticky="new")
        

        return frame

    def create_classification_frame(self):
        """Creates the Classification segment frame with dynamic parameters."""
        frame = ctk.CTkFrame(self.segment_container, fg_color="#E0E0E0", corner_radius=10)
        frame.grid_columnconfigure(0, weight=1)

        # **Classification Model Selection (Radio Buttons)**
        radio_frame = ctk.CTkFrame(frame, fg_color="#D1D1D1", corner_radius=10)
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

        return frame

    def toggle_regression_options(self):
        """Updates the Regression options dynamically based on selection."""
        model = self.regression_radio_var.get()
        self.clear_frame(self.regression_options_frame)

        if model == "Polynomial Regression":
            self.create_textbox(self.regression_options_frame, "Polynomial Degree","polynomial")

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
        """Creates a labeled slider with info button."""
        frame = ctk.CTkFrame(parent, fg_color="#D1D1D1", corner_radius=10)
        frame.grid(row=len(parent.winfo_children()), column=0, padx=10, pady=10, sticky="nsew")

        label = ctk.CTkLabel(frame, text=label_text, font=("Inter", 12, "bold"), fg_color="#A0A0A0")
        label.grid(row=0, column=0, sticky="nesw")

        self.create_info_button(frame, f"Information about {label_text}")

        value_label = ctk.CTkLabel(frame, text=f"Value: {default}", font=("Inter", 12))
        value_label.grid(row=1, column=0, pady=5)

        def update_value(value):
            value_label.configure(text=f"Value: {float(value):.0f}" if isinstance(value, float) else f"Value: {int(value)}")

        slider = ctk.CTkSlider(frame, from_=min_val, to=max_val, command=update_value)
        slider.set(default)
        slider.grid(row=2, column=0, padx=10, sticky="ew")

        self.sliders[label_text] = slider  # Store reference

    def create_dropdown(self, parent, label_text, options):
        """Creates a labeled dropdown menu."""
        frame = ctk.CTkFrame(parent, fg_color="#D1D1D1", corner_radius=10)
        frame.grid(row=len(parent.winfo_children()), column=0, padx=10, pady=10, sticky="nsew")

        label = ctk.CTkLabel(frame, text=label_text, font=("Inter", 12, "bold"), fg_color="#A0A0A0")
        label.grid(row=0, column=0, sticky="nesw")

        self.create_info_button(frame, f"Information about {label_text}")

        combobox = ctk.CTkComboBox(frame, values=options)
        combobox.set(options[0])
        combobox.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        self.dropdowns[label_text] = combobox  # Store reference


    def create_textbox(self, parent, label_text, mode):
        """
        Creates a labeled textbox for different parameter types with validation upon submission.
        
        mode:
            - "polynomial": Allows 1-5 single-digit numbers (0-9), separated by commas.
            - "alpha": Allows 1-5 float values (0-1) with at least 4 decimal places, separated by commas.
        """
        frame = ctk.CTkFrame(parent, fg_color="#D1D1D1", corner_radius=10)
        frame.grid(row=len(parent.winfo_children()), column=0, padx=10, pady=10, sticky="nsew")

        label = ctk.CTkLabel(frame, text=label_text, font=("Inter", 12, "bold"), fg_color="#A0A0A0")
        label.grid(row=0, column=0, sticky="nesw")

        self.create_info_button(frame, f"Information about {label_text}")

        entry_var = ctk.StringVar()
        entry = ctk.CTkEntry(frame, textvariable=entry_var)
        entry.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        self.textboxes[label_text] = entry_var  # Store reference for validation on submit




    def show_info_dialog(self, text):
        """Displays an information dialog box."""
        dialog = ctk.CTkToplevel(self)
        dialog.title("Information")
        dialog.geometry("300x150")
        dialog.grab_set()
        ctk.CTkLabel(dialog, text=text, font=("Inter", 12)).pack(pady=20)
        ctk.CTkButton(dialog, text="OK", command=dialog.destroy).pack()


    def create_info_button(self,parent, text):
            """Creates an inline info button next to the label."""
            button = Button(parent, text="", image=self.Info_button_image, width=8, height=8, command=lambda: self.show_info_dialog(text))
            button.grid(row=0, column=1, padx=5, sticky="w") 

    def submit_action(self):
        """Handles submission and prints selected model parameters."""
        dataobject = DataObject()
        current_segment = self.segmented_frame.get()

        print(f"\n--- {current_segment} Submission ---")
        
        # Store the preprocessed data from file_data
        if self.file_data is not None:
            split_data = self.file_data  # Assuming file_data contains the split dataset
            print(type(split_data))
            for key, value in split_data.items():
                if isinstance(value, pd.DataFrame):
                    dataobject.data_filtering["Train-Test Split"]["split_data"][key] = value.to_dict(orient="records")
                elif isinstance(value, pd.Series):
                    dataobject.data_filtering["Train-Test Split"]["split_data"][key] = value.tolist()  # Convert to list

        if current_segment == "Regression":
            model = self.regression_radio_var.get()
            print(f"Selected Regression Model: {model}")
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
                     print(f"Polynomial Degree: {self.textboxes['Polynomial Degree'].get()}")

                     print(polynomial_degree_list)
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
                    print(alpha_values_ridge_list )
                    dataobject.regression["Model_Selection"]["Ridge Regression"]["polynomial_degree_ridge"]=polynomial_degree_ridge_list
                    dataobject.regression["Model_Selection"]["Ridge Regression"]["alpha_values_ridge"]=alpha_values_ridge_list
                    print(polynomial_degree_ridge_list)
                    print(f"Polynomial Degree (Ridge): {self.textboxes['Polynomial Degree (Ridge)'].get()}")
                    print(f"Alpha Values (Ridge): {self.textboxes['Alpha Values (Ridge)'].get()}")
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
                    print(polynomial_degree_Lasso_list)
                    print(alpha_values_Lasso_list)
                    print(f"Polynomial Degree (Lasso): {self.textboxes['Polynomial Degree (Lasso)'].get()}")
                    print(f"Alpha Values (Lasso): {self.textboxes['Alpha Values (Lasso)'].get()}")

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
                print(json_data)
                # Send request
                self.send_request_classification(json_data)

             elif model == "SVC":
                dataobject.classification["SVC"]["C"]= float(self.sliders['C'].get())
                dataobject.classification["SVC"]["kernel"]= self.dropdowns['Kernel'].get()
                dataobject.classification["SVC"]["gamma"]= self.dropdowns['Gamma'].get()
                dataobject.classification["SVC"]["kernel"]
                # Convert DataObject to JSON
                json_data = {"dataobject": dataobject.to_dict()}
                print(json_data)
                # Send request
                self.send_request_classification(json_data)

             elif model == "KNN":
                print(f"n_neighbors: {self.sliders["n_neighbors"].get()}")
                print(f"Weights: {self.dropdowns["Weights"].get()}")
                print(f"n_neighbors: {self.sliders["P"].get()}")
                dataobject.classification["KNN"]["n_neighbours"]= int(self.sliders['n_neighbors'].get())
                dataobject.classification["KNN"]["weights"]=self.dropdowns['Weights'].get()
                dataobject.classification["KNN"]["p"]=int(self.sliders['P'].get())
                print(dataobject.classification["KNN"]["weights"])               
                # Convert DataObject to JSON
                json_data = {"dataobject": dataobject.to_dict()}
                print(json_data)
                # Send request
                self.send_request_classification(json_data)

        print("\nSubmission Successful!\n")

    def preview_data(self):
        """Opens a new popup window to display the scaled and encoded data."""
        
        if not hasattr(self, "file_data") or self.file_data is None or self.file_data.empty:
            messagebox.showerror("Error", "No processed data available for preview!")
            return

        # ✅ Create a new popup window
        preview_window = ctk.CTkToplevel(self)
        preview_window.title("Processed Data Preview")
        preview_window.geometry("900x500")
        preview_window.grab_set()

        # ✅ Create a frame for the Treeview
        frame = tk.Frame(preview_window)
        frame.pack(fill="both", expand=True)

        # ✅ Treeview (Table) widget
        tree = ttk.Treeview(frame, columns=list(self.file_data.columns), show="headings")

        # ✅ Add column headers
        for col in self.file_data.columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)  # Adjust column width

        # ✅ Insert rows (limit to first 50 rows to avoid UI lag)
        for index, row in self.file_data.head(50).iterrows():
            tree.insert("", "end", values=list(row))

        # ✅ Add vertical scrollbar
        v_scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscroll=v_scrollbar.set)

        # ✅ Add horizontal scrollbar
        h_scrollbar = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)
        tree.configure(xscroll=h_scrollbar.set)

        # ✅ Pack elements
        tree.pack(side="top", fill="both", expand=True)
        v_scrollbar.pack(side="right", fill="y")
        h_scrollbar.pack(side="bottom", fill="x")

        print("✅ Processed Data preview displayed successfully!")
        
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
                    print(response_data)
                    # Check if Lasso Regression data is present
                    if "Lasso_Regression" in response_data:
                        print("🔹 Processing Lasso Regression Results...")
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
                        print("🔹 Processing Ridge Regression Results...")
                        # Extracting values for Ridge Regression
                        r2_score_ridge = response_data["r2_score_ridge"]
                        best_degree_ridge = response_data["best_degree_ridge"]
                        best_alpha_ridge = response_data["best_alpha_ridge"]
                        results_ridge = response_data["results_ridge"]
                        Ridge_Regression = response_data["Ridge_Regression"]

                        # Generate Ridge Regression Plot
                        self.ridge_plot(results_ridge, Ridge_Regression)  
                        
                    elif "best_polynomial_degree" in response_data:
                        print("🔹 Processing Polynomial Regression Results...")
                        r2_score_polynomial = response_data["r2_score_polynomial"]
                        y_pred = response_data["y_pred"]
                        best_polynomial_degree = response_data["best_polynomial_degree"]
                        x_data = response_data["x_data"]
                        y_test = response_data["y_test"]
                        x_label = response_data["x_label"]
                        y_label = response_data["y_label"]
                        
                    # Polynomial fit plot
                        self.polynomial_plot(x_data,y_test,y_pred,x_label,y_label,best_polynomial_degree)
                        
                    elif "r2_score_linear" in response_data:
                        # Extracting values from response_data
                        r2_score_linear = response_data["r2_score_linear"]
                        y_pred  = response_data["y_pred"]
                        x_data  = response_data["x_data"]  # x_label is given by User
                        y_test  = response_data["y_test"]
                        x_label = response_data["x_label"]
                        y_label = response_data["y_label"] 
                        
                        fig, axs = plt.subplots(1, 2, figsize=(12, 5))
                        
                    # Regression Plot
                        self.regression_plot(x_data,y_test,x_label,y_label,ax=axs[0])
                        
                    # Residual Plot
                        self.residual_plot(y_test,y_pred,ax=axs[1]) 
            else:
                    messagebox.showerror(
                        "Error", response.json().get('error', 'File upload failed.')
                    )
        except Exception as e:
                messagebox.showerror("Error", str(e))
                
        
    def send_request_classification(self, json_data):
            
        """Send the request to the Django backend and return the response."""
        print("sending to backend")
        try:
           
            response = requests.post(
                    "http://127.0.0.1:8000/api/classification/",
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
    
    def cancel_file(self):
        """Handles file cancellation and resets only this page."""
        
        page_name = self.__class__.__name__  # Get the page's class name

        self.parent.file_paths[page_name] = None  # ✅ Reset file path for this page
        self.parent.file_names[page_name] = None  # ✅ Reset file name for this page
        self.parent.page_data[page_name] = None   # ✅ Reset data for this page

        # ✅ Remove the sidebar button for this page only
        self.parent.update_sidebar_buttons(page_name, action="remove")

        # ✅ Reset this page instance so it opens fresh on next upload
        if hasattr(self.parent, f"{page_name}_instance"):
            delattr(self.parent, f"{page_name}_instance")

        # ✅ Go back to file upload page
        self.parent.show_page("file_upload")
        
    #lasso plotting
    def lasso_plot(self,results_lasso,best_params):
        plt.close('all')
    # Extract the relevant results
    #    results = data.results_lasso
    #    best_degree_mask = (results['param_polynomial_features__degree'] == data.best_degree_lasso)
    #    alphas = results['param_lasso_regression__alpha'][best_degree_mask]
    #    mean_scores = results['mean_test_score'][best_degree_mask]

        best_degree_mask = (np.array(results_lasso['param_polynomial_features__degree']) == best_params['best_degree_lasso'])
        alphas = list(np.array(results_lasso['param_lasso_regression__alpha'])[best_degree_mask])
        mean_scores = list(np.array(results_lasso['mean_test_score'])[best_degree_mask])
        
        print("Best Degree:", best_params['best_degree_lasso'])
        print("Alphas:", alphas)
        print("Mean Scores:", mean_scores)

        # Set the figure size and style
        plt.figure(figsize=(10, 6), dpi=120)
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
        
        plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
        plt.gca().yaxis.get_offset_text().set_visible(False)
        
        # Customize the legend to remove the line
        plt.legend(
            fontsize=12, loc='upper left', frameon=True, fancybox=True, shadow=True, borderpad=1, handlelength=0
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
        plt.show()
    
    def ridge_plot(self,results_ridge,best_params):
        plt.close('all')
        # Extract the relevant results
    #    results = data.results_ridge
    #    best_degree_mask = (results['param_polynomial_features__degree'] == data.best_degree_ridge)
    #    alphas = results['param_ridge_regression__alpha'][best_degree_mask]
    #    mean_scores = results['mean_test_score'][best_degree_mask]

    #    results = data.results_ridge
        best_degree_mask = (np.array(results_ridge['param_polynomial_features__degree']) == best_params['best_degree_ridge'])
        alphas = np.array(results_ridge['param_ridge_regression__alpha'])[best_degree_mask]
        mean_scores = np.array(results_ridge['mean_test_score'])[best_degree_mask]
        # Set the figure size and style
        plt.figure(figsize=(10, 6), dpi=120)
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
        plt.ylabel('Cross-Validation Score (R2 Score)', fontsize=14, weight='bold', labelpad=15)
        plt.title('Alpha vs Model Performance (Ridge Regression)', fontsize=16, weight='bold', pad=20)
        
        plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
        plt.gca().yaxis.get_offset_text().set_visible(False)
        
        # Customize the legend
        plt.legend(
            fontsize=12, loc='center right', frameon=True, fancybox=True, shadow=True, borderpad=1
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
        plt.show()
        
    def polynomial_plot(self, x_scatter, y_scatter, y_poly, x_label, y_label, degree):
        plt.close('all')
        """Generates and displays the Polynomial Regression plot."""
        try:
            if isinstance(y_scatter, dict):
                print("⚠️ Converting y_scatter dictionary to a list...")
                y_scatter = np.array(list(y_scatter.values()))

            x_scatter = np.array(x_scatter).flatten() if not isinstance(x_scatter, np.ndarray) else x_scatter.flatten()
            y_scatter = np.array(y_scatter).flatten() if not isinstance(y_scatter, np.ndarray) else y_scatter.flatten()
            y_poly = np.array(y_poly).flatten() if not isinstance(y_poly, np.ndarray) else y_poly.flatten()

            # ✅ Debug prints
            print("✅ Processed Polynomial Plot Data:")
            print("X Scatter:", x_scatter[:5])  # Print first 5 values
            print("Y Scatter:", y_scatter[:5])
            print("Y Poly:", y_poly[:5])

            # Set figure size and seaborn style
            plt.figure(figsize=(12, 7), dpi=120)
            sns.set_theme(style="ticks")

            # Scatter plot for actual data
            sns.scatterplot(
                x=x_scatter, y=y_scatter,
                color='#1f77b4',
                label='Actual Data', s=100, alpha=0.9,
                edgecolor='black', linewidth=0.7
            )

            # Line plot for polynomial regression
            sns.lineplot(
                x=x_scatter, y=y_poly,
                color='#ff5733',
                label='Polynomial Regression Line',
                linewidth=2.5
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
            plt.show()

        except Exception as e:
            print("❌ ERROR in polynomial_plot:", str(e))
            messagebox.showerror("Plot Error", str(e))
            
    def regression_plot(self,x, y, x_label, y_label, data=None, ax=None):
        plt.close('all')
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
        plt.show()
        
    def residual_plot(self,x, y, ax=None):
        plt.close('all')
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
            plt.figure(figsize=(10, 6), dpi=600)  # Adjust size and set DPI
        sns.residplot(
            x=x, y=y, scatter_kws={"s": 60, "alpha": 0.8}, ax=ax,
            color="teal"
        )
        ax.set_title('Residual Plot', fontsize=14, weight='bold')
        ax.set_xlabel('Predicted Values', fontsize=12, weight='bold')
        ax.grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.7)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        plt.show()
