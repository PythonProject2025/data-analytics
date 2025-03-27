# plotting_manager.py
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, ttk
import pandas as pd
import numpy as np

class DataVisualization:
    def __init__(self, context):
        self.context=context

    def plot_boxplot(self, column_name, cleaned=False):
        if cleaned and self.context.cleaned_data is not None:
            plot_data = self.context.cleaned_data
        else:
            plot_data = self.context.data

        if column_name not in plot_data.columns:
            print(f" Column '{column_name}' not found in dataset!")
            return

        if cleaned:
            plot_data = plot_data.apply(pd.to_numeric, errors='coerce')

        for widget in self.context.graph_display.winfo_children():
            widget.destroy()

        fig, ax = plt.subplots(figsize=(7, 4))
        fig.patch.set_facecolor("#E0E0E0")
        ax.set_facecolor("#E0E0E0")

        ax.boxplot(plot_data[column_name].dropna(), vert=False, patch_artist=True, widths=0.6,
                   boxprops=dict(facecolor='lightblue', edgecolor='black', linewidth=1.2),
                   medianprops=dict(color='red', linewidth=1.5),
                   whiskerprops=dict(color='black', linewidth=1.2, linestyle="--"))

        ax.set_title(f"Box Plot of {column_name}", fontsize=13, fontweight="bold")
        ax.set_xlabel(column_name, fontsize=11)
        ax.tick_params(axis="x", labelsize=10)
        ax.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.7)

        canvas = FigureCanvasTkAgg(fig, master=self.context.graph_display)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill="both", expand=True)

        toolbar_frame = ctk.CTkFrame(self.context.graph_display, fg_color="#E0E0E0")
        toolbar_frame.pack(side="top", fill="x")
        toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)
        toolbar.config(background="#E0E0E0")
        for child in toolbar.winfo_children():
            child.config(bg="#E0E0E0")
        toolbar.update()
        canvas.draw()

    def plot_line_graph(self, column_name, original_data, processed_data, title):
        try:
            date_column = pd.to_datetime(self.context.data.iloc[:, 0], errors='coerce', dayfirst=True)
            if date_column.isna().sum() > 0:
                date_column = pd.to_datetime(self.context.data.iloc[:, 0], errors='coerce', format="%d/%m/%Y %H:%M", dayfirst=True)
            if date_column.isna().sum() > 0:
                date_column = original_data.index
        except:
            date_column = original_data.index

        if isinstance(original_data, np.ndarray):
            original_data = pd.Series(original_data, name=column_name, index=date_column)
        if isinstance(processed_data, np.ndarray):
            processed_data = pd.Series(processed_data, name=column_name, index=date_column)

        for widget in self.context.graph_display.winfo_children():
            widget.destroy()

        fig, ax = plt.subplots(figsize=(8, 5))
        fig.patch.set_facecolor("#E0E0E0")
        ax.set_facecolor("#E0E0E0")

        ax.plot(date_column, original_data, color="blue", label="Original Data", linestyle='dashed')
        ax.plot(date_column, processed_data, color="red", label=title, linewidth=1.5)

        ax.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%Y"))
        ax.xaxis.set_major_locator(mdates.AutoDateLocator())
        plt.xticks(rotation=30, ha="right")
        plt.subplots_adjust(bottom=0.3)

        ax.set_title(f"{title} for {column_name}", fontsize=13, fontweight="bold")
        ax.set_xlabel("Timestamp", fontsize=1)
        ax.set_ylabel(column_name, fontsize=10)
        ax.legend()
        ax.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.7)

        canvas = FigureCanvasTkAgg(fig, master=self.context.graph_display)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill="both", expand=True)

        toolbar_frame = ctk.CTkFrame(self.context.graph_display, fg_color="#E0E0E0")
        toolbar_frame.pack(side="top", fill="x")
        toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)
        toolbar.config(background="#E0E0E0")
        for child in toolbar.winfo_children():
            child.config(bg="#E0E0E0")
        toolbar.update()
        canvas.draw()

    def show_comparison_data(self, left_data, right_data, column_name):

         # Retrieve DataFrames
        left_df = self.context.get_data_by_name(left_data)
        right_df = self.context.get_data_by_name(right_data)

        if left_df is None or right_df is None:
            messagebox.showerror("Error", "Invalid Data Selection!")
            return

        if column_name not in left_df.columns or column_name not in right_df.columns:
            messagebox.showerror("Error", f"Column '{column_name}' not found in selected datasets!")
            return

        left_values = left_df[column_name].astype(str).tolist()
        right_values = right_df[column_name].astype(str).tolist()

        popup = ctk.CTkToplevel(self.context.graph_display)
        popup.title("Data Comparison")
        popup.geometry("900x500")
        popup.grab_set()

        frame = tk.Frame(popup)
        frame.pack(fill="both", expand=True)

        tree = ttk.Treeview(frame, columns=("Index", "Left Data", "Right Data"), show="headings")
        tree.heading("Index", text="Index", anchor="center")
        tree.heading("Left Data", text=f"Left ({column_name})", anchor="center")
        tree.heading("Right Data", text=f"Right ({column_name})", anchor="center")
        tree.column("Index", width=50, anchor="center")
        tree.column("Left Data", width=200, anchor="center")
        tree.column("Right Data", width=200, anchor="center")

        for i in range(min(len(left_values), len(right_values))):
            tag = "changed" if left_values[i] != right_values[i] else ""
            tree.insert("", "end", values=(i, left_values[i], right_values[i]), tags=(tag,))
        tree.tag_configure("changed", background="lightcoral")

        v_scroll = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        h_scroll = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)
        tree.configure(yscroll=v_scroll.set, xscroll=h_scroll.set)

        tree.pack(side="top", fill="both", expand=True)
        v_scroll.pack(side="right", fill="y")
        h_scroll.pack(side="bottom", fill="x")

    def plot_comparison_graph(self, left_data, right_data, column_name):
        """Generates side-by-side comparison graphs with proper date formatting, rotated X-labels, and toolbars below each plot."""

        # Retrieve DataFrames
        left_df = self.context.get_data_by_name(left_data)
        right_df = self.context.get_data_by_name(right_data)

        if left_df is None or right_df is None:
            messagebox.showerror("Error", "Invalid Data Selection!")
            return

        # Ensure column exists in both datasets
        if column_name not in left_df.columns or column_name not in right_df.columns:
            messagebox.showerror("Error", f"Column '{column_name}' not found in selected datasets!")
            return

        # Convert timestamps to same format for both datasets
        def process_datetime(df):
            if isinstance(df, pd.DataFrame):
                date_column = df.iloc[:, 0]  # Assume first column is Date/Time
            else:
                return df.index  # Use index if no explicit Date column

            try:
                return pd.to_datetime(date_column, errors='coerce', dayfirst=True)
            except:
                return df.index

        left_timestamps = process_datetime(left_df)
        right_timestamps = process_datetime(left_df)

        # Clear previous widgets in the compare popup
        for widget in self.context.compare_popup.winfo_children():
            if isinstance(widget, tk.Canvas):
                widget.destroy()

        # Create Matplotlib Figure with Two Subplots (Side-by-Side)
        fig, axes = plt.subplots(1, 2, figsize=(12, 5))  # Side-by-side comparison
        fig.patch.set_facecolor("#E0E0E0")  # Match UI Theme
        use_boxplot = (left_data == "Raw Data" and right_data == "Outlier Cleaned Data")

        if use_boxplot:
            # Left Graph - Boxplot (Raw Data)
            axes[0].boxplot(left_df[column_name].dropna(), vert=False, patch_artist=True,
                            boxprops=dict(facecolor='lightblue', edgecolor='black'),
                            medianprops=dict(color='red'))
            axes[0].set_title(f"{left_data} - Box Plot", fontsize=11)

            # Right Graph - Boxplot (Outlier Cleaned Data, also blue color)
            axes[1].boxplot(right_df[column_name].dropna(), vert=False, patch_artist=True,
                            boxprops=dict(facecolor='lightblue', edgecolor='black'),
                            medianprops=dict(color='red'))
            axes[1].set_title(f"{right_data} - Box Plot", fontsize=11)

        else:
            # Left Graph - Line Plot
            axes[0].plot(left_timestamps, left_df[column_name], color="blue", label=left_data)
            axes[0].set_title(f"{left_data} - Line Graph", fontsize=11)
            axes[0].set_xlabel("Timestamp")
            axes[0].set_ylabel(column_name)
            axes[0].legend()
            axes[0].grid(True, linestyle="--", alpha=0.5)

            # Format X-axis for Date/Time
            axes[0].xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%Y"))
            axes[0].xaxis.set_major_locator(mdates.AutoDateLocator())
            plt.setp(axes[0].xaxis.get_majorticklabels(), rotation=30, ha="right")

            # Right Graph - Line Plot
            axes[1].plot(right_timestamps, right_df[column_name], color="red", label=right_data)
            axes[1].set_title(f"{right_data} - Line Graph", fontsize=11)
            axes[1].set_xlabel("Timestamp")
            axes[1].set_ylabel(column_name)
            axes[1].legend()
            axes[1].grid(True, linestyle="--", alpha=0.5)

            # Format X-axis for Date/Time
            axes[1].xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%Y"))
            axes[1].xaxis.set_major_locator(mdates.AutoDateLocator())
            plt.setp(axes[1].xaxis.get_majorticklabels(), rotation=30, ha="right")

        # Adjust layout to prevent X-label overlap
        plt.subplots_adjust(bottom=0.3)

        # Embed the Matplotlib Figure inside Tkinter Frame
        canvas = FigureCanvasTkAgg(fig, master=self.context.compare_popup)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.grid(row=2, column=0, columnspan=2, pady=10, sticky="nsew")

        # Add Toolbars Below Each Graph
        toolbar_frame_left = ctk.CTkFrame(self.context.compare_popup, fg_color="#E0E0E0")
        toolbar_frame_left.grid(row=3, column=0, padx=10, pady=5, sticky="n")
        toolbar_left = NavigationToolbar2Tk(canvas, toolbar_frame_left)
        toolbar_left.update()

        toolbar_frame_right = ctk.CTkFrame(self.context.compare_popup, fg_color="#E0E0E0")
        toolbar_frame_right.grid(row=3, column=1, padx=10, pady=5, sticky="n")
        toolbar_right = NavigationToolbar2Tk(canvas, toolbar_frame_right)
        toolbar_right.update()

        # Render the plot
        canvas.draw()

