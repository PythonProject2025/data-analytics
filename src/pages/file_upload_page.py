import customtkinter as ctk
import os
from tkinter import Button, PhotoImage, filedialog
from src.assets_management import assets_manage

class FileUploadPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, corner_radius=0, fg_color="transparent")
        self.app = parent  # Reference to main app
        self.file_path = None

        #  Configure grid to center the upload frame
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0,weight=1)  # Top spacing
        self.grid_rowconfigure(1, weight=0)  # Centered row for upload frame
        self.grid_rowconfigure(2, weight=1)  # Bottom spacing

        #  Upload Frame (Bigger & More Spacious)
        self.upload_frame = ctk.CTkFrame(self, fg_color="#171821", width=1000, height=300, corner_radius=20)
        self.upload_frame.grid(row=1, column=0, columnspan=2, pady=40, sticky="n",ipady=30,ipadx=20)

        #  Configure upload frame grid
        self.upload_frame.grid_rowconfigure(0, weight=1)
        self.upload_frame.grid_rowconfigure(1, weight=0)
        self.upload_frame.grid_rowconfigure(2, weight=1)
        self.upload_frame.grid_columnconfigure(0, weight=1)

        #  Upload Label (Larger Font)
        self.upload_label = ctk.CTkLabel(
            self.upload_frame, text=" Upload Files Here (.csv or .zip)",
            font=("Inter", 20, "bold"), text_color="#FFFFFF",width=300
        )
        self.upload_label.grid(row=2, column=0, pady=(0, 0))


        #  Load Button Image
        self.button_image = PhotoImage(file=assets_manage("button_4.png"))

        #  Create Standard Tkinter Button (Replacing CTkButton)
        self.upload_button = Button(
            self.upload_frame,
            image=self.button_image,
            borderwidth=0,
            highlightthickness=0,
            command=self.upload_file,
            relief="flat"
        )
        self.upload_button.grid(row=1, column=0, padx=40, pady=20)  # Adjusted placement inside the frame

    def upload_file(self):
        """Handles file upload and assigns the correct page based on file type."""
        
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv"), ("Zip Files", "*.Zip")])

        if not file_path:
            return  # ✅ No file selected, do nothing

        file_name = file_path.split("/")[-1]  # Extract file name

        # ✅ Determine which page should handle the file
        if file_path.endswith(".csv"):
            target_page = "DataFilteringPage"
        else:
            target_page = "ImageProcessingPage"

        # ✅ Store the file path & name for the correct page
        self.app.file_paths[target_page] = file_path
        self.app.file_names[target_page] = file_name
        self.app.page_data[target_page] = None  # Reset previous data

        # ✅ Open the target page with the new file
        self.app.show_page(target_page)
