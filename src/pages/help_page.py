import customtkinter as ctk

class HelpPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, corner_radius=0)
        ctk.CTkLabel(self, text="Help Page", font=("Inter", 16)).pack(pady=20)
