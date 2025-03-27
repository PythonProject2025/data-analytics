# --- image_ui_manager.py ---
import customtkinter as ctk
from tkinter import filedialog
from PIL import Image, ImageTk
from src.utils.info_txt import INFO_TEXT_IM

class ImageUIManager:
    def __init__(self, context, ui):
        self.context = context
        self.ui = ui
        self.segments = {}
        self.current_segment = None

        self.font_label = ui.font_label
        self.font_normal = ui.font_normal
        self.color_info = ui.color_info
        self.color_accent = ui.color_accent
        self.color_secondary = ui.color_secondary
        self.color_transparent = ui.color_transparent

        self.context.segments = {} 
        self.context.current_segment = None

    def initialize_segment(self, segment_name):
        frame = self.create_segment_frame() if segment_name == "Image Processing" else self.create_image_train_frame()
        self.segments[segment_name] = frame
        self.change_segment(segment_name)

    def change_segment(self, segment_name):
        if self.current_segment:
            self.current_segment.grid_forget()
        self.current_segment = self.segments[segment_name]
        self.current_segment.grid(row=1, column=0, sticky="nsew")
        self.context.segmented_frame.set(segment_name)

    def create_segment_frame(self):
        frame = ctk.CTkFrame(self.context.segment_container, fg_color=self.color_secondary, corner_radius=10)
        frame.grid_columnconfigure(0, weight=1)

        # Activation Function
        act_frame = self._frame_with_label(frame, 0, "Activation Function", INFO_TEXT_IM["image_processing_frame"]["Activation Function"])
        self.context.radio_var = ctk.StringVar(value="relu")
        self.ui.create_radio_buttons(
            parent=act_frame,
            label_text="Activation Function",
            variable=self.context.radio_var,
            options=["relu", "sigmoid"],
            grid_positions=[(1, 0), (1, 1)]
        )

        # Epochs
        self.context.epoch_slider = self.ui.create_slider_with_label(
            parent=self._frame_with_label(frame, 1, "Epochs", INFO_TEXT_IM["image_processing_frame"]["Epochs"]),
            label_text="Epochs", min_val=1, max_val=50, default_val=5, steps=49
        )

        # Optimizer
        opt_frame = self._frame_with_label(frame, 2, "Optimizer", INFO_TEXT_IM["image_processing_frame"]["Optimizer"])
        optimizer_label = ctk.CTkLabel(opt_frame, text="Optimizer", font=self.font_label, fg_color=self.color_info)
        optimizer_label.grid(row=0, column=0, sticky="nesw")
        self.ui.create_info_button(opt_frame, INFO_TEXT_IM["image_processing_frame"]["Optimizer"], row=0, column=1)
        self.context.optimizer_combobox = ctk.CTkComboBox(opt_frame, values=["adam", "RMSPROP", "adamax"])
        self.context.optimizer_combobox.set("adam")
        self.context.optimizer_combobox.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        # Test Size
        self.context.test_size_slider = self.ui.create_slider_with_label(
            parent=self._frame_with_label(frame, 3, "Test Size", INFO_TEXT_IM["image_processing_frame"]["Test Size"]),
            label_text="Test Size", min_val=0.0, max_val=1.0, default_val=0.2, steps=100
        )

        # Random State
        self.context.random_state_slider = self.ui.create_slider_with_label(
            parent=self._frame_with_label(frame, 4, "Random State", INFO_TEXT_IM["image_processing_frame"]["Random State"]),
            label_text="Random State", min_val=0, max_val=100, default_val=42, steps=100
            
        )
        
        self.context.upload_button = ctk.CTkButton(
            frame, text="Upload Image", image=self.context.upload_button_image, command=self.upload_image
        )
        self.context.upload_button.grid(row=5, column=0, padx=10, pady=10)

        self.context.image_label = ctk.CTkLabel(frame, text="No file uploaded", font=self.font_normal)
        self.context.image_label.grid(row=6, column=0, padx=10, pady=5)

        self.context.preview_button = ctk.CTkButton(
            frame, text="Preview Image", command=self.preview_image, state="disabled"
        )
        self.context.preview_button.grid(row=7, column=0, padx=10, pady=10)
        
        return frame

    def upload_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            self.context.uploaded_image_path = file_path
            self.context.image_label.configure(text=f"Uploaded: {file_path.split('/')[-1]}")
            self.context.preview_button.configure(state="normal")

    def preview_image(self):
        if self.context.uploaded_image_path:
            preview_window = ctk.CTkToplevel(self.context)
            preview_window.title("Image Preview")
            preview_window.geometry("500x500")
            preview_window.grab_set()

            img = Image.open(self.context.uploaded_image_path)
            img.thumbnail((450, 450))
            img = ImageTk.PhotoImage(img)

            image_label = ctk.CTkLabel(preview_window, image=img, text="")
            image_label.image = img
            image_label.pack(expand=True)

    def _frame_with_label(self, parent, row, label_text, info_text):
        frame = ctk.CTkFrame(parent, fg_color=self.color_accent, corner_radius=10)
        frame.grid(row=row, column=0, padx=10, pady=15, sticky="nsew")
        self.ui.create_info_button(frame, info_text, row=0, column=1)
        return frame
