from tkinter import PhotoImage,Button
from utils.asset_manager import get_asset_path
import customtkinter

class ElementManager:
    def __init__(self, window , canvas, screen_width, screen_height):
        self.window =window
        self.canvas = canvas
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.images = {}  # Dictionary to store image references

        self.WR = 1366 / self.screen_width
        self.HR = 768 /self.screen_height
       

    def create_image(self, page_name: str, image_name: str, x: float, y: float):
        """
        Creates an image on the canvas.

        Parameters:
        - page_name (str): Folder where the image is stored.
        - image_name (str): Filename of the image.
        - x (float): Multiplier for screen width positioning.
        - y (float): Multiplier for screen height positioning.
        """
        try:
            # Calculate screen scaling ratios
           
            if image_name not in self.images:
            # Load image dynamically
                image_path = get_asset_path(page_name, image_name)
                self.images[image_name] = PhotoImage(file=image_path)

                # Create image on the canvas
            img_item = self.canvas.create_image(self.screen_width * x * self.WR, self.screen_height * y * self.HR, image=self.images[image_name])
            return img_item

        except Exception as e:
            print(f"Error loading image {image_name}: {e}")
            return None
        
    def create_text(self, text: str, x: float, y: float, font_size_ratio: float, color: str = "#87888C"):
        """Creates a text element on the canvas."""
        font_size = int(self.screen_width * font_size_ratio)

        text_item = self.canvas.create_text(
            self.screen_width * x * self.WR, self.screen_height * y * self.HR,
            anchor="nw", text=text, fill=color, font=("Inter Medium", font_size)
        )
        
        return text_item

    def create_button(self, page_name: str, image_name: str, x: float, y: float, width: float, height: float, command=None):
        """Creates a button with an image."""
        try:
            image_path = get_asset_path(page_name, image_name)
            button_image = PhotoImage(file=image_path)

            self.images[image_name] = button_image

            button = Button(
                self.canvas,
                image=button_image,
                borderwidth=0,
                highlightthickness=0,
                command=command if command else lambda: print(f"Button {image_name} clicked"),
                relief="flat",
            )
            button.place(
                x=self.screen_width * x * self.WR, y=self.screen_height * y * self.HR,
                width=self.screen_width * width * self.WR, height=self.screen_height * height * self.HR
            )
             
            button.image = button_image 
            return button
    
        except Exception as e:
            print(f"Error loading button image {image_name}: {e}")
            return None

    def create_button_with_hover(self, page_name: str, default_image_name: str, hover_image_name: str, x: float, y: float, width: float, height: float, command=None):
        """Creates a button with hover effects and stores it for cleanup."""
        try:
            # Load images dynamically
            default_image_path = get_asset_path(page_name, default_image_name)
            hover_image_path = get_asset_path(page_name, hover_image_name)

            default_image = PhotoImage(file=default_image_path)
            hover_image = PhotoImage(file=hover_image_path)

            # Store images to prevent garbage collection
            self.images[default_image_name] = default_image
            self.images[hover_image_name] = hover_image

            # Create button
            button_with_hover = Button(
                self.canvas,
                image=default_image,
                borderwidth=0,
                highlightthickness=0,
                command=command if command else lambda: print(f"Button {default_image_name} clicked"),
                relief="flat",
            )
            button_with_hover.place(
                x=self.screen_width * x * self.WR, y=self.screen_height * y * self.HR,
                width=self.screen_width * width * self.WR, height=self.screen_height * height * self.HR
            )

            # Hover effect functions
            def on_hover(e):
                button_with_hover.config(image=hover_image)

            def on_leave(e):
                button_with_hover.config(image=default_image)

            button_with_hover.bind("<Enter>", on_hover)
            button_with_hover.bind("<Leave>", on_leave)

            button_with_hover.image = (default_image, hover_image)  # Store images to avoid garbage collection

            # Store button in page widgets for cleanup
            return button_with_hover

        except Exception as e:
            print(f"Error creating hover button {default_image_name}: {e}")
            return None
        

    def create_combobox(self, options, x, y, command):
        """
        Creates a combobox with given options and command.

        Parameters:
        - options (list): List of dropdown values.
        - x (float): Relative x-position for placement.
        - y (float): Relative y-position for placement.
        - command (function): Callback function for selection changes.
        """
        selected_value = customtkinter.StringVar(value=" ")  # Default value
        combobox = customtkinter.CTkComboBox(
            master=self.window,
            fg_color="#343743",
            text_color="#FFFFFF",
            dropdown_hover_color="#D9D9D9",
            values=options,
            command=command,
            variable=selected_value,
        )
        combobox.place(x=self.screen_width * x * self.WR, y=self.screen_width * y * self.HR)
       

        return combobox, selected_value

    def create_slider(self, from_value, to_value, x, y, command, label_x, label_y):
        """
        Creates a horizontal slider with a linked label.

        Parameters:
        - from_value (float): Minimum slider value.
        - to_value (float): Maximum slider value.
        - x (float): Relative x-position for placement.
        - y (float): Relative y-position for placement.
        - command (function): Function to call when slider value changes.
        - label_x (float): Relative x-position for slider label.
        - label_y (float): Relative y-position for slider label.
        """
        slider = customtkinter.CTkSlider(
            master=self.window,
            from_=from_value,
            to=to_value,
            command=command,
            orientation="horizontal",
            number_of_steps=20,
            width=200,
            height=25,
            fg_color=None,
            bg_color="#343743",
            progress_color="#FFFFFF",
            button_color="White",
            button_hover_color="orange",
            state="normal",
            hover=False,
        )
        slider.place(x=self.screen_width * x * self.WR, y=self.screen_width * y * self.HR)
        

        slider_label = customtkinter.CTkLabel(
            master=self.window,
            text=f"{slider.get():.2f}",
            font=("Helvetica", 14),
            text_color="#FFFFFF",
            fg_color="#343743",
            bg_color="transparent"
        )
        slider_label.place(self.screen_width * label_x * self.WR, y=self.screen_width * label_y * self.HR)
        

        slider.set(from_value)  # Initialize slider to min value

        return slider, slider_label



