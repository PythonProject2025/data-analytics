import customtkinter as ctk
from tkinter import Button, PhotoImage, Toplevel,messagebox

import pandas as pd
import requests
from src.models.data_object_class import DataObject
from src.assets_management import assets_manage, load_image
import re
import tkinter as tk
from tkinter import ttk


class RegressionClassificationpage(ctk.CTkFrame):
    def __init__(self, parent, file_data=None, file_name=None, *args, **kwargs):
        super().__init__(parent, corner_radius=0)

        self.parent=parent
        self.file_data=file_data
        self.file_name = file_name

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
            for key, value in split_data.items():
                if isinstance(value, pd.DataFrame):
                    dataobject.data_filtering["Train-Test Split"]["split_data"][key] = value.to_dict(orient="records")
                elif isinstance(value, pd.Series):
                    dataobject.data_filtering["Train-Test Split"]["split_data"][key] = value.tolist()  # Convert to list

        if current_segment == "Regression":
            model = self.regression_radio_var.get()
            print(f"Selected Regression Model: {model}")
            dataobject.regression["Selected Model"]=model
            errors = []
            
            
            if model == "Polynomial Regression":

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
                print(json_data)
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
                print(json_data)
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

                    dataobject.regression["Model_Selection"]["Lasso Regression"]["polynomial_degree_lasso"]=polynomial_degree_ridge_list
                    dataobject.regression["Model_Selection"]["Lasso Regression"]["alpha_values_lasso"]=alpha_values_ridge_list
                # Convert DataObject to JSON
                json_data = {"dataobject": dataobject.to_dict()}
                print(json_data)
                # Send request
                self.send_request_regression(json_data)

            print("\nSubmission Successful!\n")


        elif current_segment == "Classification":
             model = self.classification_radio_var.get()
             print(f"Selected Classification Model: {model}")
             dataobject.classification["Model_Selection"]= model
             if model == "RandomForest":
                print(f"n_estimators: {self.sliders["n_estimators"].get()}")
                print(f"max_depth: {self.sliders['max_depth'].get()}")
                dataobject.classification["RandomForest"]['n_estimators']= self.sliders['n_estimators'].get()
                dataobject.classification["RandomForest"]['max_depth']=self.sliders['max_depth'].get()
                # Convert DataObject to JSON
                json_data = {"dataobject": dataobject.to_dict()}
                print(json_data)
                # Send request
                self.send_request_classification(json_data)

             elif model == "SVC":
                print(f"C: {self.sliders['C'].get()}")
                print(f"Kernel: {self.dropdowns['Kernel'].get()}")
                print(f"Gamma: {self.dropdowns['Gamma'].get()}")
                dataobject.classification["SVC"]['C']= self.sliders['C'].get()
                dataobject.classification["SVC"]['Kernel']=self.dropdowns['Kernel'].get()
                dataobject.classification["SVC"]['Gamma']=self.dropdowns['Gamma'].get()
                # Convert DataObject to JSON
                json_data = {"dataobject": dataobject.to_dict()}
                print(json_data)
                # Send request
                self.send_request_classification(json_data)

             elif model == "KNN":
                print(f"n_neighbors: {self.sliders['n_neighbors'].get()}")
                print(f"Weights: {self.dropdowns['Weights'].get()}")
                dataobject.classification["KNN"]['n_neighbors']= self.sliders['n_neighbors'].get()
                dataobject.classification["KNN"]['Weights']=self.dropdowns['Weights'].get()
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
