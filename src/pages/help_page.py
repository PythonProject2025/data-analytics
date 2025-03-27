import customtkinter as ctk
import webbrowser
import os
 
class HelpPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, corner_radius=0)
 
        ctk.CTkLabel(self, text="Help Page", font=("Inter", 16)).pack(pady=20)
 
        # OPTIONAL: Keep the button in case user wants to reopen it manually
        ctk.CTkButton(self, text="Open User Documentation", command=self.open_documentation).pack(pady=10)
 
        # ✅ Automatically open documentation when HelpPage is shown
        self.open_documentation()
 
    def open_documentation(self):
        docs_path = os.path.abspath("docs/build/html/index.html")
        webbrowser.open_new_tab(f"file:///{docs_path}")