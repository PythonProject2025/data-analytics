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

    def encode_categorical_features(self, feature_data):
        print("Encoding Data starts")
        # One-Hot Encoding for categorical columns
        encoded_data = pd.get_dummies(feature_data)
        bool_cols = encoded_data.select_dtypes(include='bool').columns
        encoded_data[bool_cols] = encoded_data[bool_cols].astype(int)
        print("Encoded Data is processed" , encoded_data)
        return encoded_data


    def scale_numerical_features(self, encoded_data):
        # Apply MinMax Scaling
        scaler = MinMaxScaler()
        scaled_data = pd.DataFrame(scaler.fit_transform(encoded_data), columns=encoded_data.columns)
        return scaled_data
    
    def train_test_split(self, processed_data, target_column, test_size, random_state):
        """
        Splits the processed dataset into training and testing sets.
        :param processed_data: The encoded and scaled dataset.
        :param test_size: Proportion of dataset to use as the test set (default 20%).
        :param random_state: Random seed for reproducibility.
        :return: Training and testing datasets.
        """
        # Debugging print statements
        print("Columns in processed_data before splitting:", processed_data.columns.tolist())
        print("Target column before splitting:", target_column)

        # Ensure target_column exists
        if target_column not in processed_data.columns:
            raise KeyError(f"Target column '{target_column}' not found in processed_data.columns!")

        # Separate the dataset into features and target variable
        X = processed_data.drop(columns=[target_column], axis=1)
        y = processed_data[target_column]

        print("X is processed" , X)
        print("y is processed" ,y)

        X_train, X_test ,y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
        #Print dataset sizes
        print("\n--- Dataset Size Summary ---")
        print(f"Original dataset size: {len(processed_data)} rows")
        print(f"Train dataset size: {len(X_train)} rows ({(1 - test_size) * 100:.0f}%)")
        print(f"Test dataset size: {len(X_test)} rows ({test_size * 100:.0f}%)")
    
        return X_train, X_test ,y_train, y_test
    
    def preprocess(self,data_object):
        """
        Runs encoding, scaling, and train-test splitting on the dataset.
        """
        test_size = data_object["test_size"]
        random_state = data_object["random_state"]
        target_column = data_object["target_column"]

        # Ensure target_column is a string, not a list
        if isinstance(target_column, list):
            if len(target_column) == 1:
                target_column = target_column[0]  # Convert list with one item to a string
            else:
                raise ValueError(f"Expected a single target column, but got multiple: {target_column}")

        # Debugging: Check the target column type
        print("Target column (after conversion):", target_column, type(target_column))


        # Debugging prints
        
        print("Target column:", target_column)
        print("Data Columns:", self.data.columns)
        print("Checking if target column exists:", target_column in self.data.columns)
        print("\nDEBUGGING INFO:")
        print("Type of target_column:", type(target_column))
        print("Value of target_column:", target_column)
        

        # Ensure target column exists
        if target_column not in self.data.columns:
            raise ValueError(f"Error: Target column '{target_column}' not found in dataset!")

        # Separate the dataset into features and target variable
        target_data = self.data[target_column]
        print("Target Data is processed" , target_data)
        feature_data = self.data.drop(target_column, axis=1)
        print("Feature Data is processed" , feature_data)

        encoded_data = self.encode_categorical_features(feature_data) # Explicitly define encoded_data
        print("Encoded Data is processed" , encoded_data)
        scaled_data = self.scale_numerical_features(encoded_data)
        print("Scaled Data is processed" , scaled_data)
        # print("scaled_data type:", type(scaled_data))
        # print("scaled_data shape:", scaled_data.shape)
        # print("target_data type:", type(target_data))
        # print("target_data shape:", target_data.shape)
        # print("target_data name:", target_data.name)

        processed_data = pd.concat([scaled_data, target_data.to_frame()], axis=1) # Explicitly define `processed_data`
        print("Processed Data is processed" , processed_data)
            
        X_train, X_test ,y_train, y_test = self.train_test_split(processed_data, target_column, test_size, random_state)

        data = {
            "X_train": X_train,
            "X_test": X_test,
            "y_train": y_train,
            "y_test": y_test
        }
        return data 
     