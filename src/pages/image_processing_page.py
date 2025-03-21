import json
import customtkinter as ctk
from tkinter import Button, PhotoImage, Toplevel,messagebox,filedialog
from src.assets_management import assets_manage, load_image
from src.models.data_object_class import DataObject
import requests
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk
from tensorflow.keras.callbacks import Callback


class ImageProcessingPage(ctk.CTkFrame):
    def __init__(self, parent,file_path=None,file_name=None,data=None,**page_state):
        super().__init__(parent, corner_radius=0)

        right_frame_height = int(0.8 * self.winfo_screenheight())
        self.parent = parent
        self.file_name = file_name
        self.file_path = file_path
        self.uploaded_image_path = None
        

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
        self.log_display = ctk.CTkTextbox(self.graph_frame, height=250, wrap='word',fg_color="transparent")
        self.log_display.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        self.Info_button_image = PhotoImage(file=assets_manage("info_B.png"))
        self.upload_button_image = load_image("Upload Icon_B.png")

        # Right Side Frame (Segmented Buttons)
        self.right_frame = ctk.CTkScrollableFrame(self, fg_color="#171821", width=300 , height= right_frame_height)
        self.right_frame.grid(row=0, column=1, sticky="en", padx=10, pady=10)
        self.right_frame.grid_columnconfigure(0, weight=1)

        # Segmented Button Frame
        self.segmented_frame = ctk.CTkSegmentedButton(self.right_frame, values=["Image Processing"],
                                                      command=self.change_segment)
        self.segmented_frame.grid(row=0, column=0, padx=10, pady=10)
        self.segmented_frame.set("Image Processing")

        # Frame that holds all segment contents
        self.segment_container = ctk.CTkFrame(self.right_frame, fg_color="transparent")
        self.segment_container.grid(row=1, column=0, sticky="s", padx=20, pady=10)

        # Create segment frames
        self.segments = {
            "Image Processing": self.create_segment_frame()
        }

        # Submit Button
        self.submit_button = ctk.CTkButton(self.right_frame, text="Submit", command=self.submit_action)
        self.submit_button.grid(row=2, column=0, pady=10)

        # Show default segment
        self.current_segment = None
        self.change_segment("Image Processing")


    def create_segment_frame(self):
        """Creates a normal frame for each segment (not scrollable)."""
        frame = ctk.CTkFrame(self.segment_container, fg_color="#E0E0E0", corner_radius=10)
        frame.grid_columnconfigure(0, weight=1)

        def create_info_button(parent, text):
            """Creates an inline info button next to the label."""
            button = Button(parent, text="", image=self.Info_button_image, width=8, height=8, 
                            command=lambda: self.show_info_dialog(text))
            button.grid(row=0, column=1, padx=5, sticky="w")  

        # 🔹 Activation Function (Radio Buttons)
        radio_frame = ctk.CTkFrame(frame, fg_color="#D1D1D1", corner_radius=10)
        radio_frame.grid(row=0, column=0, padx=10, pady=15, sticky="new")

        radio_label = ctk.CTkLabel(radio_frame, text="Activation Function", font=("Inter", 12, "bold"), fg_color="#A0A0A0")
        radio_label.grid(row=0, column=0, sticky="nesw")
        create_info_button(radio_frame, "Select activation function")

        #  Store as an instance variable
        self.radio_var = ctk.StringVar(value="relu")  # Default: relu
        ctk.CTkRadioButton(radio_frame, text="ReLU", variable=self.radio_var, value="relu").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        ctk.CTkRadioButton(radio_frame, text="sigmoid", variable=self.radio_var, value="sigmoid").grid(row=1, column=1, padx=10, pady=5, sticky="w")

        # 🔹 Epochs (Slider)
        slider_frame = ctk.CTkFrame(frame, fg_color="#D1D1D1", corner_radius=10)
        slider_frame.grid(row=1, column=0, padx=10, pady=15, sticky="nsew")

        slider_label = ctk.CTkLabel(slider_frame, text="Epochs", font=("Inter", 12, "bold"), fg_color="#A0A0A0")
        slider_label.grid(row=0, column=0, sticky="new")
        create_info_button(slider_frame, "Number of training epochs")

        self.epoch_label = ctk.CTkLabel(slider_frame, text="Value: 5", font=("Inter", 12))
        self.epoch_label.grid(row=1, column=0, pady=5)

        def update_epoch(value):
            self.epoch_label.configure(text=f"Value: {int(value)}")

        self.epoch_slider = ctk.CTkSlider(slider_frame, from_=1, to=50, command=update_epoch)
        self.epoch_slider.set(5)  
        self.epoch_slider.grid(row=2, column=0, padx=10, sticky="ew")

        # 🔹 Optimizer (ComboBox)
        optimizer_frame = ctk.CTkFrame(frame, fg_color="#D1D1D1", corner_radius=10)
        optimizer_frame.grid(row=2, column=0, padx=10, pady=15, sticky="nsew")

        optimizer_label = ctk.CTkLabel(optimizer_frame, text="Optimizer", font=("Inter", 12, "bold"), fg_color="#A0A0A0")
        optimizer_label.grid(row=0, column=0, sticky="nesw")
        create_info_button(optimizer_frame, "Select optimizer for training")

        self.optimizer_combobox = ctk.CTkComboBox(optimizer_frame, values=["adam", "RMSPROP", "adamax"])
        self.optimizer_combobox.set("adam")  
        self.optimizer_combobox.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        # 🔹 Test Size (Slider)
        test_size_frame = ctk.CTkFrame(frame, fg_color="#D1D1D1", corner_radius=10)
        test_size_frame.grid(row=3, column=0, padx=10, pady=15, sticky="nsew")

        test_size_label = ctk.CTkLabel(test_size_frame, text="Test Size", font=("Inter", 12, "bold"), fg_color="#A0A0A0")
        test_size_label.grid(row=0, column=0, sticky="new")
        create_info_button(test_size_frame, "Fraction of dataset used for testing")

        self.test_size_value = ctk.CTkLabel(test_size_frame, text="Value: 0.2", font=("Inter", 12))
        self.test_size_value.grid(row=1, column=0, pady=5)

        def update_test_size(value):
            self.test_size_value.configure(text=f"Value: {float(value):.2f}")

        self.test_size_slider = ctk.CTkSlider(test_size_frame, from_=0.0, to=1.0, command=update_test_size)
        self.test_size_slider.set(0.2)  
        self.test_size_slider.grid(row=2, column=0, padx=10, sticky="ew")

        # 🔹 Random State (Slider)
        random_state_frame = ctk.CTkFrame(frame, fg_color="#D1D1D1", corner_radius=10)
        random_state_frame.grid(row=4, column=0, padx=10, pady=15, sticky="nsew")

        random_state_label = ctk.CTkLabel(random_state_frame, text="Random State", font=("Inter", 12, "bold"), fg_color="#A0A0A0")
        random_state_label.grid(row=0, column=0, sticky="new")
        create_info_button(random_state_frame, "Seed for reproducibility")

        self.random_state_value = ctk.CTkLabel(random_state_frame, text="Value: 42", font=("Inter", 12))
        self.random_state_value.grid(row=1, column=0, pady=5)

        def update_random_state(value):
            self.random_state_value.configure(text=f"Value: {int(value)}")

        self.random_state_slider = ctk.CTkSlider(random_state_frame, from_=0, to=100, command=update_random_state)
        self.random_state_slider.set(42)  
        self.random_state_slider.grid(row=2, column=0, padx=10, sticky="ew")

        return frame
    
    def create_image_train_frame(self):
        frame = ctk.CTkFrame(self.segment_container, fg_color="#E0E0E0", corner_radius=10)
        frame.grid_columnconfigure(0, weight=1)

        # Upload Image Button
        self.upload_button = ctk.CTkButton(frame, text="Upload Image",image=self.upload_button_image,command=self.upload_image)
        self.upload_button.grid(row=0, column=0, padx=10, pady=10)

        # Label to show uploaded file name
        self.image_label = ctk.CTkLabel(frame, text="No file uploaded", font=("Inter", 12))
        self.image_label.grid(row=1, column=0, padx=10, pady=5)

        # Preview Button
        self.preview_button = ctk.CTkButton(frame, text="Preview Image", command=self.preview_image, state="disabled")
        self.preview_button.grid(row=2, column=0, padx=10, pady=10)

        return frame

    def upload_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            self.uploaded_image_path = file_path
            self.image_label.configure(text=f"Uploaded: {file_path.split('/')[-1]}")
            self.preview_button.configure(state="normal")  # Enable preview button

    def preview_image(self):
       
        if self.uploaded_image_path:
            preview_window = ctk.CTkToplevel(self)
            preview_window.title("Image Preview")
            preview_window.geometry("500x500")
            preview_window.grab_set()  # Prevents flickering

            img = Image.open(self.uploaded_image_path)
            img.thumbnail((450, 450))
            img = ImageTk.PhotoImage(img)

            image_label = ctk.CTkLabel(preview_window, image=img, text="")
            image_label.image = img  # Keep a reference
            image_label.pack(expand=True)


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
        self.segmented_frame.set(segment_name)

    def submit_action(self):
        """Collects parameters from UI components and sends them to backend."""

        active_tab = self.segmented_frame.get()  

        if active_tab == "Image Processing":
            print("Image Processing Submitted")
        
            # Create Image Train tab only if it doesn't exist
            if "Image Train" not in self.segments:
                self.segmented_frame.configure(values=["Image Processing", "Image Train"])
                self.segments["Image Train"] = self.create_image_train_frame()

            

            
            # Activation Function Selection
            activation_function = self.radio_var.get()
        
            # Epochs
            epochs = int(self.epoch_slider.get())

            # Optimizer
            optimizer = self.optimizer_combobox.get()

            # Test Size
            test_size = float(self.test_size_slider.get())

            # Random State
            random_state = int(self.random_state_slider.get())

            # Create DataObject
            dataobject = DataObject()
            dataobject.image_processing["fileio"]["zipFilePath"] = self.file_path
            dataobject.image_processing["fileio"]["isZipped"] = True
            dataobject.image_processing["model_params"]["activation_fn"] = activation_function
            dataobject.image_processing["model_params"]["optimizer"] = optimizer
            dataobject.image_processing["training_params"]["epochs"] = epochs
            dataobject.image_processing["train_test_split"]["test_size"] = test_size
            dataobject.image_processing["train_test_split"]["random_state"] = random_state

            # Convert DataObject to JSON
            json_data = {"dataobject": dataobject.to_dict()}

            try:

                response = requests.post(
                    'http://127.0.0.1:8000/api/imageprocessing/',
                    json=json_data
                )

                if response.status_code == 200:
                    response_data = response.json()
                    
                    # Extract confusion matrix data
                    cm_data= response_data["confusionMatrix"]
                    test_loss =response_data["testLoss"]
                    test_accuracy=response_data["testAccuracy"]
                    
                    if cm_data:
                        self.plot_confusion_matrix(cm_data)  # Call plotting function
                        print("Response received successfully")
                    else:
                        messagebox.showerror("Error", "Confusion Matrix data not received.")
                else:
                    messagebox.showerror(
                        "Error", response.json().get('error', 'File upload failed.')
                    )
            except Exception as e:
                messagebox.showerror("Error", str(e))

        elif active_tab == "Image Train":
            print("Image Train Submitted")


    def plot_confusion_matrix(self, cm_data):
        popup = ctk.CTkToplevel(self)
        popup.title('Confusion Matrix')
        popup.geometry('800x800')
        
        labels = cm_data["labels"]
        cm_values = np.array(cm_data["values"])
        
        fig, ax = plt.subplots(figsize=(8, 8))
        cax = ax.matshow(cm_values, cmap="viridis")
        fig.colorbar(cax)

        for i in range(cm_values.shape[0]):
            for j in range(cm_values.shape[1]):
                ax.text(j, i, f"{cm_values[i, j]:.2f}", ha="center", va="center", color="white")

        ax.set_xticklabels([""] + labels, rotation=45)
        ax.set_yticklabels([""] + labels)
        
        canvas = FigureCanvasTkAgg(fig, master=popup)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill='both', expand=True)
        canvas.draw()

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





    

        

        