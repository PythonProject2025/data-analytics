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
        if not data_dict:
            return Response({"error": "Invalid request, 'dataobject' missing"}, status=status.HTTP_400_BAD_REQUEST)
        
        data_object = DataObject()
        data_object.classification = data_dict.get("classification", {})
        data_object.data_filtering = data_dict.get("data_filtering", {})
        try:
            split_data = data_object.data_filtering["Train-Test Split"]["split_data"]

            if not all(k in split_data for k in ["X_train", "X_test", "y_train", "y_test"]):
                return {"error": "Missing one or more training/testing data in DataObject!"}
            
            X_train_list = data_object.data_filtering["Train-Test Split"]["split_data"]["X_train"]
            X_test_list = data_object.data_filtering["Train-Test Split"]["split_data"]["X_test"]
            y_train_list = data_object.data_filtering["Train-Test Split"]["split_data"]["y_train"]
            y_test_list = data_object.data_filtering["Train-Test Split"]["split_data"]["y_test"]
  
            data_train = pd.DataFrame(X_train_list)
            data_test=  pd.DataFrame(X_test_list)
            target_train= pd.DataFrame(y_train_list)
            target_test= pd.DataFrame(y_test_list)
        except KeyError:
            return {"error": "Missing training/testing data in DataObject!"}

        if data_train.size == 0 or data_test.size == 0 or target_train.size == 0 or target_test.size == 0:
            return {"error": "Training or testing data arrays are empty!"}
        # Prompt user to select a model
        selected_model = data_object.classification["Model_Selection"]

        # Create and use the selected model
        try:
            if selected_model == "RandomForest":
                n_estimators=data_object.classification["RandomForest"]["n_estimators"]
                max_depth=data_object.classification["RandomForest"]["max_depth"]
                model = RandomForestModel(data_train, data_test, target_train, target_test,n_estimators,max_depth)
            elif selected_model == "SVC":
                C= data_object.classification["SVC"]["C"]
                model = SVCModel(data_train, data_test, target_train, target_test,C)
            elif selected_model == "KNN":
                n_neighbours=data_object.classification["KNN"]["n_neighbours"]
                p=data_object.classification["KNN"]["p"]
                model = KNNModel(data_train, data_test, target_train, target_test,n_neighbours,p)
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
            
