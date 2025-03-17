import numpy as np
import pandas as pd
from rest_framework.views import APIView
from rest_framework.response import Response
from classification.knn_model import KNNModel
from classification.random_forest_model import RandomForestModel
from classification.svc_model import SVCModel
from models.data_object_class import DataObject
from rest_framework import status

class ClassificationAPIView (APIView):
    
    def post(self, request):
        
        data_dict = request.data.get("dataobject", {})
        if "dataobject" in data_dict:  
            data_dict = data_dict["dataobject"]

        if not data_dict:
            return Response({"error": "Invalid request, 'dataobject' missing"}, status=status.HTTP_400_BAD_REQUEST)
        
        data_object = DataObject()
        data_object.classification = data_dict.get("classification", {})
        data_object.data_filtering = data_dict.get("data_filtering", {})
        try:
            split_data = data_object.data_filtering["Train-Test Split"]["split_data"]

            # ✅ Ensure all keys exist before conversion
            if not all(k in split_data for k in ["X_train", "X_test", "y_train", "y_test"]):
                return {"error": "Missing one or more training/testing data in DataObject!"}

            # ✅ Convert lists (from JSON) back to NumPy arrays
            data_train = np.array([list(d.values()) for d in split_data["X_train"]]) if split_data["X_train"] else None
            data_test = np.array([list(d.values()) for d in split_data["X_test"]]) if split_data["X_test"] else None
            target_train = np.array(split_data["y_train"]) if split_data["y_train"] else None
            target_test = np.array(split_data["y_test"]) if split_data["y_test"] else None

            # ✅ Check if data is valid before proceeding
            if any(val is None or (isinstance(val, np.ndarray) and val.size == 0) for val in [data_train, data_test, target_train, target_test]):
                return {"error": "Some train-test data is empty or invalid!"}
            print(data_train)
        except KeyError:
            return {"error": "Missing training/testing data in DataObject!"}

        if data_train.size == 0 or data_test.size == 0 or target_train.size == 0 or target_test.size == 0:
            return {"error": "Training or testing data arrays are empty!"}
        # Prompt user to select a model
        print("Available models: RandomForest, SVC, KNN")
        #selected_model = input("Enter the name of the model you want to use: ")
        selected_model = data_object.classification["Model_Selection"]

        # Create and use the selected model
        try:
            if selected_model == "RandomForest":
                model = RandomForestModel(data_train, data_test, target_train, target_test)
            elif selected_model == "SVC":
                model = SVCModel(data_train, data_test, target_train, target_test)
            elif selected_model == "KNN":
                model = KNNModel(data_train, data_test, target_train, target_test)
            else:
                raise ValueError("Invalid model name entered.")

            # Train and evaluate the model
            model.train()
            accuracy, report, cm, mse = model.evaluate(model.model)
            response_data = {
            "accuracy": accuracy,
            "cm": cm,
            "mse": mse
            }
            return Response(response_data, status=status.HTTP_200_OK)
            # model.display_confusion_matrix(cm)

        except ValueError as e:
            print(e)
