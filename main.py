import customtkinter as ctk
from PIL import Image
import os

from src.assets_management import assets_manage, load_image
from src.pages.file_upload_page import FileUploadPage
from src.pages.process_selection_page import ProcessSelectionPage
from src.pages.datafiltering_frontend.data_filtering_page import DataFilteringPage
from src.pages.help_page import HelpPage
from src.pages.imageprocessing_frontend.image_processing_page import ImageProcessingPage
from src.pages.aimodel_frontend.aimodel_page import AIModelPage
from src.pages.regression_classification import RegressionClassificationPage


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Data Analytics")
        self.geometry(f"{1100}x{580}")
        self.configure_grid()
        self.load_assets()

        self.file_path = None  # ✅ Initialize file_path
        self.file_name = None  # ✅ Initialize file_name
        self.page_data = {}  #
      

        #  Sidebar (Navigation)
        self.create_sidebar()

        #  Header Frame
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent", height=50, corner_radius=100)
        self.header_frame.grid(row=0, column=2, columnspan=8, sticky="nesw")
        self.load_header_image()

        #  Main Content Area (Initially File Upload Page)
        self.current_page = None
        

        self.file_paths = {
            "DataFilteringPage": None,
            "ImageProcessingPage": None,
            "RegressionClassificationPage": None,
            "AIModelPage": None
        }

        self.file_names = {
            "DataFilteringPage": None,
            "ImageProcessingPage": None,
            "RegressionClassificationPage": None,
            "AIModelPage": None
        }

        self.page_data = {  # ✅ Store processed data for each page
            "DataFilteringPage": None,
            "ImageProcessingPage": None,
            "RegressionClassificationPage": None,
            "AIModelPage": None
        }

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
        self.data_filtering_button_image = load_image("DF Icon_B.png")
        self.regression_button_image = load_image("Regression_B.png")
        self.aimodel_button_image = load_image("IP_B.png")
        self.image_processing_button_image = load_image("AI_B.png")


    def create_sidebar(self):
        """Creates the sidebar with navigation buttons dynamically based on active pages."""

        # Sidebar Frame
        self.sidebar_frame = ctk.CTkFrame(self, fg_color="#2C72EA", width=200, corner_radius=8)
        self.sidebar_frame.grid(row=0, column=1, rowspan=8, sticky="nsw")

        # Sidebar Label (Navigation Header)
        self.navigation_frame_label = ctk.CTkLabel(
            self.sidebar_frame, text="   ", compound="left",
            font=ctk.CTkFont(size=15, weight="bold")
        )
        self.navigation_frame_label.grid(row=0, column=0, padx=10, pady=5)  # Minimal padding

        # ✅ Store buttons in a dictionary for easy access
        self.sidebar_buttons = {}

        # Define buttons (name, page_key, image)
        buttons = [
            ("Dashboard", "file_upload", self.home_image),
            ("Help", "help", self.help_image),
            ("Mode", None, self.mode_image_light),  # Mode has its own function
            ("Data Filtering", "DataFilteringPage", self.data_filtering_button_image),
            ("Regression &\n Classification", "RegressionClassificationPage", self.regression_button_image),
            ("AI Model", "AIModelPage", self.aimodel_button_image),
            ("Image Processing", "ImageProcessingPage", self.image_processing_button_image),
        ]

        # ✅ Create buttons dynamically but keep them hidden
        for idx, (name, page, image) in enumerate(buttons, start=1):
            command = self.toggle_mode if name == "Mode" else lambda p=page: self.show_page(p)

            button = ctk.CTkButton(
                self.sidebar_frame, corner_radius=8, height=30, border_spacing=8,
                text=name, fg_color="transparent", text_color=("gray10", "gray90"),
                hover_color=("gray70", "gray30"), image=image, anchor="w",
                font=("Inter", 12), command=command
            )
            button.grid(row=idx, column=0, sticky="w", padx=2, pady=5)

            # ✅ Store the button reference
            self.sidebar_buttons[page] = button

            # ✅ Initially, hide all process-related buttons
            if page not in ["file_upload", "help", None]:  # Keep Dashboard & Help always visible
                button.grid_remove()
    
    def update_sidebar_buttons(self, active_page, action="add"):
        """
        Dynamically updates the sidebar buttons based on opened/closed pages.

        - "add": Shows the sidebar button for the active page.
        - "remove": Hides the sidebar button only if the file is deleted in that page.
        """

        if action == "add":
            #  Show the button for the active page
            if active_page in self.sidebar_buttons:
                self.sidebar_buttons[active_page].grid()

        elif action == "remove":
            #  Hide only if file is deleted in that specific page
            if active_page in self.sidebar_buttons:
                self.sidebar_buttons[active_page].grid_remove()
              #  Hide all other buttons except Dashboard & Help


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

    def show_page(self, page_name, *args, **kwargs):
        """Handles navigation while ensuring each page has its own file, name, and data."""
        
        if hasattr(self, "current_page") and self.current_page:
            self.current_page.grid_forget()  # ✅ Hide instead of destroying

        page_mapping = {
            "file_upload": FileUploadPage,  # ✅ No file_path, file_name, or data needed
            "help": HelpPage,  # ✅ No file_path, file_name, or data needed
            "DataFilteringPage": DataFilteringPage,
            "ImageProcessingPage": ImageProcessingPage,
            "AIModelPage": AIModelPage,
            "RegressionClassificationPage": RegressionClassificationPage
        }

        if page_name in page_mapping:
            page_class = page_mapping[page_name]

            # ✅ Only pass file_path, file_name, and data for pages that need them
            if page_name in ["DataFilteringPage", "ImageProcessingPage", "RegressionClassificationPage", "AIModelPage"]:
                kwargs["file_path"] = self.file_paths.get(page_name, None)
                kwargs["file_name"] = self.file_names.get(page_name, None)
                kwargs["data"] = self.page_data.get(page_name, None)

            # ✅ Reset page if a new file is uploaded
            if hasattr(self, f"{page_name}_instance") and kwargs.get("file_path") is None:
                delattr(self, f"{page_name}_instance")  # Remove old instance

            # ✅ Create new instance if it does not exist
            if not hasattr(self, f"{page_name}_instance"):
                self.current_page = page_class(self, **kwargs)
                setattr(self, f"{page_name}_instance", self.current_page)
            else:
                self.current_page = getattr(self, f"{page_name}_instance")

            self.current_page.grid(row=1, column=2, columnspan=7, rowspan=7, sticky="nsew")

            # ✅ Show the sidebar button for the newly opened page
            self.update_sidebar_buttons(page_name, action="add")

        else:
            print(f"Error: Page '{page_name}' not found!")

    

    
    def update_file_info(self, file_path, file_name):
        self.file_path = file_path
        self.file_name = file_name
  

        
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
