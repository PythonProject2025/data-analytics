import sys
import os
import numpy as np
from rest_framework.response import Response
from rest_framework.views import APIView
# Now you can import from models
from ai_model.models.ann import ArtificialNeuralNetwork
from ai_model.models.base import BaseModel
from ai_model.models.catboost_model import Catboost
from ai_model.models.xgboost_model import XGBoost
from models.data_object_class import DataObject
from ai_model.models.random_forest import RandomForest
from rest_framework import status

class  AIModelAPIView (APIView):
    def post(self, request):
        data_dict = request.data.get("dataobject", {})
        if "dataobject" in data_dict:  
            data_dict = data_dict["dataobject"]
        # Create an instance of DataObject
        data_object = DataObject()
        data_object.data_filtering = data_dict.get("data_filtering", {})
        data_object.ai_model = data_dict.get("ai_model", {})

        # Run selected model
        response_data = self.run_selected_model(data_object)
        print("Response Data:", response_data)
        return Response(response_data, status=status.HTTP_200_OK)


    def extract_hyperparameters(self, data_object, model_name):
        """Extracts user-selected hyperparameters while ensuring valid defaults from ai_model."""
        params = data_object.data_filtering["Outlier Detection"]

        if not params:
            print(f"Warning: No parameters found for {model_name}, using defaults.")
            return BaseModel.HYPERPARAMETER_RANGES.get(model_name, {})

        validated_params = {
            key: (value if isinstance(value, (int, float, str, list)) else value.get("default", None)) 
            for key, value in params.items()
        }
        
        print(f"Extracted Hyperparameters for {model_name}: {validated_params}")  
        return validated_params

    def run_selected_model(self, data_object):
        """Runs only the selected AI model based on user input."""
        
        # Get the selected model from DataObject
        selected_model = data_object.ai_model["Selected Model"]
        
        if not selected_model:
            return {"error": "No model selected! Please select a model to run."}
        
        # Extract hyperparameters
        model_params = self.extract_hyperparameters(data_object, selected_model)
        print(model_params)
        try:
            split_data = data_object.data_filtering["Train-Test Split"]["split_data"]

            # ✅ Ensure all keys exist before conversion
            if not all(k in split_data for k in ["X_train", "X_test", "y_train", "y_test"]):
                return {"error": "Missing one or more training/testing data in DataObject!"}

            # ✅ Convert lists (from JSON) back to NumPy arrays
            X_train = np.array([list(d.values()) for d in split_data["X_train"]]) if split_data["X_train"] else None
            X_test = np.array([list(d.values()) for d in split_data["X_test"]]) if split_data["X_test"] else None
            y_train = np.array(split_data["y_train"]) if split_data["y_train"] else None
            y_test = np.array(split_data["y_test"]) if split_data["y_test"] else None

            # ✅ Check if data is valid before proceeding
            if any(val is None or (isinstance(val, np.ndarray) and val.size == 0) for val in [X_train, X_test, y_train, y_test]):
                return {"error": "Some train-test data is empty or invalid!"}
            print(X_train)
        except KeyError:
            return {"error": "Missing training/testing data in DataObject!"}

        if X_train.size == 0 or X_test.size == 0 or y_train.size == 0 or y_test.size == 0:
            return {"error": "Training or testing data arrays are empty!"}

        print(f"Debugging Data Before Training:")
        print(f"X_train Shape: {X_train.shape}, y_train Shape: {y_train.shape}")
        print(data_object.ai_model["RandomForest"]["n_estimators"])
        # Initialize only the selected model
        model=None
        if selected_model == "Random Forest":
            model = RandomForest(problem_type="classification", options=data_object.ai_model["RandomForest"])
        elif selected_model == "CatBoost":
            model = Catboost(problem_type="classification", options=data_object.ai_model["CatBoost"])
        elif selected_model == "ANN":
            model = ArtificialNeuralNetwork(problem_type="classification", options=data_object.ai_model["ANN"])
        elif selected_model == "XGBoost":
            model = XGBoost(problem_type="regression", options=data_object.ai_model["XGBoost"])
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
            data_object.outputs["AI_Classification"][selected_model] = {
                "Accuracy": results.get("Accuracy", 0.0),
                "Confusion Matrix": results.get("Confusion Matrix", [])
            }
            return {
                "message": f"Classification completed for {selected_model}",
                "results": data_object.outputs["AI_Classification"][selected_model]
            }
        
        elif selected_model == "XGBoost":  # Regression model
            data_object.outputs["AI_Regression"][selected_model] = {
                "MAE": results.get("MAE", 0.0),
                "MSE": results.get("MSE", 0.0),
                "R2": results.get("R2", 0.0)
            }
        print("ai working successfully")
        response_data = {
            "MAE": data_object.outputs["AI_Regression"][selected_model]["MAE"],
            "MSE": data_object.outputs["AI_Regression"][selected_model]["MSE"],
            "R2": data_object.outputs["AI_Regression"][selected_model]["R2"]
        }
        print(response_data)
        return response_data

    