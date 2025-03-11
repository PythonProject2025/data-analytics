import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split

class EncodeAndScaling:
    def __init__(self, data):
        """
        Initializes the EncodeAndScaling class with a dataset.
        :param data: Pandas DataFrame containing the dataset.
        """
        self.data = data  # Store dataset

    def encode_categorical_features(self):
        # One-Hot Encoding for categorical columns
        encoded_data = pd.get_dummies(self.data)

        # Convert boolean columns (True/False) into 1/0
        bool_cols = encoded_data.select_dtypes(include='bool').columns.values
        for col in bool_cols:
            encoded_data[col] = encoded_data[col].apply(int)
        return encoded_data

    def scale_numerical_features(self, encoded_data):
        # Apply MinMax Scaling
        scaler = MinMaxScaler()
        scaled_data = pd.DataFrame(scaler.fit_transform(encoded_data), columns=encoded_data.columns)
        return scaled_data
    
    def train_test_split(self, processed_data, test_size=0.2, random_state=42):
        """
        Splits the processed dataset into training and testing sets.
        :param processed_data: The encoded and scaled dataset.
        :param test_size: Proportion of dataset to use as the test set (default 20%).
        :param random_state: Random seed for reproducibility.
        :return: Training and testing datasets.
        """
        X_train, X_test ,y_train, y_test = train_test_split(processed_data, test_size=test_size, random_state=random_state)
        return X_train, X_test ,y_train, y_test
    
    def preprocess(self,data_object):
        """
        Runs encoding, scaling, and train-test splitting on the dataset.
        """
        test_size = data_object["test_size"]
        random_state = data_object["random_state"]

        encoded_data = self.encode_categorical_features()
        processed_data = self.scale_numerical_features(encoded_data)  # Explicitly define `processed_data`
            
        X_train, X_test ,y_train, y_test = self.train_test_split(processed_data, test_size, random_state)

        data = {
            "X_train": X_train,
            "X_test": X_test,
            "y_train": y_train,
            "y_test": y_test
        }
        return data 
     
