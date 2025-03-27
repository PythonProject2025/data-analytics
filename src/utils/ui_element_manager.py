import customtkinter as ctk
from customtkinter import CTkImage
from tkinter import Button
from src.utils.ui_style_manager import StyleManager
from src.assets_management import load_image,assets_manage
from PIL import Image


class UIElementManager:
    def __init__(self, info_icon_light, info_icon_dark, parent_widget):
       
        self.info_icon_dark = Image.open(assets_manage("Info_T.png"))
        self.info_icon_light = Image.open(assets_manage("Info_W.png"))

        self.info_button_image = CTkImage(
        light_image=self.info_icon_dark,
        dark_image=self.info_icon_light,
        size=(16, 16)
            )
        self.parent_widget = parent_widget
        self.font_normal = StyleManager.get_font("normal")
        self.font_label = StyleManager.get_font("label")
        self.color_info = StyleManager.get_color("info")
        self.color_accent = StyleManager.get_color("accent")
        self.color_secondary = StyleManager.get_color("secondary")
        self.color_primary = StyleManager.get_color("primary")
        self.color_transparent = StyleManager.get_color("transparent")
        self.sliders = {}
        self.comboboxes = {}


   

    def create_info_button(self, parent, text, row=0, column=1):
        button = ctk.CTkButton(
            parent,
            text="",  
            image=self.info_button_image,  # CTkImage
            width=24,  
            height=24,
            fg_color="transparent",  # Make button background transparent
            hover_color="#d3d3d3",  #  hovering effect
            command=lambda: self.show_info_dialog(text)
        )
        button.grid(row=row, column=column, padx=5, sticky="e")


    def show_info_dialog(self, text):
        # The popup window
        dialog = ctk.CTkToplevel(self.parent_widget)
        dialog.title("Information")

        # --- dimensions ---
        dialog_width = 350
        dialog_height = 180

        # Centering the dialog on the screen
        screen_width = dialog.winfo_screenwidth()
        screen_height = dialog.winfo_screenheight()
        x = int((screen_width / 2) - (dialog_width / 2))
        y = int((screen_height / 2) - (dialog_height / 2))
        dialog.geometry(f"{dialog_width}x{dialog_height}+{x}+{y}")

        dialog.grab_set()

        # Wrapped Label
        ctk.CTkLabel(
            dialog,
            text=text,
            font=self.font_normal,
            wraplength=300,
            justify="center"
        ).pack(padx=20, pady=(20, 10), expand=True)


        ctk.CTkButton(
            dialog,
            text="OK",
            command=dialog.destroy
        ).pack(pady=(0, 20))



    def create_slider_with_label(self, parent, label_text, min_val, max_val, default_val, steps, row_offset=0, info_text=None, model=None):
        label = ctk.CTkLabel(parent, text=label_text, font=self.font_label, fg_color=self.color_info)
        label.grid(row=row_offset, column=0, padx=10, sticky="w")
        self.create_info_button(parent, info_text, row=row_offset, column=1)

        value_label = ctk.CTkLabel(parent, text=f"Value: {default_val:.2f}", font=self.font_normal)
        value_label.grid(row=row_offset+1, column=0, pady=5)

        def update_value(value):
            try:
                val = float(value)
                value_label.configure(text=f"Value: {int(val)}" if val.is_integer() else f"Value: {val:.2f}")
            except:
                value_label.configure(text="Value: ?")

        slider = ctk.CTkSlider(parent, from_=min_val, to=max_val, number_of_steps=steps, command=update_value)
        slider.set(default_val)
        slider.grid(row=row_offset+2, column=0, padx=10, sticky="ew")

        update_value(float(default_val))

        if model:
            if model not in self.sliders:
                self.sliders[model] = {}
            self.sliders[model][label_text] = slider
        else:
            self.sliders[label_text] = slider

        return slider

    def create_combobox_with_label(self, parent, label_text, options, default, row_offset=0, info_text=None):
        label = ctk.CTkLabel(parent, text=label_text, font=self.font_label, fg_color=self.color_info)
        label.grid(row=row_offset, column=0, padx=10,sticky="w")
        self.create_info_button(parent, info_text, row=row_offset, column=1)

        combobox = ctk.CTkComboBox(parent, values=options)
        combobox.set(default)
        combobox.grid(row=row_offset+1, column=0, padx=10, pady=5, sticky="ew")

        self.comboboxes[label_text] = combobox
        return combobox
    
    def create_radio_buttons(self, parent, label_text, variable, options, grid_positions, info_text=None, command=None):
        if label_text:
            label = ctk.CTkLabel(parent, text=label_text, font=self.font_label, fg_color=self.color_info)
            label.grid(row=0, column=0, padx=10, sticky="w")
        if info_text:
            self.create_info_button(parent, info_text, row=0, column=1)

        for i, (option, (row, col)) in enumerate(zip(options, grid_positions)):
            rb = ctk.CTkRadioButton(
                parent, text=option, variable=variable, value=option, command=command
            )
            rb.grid(row=row, column=col, padx=10, pady=10, sticky="w")
