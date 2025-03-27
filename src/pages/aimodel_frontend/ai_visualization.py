
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import customtkinter as ctk

class AIVisualization:
    def __init__(self, context):
        self.context = context
        self.graph_display = context.graph_display  # Make sure this is passed correctly

    def plot_results_classification(self, cm, accuracy=None):
        # Clear previous content
        for widget in self.graph_display.winfo_children():
            widget.destroy()

        # Display accuracy score above the plot
        if accuracy is not None:
            accuracy_label = ctk.CTkLabel(
                self.graph_display,
                text=f"Accuracy: {accuracy:.2f}",
                font=("Inter", 14, "bold"),
                text_color="black",
                height=30
            )
            accuracy_label.pack(pady=(5, 0))

        # Create and embed confusion matrix
        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)
        sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", ax=ax)
        ax.set_xlabel("Predicted")
        ax.set_ylabel("Actual")
        ax.set_title("Confusion Matrix")

        canvas = FigureCanvasTkAgg(fig, master=self.graph_display)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        
        
    def plot_results_regression(self, y_pred, y_test, x_label, y_label, mae=None, mse=None, r2=None):
        y_pred = np.array(y_pred)
        y_test = np.array(y_test)

        # Clear previous widgets in graph display
        for widget in self.graph_display.winfo_children():
            widget.destroy()

        # Display regression metrics (MAE, MSE, R²)
        metrics_text = f"MAE: {mae:.4f} | MSE: {mse:.4f} | R² Score: {r2:.4f}"
        metrics_label = ctk.CTkLabel(
            self.graph_display,
            text=metrics_text,
            font=("Inter", 14, "bold"),
            text_color="black",
            height=30
        )
        metrics_label.pack(pady=(5, 0))

        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)
        ax.scatter(y_test, y_pred, alpha=0.5, label="Predictions")
        ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], "r--", lw=2, label="Perfect Fit")
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        ax.set_title("Regression Results")
        ax.legend()

        # Embed matplotlib figure into the Tkinter frame
        canvas = FigureCanvasTkAgg(fig, master=self.graph_display)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
