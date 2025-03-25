# --- image_request_manager.py ---
import json
import requests
from tkinter import messagebox
from src.models.data_object_class import DataObject

class ImageRequestManager:
    def __init__(self, context):
        self.context = context

    def submit_action(self):
        active_tab = self.context.segmented_frame.get()

        if active_tab == "Image Processing":
            self._handle_image_processing_submission()

        elif active_tab == "Image Train":
            print("Image Train Submitted")

    def _handle_image_processing_submission(self):
        print("Image Processing Submitted")

        if "Image Train" not in self.context.segments:
            self.context.segmented_frame.configure(values=["Image Processing", "Image Train"])
            self.context.managers["ui"].initialize_segment("Image Train")

        # Extract parameters from context
        activation_function = self.context.radio_var.get()
        epochs = int(self.context.epoch_slider.get())
        optimizer = self.context.optimizer_combobox.get()
        test_size = float(self.context.test_size_slider.get())
        random_state = int(self.context.random_state_slider.get())


        # Build data object
        dataobject = DataObject()
        dataobject.image_processing["fileio"]["zipFilePath"] = self.context.file_path
        dataobject.image_processing["fileio"]["isZipped"] = True
        dataobject.image_processing["model_params"]["activation_fn"] = activation_function
        dataobject.image_processing["model_params"]["optimizer"] = optimizer
        dataobject.image_processing["training_params"]["epochs"] = epochs
        dataobject.image_processing["train_test_split"]["test_size"] = test_size
        dataobject.image_processing["train_test_split"]["random_state"] = random_state

        json_data = {"dataobject": dataobject.to_dict()}

        try:
            response = requests.post('http://127.0.0.1:8000/api/imageprocessing/', json=json_data)
            if response.status_code == 200:
                response_data = response.json()
                cm_data = response_data.get("confusionMatrix")
                test_loss = response_data.get("testLoss")
                test_accuracy = response_data.get("testAccuracy")

                if cm_data:
                    self.context.managers["visualization"].plot_confusion_matrix(cm_data)
                    print("Response received successfully")
                else:
                    messagebox.showerror("Error", "Confusion Matrix data not received.")
            else:
                messagebox.showerror("Error", response.json().get('error', 'File upload failed.'))
        except Exception as e:
            messagebox.showerror("Error", str(e))
