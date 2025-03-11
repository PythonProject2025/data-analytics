import gradio as gr
import requests
from data_object_final_edited import DataObject  

data_object = DataObject()
# Define API endpoints
CLASSIFICATION_API = "http://localhost:8000/api/run-classification"
REGRESSION_API = "http://localhost:8000/api/run-regression"

class AIPipelinePage:
    def __init__(self, navigate_callback=None):
        self.navigate_callback = navigate_callback

    def run_classification(self, model_name, n_estimators, max_depth):
        """Updates DataObject and calls classification API."""

        # Store user-selected parameters in DataObject
        data_object.ai_model[model_name] = {
            "n_estimators": int(n_estimators),
            "max_depth": int(max_depth)
        }

        # Send request to backend API
        response = requests.post(CLASSIFICATION_API, json=data_object.to_dict())

        if response.status_code == 200:
            results = response.json()
            return f"Model Accuracy: {results['accuracy']}\nConfusion Matrix: {results['confusion_matrix']}"
        else:
            return f"Error: {response.text}"

    def run_regression(self, model_name, n_estimators, learning_rate, max_depth):
        """Updates DataObject and calls regression API."""

        # Store user-selected parameters in DataObject
        data_object.ai_model[model_name] = {
            "n_estimators": int(n_estimators),
            "learning_rate": float(learning_rate),
            "max_depth": int(max_depth)
        }

        # Send request to backend API
        response = requests.post(REGRESSION_API, json=data_object.to_dict())

        if response.status_code == 200:
            results = response.json()
            return f"MAE: {results['mae']}\nMSE: {results['mse']}\nR² Score: {results['r2']}"
        else:
            return f"Error: {response.text}"

    def get_interface(self):
        """Creates Gradio interface for AI pipeline."""
        with gr.Blocks() as ai_pipeline_ui:
            gr.Markdown("### Select AI Model and Task")

            with gr.Tab("Classification"):
                gr.Markdown("#### Classification Model Selection")
                classification_model = gr.Dropdown(
                    ["RandomForest", "CatBoost", "ArtificialNeuralNetwork"],
                    label="Choose Model"
                )
                n_estimators = gr.Slider(50, 500, step=50, label="n_estimators")
                max_depth = gr.Slider(5, 50, step=5, label="max_depth")

                classify_btn = gr.Button("Run Classification")
                classification_output = gr.Textbox(label="Classification Results")

                classify_btn.click(
                    self.run_classification,
                    inputs=[classification_model, n_estimators, max_depth],
                    outputs=classification_output
                )

            with gr.Tab("Regression"):
                gr.Markdown("#### Regression Model Selection")
                regression_model = gr.Dropdown(
                    ["RandomForest", "CatBoost", "XGBoost"],
                    label="Choose Model"
                )
                reg_n_estimators = gr.Slider(50, 1000, step=50, label="n_estimators")
                learning_rate = gr.Slider(0.01, 0.3, step=0.01, label="Learning Rate")
                reg_max_depth = gr.Slider(3, 10, step=1, label="max_depth")

                regress_btn = gr.Button("Run Regression")
                regression_output = gr.Textbox(label="Regression Results")

                regress_btn.click(
                    self.run_regression,
                    inputs=[regression_model, reg_n_estimators, learning_rate, reg_max_depth],
                    outputs=regression_output
                )

        return ai_pipeline_ui
