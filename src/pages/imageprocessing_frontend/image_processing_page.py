# --- image_processing_page.py ---
import customtkinter as ctk
from tkinter import PhotoImage
from src.pages.imageprocessing_frontend.ui_manager import ImageUIManager
from src.pages.imageprocessing_frontend.request_manager import ImageRequestManager
from src.pages.imageprocessing_frontend.image_visualization import ImageVisualization
from src.utils.ui_element_manager import UIElementManager
from src.utils.ui_style_manager import StyleManager
from src.assets_management import assets_manage, load_image

class ImageProcessingPage(ctk.CTkFrame):
    def __init__(self, parent, file_path=None, file_name=None, data=None, **page_state):
        super().__init__(parent, corner_radius=0)
        self.parent = parent
        self.file_path = file_path
        self.file_name = file_name
        self.uploaded_image_path = None

        # Style
        self.color_theme = StyleManager.get_color("secondary")
        self.color_sidebar = StyleManager.get_color("dark_bg")
        self.right_frame_height = int(0.8 * self.winfo_screenheight())

        # Assets
        self.Info_button_image = PhotoImage(file=assets_manage("info_B.png"))
        self.upload_button_image = load_image("Upload Icon_B.png")

        # UI Element Manager
        self.ui = UIElementManager(
        info_icon_light=parent.info_icon_light,
        info_icon_dark=parent.info_icon_dark,
        parent_widget=self
        )
        

        # Managers
        self.managers = {}
        self.managers["ui"] = ImageUIManager(self, self.ui)
        self.managers["request"] = ImageRequestManager(self)
        self.managers["visualization"] = ImageVisualization(self)

        # Configure grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=9)
        self.grid_columnconfigure(1, weight=1)

        self._create_left_frame()
        self._create_right_frame()

        self.managers["ui"].initialize_segment("Image Processing")

    def _create_left_frame(self):
        self.left_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.left_frame.grid(row=0, column=0, sticky="nsew", padx=50, pady=10)
        self.left_frame.grid_columnconfigure(0, weight=2)

        self.label_frame = ctk.CTkFrame(self.left_frame, fg_color=self.color_theme, corner_radius=10, height=50)
        self.label_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.label = ctk.CTkLabel(self.label_frame, text=self.file_name, font=StyleManager.get_font("title"))
        self.label.place(relx=0.5, rely=0.5, anchor="center")

        self.cancel_button = ctk.CTkButton(self.left_frame, text="X", width=30, height=25, command=self.cancel_file)
        self.cancel_button.grid(row=0, column=1, padx=10, pady=10)

        self.graph_frame = ctk.CTkFrame(self.left_frame, fg_color=self.color_theme, corner_radius=10, height=350)
        self.graph_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.graph_frame.grid_columnconfigure(0, weight=1)
        self.graph_frame.grid_rowconfigure(0, weight=1)
        self.graph_frame.grid_rowconfigure(1, weight=4)

        self.log_display = ctk.CTkTextbox(self.graph_frame, height=250, wrap='word', fg_color="transparent")
        self.log_display.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

    def _create_right_frame(self):
        self.right_frame = ctk.CTkScrollableFrame(self, fg_color=self.color_sidebar, width=300, height=self.right_frame_height)
        self.right_frame.grid(row=0, column=1, sticky="en", padx=10, pady=10)
        self.right_frame.grid_columnconfigure(0, weight=1)

        self.segmented_frame = ctk.CTkSegmentedButton(self.right_frame, values=["Image Processing"], command=self.change_segment)
        self.segmented_frame.grid(row=0, column=0, padx=10, pady=10)
        self.segmented_frame.set("Image Processing")

        self.segment_container = ctk.CTkFrame(self.right_frame, fg_color="transparent")
        self.segment_container.grid(row=1, column=0, sticky="s", padx=20, pady=10)

        self.submit_button = ctk.CTkButton(self.right_frame, text="Submit", command=self.submit_action)
        self.submit_button.grid(row=2, column=0, pady=10)

    def change_segment(self, segment_name):
        self.managers["ui"].change_segment(segment_name)

    def submit_action(self):
        self.managers["request"].submit_action()

    def cancel_file(self):
        page_name = self.__class__.__name__
        self.parent.file_paths[page_name] = None
        self.parent.file_names[page_name] = None
        self.parent.page_data[page_name] = None

        self.parent.update_sidebar_buttons(page_name, action="remove")

        if hasattr(self.parent, f"{page_name}_instance"):
            delattr(self.parent, f"{page_name}_instance")

        self.parent.show_page("file_upload")
