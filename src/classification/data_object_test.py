from data_filtering.Scaling_Encoding_Train_Test import EncodeAndScaling
from models.data_object_class import DataObject
import pandas as pd

def run_encoding_scaling_train_test_split(data, data_object):
    """
    Runs encoding, scaling, and train-test splitting on the dataset after smoothing.
    
    :param smoothed_data: The dataset after smoothing.
    :return: Dictionary containing train-test split and details.
    """
    # Initialize the Encoder & Scaler
    processor = EncodeAndScaling(data)
    data= processor.preprocess(data_object["parameters"]) 

    return data
 

data_object = DataObject()  

data_object.data_filtering["Train-Test Split"]["parameters"]["test_size"] = 0.2
data_object.data_filtering["Train-Test Split"]["parameters"]["random_state"] = 42

# Retrieve dataset from DataObject's raw_data
data_object.raw_data = pd.read_csv("data/cars.csv")  # Stores uploaded file data

dataset = data_object.raw_data
data_object.data_filtering["Train-Test Split"]["parameters"]["target_column"] = "values"

# classification_data = load_classification_data(dataset, data_object.data_filtering['Train-Test Split'])
# regression_data = load_regression_data(regression_path)
# classification_data=run_encoding_scaling_train_test_split(dataset, data_object.data_filtering['Train-Test Split'])
data_object.data_filtering["Train-Test Split"]["split_data"] = run_encoding_scaling_train_test_split(dataset ,
                                                                                                         data_object.data_filtering["Train-Test Split"])
print(data_object.data_filtering["Train-Test Split"]["split_data"])