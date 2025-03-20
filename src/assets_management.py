import os
from pathlib import Path
from PIL import Image
import customtkinter as ctk

ASSETS_PATH = Path("src\\assets")  # Update ASSETS_PATH to be relative to src

def assets_manage(path: str):
    return ASSETS_PATH / Path(path)

def load_image(path: str, size=None):
    image = Image.open(assets_manage(path))
    if size:
        image = image.resize(size)
    return ctk.CTkImage(light_image=image, dark_image=image)
