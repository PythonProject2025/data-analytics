
from views.base_page import BaseScreen
from utils.ui_element_manager import ElementManager
from utils.file_utils import open_file_dialog
 

class FileUploader(BaseScreen):
    def display(self):
        self.clear_screen()  # Clears previous UI
        self.add_common_ui_elements()
        self.slidebar()

        # Load Upload Text & Button
        self.page_widgets.append(self.app.element_manager.create_image("fileuploader_assets", "Rectangle.png", 0.550, 0.510))
        self.page_widgets.append(self.app.element_manager.create_image("fileuploader_assets", "Dot_Rectangle.png", 0.546, 0.504))
        self.page_widgets.append(self.app.element_manager.create_text("Upload Files Here (.csv or .zip)", 0.438, 0.563,0.011, color="#FFFFFF"))
        
        upload_button = self.app.element_manager.create_button_with_hover(
            "fileuploader_assets",  # Folder where images are stored
            "upload_button.png",  # Default image
            "upload_button_hover.png",  # Hover image
            0.493, 0.419, 0.089, 0.129,  # x, y, width, height (relative)
            command= self.handle_file_upload
        )
        self.page_widgets.append(upload_button)

    def handle_file_upload(self):
        """Handles file selection and navigates based on file type."""
        file_path = open_file_dialog()
        if file_path:
            # Logic to navigate based on file type
            if file_path.endswith(".csv"):
                self.app.show_page("process_selection_page")  # Navigate to process selection
            elif file_path.endswith((".png", ".jpg", ".jpeg")):
                self.app.show_page("image_processing_pipeline")  # Navigate to image processing

