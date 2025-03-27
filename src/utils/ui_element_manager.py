import customtkinter as ctk
from tkinter import Button
from src.utils.ui_style_manager import StyleManager


class UIElementManager:
    def __init__(self, info_button_image, parent_widget):
        self.info_button_image = info_button_image
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
        button = Button(parent, text="", image=self.info_button_image, width=8, height=8,
                        command=lambda: self.show_info_dialog(text))
        button.grid(row=row, column=column, padx=5, sticky="w")

    def show_info_dialog(self, text):
        dialog = ctk.CTkToplevel(self.parent_widget)
        dialog.title("Information")
        dialog.geometry("300x150")
        dialog.grab_set()
        ctk.CTkLabel(dialog, text=text, font=self.font_normal).pack(pady=20)
        ctk.CTkButton(dialog, text="OK", command=dialog.destroy).pack()

    def create_slider_with_label(self, parent, label_text, min_val, max_val, default_val, steps, row_offset=0, info_text=None, model=None):
        label = ctk.CTkLabel(parent, text=label_text, font=self.font_label, fg_color=self.color_info)
        label.grid(row=row_offset, column=0, sticky="new")
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

        self.sliders[label_text] = slider

        return slider

    def create_combobox_with_label(self, parent, label_text, options, default, row_offset=0, info_text=None):
        label = ctk.CTkLabel(parent, text=label_text, font=self.font_label, fg_color=self.color_info)
        label.grid(row=row_offset, column=0, sticky="new")
        self.create_info_button(parent, info_text, row=row_offset, column=1)

        combobox = ctk.CTkComboBox(parent, values=options)
        combobox.set(default)
        combobox.grid(row=row_offset+1, column=0, padx=10, pady=5, sticky="ew")

        self.comboboxes[label_text] = combobox
        return combobox
    
    def create_radio_buttons(self, parent, label_text, variable, options, grid_positions, info_text=None, command=None):
        if label_text:
            label = ctk.CTkLabel(parent, text=label_text, font=self.font_label, fg_color=self.color_info)
            label.grid(row=0, column=0, sticky="nesw")
        if info_text:
            self.create_info_button(parent, info_text, row=0, column=1)

        for i, (option, (row, col)) in enumerate(zip(options, grid_positions)):
            rb = ctk.CTkRadioButton(
                parent, text=option, variable=variable, value=option, command=command
            )
            rb.grid(row=row, column=col, padx=10, pady=10, sticky="w")
