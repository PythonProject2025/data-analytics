import customtkinter as ctk


class StyleManager:
    COLORS = {
        "primary": "#3C506A",
        "secondary": ("#E0E0E0", "#2A2A2A"),
        "accent": ("#CDCDCD", "#676767"),
        "transparent": "#F5EFE6",
        "info": "#A0A0A0",
        "dark_bg": "#171821",
        "Text Color": "#FFFFFF",
        "Default Mode": ("#E0E0E0", "#2A2A2A"),
        "Default Mode I": ("#2A2A2A","#E0E0E0")
    }

    FONTS = {
        "title": ("Inter", 16, "bold"),
        "label": ("Inter", 12, "bold"),
        "normal": ("Inter", 12)
    }

    @staticmethod
    def get_color(name):
        color = StyleManager.COLORS.get(name, "#FFFFFF")

    @staticmethod
    def get_font(name):
        return StyleManager.FONTS.get(name, ("Inter", 12))

