import customtkinter as ctk
from tkinter import messagebox, ttk
import tkinter as tk
import pandas as pd

class PreviewManager:
    def __init__(self, context):
        self.context = context

    def preview_scaled_encoded_data(self):
        """Opens a new popup window to display the scaled and encoded data."""
        if not hasattr(self.context, "scaled_encoded_data") or self.context.scaled_encoded_data.empty:
            messagebox.showerror("Error", "No scaled and encoded data available!")
            return

        preview_window = ctk.CTkToplevel(self.context)
        preview_window.title("Scaled and Encoded Data Preview")
        preview_window.geometry("900x500")
        preview_window.grab_set()

        frame = tk.Frame(preview_window)
        frame.pack(fill="both", expand=True)

        tree = ttk.Treeview(frame, columns=list(self.context.scaled_encoded_data.columns), show="headings")

        for col in self.context.scaled_encoded_data.columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)

        for index, row in self.context.scaled_encoded_data.head(50).iterrows():
            tree.insert("", "end", values=list(row))

        v_scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscroll=v_scrollbar.set)

        h_scrollbar = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)
        tree.configure(xscroll=h_scrollbar.set)

        tree.pack(side="top", fill="both", expand=True)
        v_scrollbar.pack(side="right", fill="y")
        h_scrollbar.pack(side="bottom", fill="x")

    def preview_csv_in_graph_frame(self):
        """Displays a limited preview (50 rows) of the CSV inside `graph_frame`, filling available space with proper scrolling."""

        # Clear Previous Widgets in `graph_display`
        for widget in self.context.graph_display.winfo_children():
            widget.destroy()

        if not self.context.file_path:
            messagebox.showerror("Error", "No CSV file selected!")
            return

        # Read CSV File
        try:
            df = pd.read_csv(self.context.file_path)  # Load CSV
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open CSV: {e}")
            return

        # Create Frame Inside `graph_display` to Contain Table
        table_frame = tk.Frame(self.context.graph_display, height=1000)
        table_frame.pack(fill="both", expand=True)

        # Create a Canvas for Horizontal Scrolling Only
        canvas = tk.Canvas(table_frame)
        scrollbar_x = ttk.Scrollbar(table_frame, orient="horizontal", command=canvas.xview)
        scrollbar_y = ttk.Scrollbar(table_frame, orient="vertical", command=canvas.yview)

        # Create Inner Frame for Table Inside Canvas
        content_frame = tk.Frame(canvas, height=1000)
        content_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        canvas.create_window((0, 0), window=content_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

        # Create Treeview (Table) Inside `content_frame`
        tree = ttk.Treeview(content_frame, columns=list(df.columns), show="headings")

        # Dynamically Adjust Column Widths
        total_columns = len(df.columns)
        column_width = max(150, int(self.context.graph_display.winfo_width() / total_columns))  # Auto-size columns

        for col in df.columns:
            tree.heading(col, text=col, anchor="center")
            tree.column(col, width=column_width, anchor="center")

        # Insert First 50 Rows to Prevent UI Lag
        for _, row in df.head(50).iterrows():
            tree.insert("", "end", values=list(row))

        # Pack Elements to Use Full Graph Frame Height
        canvas.pack(fill="both", expand=True)
        scrollbar_x.pack(side="bottom", fill="x")
        scrollbar_y.pack(side="right", fill="y")
        tree.pack(fill="both", expand=True)

    def preview_csv_popup(self):
        if not self.context.file_path:
            messagebox.showerror("Error", "No CSV file selected!")
            return

        try:
            df = pd.read_csv(self.context.file_path)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open CSV: {e}")
            return

        preview_window = ctk.CTkToplevel(self.context)
        preview_window.title("CSV Full Preview")
        preview_window.geometry("1000x600")
        preview_window.grab_set()

        frame = tk.Frame(preview_window)
        frame.pack(fill="both", expand=True)

        tree = ttk.Treeview(frame, columns=list(df.columns), show="headings")

        for col in df.columns:
            tree.heading(col, text=col, anchor="center")
            tree.column(col, width=150, anchor="center")

        for _, row in df.iterrows():
            tree.insert("", "end", values=list(row))

        v_scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        h_scrollbar = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)

        tree.configure(yscroll=v_scrollbar.set, xscroll=h_scrollbar.set)

        tree.pack(side="top", fill="both", expand=True)
        v_scrollbar.pack(side="right", fill="y")
        h_scrollbar.pack(side="bottom", fill="x")

