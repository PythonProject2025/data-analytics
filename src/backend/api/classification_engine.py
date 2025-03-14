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
        # ask pratheek about the dataobject data_train
        data_object.classification = data_dict.get("classification", {})
        data_train = data_object.classification["Inputs"]["data_train"]
        data_test = data_object.classification["Inputs"]["data_test"]
        target_train = data_object.classification["Inputs"]["target_train"]
        target_test = data_object.classification["Inputs"]["target_test"]
        target_labels = data_object.classification["Inputs"]["target_labels"]
        
        # Prompt user to select a model
        print("Available models: RandomForest, SVC, KNN")
        #selected_model = input("Enter the name of the model you want to use: ")
        selected_model = data_object.classification["Model_Selection"]

        # Create and use the selected model
        try:
            if selected_model == "RandomForest":
                model = RandomForestModel(data_train, data_test, target_train, target_test, target_labels)
            elif selected_model == "SVC":
                model = SVCModel(data_train, data_test, target_train, target_test, target_labels)
            elif selected_model == "KNN":
                model = KNNModel(data_train, data_test, target_train, target_test, target_labels)
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
