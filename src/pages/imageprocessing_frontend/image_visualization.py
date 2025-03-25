# --- image_visualization.py ---
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import customtkinter as ctk

class ImageVisualization:
    def __init__(self, context):
        self.context = context

    def plot_confusion_matrix(self, cm_data):
        popup = ctk.CTkToplevel(self.context)
        popup.title('Confusion Matrix')
        popup.geometry('800x800')

        labels = cm_data.get("labels", [])
        cm_values = np.array(cm_data.get("values", []))

        fig, ax = plt.subplots(figsize=(8, 8))
        cax = ax.matshow(cm_values, cmap="viridis")
        fig.colorbar(cax)

        for i in range(cm_values.shape[0]):
            for j in range(cm_values.shape[1]):
                ax.text(j, i, f"{cm_values[i, j]:.2f}", ha="center", va="center", color="white")

        ax.set_xticks(np.arange(len(labels)))
        ax.set_yticks(np.arange(len(labels)))
        ax.set_xticklabels(labels, rotation=45)
        ax.set_yticklabels(labels)

        canvas = FigureCanvasTkAgg(fig, master=popup)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill='both', expand=True)
        canvas.draw()
