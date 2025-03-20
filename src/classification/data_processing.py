import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler

def preprocess_data(data_object):
    """
    Preprocesses the train-test split data from DataObject by encoding categorical features and scaling numerical features.
    
    Parameters:
    data_object (DataObject): The DataObject containing train-test split data.
    
    Returns:
    dict: Dictionary containing preprocessed train-test split data and target labels.
    """
    if not data_object or not hasattr(data_object, 'data_filtering'):
        raise ValueError("Invalid DataObject provided")
    
    # Extract train-test split data
    X_train = data_object.data_filtering['Train-Test Split']['split_data']['X_train']
    X_test = data_object.data_filtering['Train-Test Split']['split_data']['X_test']
    y_train = data_object.data_filtering['Train-Test Split']['split_data']['y_train']
    y_test = data_object.data_filtering['Train-Test Split']['split_data']['y_test']
    
    if X_train is None or X_test is None or y_train is None or y_test is None:
        raise ValueError("Train-test split data is missing in DataObject")
    
    # Convert to DataFrames if needed
    X_train = pd.DataFrame(X_train)
    X_test = pd.DataFrame(X_test)
    y_train = pd.Series(y_train)
    y_test = pd.Series(y_test)
    
    # Encode categorical features
    label_encoders = {}
    for col in X_train.columns:
        if X_train[col].dtype == 'object':  # Only encode categorical columns
            label_encoders[col] = LabelEncoder()
            X_train[col] = label_encoders[col].fit_transform(X_train[col])
            X_test[col] = label_encoders[col].transform(X_test[col])
    
    # Scale numerical features
    scaler = StandardScaler()
    X_train = pd.DataFrame(scaler.fit_transform(X_train), columns=X_train.columns)
    X_test = pd.DataFrame(scaler.transform(X_test), columns=X_test.columns)
    
    return {
        "X_train": X_train,
        "X_test": X_test,
        "y_train": y_train,
        "y_test": y_test
    }
