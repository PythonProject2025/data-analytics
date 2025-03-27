import pandas as pd
import customtkinter as ctk
from tkinter import messagebox


class DataManager:
    def __init__(self, context,managers):
        self.context = context
        self.managers= managers

    def load_csv_columns(self, file_path):
        try:
            df = pd.read_csv(file_path)
            numeric_columns = df.select_dtypes(include=['number']).columns.tolist()

            if hasattr(self.context, "Outlier Detection"):
                if hasattr(self.context, "dropdown"):
                    self.context.dropdown.destroy()
                    self.context.dropdown = ctk.CTkComboBox(
                        self.context.graph_frame,
                        values=numeric_columns,
                        command=self.context.update_boxplot,
                        width=280,
                        justify="center"
                    )
                    self.context.dropdown.grid(row=0, column=0, padx=10, pady=20, sticky="n")
                    self.context.dropdown.set(numeric_columns[0] if numeric_columns else "Select Column")

            for widget in self.context.scroll_frame.winfo_children():
                widget.destroy()

            for col in numeric_columns:
                checkbox = ctk.CTkCheckBox(self.context.scroll_frame, text=col)
                checkbox.grid(sticky="w", padx=5, pady=2)

            if hasattr(self.context, "scaling_scroll_frame"):
                self.load_scaling_columns(numeric_columns)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load CSV: {e}")

    def load_scaling_columns(self, column_names):
        if not hasattr(self.context, "scaling_scroll_frame"):
            return

        for widget in self.context.scaling_scroll_frame.winfo_children():
            widget.destroy()

        ctk.CTkLabel(
            self.context.scaling_scroll_frame,
            text="Column for Scaling & Encoding",
            font=("Inter", 12, "bold"),
            fg_color="#A0A0A0"
        ).pack(pady=5)

        for col in column_names:
            var = ctk.BooleanVar()
            checkbox = ctk.CTkCheckBox(
                self.context.scaling_scroll_frame,
                text=col,
                variable=var,
                command=lambda c=col, v=var: self.handle_scaling_column_selection(c, v)
            )
            checkbox.pack(anchor="w", padx=5, pady=2)
            self.context.scaling_column_checkboxes[col] = checkbox
            self.context.scaling_column_var[col] = var

    def handle_scaling_column_selection(self, column, var):
        if var.get():
            if self.context.selected_scaling_column and self.context.selected_scaling_column != column:
                self.context.scaling_column_var[self.context.selected_scaling_column].set(False)
                self.context.scaling_column_checkboxes[self.context.selected_scaling_column].deselect()
                messagebox.showwarning("Selection Error", "You can select only one column for Scaling & Encoding.")
            self.context.selected_scaling_column = column
        else:
            self.context.selected_scaling_column = None

    def update_dropdown(self, selected_columns):
        if hasattr(self.context, "dropdown"):
            self.context.dropdown.destroy()

        current_segment = self.context.segmented_frame.get()

        if current_segment == "Outlier Detection":
            command = lambda col:  self.managers["visualization"].plot_boxplot(col, cleaned=True)
        elif current_segment == "Interpolation":
            command = lambda col:  self.managers["visualization"].plot_line_graph(
                column_name=col,
                original_data=self.context.data[col],
                processed_data=self.context.interpolated_data[col],
                title="Interpolated Data"
            ) if col in self.context.interpolated_data.columns else None
        elif current_segment == "Smoothing":
            command = lambda col:  self.managers["visualization"].plot_line_graph(
                column_name=col,
                original_data=self.context.data[col],
                processed_data=self.context.smoothed_data[col],
                title="Smoothed Data"
            ) if col in self.context.smoothed_data.columns else None
        elif current_segment == "Scaling & Encoding":
            self.context.preview_scaled_encoded_data()
            return
        else:
            command = lambda col:  self.managers["visualization"].plot_boxplot(col)

        self.context.dropdown = ctk.CTkComboBox(
            self.context.graph_frame,
            values=selected_columns,
            command=command,
            width=280,
            justify="center"
        )
        self.context.dropdown.grid(row=0, column=0, padx=10, pady=20, sticky="n")
        self.context.dropdown.set(selected_columns[0] if selected_columns else "Select Column")
