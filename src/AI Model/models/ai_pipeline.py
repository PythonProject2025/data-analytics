# Import necessary AI models
from models.random_forest import RandomForest
from models.catboost_model import Catboost
from models.ann import ArtificialNeuralNetwork
from models.xgboost_model import XGBoost
import numpy as np
from data_object_final_edited import DataObject
import numpy as np
# Create an instance of DataObject
data_instance = DataObject()

def extract_hyperparameters(model_name):
    """Extracts user-selected hyperparameters while ensuring valid defaults from ai_model."""
    params = data_instance.ai_model.get(model_name, {})

    # Ensure params is always a dictionary and not empty
    if not params:
        print(f"Warning: No parameters found for {model_name}, using defaults.")
        return BaseModel.HYPERPARAMETER_RANGES.get(model_name, {})

    # Extract user-set values or fallback to defaults
    validated_params = {
        key: (value if isinstance(value, (int, float, str, list)) else value.get("default", None)) 
        for key, value in params.items()
    }
    
    print(f"Extracted Hyperparameters for {model_name}: {validated_params}")  # Debugging print
    return validated_params

def run_ai_classification():
    """Executes AI classification using selected models and user-defined hyperparameters."""
    
    # Extract training/testing data and Convert to numpy arrays
    X_train = data_instance.data_filtering["Train-Test Split"]["split_data"]["x_train"]
    X_test = data_instance.data_filtering["Train-Test Split"]["split_data"]["x_test"]
    y_train = data_instance.data_filtering["Train-Test Split"]["split_data"]["y_train"]
    y_test = data_instance.data_filtering["Train-Test Split"]["split_data"]["y_test"]

    # Check if any are `None` BEFORE conversion
    if X_train is None or X_test is None or y_train is None or y_test is None:
        return {"error": "🚨 Missing training or testing data in DataObject."}

    # Convert to NumPy arrays (only if they are not None)
    X_train, X_test, y_train, y_test = map(np.array, (X_train, X_test, y_train, y_test))

    # Check if any arrays are EMPTY
    if X_train.size == 0 or X_test.size == 0 or y_train.size == 0 or y_test.size == 0:
        return {"error": "🚨 Training or testing data arrays are empty!"}

    # Debugging: Confirm Data Types
    print(f" Debugging Data Before Training:")
    print(f" X_train Type: {type(X_train)}, Shape: {X_train.shape}")
    print(f" y_train Type: {type(y_train)}, Shape: {y_train.shape}")

    # Iterate through all AI classification models
    for model_name in data_instance.ai_model.keys():
        model_params = extract_hyperparameters(model_name)  # Extract hyperparameters

        # Initialize the selected model
        if model_name == "RandomForest":
            model = RandomForest(problem_type="classification", options=model_params)
        elif model_name == "CatBoost":
            model = Catboost(problem_type="classification", options=model_params)
        elif model_name == "ArtificialNeuralNetwork":
            model = ArtificialNeuralNetwork(problem_type="classification", options=model_params)
        else:
            continue  # Skip models not meant for classification

        # Assign Converted Data (NumPy Arrays)
        model.X_train, model.X_test, model.y_train, model.y_test = X_train, X_test, y_train, y_test

        # Train the model
        model.train()

        # Evaluate the model
        results = model.evaluate()
        
        if results is None:
            print(f"⚠ Warning: Model {model_name} returned None during evaluation.")
            continue  # Avoid crashing if evaluation fails

        # Store results in DataObject
        data_instance.outputs["AI_Classification"][model_name] = {
            "Accuracy": results.get("Accuracy", 0.0),
            "Confusion Matrix": results.get("Confusion Matrix", [])
        }

    return {"message": "🚀 AI Classification completed", "results": data_instance.outputs["AI_Classification"]}


def run_ai_regression():
    """Executes AI regression using selected models and user-defined hyperparameters."""

    # Extract processed training/testing data from data_filtering
    X_train = data_instance.data_filtering["Train-Test Split"]["split_data"]["x_train"]
    X_test = data_instance.data_filtering["Train-Test Split"]["split_data"]["x_test"]
    y_train = data_instance.data_filtering["Train-Test Split"]["split_data"]["y_train"]
    y_test = data_instance.data_filtering["Train-Test Split"]["split_data"]["y_test"]

    # Validate that the data is available
    if None in (X_train, X_test, y_train, y_test):
        return {"error": "Missing training or testing data in DataObject."}

    # Iterate through all AI regression models in DataObject
    for model_name in data_instance.ai_model.keys():
        model_params = extract_hyperparameters(model_name)  # ✅ Fix: Extract actual values

        # Initialize the selected model
        if model_name == "RandomForest":
            model = RandomForest(problem_type="regression", options=model_params)
        elif model_name == "CatBoost":
            model = Catboost(problem_type="regression", options=model_params)
        elif model_name == "XGBoost":
            model = XGBoost(problem_type="regression", options=model_params)
        else:
            continue  # Skip models not meant for regression

        # Train the model
        model.X_train, model.X_test, model.y_train, model.y_test = X_train, X_test, y_train, y_test
        model.train()

        # Evaluate the model
        results = model.evaluate()

        # Store results in DataObject under AI_Regression
        data_instance.outputs["AI_Regression"][model_name] = {
            "MAE": results.get("MAE", 0.0),
            "MSE": results.get("MSE", 0.0),
            "R2": results.get("R2", 0.0)
        }

    return {"message": "AI Regression completed", "results": data_instance.outputs["AI_Regression"]}
