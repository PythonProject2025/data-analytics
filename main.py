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

        self.file_path = None
        self.file_name = None
        self.page_data = {}

        # Sidebar
        self.create_sidebar()

        # Header
        self.create_header()

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

        self.page_data = {
            "DataFilteringPage": None,
            "ImageProcessingPage": None,
            "RegressionClassificationPage": None,
            "AIModelPage": None
        }

        self.show_page("file_upload")

    def configure_grid(self):
        self.grid_columnconfigure((4, 5, 6, 7, 8), weight=1)
        self.grid_columnconfigure((1), weight=0)
        self.grid_columnconfigure((2, 3), weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure((1, 2, 3, 4, 5, 6, 7), weight=1)

    def load_assets(self):
        self.home_image_dark = load_image("home_dark.png")
        self.home_image_light = load_image("home_light.png")
        self.help_image_dark = load_image("Help_B.png")
        self.help_image_light = load_image("Help_W.png")
        self.mode_image_light = load_image("Mode_W.png")
        self.mode_image_dark = load_image("Mode_B.png")
        self.upload_button_image_dark = load_image("Upload Icon_B.png")
        self.upload_button_image_light = load_image("Upload Icon_W.png")
        self.data_filtering_button_image_dark = load_image("DF Icon_B.png")
        self.data_filtering_button_image_light = load_image("DF Icon_W.png")
        self.regression_button_image_dark = load_image("Regression_B.png")
        self.regression_button_image_light = load_image("Regression_W.png")
        self.aimodel_button_image_dark = load_image("IP_B.png")
        self.aimodel_button_image_light = load_image("IP_W.png")
        self.image_processing_button_image_dark = load_image("AI_B.png")
        self.image_processing_button_image_light = load_image("AI_W.png")
        self.header_icon_light = assets_manage("Combo Chart_W.png")
        self.info_icon_dark = load_image("Info_B.png")
        self.info_icon_light = load_image("Info_W.png")

    def create_header(self):
        self.header_frame = ctk.CTkFrame(
            self, fg_color="#3B506B", height=65, corner_radius=8
        )
        self.header_frame.grid(row=0, column=2, columnspan=8, sticky="nsew", padx=10, pady=10)

        header_inner_frame = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        header_inner_frame.place(relx=0.5, rely=0.5, anchor="center")

        icon_img = Image.open(self.header_icon_light).resize((22, 22))
        icon_ctk = ctk.CTkImage(light_image=icon_img, dark_image=icon_img, size=(35, 35))

        icon_label = ctk.CTkLabel(header_inner_frame, text="", image=icon_ctk)
        icon_label.pack(side="left", padx=(0, 8))

        header_font = ctk.CTkFont(family="Verdana", size=20, weight="bold")
        title_label = ctk.CTkLabel(header_inner_frame, text="DataAnalytics", font=header_font, text_color="white")
        title_label.pack(side="left")

    def create_sidebar(self):
        self.sidebar_frame = ctk.CTkFrame(self, fg_color="#3B506B", width=200, corner_radius=8)
        self.sidebar_frame.grid(row=0, column=1, rowspan=8, sticky="nsw")

        self.navigation_frame_label = ctk.CTkLabel(
            self.sidebar_frame, text="   ", compound="left",
            font=ctk.CTkFont(size=15, weight="bold")
        )
        self.navigation_frame_label.grid(row=0, column=0, padx=10, pady=5)

        self.sidebar_buttons = {}

        self.mode_button = None  # <-- Define it so we can access it in toggle_mode

        buttons = [
            ("Dashboard", "file_upload", self.home_image_light),
            ("Help", "help", self.help_image_light),
            ("Mode", None, self.mode_image_light),
            ("Data Filtering", "DataFilteringPage", self.data_filtering_button_image_light),
            ("Regression &\n Classification", "RegressionClassificationPage", self.regression_button_image_light),
            ("AI Model", "AIModelPage", self.aimodel_button_image_light),
            ("Image Processing", "ImageProcessingPage", self.image_processing_button_image_light),
        ]

        for idx, (name, page, image) in enumerate(buttons, start=1):
            command = self.toggle_mode if name == "Mode" else lambda p=page: self.show_page(p)

            button = ctk.CTkButton(
                self.sidebar_frame, corner_radius=8, height=30, border_spacing=8,
                text=name, fg_color="transparent", text_color=("gray90"),
                hover_color=("gray70", "gray30"), image=image, anchor="w",
                font=("Inter", 12), command=command
            )
            button.grid(row=idx, column=0, sticky="w", padx=2, pady=5)

            if name == "Mode":
                self.mode_button = button  # <-- Store reference for toggling icon

            self.sidebar_buttons[page] = button
            if page not in ["file_upload", "help", None]:
                button.grid_remove()

    def update_sidebar_buttons(self, active_page, action="add"):
        if action == "add":
            if active_page in self.sidebar_buttons:
                self.sidebar_buttons[active_page].grid()
        elif action == "remove":
            if active_page in self.sidebar_buttons:
                self.sidebar_buttons[active_page].grid_remove()

    def show_page(self, page_name, *args, **kwargs):
        if hasattr(self, "current_page") and self.current_page:
            self.current_page.grid_forget()

        page_mapping = {
            "file_upload": FileUploadPage,
            "help": HelpPage,
            "DataFilteringPage": DataFilteringPage,
            "ImageProcessingPage": ImageProcessingPage,
            "AIModelPage": AIModelPage,
            "RegressionClassificationPage": RegressionClassificationPage
        }

        if page_name in page_mapping:
            page_class = page_mapping[page_name]
            if page_name in self.file_paths:
                kwargs["file_path"] = self.file_paths.get(page_name, None)
                kwargs["file_name"] = self.file_names.get(page_name, None)
                kwargs["data"] = self.page_data.get(page_name, None)

            if hasattr(self, f"{page_name}_instance") and kwargs.get("file_path") is None:
                delattr(self, f"{page_name}_instance")

            if not hasattr(self, f"{page_name}_instance"):
                self.current_page = page_class(self, **kwargs)
                setattr(self, f"{page_name}_instance", self.current_page)
            else:
                self.current_page = getattr(self, f"{page_name}_instance")

            self.current_page.grid(row=1, column=2, columnspan=7, rowspan=7, sticky="nsew")
            self.update_sidebar_buttons(page_name, action="add")
        else:
            print(f"Error: Page '{page_name}' not found!")

    def update_file_info(self, file_path, file_name):
        self.file_path = file_path
        self.file_name = file_name

    def toggle_mode(self):
        """Toggles between Light and Dark mode and updates button icon."""
        current_mode = ctk.get_appearance_mode()
        new_mode = "dark" if current_mode == "Light" else "Light"
        ctk.set_appearance_mode(new_mode)


if __name__ == "__main__":
    app = App()
    app.mainloop()
