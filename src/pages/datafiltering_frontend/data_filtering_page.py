from src.utils.ui_element_manager import UIElementManager
from src.utils.ui_style_manager import StyleManager
from src.utils.info_txt import INFO_TEXT_DF
from src.pages.datafiltering_frontend.button_manager import ButtonManager
from src.pages.datafiltering_frontend.data_manager import DataManager
from src.pages.datafiltering_frontend.request_manager import RequestManager
from src.pages.datafiltering_frontend.data_visualization import DataVisualization
from src.pages.datafiltering_frontend.preview_manager import PreviewManager
import customtkinter as ctk
from tkinter import Button, PhotoImage,messagebox
from src.assets_management import assets_manage, load_image
import pandas as pd
import threading


class DataFilteringPage(ctk.CTkFrame):
    def __init__(self, parent,file_path=None,file_name=None,data=None,**page_state):
        super().__init__(parent, corner_radius=0)

        self.font_normal = StyleManager.get_font("normal")
        self.font_label = StyleManager.get_font("label")
        self.color_secondary = StyleManager.get_color("secondary")
        self.color_accent = StyleManager.get_color("accent")
        self.color_transparent = StyleManager.get_color("transparent")
        self.color_info = StyleManager.get_color("info")
        self.parent = parent

        self.Info_button_image = load_image("info_B.png", size=(16, 16))  
        self.ui = UIElementManager(
        info_icon_light=parent.info_icon_light,
        info_icon_dark=parent.info_icon_dark,
        parent_widget=self
        )

        self.managers = {}  

        self.managers["button"] = ButtonManager(self)
        self.managers["data"] = DataManager(self, self.managers)
        self.managers["visualization"] = DataVisualization(self)
        self.managers["preview"] = PreviewManager(self)
        self.managers["request"] = RequestManager(self, self.managers)  # Now it's safe

        

        self.file_name = file_name or "No file Uploaded"
        self.file_path=file_path
        self.current_segment_index = 0
        window_height = self.winfo_screenheight()  # Get the total screen height
        right_frame_height = int(0.8 * window_height)

        self.segment_completion = {
                                    "Select Filter Process": False,
                                    "Outlier Detection": False,
                                    "Interpolation": False,
                                    "Smoothing": False,
                                    "Scaling & Encoding": False
                                  }
        self.visible_segments = ["Select Filter Process"]

        if self.file_path:
            try:
                self.data = pd.read_csv(self.file_path)  # Load CSV data
                self.column_names = list(self.data.columns)[1:]  # Exclude first column (Date)
                self.column_name = self.column_names[0] if self.column_names else None

               

            except Exception as e:
                self.data = pd.DataFrame() 
        else:
            self.data = pd.DataFrame()  #  If no file, use empty DataFrame
            self.column_names = []
            self.column_name = None


        # Configure grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=8)  
        self.grid_columnconfigure(1, weight=2)  
               
         # Left Side Frame
        self.left_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.left_frame.grid(row=0, column=0, sticky="nsew", padx=50, pady=10)
        self.left_frame.grid_columnconfigure(0, weight=2)

        # First Frame (Text Box with Cancel Button)
        self.label_frame = ctk.CTkFrame(self.left_frame, fg_color=StyleManager.COLORS.get("Default Mode"), corner_radius=10,height=50)
        self.label_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.left_frame.grid_rowconfigure(0, weight=0)
        self.label = ctk.CTkLabel(self.label_frame, text=self.file_name, font=("Inter", 16, "bold"))
        self.label.place(relx=0.5, rely=0.5, anchor="center")
        self.preview_label = ctk.CTkLabel(self.label_frame, text="Preview", font=("Inter", 12, "bold"),
                                  text_color="red", cursor="hand2")
        self.preview_label.place(relx=0.9, rely=0.5, anchor="center")  # Adjusted position
        self.preview_label.bind("<Button-1>", lambda event:  self.managers["preview"].preview_csv_popup())
        self.cancel_button = ctk.CTkButton(self.left_frame, text="X", width=30, height=25, command=lambda:self.cancel_file())
        self.cancel_button.grid(row=0, column=1, padx=10, pady=10)

        # Second Frame (Dropdown & Graph Display)
        self.graph_frame = ctk.CTkScrollableFrame(self.left_frame, fg_color=StyleManager.COLORS.get("Default Mode"), width = 500, corner_radius=10, height=1050)  # Increased Height
        self.graph_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.left_frame.grid_rowconfigure(1, weight=1)  # Keep left frame standard but allow graph frame to take space

        # Configure Graph Frame Grid
        self.graph_frame.grid_rowconfigure(0, weight=1)  # Center the dropdown
        self.graph_frame.grid_rowconfigure(1, weight=4)  # Allow graph display to expands
        self.graph_frame.grid_columnconfigure(0, weight=1)

        # Graph Display Area
        self.graph_display = ctk.CTkFrame(self.graph_frame, fg_color=StyleManager.COLORS.get("Default Mode"), height=1000, corner_radius=10)  # Increased Size
        self.graph_display.grid(row=1, column=0, padx=0, pady=10, sticky="nsew")  # Expands to fill space


        self.Info_button_image = PhotoImage(file=assets_manage("info_B.png"))

        # Right Side Frame (Segmented Buttons)
        self.right_frame = ctk.CTkScrollableFrame(self, fg_color=StyleManager.COLORS.get("Default Mode"), width=300 , height= right_frame_height)
        self.right_frame.grid(row=0, column=1, sticky="en", padx=10, pady=10)
        self.right_frame.grid_columnconfigure(0, weight=1)
      

        # Segmented Button Frame
        self.segmented_frame = ctk.CTkSegmentedButton(self.right_frame, values=self.visible_segments,
                                                      command=self.change_segment)
        self.segmented_frame.grid(row=0, column=0, padx=10, pady=10)
        self.segmented_frame.set("Outlier Detection")

        # Frame that holds all segment contents
        self.segment_container = ctk.CTkFrame(self.right_frame, fg_color=StyleManager.COLORS.get("Default Mode"))
        self.segment_container.grid(row=1, column=0, sticky="s", padx=10, pady=10)

        # Define ordered segment list
        self.segment_order = ["Select Filter Process","Outlier Detection", "Interpolation", "Smoothing"]
        self.scaling_segment = "Scaling & Encoding"

        # Create segment frames
        self.segments = {
            "Select Filter Process": self.create_process_selection_frame(),
            "Outlier Detection": self.create_segment_frame(),
            "Interpolation": self.create_interpolation_frame(),
            "Smoothing": self.create_smoothing_frame(),
            
        }

        # Submit Button
        self.submit_button = ctk.CTkButton(self.right_frame, text="Submit", command=self.submit_action)
        self.submit_button.grid(row=2, column=0, pady=10)

        #self.add_export_send_buttons()
        self.current_segment = None
        self.change_segment("Select Filter Process")

        if self.file_path:  
            self.managers["data"].load_csv_columns(self.file_path)
            self.managers["preview"].preview_csv_in_graph_frame()
        
        #Initial Boxplot for first column
    

    def create_process_selection_frame(self):
        frame = ctk.CTkFrame(self.segment_container, fg_color=self.color_secondary, corner_radius=10)
        frame.grid_columnconfigure(0, weight=1)

        radio_frame = ctk.CTkFrame(frame, fg_color=self.color_accent, corner_radius=10)
        radio_frame.grid(row=1, column=0, padx=10, pady=15, sticky="new")

        self.process_radio_var = ctk.StringVar(value="Filtering Method")
        self.ui.create_radio_buttons(
            parent=radio_frame,
            label_text="",
            variable=self.process_radio_var,
            options=["Filtering Method", "Scaling & Encoding"],
            grid_positions=[(0, 0), (1, 0)]
        )

        return frame

    def create_segment_frame(self):
        frame = ctk.CTkFrame(self.segment_container, fg_color=self.color_secondary, corner_radius=10)
        frame.grid_columnconfigure(0, weight=1)

        radio_frame = ctk.CTkFrame(frame, fg_color=self.color_accent, corner_radius=10)
        radio_frame.grid(row=1, column=0, padx=10, pady=15, sticky="nsew")

        self.radio_var = ctk.StringVar(value="Isolation Forest")
        self.ui.create_radio_buttons(
            parent=radio_frame,
            label_text="Select Method",
            variable=self.radio_var,
            options=["Isolation Forest", "IQR"],
            grid_positions=[(1, 0), (1, 1)],
            info_text= INFO_TEXT_DF ["segment_frame"]["Select Method"],
 			command=lambda: self.toggle_slider(frame,True)
        )

        slider_frame = ctk.CTkFrame(frame, fg_color=self.color_accent, corner_radius=10)
        slider_frame.grid(row=2, column=0, padx=10, pady=15, sticky="nsew")

        self.ui.create_slider_with_label(
            parent=slider_frame,
            label_text="Contamination Value",
            min_val=0.00,
            max_val=0.50,
            default_val=0.2,
            steps=20,
            row_offset=0,
            info_text= INFO_TEXT_DF ["segment_frame"]["Contamination Value"]
        )

        self.scroll_frame = ctk.CTkScrollableFrame(frame, fg_color=self.color_accent, label_text="Columns", corner_radius=10)
        self.scroll_frame.grid(row=0, column=0, padx=10, pady=15, sticky="nsew")

        scroll_label = ctk.CTkLabel(self.scroll_frame, text="Choose Columns", font=self.font_label, fg_color=self.color_info)
        scroll_label.grid(row=0, column=0, sticky="new")
        self.ui.create_info_button(self.scroll_frame, INFO_TEXT_DF ["segment_frame"][ "Choose Columns"] , row=0, column=1)

        frame.slider_frame = slider_frame

        return frame

    def create_interpolation_frame(self):
        frame = ctk.CTkFrame(self.segment_container, fg_color=self.color_secondary, corner_radius=10)
        frame.grid_columnconfigure(0, weight=1)

        radio_frame = ctk.CTkFrame(frame, fg_color=self.color_accent, corner_radius=10)
        radio_frame.grid(row=0, column=1, padx=10, pady=15, sticky="ew")

        self.interpolation_radio_var = ctk.StringVar(value="Spline")
        self.ui.create_radio_buttons(
            parent=radio_frame,
            label_text="Select Method",
            variable=self.interpolation_radio_var,
            options=["Spline"],
            grid_positions=[(1, 0)],
            info_text= INFO_TEXT_DF ["interpolation_frame"]["Select Method"]
        )

        return frame


    def create_smoothing_frame(self):
        frame = ctk.CTkFrame(self.segment_container, fg_color=self.color_secondary, corner_radius=10)
        frame.grid_columnconfigure(0, weight=1)

        radio_frame = ctk.CTkFrame(frame, fg_color=self.color_accent, corner_radius=10)
        radio_frame.grid(row=0, column=0, padx=10, pady=15, sticky="ew")
        radio_frame.grid_columnconfigure(0, weight=1)

        self.smoothing_radio_var = ctk.StringVar(value="SMA")
        self.ui.create_radio_buttons(
            parent=radio_frame,
            label_text="Select Method",
            variable=self.smoothing_radio_var,
            options=["SMA", "TES"],
            grid_positions=[(1, 0), (1, 1)],
            info_text= INFO_TEXT_DF ["smoothing_frame"]["Select Method"],
            command=lambda: self.toggle_smoothing_options(frame, self.smoothing_radio_var.get())
    
        )

        # SMA Slider Frame
        sma_slider_frame = ctk.CTkFrame(frame, fg_color=self.color_accent, corner_radius=10)
        sma_slider_frame.grid(row=1, column=0, padx=10, pady=15, sticky="ew")

        self.sma_slider = self.ui.create_slider_with_label(
            parent=sma_slider_frame,
            label_text="Window Size",
            min_val=5,
            max_val=100,
            default_val=5,
            steps=95,
            row_offset=0,
            info_text= INFO_TEXT_DF ["smoothing_frame"]["Window Size"]
        )
        #self.ui.create_info_button(sma_slider_frame,  INFO_TEXT_DF ["smoothing_frame"]["Select Method"], row=0, column=1)

        # TES Frame (hidden initially)
        self.tes_params = {}
        tes_frame = ctk.CTkFrame(frame, fg_color=self.color_accent)
        tes_frame.grid(row=1, column=0, padx=10, pady=0, sticky="ew")
        tes_frame.grid_remove()

        def add_tes_parameter(parent, label_text, widget_type="slider", from_=0, to=1, row_index=0):
            param_frame = ctk.CTkFrame(parent, fg_color=self.color_secondary, corner_radius=10)
            param_frame.grid(row=row_index, column=0, padx=10, pady=10, sticky="nesw")

            label = ctk.CTkLabel(param_frame, text=label_text, font=self.font_label, fg_color=self.color_info)
            label.grid(row=0, column=0, sticky="nesw")
            self.ui.create_info_button(param_frame, INFO_TEXT_DF ["smoothing_frame"][label_text] , row=0, column=1)

            if widget_type == "slider":
                value_label = ctk.CTkLabel(param_frame, text="0.00", font=self.font_normal)
                value_label.grid(row=1, column=0, padx=10, sticky="ew")

                slider = ctk.CTkSlider(param_frame, from_=from_, to=to,
                                       command=lambda val: value_label.configure(text=f"{float(val):.2f}"))
                slider.grid(row=2, column=0, padx=10, sticky="ew")
                self.tes_params[label_text] = slider

            else:
                entry = ctk.CTkEntry(param_frame)
                entry.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
                self.tes_params[label_text] = entry

        add_tes_parameter(tes_frame, "Seasonal Periods", "slider", 1, 12, 0)
        add_tes_parameter(tes_frame, "Trend", "entry", row_index=1)
        add_tes_parameter(tes_frame, "Seasonal", "entry", row_index=2)
        add_tes_parameter(tes_frame, "Smoothing Level", "slider", 0, 1, 3)
        add_tes_parameter(tes_frame, "Smoothing Trend", "slider", 0, 1, 4)
        add_tes_parameter(tes_frame, "Smoothing Seasonal", "slider", 0, 1, 5)

        frame.sma_slider_frame = sma_slider_frame
        frame.tes_frame = tes_frame

        return frame

    def create_scaling_encoding_frame(self):
        frame = ctk.CTkFrame(self.segment_container, fg_color=self.color_secondary, corner_radius=10)
        frame.grid_columnconfigure(0, weight=1)

        # Test Size Slider
        test_size_frame = ctk.CTkFrame(frame, fg_color=self.color_accent, corner_radius=10)
        test_size_frame.grid(row=0, column=0, padx=10, pady=15, sticky="nsew")

        self.ui.create_slider_with_label(
            parent=test_size_frame,
            label_text="Test Size",
            min_val=0.0,
            max_val=1.0,
            default_val=0.2,
            steps=100,
            row_offset=0,
            info_text= INFO_TEXT_DF ["scaling_encoding_frame"]["Test Size"]
        )

        # Random State Slider
        random_state_frame = ctk.CTkFrame(frame, fg_color=self.color_accent, corner_radius=10)
        random_state_frame.grid(row=1, column=0, padx=10, pady=15, sticky="nsew")

        self.ui.create_slider_with_label(
            parent=random_state_frame,
            label_text="Random State",
            min_val=0,
            max_val=100,
            default_val=42,
            steps=100,
            row_offset=0,
            info_text= INFO_TEXT_DF ["scaling_encoding_frame"]["Random State"]
        )
        self.ui.create_info_button(random_state_frame, "Seed value for reproducibility in data splitting.", row=0, column=1)

        self.scaling_scroll_frame = ctk.CTkScrollableFrame(frame, fg_color=self.color_accent, corner_radius=10, label_text="Target Column")
        self.scaling_scroll_frame.grid(row=2, column=0, padx=10, pady=15, sticky="nsew")

        self.scaling_column_checkboxes = {}
        self.scaling_column_var = {}
        self.selected_scaling_column = None

        return frame



    def toggle_smoothing_options(self, frame, method):
        """Toggles between SMA and TES parameters using grid layout."""
        if method == "SMA":
            frame.sma_slider_frame.grid()
            frame.tes_frame.grid_remove()
        else:
            frame.sma_slider_frame.grid_remove()
            frame.tes_frame.configure(height=250)
            frame.tes_frame.grid()



    def toggle_slider(self, frame, show):
        """Shows or hides the slider based on radio button selection."""
        if show:
            frame.slider_frame.grid()
        else:
            frame.slider_frame.grid_remove()


    def change_segment(self, segment_name):
        """Switch between segment frames while controlling access."""
        segment_order = ["Select Filter Process", "Outlier Detection", "Interpolation", "Smoothing"]
        
        # Ensure all previous segments are completed before allowing the switch
        if segment_name in segment_order:
            selected_index = segment_order.index(segment_name)
            for i in range(selected_index):
                if not self.segment_completion[segment_order[i]]:
                    return  # Prevent access if a previous segment is incomplete

        # If allowed, switch segment
        if self.current_segment:
            self.current_segment.grid_forget()

        #  Show correct frame when Scaling & Encoding is selected directly
        if segment_name == "Scaling & Encoding":
            self.current_segment = self.create_scaling_encoding_frame()
            self.segmented_frame.configure(values=["Scaling & Encoding"])
            
            if hasattr(self, "scaling_scroll_frame") and hasattr(self, "data"):
                self.managers["data"].load_scaling_columns(self.data.columns)  # Send column names  # Only show this tab
        else:
            self.current_segment = self.segments[segment_name]
            self.segmented_frame.configure(values=self.visible_segments)  # Maintain available tabs

        self.current_segment.grid(row=1, column=0, sticky="nsew")
        self.segmented_frame.set(segment_name)

    
    def submit_action(self):
        """Handles segment transitions and submission logic."""
        current_segment = self.segmented_frame.get()  # Get the active segment

        # If already completed, move to the next segment instead of re-submitting
        if self.segment_completion[current_segment]:
            self.move_to_next_segment()
            return
        
         #  Check for column selection if in "Outlier Detection"
        if current_segment == "Outlier Detection":
            selected_columns = [
                child.cget("text") for child in self.scroll_frame.winfo_children()
                if isinstance(child, ctk.CTkCheckBox) and child.get()
            ]
            if not selected_columns:
                messagebox.showerror("Error", "You must select at least one column before proceeding!")
                return  #  Stop further execution

        self.segment_completion[current_segment] = True  # Mark as completed

        # Lock the completed segment
        if current_segment in self.segments:
            self.lock_segment(self.segments[current_segment])

      

        # Print parameter values based on segment
        if current_segment == "Outlier Detection":
            self.managers["request"].run_outlier_detection()

        elif current_segment == "Interpolation":
            self.managers["request"].run_interpolation()

        elif current_segment == "Smoothing":
            self.managers["request"].run_smoothing()

            #  Print TES Parameters if TES is selected
            if self.smoothing_radio_var.get() == "TES":
                for key, widget in self.tes_params.items():
                    if isinstance(widget, ctk.CTkSlider):
                        print(f"{key}: {widget.get()}")
                    elif isinstance(widget, ctk.CTkEntry):
                        print(f"{key}: {widget.get()}")

        elif current_segment == "Scaling & Encoding":

            if hasattr(self, "scaling_scroll_frame") and hasattr(self, "data"):
                self.managers["data"].load_scaling_columns(self.data.columns[1:])  # Ensure columns are loaded
                self.managers["request"].run_scaling_and_encoding()

        #  Remove Filtering Segments After Smoothing Completion
        if current_segment == "Smoothing":
            self.visible_segments = ["Scaling & Encoding"]


           #  Update button visibility
        self.managers["button"].update_buttons_visibility()

        # Enable the next segment in the segmented frame
        self.move_to_next_segment()


    def move_to_next_segment(self):
        """Move to the next available segment after submission."""
        segment_order = ["Select Filter Process", "Outlier Detection", "Interpolation", "Smoothing"]
        current_segment = self.segmented_frame.get()
        
        # Check the index of the current segment
        if current_segment == "Select Filter Process":
            selected_process = self.process_radio_var.get()
            if selected_process == "Filtering Method":
                self.visible_segments = ["Outlier Detection"]
            else:
                self.visible_segments = ["Scaling & Encoding"]
                self.change_segment("Scaling & Encoding")
                return  # Prevent unnecessary switching

        elif current_segment == "Outlier Detection":
            self.visible_segments.append("Interpolation")

        elif current_segment == "Interpolation":
            self.visible_segments.append("Smoothing")

        elif current_segment == "Smoothing":
            #  Remove previous tabs & show only Scaling & Encoding
            self.visible_segments = ["Scaling & Encoding"]

        elif current_segment == "Scaling & Encoding":
            #  Hide submit button once Scaling & Encoding is completed
            self.submit_button.configure(state="disabled")
            return

        self.segmented_frame.configure(values=self.visible_segments)
        self.change_segment(self.visible_segments[-1])

    def lock_segment(self, frame):
        """Disable all widgets in the given segment."""
        for child in frame.winfo_children():
            if isinstance(child, (ctk.CTkRadioButton, ctk.CTkSlider, ctk.CTkEntry, ctk.CTkCheckBox, ctk.CTkComboBox)):
                child.configure(state="disabled")

    

    def update_boxplot(self, column_name):
        """Triggered when a new column is selected in the dropdown."""
        
        self.column_name = column_name

        # Show loading text
        self.show_loading_message()

        # Generate plot asynchronously to prevent UI freezing
        threading.Thread(target=lambda: self.self.managers["visualization"].plot_boxplot(column_name), daemon=True).start()

    def show_loading_message(self):
        """Displays a loading message in the graph display area."""
        for widget in self.graph_display.winfo_children():
            widget.destroy()

        loading_label = ctk.CTkLabel(self.graph_display, text="Loading...", font=("Inter", 14, "bold"))
        loading_label.place(relx=0.5, rely=0.5, anchor="center")
        
    

    def update_comparison_view(self):
        
        """Updates the comparison popup based on user selections."""
        compare_type = self.compare_type.get()
        left_data = self.left_selection.get()
        right_data = self.right_selection.get()
        column_name = self.column_selection.get()

        if compare_type == "Graph":
            self.managers["visualization"].plot_comparison_graph(left_data, right_data, column_name)
        else:
            self.managers["visualization"].show_comparison_data(left_data, right_data, column_name)

    def get_data_by_name(self, name):
        """Returns the corresponding DataFrame for the given name."""
        if name == "Raw Data":
            return self.data
        elif name == "Outlier Cleaned Data":
            return self.cleaned_data
        elif name == "Interpolated Data":
            return self.interpolated_data
        elif name == "Smoothed Data":
            return self.smoothed_data
        return None
    
    def cancel_file(self):
        """Handles file cancellation and resets only this page."""
        
        page_name = self.__class__.__name__  # Get the page's class name

        self.parent.file_paths[page_name] = None  #  Reset file path for this page
        self.parent.file_names[page_name] = None  #  Reset file name for this page
        self.parent.page_data[page_name] = None   #  Reset data for this page

        #  Remove the sidebar button for this page only
        self.parent.update_sidebar_buttons(page_name, action="remove")

        #  Reset this page instance so it opens fresh on next upload
        if hasattr(self.parent, f"{page_name}_instance"):
            delattr(self.parent, f"{page_name}_instance")

        #  Go back to file upload page
        self.parent.show_page("file_upload")