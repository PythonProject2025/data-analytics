from views.base_page import BaseScreen

class process_selection_page (BaseScreen):
    
    def display(self):
        self.clear_screen()  # Clears previous UI
        self.add_common_ui_elements()
        self.slidebar()

        self.page_widgets.append(self.app.element_manager.create_image("process_selection_assets", "dashboard.png", 0.120, 0.113))
        self.page_widgets.append(self.app.element_manager.create_image("process_selection_assets", "file_name_display.png", 0.5659, 0.1563))
        #self.page_widgets.append(self.app.image_manager.create_text(self.file_name, 0.5095, 0.1341,0.026, color="#FFFFFF"))

        self.page_widgets.append(self.app.element_manager.create_button_with_hover(
            "process_selection_assets", "close.png", "close_hover.png",
            0.6867, 0.1315, 0.0220, 0.0482,
            command=lambda: self.app.show_page("file_uploader")
        ))
        self.page_widgets.append(self.app.element_manager.create_image("process_selection_assets", "down_arrow.png", 0.5549, 0.2474))
        
        self.page_widgets.append(self.app.element_manager.create_button("process_selection_assets", "datafiltering_option.png", 0.2834, 0.2734, 0.6378, 0.1732 , command=lambda: self.app.show_page("data_preprocessing_pipeline")))

        self.page_widgets.append(self.app.element_manager.create_button("process_selection_assets", "info_button.png", 0.7905, 0.3320, 0.0366, 0.0651 ))

        self.page_widgets.append(self.app.element_manager.create_image("process_selection_assets", "down_arrow.png", 0.5549, 0.4896))

        self.page_widgets.append(self.app.element_manager.create_button("process_selection_assets", "regression_classification_option.png", 0.2834, 0.5208, 0.6859, 0.1615 , command=lambda: self.app.show_page("data_preprocessing_pipeline")))

        self.page_widgets.append(self.app.element_manager.create_button("process_selection_assets", "info_button.png", 0.7905, 0.5703, 0.0366, 0.0651 ))
        
        self.page_widgets.append(self.app.element_manager.create_image("process_selection_assets", "down_arrow.png", 0.5549, 0.7292))

        self.page_widgets.append(self.app.element_manager.create_button("process_selection_assets", "ai_model_option.png", 0.2834, 0.7643, 0.6632, 0.1602 , command=lambda: self.app.show_page("data_preprocessing_pipeline")))

        self.page_widgets.append(self.app.element_manager.create_button("process_selection_assets", "info_button.png", 0.7905, 0.8138, 0.0366, 0.0651 ))
        

     

        