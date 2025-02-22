from tkinter import PhotoImage, Button
from utils.asset_manager import get_asset_path
from utils.ui_element_manager import ElementManager

class BaseScreen:
    def __init__(self, app):
        self.app = app
        self.canvas = app.canvas
        self.page_widgets = []

    def add_common_ui_elements(self):
        """Adds shared UI components like sidebar and header."""
        
        self.page_widgets.append(self.app.element_manager.create_image("common_assets", "header.png", 0.6, 0.05))
        self.page_widgets.append(self.app.element_manager.create_image("common_assets", "slidebar.png", 0.026, 0.500))

    def slidebar(self):
        
        self.page_widgets.append(self.app.element_manager.create_image("common_assets", "slidebar_2.png", 0.121, 0.5))
        self.page_widgets.append(self.app.element_manager.create_image("common_assets", "dashboard_bright.png", 0.120, 0.113))
        self.page_widgets.append(self.app.element_manager.create_text("Help", 0.113, 0.189,0.008))
        self.page_widgets.append(self.app.element_manager.create_text("Mode", 0.113, 0.260,0.008))
        self.page_widgets.append(self.app.element_manager.create_button("common_assets", "mode_icon.png", 0.088, 0.254, 0.019, 0.030))
    
    def clear_screen(self):
        """Clears only the widgets stored for this page."""
        for widget in self.page_widgets:
            if isinstance(widget, int):  # Canvas item
                self.canvas.delete(widget)
            else:  # Tkinter widget (e.g., buttons)
                widget.destroy()
        self.page_widgets.clear()
    

