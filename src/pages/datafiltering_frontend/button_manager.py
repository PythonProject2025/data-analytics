import customtkinter as ctk
from tkinter import messagebox, filedialog
from src.utils.ui_style_manager import StyleManager
class ButtonManager:
    def __init__(self, context):
        self.context = context

    def add_export_send_buttons(self):
        self.context.button_frame = ctk.CTkFrame(self.context, fg_color="transparent")
        self.context.button_frame.grid(row=2, column=1, padx=10, pady=10, sticky="se")

        self.context.export_button = ctk.CTkButton(
            self.context.button_frame, text="Export", fg_color="transparent",
            border_width=2, border_color=StyleManager.COLORS.get("Default Mode I"), text_color=StyleManager.COLORS.get("Default Mode I"),
            command=self.export_data
        )
        self.context.export_button.grid(row=0, column=0, pady=5, padx=10, sticky="ew")
        self.context.export_button.grid_remove()

        self.context.compare_button = ctk.CTkButton(
            self.context.button_frame, text="Compare", fg_color="transparent",
            border_width=2, border_color=StyleManager.COLORS.get("Default Mode I"), text_color=StyleManager.COLORS.get("Default Mode I"),
            command=self.open_comparison_popup
        )
        self.context.compare_button.grid(row=0, column=1, pady=5, padx=10, sticky="ew")
        self.context.compare_button.grid_remove()

        self.context.send_button = ctk.CTkButton(
            self.context.button_frame, text="Send", fg_color="transparent",
            border_width=2, border_color=StyleManager.COLORS.get("Default Mode I"), text_color=StyleManager.COLORS.get("Default Mode I"),
            command=self.open_send_popup
        )
        self.context.send_button.grid(row=0, column=1, pady=5, padx=10, sticky="ew")
        self.context.send_button.grid_remove()

    def open_comparison_popup(self):
        self.context.compare_popup = ctk.CTkToplevel(self.context)
        self.context.compare_popup.title("Compare Data")
        self.context.compare_popup.geometry("900x500")
        self.context.compare_popup.grab_set()

        left_frame = ctk.CTkFrame(self.context.compare_popup, fg_color="#E0E0E0", corner_radius=10)
        left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        right_frame = ctk.CTkFrame(self.context.compare_popup, fg_color="#E0E0E0", corner_radius=10)
        right_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.context.compare_type = ctk.StringVar(value="Graph")
        compare_dropdown = ctk.CTkComboBox(right_frame, values=["Graph", "Data"], variable=self.context.compare_type, width=150)
        compare_dropdown.grid(row=0, column=1, padx=10, pady=10, sticky="e")

        left_options = ["Raw Data"]
        if hasattr(self.context, "interpolated_data"): left_options.append("Outlier Cleaned Data")
        if hasattr(self.context, "smoothed_data"): left_options.append("Interpolated Data")

        self.context.left_selection = ctk.StringVar(value=left_options[0])
        left_dropdown = ctk.CTkComboBox(left_frame, values=left_options, variable=self.context.left_selection, width=200)
        left_dropdown.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        right_options = []
        if hasattr(self.context, "cleaned_data"): right_options.append("Outlier Cleaned Data")
        if hasattr(self.context, "interpolated_data"): right_options.append("Interpolated Data")
        if hasattr(self.context, "smoothed_data"): right_options.append("Smoothed Data")

        self.context.right_selection = ctk.StringVar(value=right_options[0] if right_options else "")
        right_dropdown = ctk.CTkComboBox(right_frame, values=right_options, variable=self.context.right_selection, width=200)
        right_dropdown.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.context.column_selection = ctk.StringVar(value=self.context.selected_columns[0])
        column_dropdown = ctk.CTkComboBox(
            self.context.compare_popup,
            values=self.context.selected_columns,
            variable=self.context.column_selection,
            width=200
        )
        column_dropdown.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        compare_button = ctk.CTkButton(
            right_frame, text="Compare", command=self.context.update_comparison_view,
            fg_color="transparent", border_width=2, border_color="black", text_color="black"
        )
        compare_button.grid(row=0, column=2, pady=10, sticky="ew")

    def export_data(self):
        if self.context.segment_completion.get("Scaling & Encoding", False):
            data_to_export = self.context.scaled_encoded_data
            message = None
        elif self.context.segment_completion.get("Smoothing", False):
            data_to_export = self.context.smoothed_data
            message = "Only Smoothed data available for export."
        elif self.context.segment_completion.get("Interpolation", False):
            data_to_export = self.context.interpolated_data
            message = "Only Interpolated data available for export."
        elif self.context.segment_completion.get("Outlier Detection", False):
            data_to_export = self.context.cleaned_data
            message = "Only Outlier Cleaned data available for export."
        else:
            messagebox.showerror("Error", "No processed data available for export!")
            return

        if message:
            messagebox.showinfo("Export Data", message)

        file_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                                 filetypes=[("CSV files", "*.csv"), ("All Files", "*.*")],
                                                 title="Save Processed Data")

        if file_path:
            data_to_export.to_csv(file_path, index=False)
            messagebox.showinfo("Success", "Data successfully exported!")

    def open_send_popup(self):
        if not hasattr(self.context, "scaled_encoded_data"):
            messagebox.showerror("Error", "Scaling & Encoding must be completed before sending the file.")
            return

        popup = ctk.CTkToplevel(self.context)
        popup.title("Select Destination")
        popup.geometry("400x200")
        popup.grab_set()

        ctk.CTkLabel(popup, text="Choose the Process :", font=("Inter", 14, "bold")).pack(pady=20)
        process_var = ctk.StringVar(value="Regression & Classification")
        process_dropdown = ctk.CTkComboBox(popup, values=["Regression & Classification", "AI Model"], variable=process_var, width=250)
        process_dropdown.pack(pady=10)

        def send_file():
            selected_process = process_var.get()
            popup.destroy()

            target_page = "RegressionClassificationPage" if selected_process == "Regression & Classification" else "AIModelPage"

            self.context.parent.file_paths[target_page] = self.context.file_path
            self.context.parent.file_names[target_page] = "Preprocessed Data"
            self.context.parent.page_data[target_page] = self.context.scaled_encoded_data

            self.context.parent.show_page(target_page)

        ctk.CTkButton(popup, text="Proceed", command=send_file).pack(pady=10)

    def update_buttons_visibility(self):
        if self.context.segment_completion.get("Outlier Detection", False) or self.context.segment_completion.get("Scaling & Encoding", False):
            self.add_export_send_buttons()

        if hasattr(self.context, "cleaned_data"):
            self.context.export_button.grid()
            self.context.compare_button.grid()

        if hasattr(self.context, "interpolated_data"):
            self.context.export_button.grid()
            self.context.compare_button.grid()

        if hasattr(self.context, "smoothed_data"):
            self.context.export_button.grid()
            self.context.compare_button.grid()

        if hasattr(self.context, "scaled_encoded_data"):
            self.context.export_button.grid()
            self.context.compare_button.grid_remove()
            self.context.send_button.grid()
