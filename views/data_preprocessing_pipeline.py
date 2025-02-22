from views.base_page import BaseScreen
from utils.ui_states import UIState 
from threading import Timer

class data_preprocessing_pipeline(BaseScreen):


    def __init__(self, app):
        super().__init__(app)
        self.current_state = UIState.DEFAULT  
        self.dynamic_widgets = []

    def display(self):
        self.clear_screen()
        self.add_common_ui_elements()

        # Sidebar & Headers
        self.page_widgets.append(self.app.element_manager.create_image("datapreprocessing_assets", "image_3.png", 0.0256, 0.4948))
        self.page_widgets.append(self.app.element_manager.create_image("datapreprocessing_assets", "DF_Header.png", 0.5162, 0.0443))
        self.page_widgets.append(self.app.element_manager.create_image("process_selector", "image_5.png", 0.5441, 0.1563))
        
        # Home & Help Buttons
        self.page_widgets.append(self.app.element_manager.create_button("data_preprocessing", "Home_Icon.png", 0.0110, 0.1042, 0.0293, 0.0521, command=lambda: self.app.show_screen("file_uploader")))
        self.page_widgets.append(self.app.element_manager.create_button("data_preprocessing", "Help_Icon.png", 0.0110, 0.1823, 0.0293, 0.0521, command=lambda: self.app.show_screen("help_page")))
        
        # File Name Display
        #self.page_widgets.append(self.app.element_manager.create_text(self.file_name, 0.4876, 0.1341, font_size_ratio=0.026, color="#FFFFFF"))
        
        # Back Button with Hover
        self.page_widgets.append(self.app.element_manager.create_button_with_hover(
            "data_preprocessing", "button_2.png", "button_hover_1.png", 0.6647, 0.1315, 0.0220, 0.0482, command=lambda: self.app.show_screen("file_uploader")))
        
        # Selection Box for Filtering Methods
        self.filter_options = ["Outlier Detection", "Interpolation", "Smoothing"]
        self.filter_combobox, self.selected_filter = self.app.element_manager.create_combobox(self.filter_options, 0.5470, 0.3216, self.update_state)
        
    
    def update_state(self, selected_option):
        """Handles state transitions dynamically."""
        self.clear_dynamic_widgets()
        
        if selected_option == "Outlier Detection":
            self.current_state = UIState.OUTLIER_DETECTION
            self.show_outlier_options()
        elif selected_option == "Interpolation":
            self.current_state = UIState.INTERPOLATION
        elif selected_option == "Smoothing":
            self.current_state = UIState.SMOOTHING
    
    def show_outlier_options(self):
        """Updates UI when Outlier Detection is selected."""
        self.outlier_options = ["Isolation Forest", "IQR"]
        self.outlier_combobox, self.selected_outlier = self.app.element_manager.create_combobox(self.outlier_options, 0.6420, 0.3320, self.outlier_selection_changed)
        self.dynamic_widgets.append(self.outlier_combobox)
    
    def outlier_selection_changed(self, selected_outlier):
        """Handles selection inside Outlier Detection."""
        self.clear_dynamic_widgets()
        
        if selected_outlier == "Isolation Forest":
            self.current_state = UIState.ISOLATION_FOREST
            self.show_contamination_slider()
        elif selected_outlier == "IQR":
            self.current_state = UIState.IQR
            self.show_column_selection()
    
    def show_contamination_slider(self):
        """Displays the slider for Isolation Forest selection."""
        self.contamination_slider = self.app.element_manager.create_slider(0.00, 0.50, 0.7393, 0.3452, self.on_slider_movement)
        self.dynamic_widgets.append(self.contamination_slider)
    
    def show_column_selection(self):
        """Displays column selection when IQR is chosen."""
        self.column_combobox, self.selected_column = self.app.element_manager.create_combobox(self.column_names, 0.8641, 0.3320, self.column_selection_changed)
        self.dynamic_widgets.append(self.column_combobox)
    
    def column_selection_changed(self, selected_column):
        if selected_column:
            self.create_submit_button()
    
    def on_slider_movement(self, value):
        self.app.slider_label.configure(text=f"{float(value):.2f}")
        if self.app.update_timer:
            self.app.update_timer.cancel()
        self.app.update_timer = Timer(0.5, self.create_submit_button)
        self.app.update_timer.start()
    
    def create_submit_button(self):
        self.clear_dynamic_widgets()
        self.page_widgets.append(self.app.image_manager.create_button_with_hover(
            "data_preprocessing", "Submit.png", "Submit_Hover.png", 0.5199, 0.4297, 0.0402, 0.0911, command=self.submit_parameters
        ))
    
    def clear_dynamic_widgets(self):
        """Removes dynamically added UI elements."""
        for widget in self.dynamic_widgets:
            widget.destroy()
        self.dynamic_widgets.clear()
    
    def submit_parameters(self):
        filter_method = self.selected_filter.get()
        outlier_method = self.selected_outlier.get() if hasattr(self, 'selected_outlier') else None
        contamination_value = self.contamination_slider.get() if hasattr(self, 'contamination_slider') else None
        column_name = self.selected_column.get() if hasattr(self, 'selected_column') else None
        
        print(f"Filter Method: {filter_method}")
        print(f"Outlier Method: {outlier_method}")
        print(f"Contamination Value: {contamination_value}")
        print(f"Column Name: {column_name}")

