import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import messagebox

class DataVisualization:
    def __init__(self, app):
        self.app = app
        self.page_widgets = []

    def display_graph(self, data_dict):
        """
        Displays multiple graphs based on the provided data.
        
        Parameters:
        - data_dict (dict): A dictionary where keys are titles (e.g., "Cleaned Data") and values are DataFrames.
        """
        if not data_dict or all(isinstance(df, pd.DataFrame) and df.empty for df in data_dict.values()):
            messagebox.showwarning("Warning", "No data to display.")
            return

        x_offset = 50  # Initial x-offset for placing graphs
        spacing = 600   # Space between multiple graphs
        
        for title, df in data_dict.items():
            self.plot_graph(df, title, x_offset)
            x_offset += spacing  # Move the next graph to the right

    def plot_graph(self, df, title, x_offset):
        """
        Plots a single graph from a given DataFrame.
        
        Parameters:
        - df (DataFrame): The data to plot.
        - title (str): The title of the graph.
        - x_offset (int): Horizontal position offset.
        """
        if df is None or df.empty:
            return
        
        # Ensure the selected column exists in the DataFrame
        if self.app.choice_col not in df.columns:
            messagebox.showerror("Error", f"Column '{self.app.choice_col}' not found in the dataset.")
            return

        fig, ax = plt.subplots(figsize=(6, 4))
        fig.patch.set_facecolor("#171821")
        ax.set_facecolor("#171821")
        ax.plot(df.index, df[self.app.choice_col], label=self.app.choice_col)
        ax.set_title(f"{title} Output", {'color': "#FFFFFF"})
        ax.set_xlabel("Index", {'color': "#FFFFFF"})
        ax.set_ylabel(self.app.choice_col, {'color': "#FFFFFF"})

        ax.tick_params(axis='both', colors='#FFFFFF') 
        ax.legend(edgecolor="#FFFFFF", labelcolor='black')

        for spine in ax.spines.values():
            spine.set_edgecolor("#FFFFFF")
        
        # Create and place the FigureCanvasTkAgg widget
        canvas_widget = FigureCanvasTkAgg(fig, master=self.app.window)
        canvas_tk_widget = canvas_widget.get_tk_widget()
        canvas_tk_widget.place(x=x_offset, y=330)
        canvas_widget.draw()

        # Keep track of widgets for cleanup if needed
        self.page_widgets.append((canvas_tk_widget, None))
