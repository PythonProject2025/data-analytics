import customtkinter as ctk
from PIL import Image
import os

from src.assets_management import assets_manage, load_image
from src.pages.file_upload_page import FileUploadPage
from src.pages.process_selection_page import ProcessSelectionPage
from src.pages.data_filtering_page import DataFilteringPage
from src.pages.help_page import HelpPage
from src.pages.image_processing_page import ImageProcessingPage
from src.pages.aimodel_page import AImodelPage
from src.pages.regression_classification import RegressionClassificationpage


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Data Analytics")
        self.geometry(f"{1100}x{580}")
        self.configure_grid()
        self.load_assets()
      

        #  Sidebar (Navigation)
        self.create_sidebar()

        #  Header Frame
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent", height=50, corner_radius=100)
        self.header_frame.grid(row=0, column=2, columnspan=8, sticky="nesw")
        self.load_header_image()

        #  Main Content Area (Initially File Upload Page)
        self.current_page = None
        self.show_page("file_upload")

    def configure_grid(self):
        """Configures the layout grid."""
        self.grid_columnconfigure((4, 5, 6, 7, 8), weight=1)
        self.grid_columnconfigure((1), weight=0)
        self.grid_columnconfigure((2, 3), weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure((1, 2, 3, 4, 5, 6, 7), weight=1)

    def load_assets(self):
        """Loads all images used in the application."""
        self.home_image = load_image("home_dark.png")
        self.help_image = load_image("Help_B.png")
        self.mode_image_light = load_image("Mode_B.png")
        self.mode_image_dark = load_image("Mode_W.png")
        self.upload_button_image = load_image("button_4.png")


    def create_sidebar(self):
        """Creates the sidebar with navigation buttons."""


        self.sidebar_frame = ctk.CTkFrame(self, fg_color="#2C72EA", width=200, corner_radius=10)
        self.sidebar_frame.grid(row=0, column=1, rowspan=8, sticky="nsw")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.navigation_frame_label = ctk.CTkLabel(self.sidebar_frame, text="  ",
                                                             compound="left", font=ctk.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=5)

        self.home_button = ctk.CTkButton(self.sidebar_frame, corner_radius=16, height=30, border_spacing=10, text="Dashboard",
                                         fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                         image=self.home_image, anchor="w", font=("Inter", 12), command=lambda: self.show_page("file_upload"))
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.help_button = ctk.CTkButton(self.sidebar_frame, corner_radius=16, height=40, border_spacing=10, text="Help",
                                         fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                         image=self.help_image, anchor="w", font=("Inter", 12), command=lambda: self.show_page("help"))
        self.help_button.grid(row=2, column=0, sticky="ew")

        self.mode_button = ctk.CTkButton(self.sidebar_frame, corner_radius=16, height=40, border_spacing=10, text="Mode",
                                         fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                         image=self.mode_image_light, anchor="w", font=("Inter", 12), command=self.toggle_mode)
        self.mode_button.grid(row=3, column=0, sticky="ew")

    def load_header_image(self):
        """Loads the header image."""
        image_path = assets_manage("Data Analytics.png")
        img = Image.open(image_path)
        resized_img = img.resize((self.winfo_width(), 60))
        header_img = ctk.CTkImage(light_image=resized_img, dark_image=resized_img, size=(self.winfo_width(), 60))

        self.header_label = ctk.CTkLabel(self.header_frame, text="", image=header_img)
        self.header_label.grid(sticky="n")
        self.header_label.image = header_img

        self.bind("<Configure>", self.resize_header_image)

    def resize_header_image(self, event):
        """Resizes the header image when the window is resized."""
        image_path = assets_manage("Data Analytics.png")
        img = Image.open(image_path)
        resized_img = img.resize((self.winfo_width(), 60))
        header_img = ctk.CTkImage(light_image=resized_img, dark_image=resized_img, size=(self.winfo_width(), 60))

        self.header_label.configure(image=header_img)
        self.header_label.image = header_img

    def show_page(self, page_name,*args,**kwargs):
        """Handles navigation between different pages."""

        if hasattr(self, "current_page") and self.current_page:
            self.current_page.destroy()  # Destroy the current page before switching

        # Map page names to corresponding classes
        page_mapping = {
            "file_upload": FileUploadPage,
            "Process_selection":ProcessSelectionPage,
            "help": HelpPage,
            "DataFilteringPage": DataFilteringPage,
           "ImageProcessingPage": ImageProcessingPage,
           "AIModelPage" : AImodelPage,
           "RegressionClassificationPage": RegressionClassificationpage
        }

        if page_name in page_mapping:
            self.current_page = page_mapping[page_name](self, *args,**kwargs)
            self.current_page.grid(row=1, column=2, columnspan=7, rowspan=7, sticky="nsew") # Ensure it fills the UI
        else:
            print(f"Error: Page '{page_name}' not found!")




    def toggle_mode(self):
        """Toggles between Light and Dark mode."""
        current_mode = ctk.get_appearance_mode()
        new_mode = "dark" if current_mode == "Light" else "Light"
        ctk.set_appearance_mode(new_mode)

        # Update mode button icon
        self.mode_button.configure(image=self.mode_image_dark if new_mode == "dark" else self.mode_image_light)


if __name__ == "__main__":
    app = App()
    app.mainloop()
