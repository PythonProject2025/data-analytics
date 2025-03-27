import requests
import json
import pandas as pd
import customtkinter as ctk
from tkinter import messagebox
from src.models.data_object_class import DataObject

class RequestManager:
    def __init__(self, context,managers):
        self.context = context  # Reference to main class/page for accessing widgets, data, etc.
        self.managers=managers

    def send_request(self, process_name, json_data):
        try:
            response = requests.post(f"http://127.0.0.1:8000/api/{process_name}/", json=json_data)
            if response.status_code == 200:
                response_data = response.json()
                if process_name == "outlier_detection" and "cleaned_data" in response_data:
                    self.context.cleaned_data = response_data["cleaned_data"]
                elif process_name == "interpolation" and "interpolated_data" in response_data:
                    self.context.interpolated_data = response_data["interpolated_data"]
                elif process_name == "smoothing" and "smoothed_data" in response_data:
                    self.context.smoothed_data = response_data["smoothed_data"]
                return response_data
            else:
                messagebox.showerror("Error", response.json().get('error', 'File upload failed.'))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def run_outlier_detection(self):
        if self.context.column_name:

            self.managers["visualization"].plot_boxplot(self.context.column_name)

        self.context.selected_columns = []

        for child in self.context.scroll_frame.winfo_children():
            if isinstance(child, ctk.CTkCheckBox) and child.get():
                self.context.selected_columns.append(child.cget("text"))

        if not self.context.selected_columns:
            messagebox.showerror("Error", "You must select at least one column before proceeding!")
            return

        dataobject = DataObject()
        dataobject.data_filtering["filepath"] = self.context.file_path
        dataobject.data_filtering["Outlier Detection"]["Method"] = self.context.radio_var.get()
        dataobject.data_filtering["Outlier Detection"]["Parameters"]["contamination"] = self.context.ui.sliders["Contamination Value"].get()
        dataobject.data_filtering["Outlier Detection"]["Parameters"]["column_names"] = self.context.selected_columns

        json_data = {"dataobject": dataobject.to_dict()}

        self.context.show_loading_message()
        self.context.graph_display.update_idletasks()
        response = self.send_request("outlier_detection", json_data)

        if response and "cleaned_data" in response:
            self.context.cleaned_data_str = response["cleaned_data"]

        try:
            cleaned_data_dict = json.loads(self.context.cleaned_data_str)
            self.context.cleaned_data = pd.DataFrame.from_dict(cleaned_data_dict)

            if not self.context.cleaned_data.empty:
                self.context.managers["data"].update_dropdown(self.context.selected_columns)
                self.context.managers["visualization"].plot_boxplot(self.context.selected_columns[0], cleaned=True)

        except json.JSONDecodeError as e:
            print("Error: Failed to parse cleaned data JSON:", e)
            self.context.cleaned_data = None

    def run_interpolation(self):
        if not hasattr(self.context, "cleaned_data"):
            messagebox.showerror("Error", "Cleaned data is missing. Please run Outlier Detection first.")
            return

        json_data = {"cleaned_data": self.context.cleaned_data_str}
        response = self.send_request("interpolation", json_data)

        if response and "interpolated_data" in response:
            self.context.interpolated_data_str = response["interpolated_data"]

            try:
                interpolated_data_dict = json.loads(self.context.interpolated_data_str)
                self.context.interpolated_data = pd.DataFrame.from_dict(interpolated_data_dict)

                if not self.context.interpolated_data.empty:
                    self.context.managers["data"].update_dropdown(self.context.selected_columns)
                    self.context.managers["visualization"].plot_line_graph(
                        column_name=self.context.selected_columns[0],
                        original_data=self.context.data[self.context.selected_columns[0]],
                        processed_data=self.context.interpolated_data[self.context.selected_columns[0]],
                        title="Interpolated Data"
                    )
            except json.JSONDecodeError as e:
                print("Error: Failed to parse interpolated data JSON:", e)
                self.context.interpolated_data = None

    def run_smoothing(self):
        if not hasattr(self.context, "interpolated_data"):
            messagebox.showerror("Error", "Interpolated data is missing. Please run Outlier Detection first and then Interpolation.")
            return

        dataobject = DataObject()
        dataobject.data_filtering["Smoothing"]["Method"] = self.context.smoothing_radio_var.get()

        if self.context.smoothing_radio_var.get() == "SMA":
            dataobject.data_filtering["Smoothing"]["parameters"]["window_size"] = int(round(self.context.sma_slider.get()))
        elif self.context.smoothing_radio_var.get() == "TES":
            tes_params = {}
            for key, widget in self.context.tes_params.items():
                if isinstance(widget, ctk.CTkSlider):
                    tes_params[key] = float(widget.get())
                elif isinstance(widget, ctk.CTkEntry):
                    tes_params[key] = widget.get()
            dataobject.data_filtering["Smoothing"]["parameters"].update(tes_params)

        json_data = {
            "dataobject": dataobject.to_dict(),
            "interpolated_data": self.context.interpolated_data_str
        }

        response = self.send_request("smoothing", json_data)

        if response and "smoothed_data" in response:
            self.context.smoothed_data_str = response["smoothed_data"]

            try:
                smoothed_data_dict = json.loads(self.context.smoothed_data_str)
                self.context.smoothed_data = pd.DataFrame.from_dict(smoothed_data_dict)

                if not self.context.smoothed_data.empty:
                    self.context.managers["data"].update_dropdown(self.context.selected_columns)
                    self.context.managers["visualization"].plot_line_graph(
                        column_name=self.context.selected_columns[0],
                        original_data=self.context.data[self.context.selected_columns[0]],
                        processed_data=self.context.smoothed_data[self.context.selected_columns[0]],
                        title="Smoothed Data"
                    )
            except json.JSONDecodeError as e:
                print(" Error: Failed to parse smoothed data JSON:", e)
                self.context.smoothed_data = None

    def run_scaling_and_encoding(self):
        if hasattr(self.context, "smoothed_data"):
            data_str = self.context.smoothed_data_str
        else:
            if not hasattr(self.context, "data"):
                messagebox.showerror("Error", "No raw data found! Please upload a dataset first.")
                return
            data_str = self.context.data.to_json()

        dataobject = DataObject()
        dataobject.data_filtering["Train-Test Split"]["parameters"]["test_size"] = float(self.context.ui.sliders["Test Size"].get())
        dataobject.data_filtering["Train-Test Split"]["parameters"]["random_state"] = int(round(self.context.ui.sliders["Random State"].get()))
        dataobject.data_filtering["Train-Test Split"]["parameters"]["target_column"] = self.context.selected_scaling_column

        json_data = {
            "dataobject": dataobject.to_dict(),
            "smoothed_data": data_str
        }

        response = self.send_request("scaling_encoding", json_data)

        if response and "processed_data" in response:
            processed_data = response["processed_data"]

            if not isinstance(processed_data, dict):
                messagebox.showerror("Error", "Invalid processed data format received.")
                return

            column_lengths = [len(v) for v in processed_data.values()]
            min_length = min(column_lengths)
            cleaned_data = {k: list(v)[:min_length] for k, v in processed_data.items()}

            self.context.scaled_encoded_data = pd.DataFrame(cleaned_data)
            self.context.managers["preview"].preview_scaled_encoded_data()
        else:
            messagebox.showerror("Error", "Failed to retrieve scaled and encoded data.")