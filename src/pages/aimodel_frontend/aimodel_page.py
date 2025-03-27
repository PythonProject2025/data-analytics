import customtkinter as ctk
from tkinter import messagebox, PhotoImage
from tkinter import ttk
import tkinter as tk
from src.utils.ui_element_manager import UIElementManager
from src.utils.ui_style_manager import StyleManager
from src.pages.aimodel_frontend.ui_manager import AIUIManager
from src.pages.aimodel_frontend.request_manager import AIRequestManager
from src.assets_management import assets_manage, load_image
from src.pages.aimodel_frontend.ai_visualization import AIVisualization

class AIModelPage(ctk.CTkFrame):
    def __init__(self, parent, file_path=None, file_name=None, data=None, **page_state):
        super().__init__(parent, corner_radius=0)
        self.parent = parent
        self.file_path = file_path
        self.file_name = file_name
        self.file_data = data
        self.current_segment = None
        self.sliders = {}
        self.comboboxes = {}
        self.submitted = False

        # internal segment mapping
        self.ui_to_internal = {
            "RandomForest": "RandomForest",
            "CatBoost": "CatBoost",
            "XGBoost": "XGBoost",
            "ANN": "ArtificialNeuralNetwork",
            "Problem Selection": "Problem Selection",
        }

        # Styling
        self.Info_button_image = load_image("info_B.png", size=(16, 16)) 
        self.ui = UIElementManager(
        info_icon_light=parent.info_icon_light,
        info_icon_dark=parent.info_icon_dark,
        parent_widget=self
        )
        self.font_normal = StyleManager.get_font("normal")
        self.font_label = StyleManager.get_font("label")
        self.color_secondary = StyleManager.get_color("secondary")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=9)
        self.grid_columnconfigure(1, weight=1)

        self._create_left_frame()
        self._create_right_frame()

        self.managers = {
            "ui": AIUIManager(self, self.ui),
            "request": AIRequestManager(self),
            "Visualization":AIVisualization(self)
        }

        self.managers["ui"].initialize_segment("Problem Selection")
        self.segments = self.managers["ui"].context.segments
        self.change_segment("Problem Selection")

    def _create_left_frame(self):
        self.left_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.left_frame.grid(row=0, column=0, sticky="nsew", padx=50, pady=10)
        self.left_frame.grid_columnconfigure(0, weight=2)
        self.left_frame.grid_rowconfigure(1, weight=1)

        self.label_frame = ctk.CTkFrame(self.left_frame, fg_color=StyleManager.COLORS.get("Default Mode"), corner_radius=10, height=50)
        self.label_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.label = ctk.CTkLabel(self.label_frame, text=self.file_name, font=("Inter", 16, "bold"))
        self.label.place(relx=0.5, rely=0.5, anchor="center")

        self.preview_label = ctk.CTkLabel(self.label_frame, text="Preview", font=("Inter", 12, "bold"),
                                          text_color="red", cursor="hand2")
        self.preview_label.place(relx=0.9, rely=0.5, anchor="center")
        self.preview_label.bind("<Button-1>", lambda event: self.preview_data())

        self.cancel_button = ctk.CTkButton(self.left_frame, text="X", width=30, height=25, command=self.cancel_file)
        self.cancel_button.grid(row=0, column=1, padx=10, pady=10)

        self.graph_frame = ctk.CTkFrame(self.left_frame, fg_color=StyleManager.COLORS.get("Default Mode"), corner_radius=10, height=350)
        self.graph_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.graph_frame.grid_columnconfigure(0, weight=1)
        self.graph_frame.grid_rowconfigure(0, weight=1)

        self.graph_display = ctk.CTkFrame(self.graph_frame, fg_color="#D1D1D1", height=250, corner_radius=10)
        self.graph_display.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    def _create_right_frame(self):
        right_frame_height = int(0.8 * self.winfo_screenheight())
        self.right_frame = ctk.CTkScrollableFrame(self, fg_color=StyleManager.COLORS.get("Default Mode"),
                                                  width=300, height=right_frame_height)
        self.right_frame.grid(row=0, column=1, sticky="en", padx=10, pady=10)
        self.right_frame.grid_columnconfigure(0, weight=1)

        self.segmented_frame = ctk.CTkSegmentedButton(self.right_frame,
                                                      values=["Problem Selection"],
                                                      command=self.change_segment)
        self.segmented_frame.grid(row=0, column=0, padx=10, pady=10)

        self.segment_container = ctk.CTkFrame(self.right_frame, fg_color="transparent")
        self.segment_container.grid(row=1, column=0,  pady=10)

        self.submit_button = ctk.CTkButton(self.right_frame, text="Submit", command=self.submit_action)
        self.submit_button.grid(row=2, column=0, pady=10)

    def change_segment(self, segment_name):
        internal_name = self.ui_to_internal.get(segment_name, segment_name)
        
        if self.current_segment:
            self.current_segment.grid_forget()
        self.current_segment = self.segments[internal_name]
        self.current_segment.grid(row=1, column=0, sticky="nsew")
        self.segmented_frame.set(segment_name)

    def submit_action(self):
        if self.submitted:
            return

        current = self.segmented_frame.get()

        if current == "Problem Selection":
            problem_type = self.managers["ui"].context.problem_var.get()
            if problem_type == "Regression":
                model_segments = ["RandomForest", "CatBoost", "XGBoost"]
            else:
                model_segments = ["RandomForest", "CatBoost", "ANN"]

            for name in model_segments:
                internal_name = self.ui_to_internal[name]
                self.managers["ui"].initialize_segment(internal_name)

            self.segments = self.managers["ui"].context.segments
            self.segmented_frame.configure(values=model_segments)
            self.change_segment(model_segments[0])
            return

        # submission logic from request manager
        self.managers["request"].submit_action()
        self.submit_button.configure(state="disabled")
        self.submitted = True

    def preview_data(self):
        if not hasattr(self, "file_data") or self.file_data is None:
            messagebox.showerror("Error", "No processed data available for preview!")
            return

        preview_window = ctk.CTkToplevel(self)
        preview_window.title("Processed Data Preview")
        preview_window.geometry("900x500")
        preview_window.grab_set()

        frame = tk.Frame(preview_window)
        frame.pack(fill="both", expand=True)

        columns = list(self.file_data.columns)
        tree = ttk.Treeview(frame, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)

        for index, row in self.file_data.head(50).iterrows():
            tree.insert("", "end", values=list(row))

        v_scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        h_scrollbar = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)
        tree.configure(yscroll=v_scrollbar.set, xscroll=h_scrollbar.set)

        tree.pack(side="top", fill="both", expand=True)
        v_scrollbar.pack(side="right", fill="y")
        h_scrollbar.pack(side="bottom", fill="x")

    def cancel_file(self):
        page_name = self.__class__.__name__
        self.parent.file_paths[page_name] = None
        self.parent.file_names[page_name] = None
        self.parent.page_data[page_name] = None
        self.parent.update_sidebar_buttons(page_name, action="remove")

        if hasattr(self.parent, f"{page_name}_instance"):
            delattr(self.parent, f"{page_name}_instance")

        self.parent.show_page("file_upload")