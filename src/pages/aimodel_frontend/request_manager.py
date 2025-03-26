import pandas as pd
import requests
from tkinter import messagebox
from src.models.data_object_class import DataObject

class AIRequestManager:
    def __init__(self, context):
        self.context = context

    def submit_action(self):
        selected_model = self.context.segmented_frame.get()
        print(f"\n🟩 Submitting AI Model: {selected_model}\n")

        # Map UI name to internal model key
        model_map = {
            "ANN": "ArtificialNeuralNetwork"
        }
        backend_model_key = model_map.get(selected_model, selected_model)

        dataobject = DataObject()

        # Step 1: Add preprocessed data
        if self.context.file_data is not None:
            for key, value in self.context.file_data.items():
                if isinstance(value, pd.DataFrame):
                    dataobject.data_filtering["Train-Test Split"]["split_data"][key] = value.to_dict(orient="records")
                elif isinstance(value, pd.Series):
                    dataobject.data_filtering["Train-Test Split"]["split_data"][key] = value.tolist()

        # Step 2: Add problem type
        if hasattr(self.context, "problem_var"):
            problem_type = self.context.problem_var.get().lower()
            dataobject.ai_model["problem_type"] = problem_type
            print(f"🧩 Problem Type: {problem_type}")

        # Step 3: Add selected model
        dataobject.ai_model["Selected Model"] = backend_model_key

        # Step 4: Collect slider values
        print("📊 Slider Parameters:")
        if backend_model_key in self.context.sliders:
            for param, slider in self.context.sliders[backend_model_key].items():
                val = slider.get()
                parsed_val = int(val) if float(val).is_integer() else float(val)
                dataobject.ai_model[backend_model_key][param] = parsed_val
                print(f"   • {param}: {parsed_val}")
        else:
            print("⚠️ No sliders found for this model.")

        # Step 5: Collect combobox values
        print("📦 Combobox Parameters:")
        if backend_model_key in self.context.comboboxes:
            for param, combo in self.context.comboboxes[backend_model_key].items():
                val = combo.get()
                dataobject.ai_model[backend_model_key][param] = val
                print(f"   • {param}: {val}")
        else:
            print("⚠️ No comboboxes found for this model.")

        # Step 6: Final summary
        print("\n📤 Final Payload Summary:")
        print(f"   - Model: {backend_model_key}")
        print(f"   - Problem Type: {dataobject.ai_model['problem_type']}")
        print(f"   - Payload:")
        for key, val in dataobject.ai_model[backend_model_key].items():
            print(f"     • {key}: {val}")

        # Step 7: Send to backend
        self._send_request({"dataobject": dataobject.to_dict()})
        print (dataobject.ai_model)

    def _send_request(self, json_data):
        try:
            response = requests.post("http://127.0.0.1:8000/api/ai_model/", json=json_data)
            if response.status_code == 200:
                print("✅ Success! Response:", response.json())
            else:
                messagebox.showerror("Error", response.json().get("error", "Request failed."))
        except Exception as e:
            messagebox.showerror("Connection Error", str(e))
