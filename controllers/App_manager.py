import time
from tkinter import Canvas,PhotoImage,Button
from utils.ui_element_manager import ElementManager
from utils.asset_manager import get_asset_path
from views.file_uploader_page import FileUploader
from views.process_selection_page import process_selection_page
from views.data_preprocessing_pipeline import data_preprocessing_pipeline
from views.regression_classification_pipeline import regression_classification_pipeline
from views.ai_models_pipeline import ai_models_pipeline
from views.image_processing_pipeline import image_processing_pipeline


class App:
    def __init__(self, window):
        self.window = window
        self.screen_width = self.window.winfo_screenwidth() 
        self.screen_height = self.window.winfo_screenheight() 
        self.window.geometry(f"{self.screen_width}x{self.screen_height}")
        self.window.configure(bg="#171821")
        self.window.resizable(True, True)

         # Calculate scaling factors
        self.WR = 1366 / self.screen_width
        self.HR = 768 / self.screen_height

        self.last_update_time = time.time()
        self.current_page = None

        # Initialize canvas
        self.canvas = Canvas(
            self.window,
            bg="#171821",
            height=self.screen_height,
            width=self.screen_width,
            bd=0,
            highlightthickness=0,
            relief="ridge",
        )
        self.canvas.place(x=0, y=0)

         # Image Manager instance
        self.element_manager = ElementManager(self.window,self.canvas, self.screen_width, self.screen_height)

        self.elements = []

        # Start with the first page
        self.show_page("file_uploader")

    def show_page(self, page_class, *args):
        """Switches to a new page"""
        if self.current_page:
            self.current_page.clear_screen()

        screens = {
            "file_uploader": FileUploader,
            "process_selection_page": process_selection_page,
            "data_preprocessing_pipeline": data_preprocessing_pipeline,
            "ai_models_pipeline": ai_models_pipeline,
            "regression_classification_pipeline": regression_classification_pipeline,
            "image_processing_pipeline": image_processing_pipeline
        }

        if page_class in screens:

            self.current_page = screens[page_class](self, *args)
            self.current_page.display()
        else:
            print(f"Error: Unknown screen '{page_class}'")

    def clear_page_widgets(self):
        """Destroy all widgets tracked for the current page."""
        for widget in self.page_widgets:
            widget.destroy()
        self.page_widgets.clear()


