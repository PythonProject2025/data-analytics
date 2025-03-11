import customtkinter as ctk
from tkinter import Button, PhotoImage
from src.assets_management import assets_manage


class ProcessSelectionPage(ctk.CTkFrame):
    def __init__(self, parent, file_path,filename):
        super().__init__(parent, corner_radius=0)


        #  Configure Main Frame Layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        #  Reduced Height Text Box Frame
        self.textbox_frame = ctk.CTkFrame(self, fg_color="#E0E0E0", corner_radius=10, height=40)
        self.textbox_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        self.textbox_frame.grid_columnconfigure(0, weight=1)

        # Display Filename (Centered)
        self.filename_label = ctk.CTkLabel(self.textbox_frame, text=filename, font=("Inter", 14, "bold"))
        self.filename_label.place(relx=0.5, rely=0.5, anchor="center")


        # Cancel Button (Navigates to File Upload Page)
        self.cancel_button = ctk.CTkButton(
            self.textbox_frame, text="X", width=30, height=25,
            command=lambda: parent.show_page("file_upload")
        )
        self.cancel_button.grid(row=0, column=1, padx=10, pady=5, sticky="e")  # Align Right

        # Button Frame (Holds Process Selection Buttons)
        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.grid(row=1, column=0, pady=20, sticky="nsew")
        self.button_frame.grid_columnconfigure(0, weight=1)


        self.data_filtering_button_image = PhotoImage(file=assets_manage("datafiltering_option.png"))
        # Data Filtering Button
        self.data_filtering_button = Button(
            self.button_frame, text="", image=self.data_filtering_button_image,font=("Inter", 14, "bold"),
            width=int(parent.winfo_width() * 0.4),  # 60% Width
            height=70,
            command=lambda: parent.show_page("DataFilteringPage",file_path,filename)
        )
        self.data_filtering_button.grid(row=0, column=0, padx=20, pady=40, sticky="ew")

        #  Regression & Classification Button
        self.regression_button = ctk.CTkButton(
            self.button_frame, text="Regression and Classification", font=("Inter", 14, "bold"),
            width=100,  # 60% Width
            height=70, fg_color="#2C72EA",
            command=lambda: parent.show_page("RegressionClassificationPage",filename)
        )
        self.regression_button.grid(row=1, column=0, padx=20, pady=40, sticky="ew")

        #  AI Model Button
        self.ai_model_button = ctk.CTkButton(
            self.button_frame, text="AI Model", font=("Inter", 14, "bold"),
            width=int(parent.winfo_width() * 0.4),  # 60% Width
            height=70, fg_color="#2C72EA",
            command=lambda: parent.show_page("AIModelPage",filename)
        )
        self.ai_model_button.grid(row=2, column=0, padx=20, pady=40, sticky="ew")
