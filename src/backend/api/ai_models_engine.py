import sys
import os
import numpy as np
import pandas as pd
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
        data_object = DataObject()
        data_object.data_filtering = data_dict.get("data_filtering", {})
        data_object.ai_model = data_dict.get("ai_model", {})

        response_data = self.run_selected_model(data_object)
        return Response(response_data, status=status.HTTP_200_OK)


    def extract_hyperparameters(self, data_object, model_name):
        """Extracts user-selected hyperparameters while ensuring valid defaults from ai_model."""
        params = data_object.data_filtering["Outlier Detection"]

        if not params:
            return BaseModel.HYPERPARAMETER_RANGES.get(model_name, {})

        validated_params = {
            key: (value if isinstance(value, (int, float, str, list)) else value.get("default", None)) 
            for key, value in params.items()
        }
        
        return validated_params

    def run_selected_model(self, data_object):
        """Runs only the selected AI model based on user input."""
        
        selected_model = data_object.ai_model.get("Selected Model")
        problem_type = data_object.ai_model.get("problem_type")

        
        if not selected_model:
            return {"error": "No model selected! Please select a model to run."}
        
        # Extract hyperparameters
        model_params = self.extract_hyperparameters(data_object, selected_model)
        try:
            split_data = data_object.data_filtering["Train-Test Split"]["split_data"]
            if not all(k in split_data for k in ["X_train", "X_test", "y_train", "y_test"]):
                return {"error": "Missing one or more training/testing data in DataObject!"}
            X_train = pd.DataFrame(split_data["X_train"]).values if split_data["X_train"] else None
            X_test = pd.DataFrame(split_data["X_test"]).values if split_data["X_test"] else None
            y_train = np.array(split_data["y_train"]) if split_data["y_train"] else None
            y_test = np.array(split_data["y_test"]) if split_data["y_test"] else None
            
            if any(val is None or (isinstance(val, np.ndarray) and val.size == 0)
                   for val in [X_train, X_test, y_train, y_test]):
                return {"error": "Some train-test data is empty or invalid!"}
        except KeyError:
            return {"error": "Missing training/testing data in DataObject!"}

        if X_train.size == 0 or X_test.size == 0 or y_train.size == 0 or y_test.size == 0:
            return {"error": "Training or testing data arrays are empty!"}

        model = None
        if selected_model == "RandomForest":
            model = RandomForest(problem_type=problem_type, options=data_object.ai_model["RandomForest"])
        elif selected_model == "CatBoost":
            model = Catboost(problem_type=problem_type, options=data_object.ai_model["CatBoost"])
        elif selected_model == "ArtificialNeuralNetwork":
            model = ArtificialNeuralNetwork(problem_type=problem_type, options=data_object.ai_model["ArtificialNeuralNetwork"])
        elif selected_model == "XGBoost":
            model = XGBoost(problem_type=problem_type, options=data_object.ai_model["XGBoost"])
        else:
            return {"error": f"Selected model '{selected_model}' is not recognized!"}

        model.train(X_train, y_train)

        # Evaluate the model
        results = model.evaluate(X_test, y_test)
        
        if results is None:
            return {"error": f"Model {selected_model} failed during evaluation."}   
        
        if problem_type == "classification":
            data_object.outputs["AI_Classification"][selected_model] = {
                "Accuracy": results.get("Accuracy", 0.0),
                "Confusion Matrix": results.get("Confusion Matrix", [])
            }

            response_data = {
                "Accuracy": data_object.outputs["AI_Classification"][selected_model]["Accuracy"],
                "Confusion Matrix": data_object.outputs["AI_Classification"][selected_model]["Confusion Matrix"]
            }

        elif problem_type == "regression":
            data_object.outputs["AI_Regression"][selected_model] = {
                "MAE": results.get("MAE", 0.0),
                "MSE": results.get("MSE", 0.0),
                "R2": results.get("R2", 0.0),
                "y_pred": model.predictions.tolist(),
                "y_test": y_test.tolist()
            }
        
            response_data = {
                "MAE": data_object.outputs["AI_Regression"][selected_model]["MAE"],
                "MSE": data_object.outputs["AI_Regression"][selected_model]["MSE"],
                "R2": data_object.outputs["AI_Regression"][selected_model]["R2"],
                "y_pred": data_object.outputs["AI_Regression"][selected_model]["y_pred"],
                "y_test": data_object.outputs["AI_Regression"][selected_model]["y_test"],
                "x_label": "Actual",     # Or get from user if available
                "y_label": "Predicted"
            }
        return response_data
