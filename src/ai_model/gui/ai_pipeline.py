import os
import sys

# Ensure the project root is in sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import necessary AI models
from models.random_forest import RandomForest
from models.catboost_model import Catboost
from models.ann import ArtificialNeuralNetwork
from models.xgboost_model import XGBoost
from models.base import BaseModel
import numpy as np
from data_object_final_edited import DataObject

# Create an instance of DataObject
data_instance = DataObject()

def extract_hyperparameters(model_name):
    """Extracts user-selected hyperparameters while ensuring valid defaults from ai_model."""
    params = data_instance.ai_model.get(model_name, {})

    if not params:
        print(f"Warning: No parameters found for {model_name}, using defaults.")
        return BaseModel.HYPERPARAMETER_RANGES.get(model_name, {})

    validated_params = {
        key: (value if isinstance(value, (int, float, str, list)) else value.get("default", None)) 
        for key, value in params.items()
    }
    
    print(f"Extracted Hyperparameters for {model_name}: {validated_params}")  
    return validated_params

def run_selected_model(data_instance):
    """Runs only the selected AI model based on user input."""
    
    # Get the selected model from DataObject
    selected_model = data_instance.ai_model.get("selected_model", None)
    
    if not selected_model:
        return {"error": "No model selected! Please select a model to run."}
    
    # Extract hyperparameters
    model_params = extract_hyperparameters(selected_model)

    # Extract dataset & Convert to NumPy arrays
    try:
        X_train = np.array(data_instance.data_filtering["Train-Test Split"]["split_data"]["x_train"])
        X_test = np.array(data_instance.data_filtering["Train-Test Split"]["split_data"]["x_test"])
        y_train = np.array(data_instance.data_filtering["Train-Test Split"]["split_data"]["y_train"])
        y_test = np.array(data_instance.data_filtering["Train-Test Split"]["split_data"]["y_test"])
    except KeyError:
        return {"error": "Missing training/testing data in DataObject!"}

    if X_train.size == 0 or X_test.size == 0 or y_train.size == 0 or y_test.size == 0:
        return {"error": "Training or testing data arrays are empty!"}

    print(f"Debugging Data Before Training:")
    print(f"X_train Shape: {X_train.shape}, y_train Shape: {y_train.shape}")

    # Initialize only the selected model
    model=None
    if selected_model == "RandomForest":
        model = RandomForest(problem_type="classification", options=model_params)
    elif selected_model == "CatBoost":
        model = Catboost(problem_type="classification", options=model_params)
    elif selected_model == "ArtificialNeuralNetwork":
        model = ArtificialNeuralNetwork(problem_type="classification", options=model_params)
    elif selected_model == "XGBoost":
        model = XGBoost(problem_type="regression", options=model_params)
    else:
        return {"error": f"Selected model '{selected_model}' is not recognized!"}

    # Assign Data
    model.X_train, model.X_test, model.y_train, model.y_test = X_train, X_test, y_train, y_test

    # Train the model
    model.train()

    # Evaluate the model
    results = model.evaluate()
    
    if results is None:
        print(f"Warning: Model {selected_model} returned None during evaluation.")
        return {"error": f"Model {selected_model} failed during evaluation."}

    # Store results in DataObject under respective category
    if selected_model in ["RandomForest", "CatBoost", "ArtificialNeuralNetwork"]:  # Classification models
        data_instance.outputs["AI_Classification"][selected_model] = {
            "Accuracy": results.get("Accuracy", 0.0),
            "Confusion Matrix": results.get("Confusion Matrix", [])
        }
        return {
            "message": f"Classification completed for {selected_model}",
            "results": data_instance.outputs["AI_Classification"][selected_model]
        }
    
    elif selected_model == "XGBoost":  # Regression model
        data_instance.outputs["AI_Regression"][selected_model] = {
            "MAE": results.get("MAE", 0.0),
            "MSE": results.get("MSE", 0.0),
            "R2": results.get("R2", 0.0)
        }
        return {
            "message": f"Regression completed for {selected_model}",
            "results": data_instance.outputs["AI_Regression"][selected_model]
        }
