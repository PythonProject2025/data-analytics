class StyleManager:
    COLORS = {
        "primary": "#2C72EA",
        "secondary": "#E0E0E0",
        "accent": "#D1D1D1",
        "transparent": "transparent",
        "info": "#A0A0A0",
        "dark_bg": "#171821"
    }

    FONTS = {
        "title": ("Inter", 16, "bold"),
        "label": ("Inter", 12, "bold"),
        "normal": ("Inter", 12)
    }

    @staticmethod
    def get_color(name):
        return StyleManager.COLORS.get(name, "#FFFFFF")

    @staticmethod
    def get_font(name):
        return StyleManager.FONTS.get(name, ("Inter", 12))

