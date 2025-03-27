import customtkinter as ctk
from tkinter import Button, PhotoImage, Toplevel,messagebox

import pandas as pd
import requests
from src.models.data_object_class import DataObject
from src.assets_management import assets_manage, load_image
import tkinter as tk
from tkinter import ttk


class AIModelPage(ctk.CTkFrame):
    def __init__(self, parent,file_path=None,file_name=None,data=None,**page_state):
        super().__init__(parent, corner_radius=0)

        self.parent=parent
        self.file_data=data
        self.file_name = file_name
        right_frame_height = int(0.8 * self.winfo_screenheight())
        self.sliders = {}
        self.comboboxes ={}


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

       
        # Graph Display Area (Expanded)
        self.graph_display = ctk.CTkFrame(self.graph_frame, fg_color="#D1D1D1", height=250, corner_radius=10)  # Increased Size
        self.graph_display.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")  # Expands to fill space


        self.Info_button_image = PhotoImage(file=assets_manage("info_B.png"))

        # Right Side Frame (Segmented Buttons for AI Model)
        self.right_frame = ctk.CTkScrollableFrame(self, fg_color="#171821", width=300 , height= right_frame_height)
        self.right_frame.grid(row=0, column=1, sticky="en", padx=10, pady=10)
        self.right_frame.grid_columnconfigure(0, weight=1)

        # Segmented Button for AI Model
        self.segmented_frame = ctk.CTkSegmentedButton(self.right_frame, values=["RandomForest", "CatBoost", "ArtificialNeuralNetwork", "XGBoost"],
                                                    command=self.change_segment)
        self.segmented_frame.grid(row=0, column=0, padx=10, pady=10)
        self.segmented_frame.set("RandomForest")  # Default Segment

        # Frame that holds AI Model settings
        self.segment_container = ctk.CTkFrame(self.right_frame, fg_color="transparent")
        self.segment_container.grid(row=1, column=0, sticky="s", padx=20, pady=10)

        # Create segment frames
        self.segments = {
            "RandomForest": self.create_rf_frame(),
            "CatBoost": self.create_cb_frame(),
            "ArtificialNeuralNetwork": self.create_ann_frame(),
            "XGBoost": self.create_xgb_frame()
        }

        # Submit Button
        self.submit_button = ctk.CTkButton(self.right_frame, text="Submit", command=self.submit_action)
        self.submit_button.grid(row=2, column=0, pady=10)

        # Show default segment
        self.current_segment = None
        self.change_segment("RandomForest")
        


    def create_rf_frame(self):
        """Creates a frame for Random Forest parameters."""
        frame = ctk.CTkFrame(self.segment_container, fg_color="#E0E0E0", corner_radius=10)
        frame.grid_columnconfigure(0, weight=1)

        # Sliders for Random Forest
        self.create_slider_frame(frame, "RandomForest","n_estimators", 10, 500, 200, row=0)
        self.create_slider_frame(frame, "RandomForest","max_depth", 3, 50, 20, row=1)
        self.create_slider_frame(frame, "RandomForest","min_samples_split", 4, 10, 5, row=2)
        self.create_slider_frame(frame, "RandomForest","min_samples_leaf", 1, 10, 1, row=3)

        return frame


    def create_cb_frame(self):
        """Creates a frame for CatBoost parameters."""
        frame = ctk.CTkFrame(self.segment_container, fg_color="#E0E0E0", corner_radius=10)
        frame.grid_columnconfigure(0, weight=1)

        # Sliders for CatBoost
        self.create_slider_frame(frame, "CatBoost","n_estimators", 100, 1000, 500, row=0)
        self.create_slider_frame(frame, "CatBoost","learning_rate", 0.01, 0.1, 0.03, row=1)
        self.create_slider_frame(frame, "CatBoost","max_depth", 4, 10, 6, row=2)
        self.create_slider_frame(frame, "CatBoost","reg_lambda", 1, 10, 3, row=3)

        return frame


    def create_ann_frame(self):
        """Creates a frame for Artificial Neural Network parameters."""
        frame = ctk.CTkFrame(self.segment_container, fg_color="#E0E0E0", corner_radius=10)
        frame.grid_columnconfigure(0, weight=1)

        # Sliders for ArtificialNeuralNetwork
        self.create_slider_frame(frame, "ArtificialNeuralNetwork","Layer Number", 1, 6, 3, row=0)
        self.create_slider_frame(frame, "ArtificialNeuralNetwork","Units", 1, 256, 128, row=1)
        
        # Activation Function Dropdown
        self.create_combobox_frame(frame, "Activation Function", ["relu", "sigmoid", "tanh", "softmax"], "relu", row=2)
        
        # Optimizer Dropdown
        self.create_combobox_frame(frame, "Optimizer", ["adam", "sgd", "rmsprop"], "adam", row=3)
        
        # Sliders for ANN
        self.create_slider_frame(frame, "ArtificialNeuralNetwork","Batch Size", 16, 128, 30, row=4)
        self.create_slider_frame(frame, "ArtificialNeuralNetwork","Epochs", 10, 300, 100, row=5)

        return frame


    def create_xgb_frame(self):
        """Creates a frame for XGBoost parameters."""
        frame = ctk.CTkFrame(self.segment_container, fg_color="#E0E0E0", corner_radius=10)
        frame.grid_columnconfigure(0, weight=1)

        # Sliders for XGBoost
        self.create_slider_frame(frame, "XGBoost","n_estimators", 100, 1000, 200, row=0)
        self.create_slider_frame(frame, "XGBoost","learning_rate", 0.01, 0.3, 0.3, row=1)
        self.create_slider_frame(frame, "XGBoost","min_split_loss", 3, 10, 10, row=2)
        self.create_slider_frame(frame, "XGBoost","max_depth", 0, 10, 6, row=3)

        return frame
    

    def create_slider_frame(self, parent, model_name,label_text, from_, to, default, row):
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

        
        if model_name not in self.sliders:
            self.sliders[model_name] = {}

        # ✅ Store the slider under its model category
        self.sliders[model_name][label_text] = slider


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

        self.comboboxes[label_text] = combobox


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

    from tkinter import messagebox

    def change_segment(self, segment_name):
        """Switch between segment frames with validation checks."""
        if segment_name == "ArtificialNeuralNetwork":
            messagebox.showwarning("Model Restriction", "This method is only for regression.")
            

        elif segment_name == "XGBoost":
            messagebox.showwarning("Model Restriction", "This method is only for classification.")
           

        # If switching is allowed, update the tab
        if self.current_segment:
            self.current_segment.grid_forget()
        self.current_segment = self.segments[segment_name]
        self.current_segment.grid(row=1, column=0, sticky="nsew")
        self.segmented_frame.set(segment_name)  # Highlight the active segment

    def submit_action(self):
        """Submit button action with printing respective slider values."""
        selected_model = self.segmented_frame.get()  # Get the currently selected model
        
        dataobject = DataObject()
        # Store the preprocessed data from file_data
        if self.file_data is not None:
            split_data = self.file_data  # Assuming file_data contains the split dataset
            for key, value in split_data.items():
                if isinstance(value, pd.DataFrame):
                    dataobject.data_filtering["Train-Test Split"]["split_data"][key] = value.to_dict(orient="records")
                elif isinstance(value, pd.Series):
                    dataobject.data_filtering["Train-Test Split"]["split_data"][key] = value.tolist()  # Convert to list

            # Retrieve slider values for the selected model
        if selected_model == "RandomForest":
        
            dataobject.ai_model["Selected Model"]= selected_model
            dataobject.ai_model["RandomForest"]["n_estimators"] = int(round(self.sliders["RandomForest"]["n_estimators"].get()))
            dataobject.ai_model["RandomForest"]["max_depth"] = int(round(self.sliders["RandomForest"]["max_depth"].get()))
            dataobject.ai_model["RandomForest"]["min_samples_split"]= int(round(self.sliders["RandomForest"]["min_samples_split"].get()))
            dataobject.ai_model["RandomForest"]["min_samples_leaf"]= int(round(self.sliders["RandomForest"]["min_samples_leaf"].get()))
            

            # Convert DataObject to JSON
            json_data = {"dataobject": dataobject.to_dict()}
            # Send request
            self.send_request(json_data)
            
        elif selected_model == "CatBoost":
            
            dataobject.ai_model["Selected Model"]= selected_model
            dataobject.ai_model["CatBoost"]["n_estimators"] = float(self.sliders["CatBoost"]["n_estimators"].get())
            dataobject.ai_model["CatBoost"]["learning_rate"] = float(self.sliders["CatBoost"]["learning_rate"].get())
            dataobject.ai_model["CatBoost"]["max_depth"]= float(self.sliders["CatBoost"]["max_depth"].get())
            dataobject.ai_model["CatBoost"]["reg_lambda"]= float(self.sliders["CatBoost"]["reg_lambda"].get())
            
            # Convert DataObject to JSON
            json_data = {"dataobject": dataobject.to_dict()}
            # Send request
            self.send_request(json_data)
            
        elif selected_model == "ArtificialNeuralNetwork":
            
            dataobject.ai_model["Selected Model"]= selected_model
            dataobject.ai_model["ArtificialNeuralNetwork"]["layer_number"] = float(self.sliders["ArtificialNeuralNetwork"]["Layer Number"].get())
            dataobject.ai_model["ArtificialNeuralNetwork"]["units"] = float(self.sliders["ArtificialNeuralNetwork"]["Units"].get())
            dataobject.ai_model["ArtificialNeuralNetwork"]["activation"]= self.get_combobox_value("Activation Function")
            dataobject.ai_model["ArtificialNeuralNetwork"]["optimizer"]= self.get_combobox_value("Optimizer")
            dataobject.ai_model["ArtificialNeuralNetwork"]["batch_size"]= float(self.sliders["ArtificialNeuralNetwork"]["Batch Size"].get())
            dataobject.ai_model["ArtificialNeuralNetwork"]["epochs"]= float(self.sliders["ArtificialNeuralNetwork"]["Epochs"].get())
            
            # Convert DataObject to JSON
            json_data = {"dataobject": dataobject.to_dict()}
            # Send request
            self.send_request(json_data)

        elif selected_model == "XGBoost":
            
            dataobject.ai_model["Selected Model"] = selected_model
            dataobject.ai_model["XGBoost"]["n_estimators"] = int(round(self.sliders["XGBoost"]["n_estimators"].get()))
            dataobject.ai_model["XGBoost"]["learning_rate"] = int(round(self.sliders["XGBoost"]["learning_rate"].get()))
            dataobject.ai_model["XGBoost"]["min_split_loss"]= int(round(self.sliders["XGBoost"]["min_split_loss"].get()))
            dataobject.ai_model["XGBoost"]["max_depth"]= int(round(self.sliders["XGBoost"]["max_depth"].get()))
            
            # Convert DataObject to JSON
            json_data = {"dataobject": dataobject.to_dict()}
            # Send request
            self.send_request(json_data)

    def get_slider_value(self, slider_name):
        """Helper function to retrieve slider values."""
        for widget in self.current_segment.winfo_children():
            if isinstance(widget, ctk.CTkSlider) and slider_name in widget.winfo_parent():
                return widget.get()
        return 0

    def get_combobox_value(self, combobox_name):
        """Helper function to retrieve combobox values."""
        for widget in self.current_segment.winfo_children():
            if isinstance(widget, ctk.CTkComboBox) and combobox_name in widget.winfo_parent():
                return widget.get()
        return None
    
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
    
    def send_request(self, json_data):
        """Send the request to the Django backend and return the response."""
 
        try:
           
            response = requests.post(
                    "http://127.0.0.1:8000/api/ai_model/",
                    json=json_data
            )
 
            if response.status_code == 200:
                    response_data = response.json()
                    
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