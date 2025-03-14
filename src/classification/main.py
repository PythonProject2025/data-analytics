# File: main.py
from requests import Response
from data_processing import load_and_preprocess_data
from random_forest_model import RandomForestModel
from svc_model import SVCModel
from knn_model import KNNModel
from data_object_final import data_object
from rest_framework import status

def main():
    # Load and preprocess data
    # filepath = r"E:\TH_koeln_AIT\Courses\Oop\Project\ml_project_final\classification\data\car.data"
    #data_train, data_test, target_train, target_test, target_labels = load_and_preprocess_data(filepath)
    
    # Extract dataset from DataObject
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
        data_object.outputs["Classification"][model] = {
            "accuracy": accuracy,
            "mse": mse,
            "cm": cm.tolist()  # Convert to list for JSON serialization
        }
        response_data = {
            "testLoss": dataObj.outputs["Image_Processing"]["testLoss"],
            "testAccuracy": dataObj.outputs["Image_Processing"]["testAccuracy"],
            "confusionMatrix": dataObj.outputs["Image_Processing"]["confusionMatrix"]
        }

        return Response(response_data, status=status.HTTP_200_OK)
        # model.display_confusion_matrix(cm)

    except ValueError as e:
        print(e)

if __name__ == "__main__":
    main()

