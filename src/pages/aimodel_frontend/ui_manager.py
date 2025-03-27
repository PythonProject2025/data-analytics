import customtkinter as ctk
from src.utils.info_txt import INFO_TEXT_AI

class AIUIManager:
    def __init__(self, context, ui):
        self.context = context
        self.ui = ui

        self.font_label = ui.font_label
        self.font_normal = ui.font_normal
        self.color_info = ui.color_info
        self.color_accent = ui.color_accent
        self.color_secondary = ui.color_secondary

        self.context.segments = {}
        self.context.problem_var = ctk.StringVar(value="Regression")
        self.context.sliders = {}
        self.context.comboboxes = {}

        self.ui_to_internal = {
            "ANN": "ArtificialNeuralNetwork",
            "ArtificialNeuralNetwork": "ArtificialNeuralNetwork",
            "RandomForest": "RandomForest",
            "CatBoost": "CatBoost",
            "XGBoost": "XGBoost",
            "Problem Selection": "Problem Selection"
        }

    def initialize_segment(self, segment_name):
        internal_name = self.ui_to_internal.get(segment_name, segment_name)
        segment_method_map = {
            "Problem Selection": self.create_problem_selection_frame,
            "RandomForest": self.create_rf_frame,
            "CatBoost": self.create_cb_frame,
            "ArtificialNeuralNetwork": self.create_ann_frame,
            "XGBoost": self.create_xgb_frame
        }
        frame = segment_method_map[internal_name]() if internal_name in segment_method_map else None
        if frame:
            self.context.segments[segment_name] = frame

    def create_problem_selection_frame(self):
        frame = ctk.CTkFrame(self.context.segment_container, fg_color=self.color_secondary, corner_radius=10)
        frame.grid_columnconfigure(0, weight=1)

        radio_frame = ctk.CTkFrame(frame, fg_color=self.color_accent, corner_radius=10)
        radio_frame.grid(row=1, column=0, padx=30, pady=15, sticky="w")

        self.ui.create_radio_buttons(
            parent=radio_frame,
            label_text="",
            variable=self.context.problem_var,
            options=["Regression", "Classification"],
            grid_positions=[(0, 0), (1, 0)]
        )

        return frame

    def create_rf_frame(self):
        return self._build_model_frame("RandomForest", [
            ("n_estimators", 10, 500, 200),
            ("max_depth", 3, 50, 20),
            ("min_samples_split", 4, 10, 5),
            ("min_samples_leaf", 1, 10, 1)
        ])

    def create_cb_frame(self):
        return self._build_model_frame("CatBoost", [
            ("n_estimators", 100, 1000, 500),
            ("learning_rate", 0.01, 0.1, 0.03),
            ("max_depth", 4, 10, 6),
            ("reg_lambda", 1, 10, 3)
        ])

    def create_ann_frame(self):
        model = "ArtificialNeuralNetwork"
        frame = ctk.CTkFrame(self.context.segment_container, fg_color=self.color_secondary, corner_radius=10)
        frame.grid_columnconfigure(0, weight=1)

        self._create_slider_frame(frame, model, "layer_number", 1, 6, 3, 0)
        self._create_slider_frame(frame, model, "units", 1, 256, 128, 1)
        self._create_combobox(frame, model, "activation", ["relu", "sigmoid", "tanh", "softmax"], "relu", 2)
        self._create_combobox(frame, model, "optimizer", ["adam", "sgd", "rmsprop"], "adam", 3)
        self._create_slider_frame(frame, model, "batch_size", 16, 128, 30, 4)
        self._create_slider_frame(frame, model, "epochs", 10, 300, 100, 5)

        return frame

    def create_xgb_frame(self):
        return self._build_model_frame("XGBoost", [
            ("n_estimators", 100, 1000, 200),
            ("learning_rate", 0.01, 0.3, 0.3),
            ("min_split_loss", 3, 10, 10),
            ("max_depth", 0, 10, 6)
        ])

    def _build_model_frame(self, model_name, sliders):
        frame = ctk.CTkFrame(self.context.segment_container, fg_color=self.color_secondary, corner_radius=10)
        frame.grid_columnconfigure(0, weight=1)
        for i, (label, min_val, max_val, default_val) in enumerate(sliders):
            self._create_slider_frame(frame, model_name, label, min_val, max_val, default_val, i)
        return frame

    def _create_slider_frame(self, parent, model_name, label_text, from_, to, default, row):
        if model_name not in self.context.sliders:
            self.context.sliders[model_name] = {}

        frame = ctk.CTkFrame(parent, fg_color="#D1D1D1", corner_radius=10)
        frame.grid(row=row, column=0, padx=10, pady=10, sticky="nsew")
        frame.grid_columnconfigure(0, weight=1)

        label = ctk.CTkLabel(frame, text=label_text, font=self.font_label, fg_color=self.color_info)
        label.grid(row=0, column=0, sticky="nsew")
        self.ui.create_info_button(frame, INFO_TEXT_AI.get(model_name, {}).get(label_text, "No info"), row=0, column=1)

        value_label = ctk.CTkLabel(frame, text=f"Value: {default}", font=self.font_normal)
        value_label.grid(row=1, column=0, pady=5)

        def update_value(value):
            val = float(value)
            value_label.configure(text=f"Value: {int(val)}" if val.is_integer() else f"Value: {val:.2f}")

        steps = (to - from_) if isinstance(from_, int) and isinstance(to, int) else 100

        slider = ctk.CTkSlider(frame, from_=from_, to=to, number_of_steps=steps, command=update_value)
        slider.set(default)
        slider.grid(row=2, column=0, padx=10, sticky="ew")

        self.context.sliders[model_name][label_text] = slider

    def _create_combobox(self, parent, model_name, label, options, default, row):
        if model_name not in self.context.comboboxes:
            self.context.comboboxes[model_name] = {}

        frame = ctk.CTkFrame(parent, fg_color=self.color_accent, corner_radius=10)
        frame.grid(row=row, column=0, padx=10, pady=10, sticky="nsew")
        frame.grid_columnconfigure(0, weight=1)

        label_widget = ctk.CTkLabel(frame, text=label, font=self.font_label, fg_color=self.color_info)
        label_widget.grid(row=0, column=0, sticky="nsew")
        self.ui.create_info_button(frame, INFO_TEXT_AI.get(model_name, {}).get(label, "No info"), row=0, column=1)

        combobox = ctk.CTkComboBox(frame, values=options)
        combobox.set(default)
        combobox.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

        self.context.comboboxes[model_name][label] = combobox
