# File: main.py
from data_processing import preprocess_data
from random_forest_model import RandomForestModel
from svc_model import SVCModel
from knn_model import KNNModel
from Data_object import DataObject
import data_object_test
import pandas as pd

def main():
    # Load dataset from CSV file
    #filepath = r"E:\TH_koeln_AIT\Courses\Oop\Project\ml_project_final\classification\data\cars.csv"
    #dataset = pd.read_csv(filepath)  # Ensure dataset is a DataFrame

    # Preprocess the dataset (encoding, scaling, train-test split)
    #split_data = preprocess_data(dataset)

    # Extract dataset from preprocessed dictionary
    """
    data_train = split_data["data_train"]
    data_test = split_data["data_test"]
    target_train = split_data["target_train"]
    target_test = split_data["target_test"]
    target_labels = split_data["target_labels"]
    """
 
    """
    # Extract dataset from DataObject
    data_train = DataObject.classification["Inputs"]["data_train"]
    data_test = DataObject.classification["Inputs"]["data_test"]
    target_train = DataObject.classification["Inputs"]["target_train"]
    target_test = DataObject.classification["Inputs"]["target_test"]
    target_labels = DataObject.classification["Inputs"]["target_labels"]
    """
    data_train = data_object_test.data_object.data_filtering["Train-Test Split"]["split_data"]["X_train"]
    data_test = data_object_test.data_object.data_filtering["Train-Test Split"]["split_data"]["X_test"]
    target_train = data_object_test.data_object.data_filtering["Train-Test Split"]["split_data"]["y_train"]
    target_test = data_object_test.data_object.data_filtering["Train-Test Split"]["split_data"]["y_test"]
    #target_labels = data_object_test.data_object.data_filtering["Train-Test Split"]["split_data"]["y_labels"]

    # Prompt user to select a model
    print("Available models: RandomForest, SVC, KNN")
    selected_model = input("Enter the name of the model you want to use: ")

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
        #model.display_confusion_matrix(cm)

    except ValueError as e:
        print(e)

if __name__ == "__main__":
    main()
