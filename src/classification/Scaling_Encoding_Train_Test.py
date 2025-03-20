import pandas as pd
from sklearn.preprocessing import MinMaxScaler, LabelEncoder
from sklearn.model_selection import train_test_split

class EncodeAndScaling:
    """
    A class for encoding categorical features, scaling numerical features, 
    and splitting datasets for machine learning preprocessing.

    Attributes:
    data (pd.DataFrame): The input dataset to be processed.
    """
    def __init__(self, data):
        """
        Initializes the EncodeAndScaling class with a dataset.
        
        Parameters:
            data (pd.DataFrame): The dataset containing features and target columns.
        """

        self.data = data  # Store dataset

    def encode_categorical_features(self, data):
        """
        Encodes categorical features using One-Hot Encoding.

        Parameters:
            data (pd.DataFrame): The feature dataset containing categorical columns.

        Returns:
            pd.DataFrame: The dataset with categorical features encoded as numerical values.
        """
        print("Encoding Data starts")
        # One-Hot Encoding for categorical columns
        encoded_data = pd.get_dummies(data)
        bool_cols = encoded_data.select_dtypes(include='bool').columns
        encoded_data[bool_cols] = encoded_data[bool_cols].astype(int)
        # print("Encoded Data is processed" , encoded_data)
        return encoded_data


    def scale_numerical_features(self, data):
        """
        Scales numerical features using Min-Max Scaling.

        Parameters:
            data (pd.DataFrame): The dataset with encoded categorical features.

        Returns:
            pd.DataFrame: The dataset with numerical features scaled to a range of [0,1].
        """
        # Apply MinMax Scaling
        scaler = MinMaxScaler()

        # Select only the columns that are not strings
        numerical_columns = data.select_dtypes(include=['number']).columns
        scaled_data = data.copy()
        scaled_data[numerical_columns] = scaler.fit_transform(data[numerical_columns])

        # scaled_data = pd.DataFrame(scaler.fit_transform(encoded_data), columns=encoded_data.columns)
        return scaled_data
    
    def train_test_split(self, processed_data, target_column, test_size=0.2, random_state=42):
        """
        Splits the processed dataset into training and testing sets.
        
        Parameters:
            processed_data (pd.DataFrame): The encoded and scaled dataset.
            target_column (str): The name of the target column.
            test_size (float, optional): Proportion of dataset to use as the test set (default is 0.2).
            random_state (int, optional): Random seed for reproducibility (default is 42).

        Returns:
            tuple: 
                - X_train (pd.DataFrame): Training feature dataset.
                - X_test (pd.DataFrame): Testing feature dataset.
                - y_train (pd.Series): Training target dataset.
                - y_test (pd.Series): Testing target dataset.

        Raises:
            KeyError: If the target column is not found in the dataset.
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
        
        Parameters:
            data_object (dict): A dictionary containing preprocessing parameters:
                - "test_size" (float): The proportion of data used for testing.
                - "random_state" (int): The random state for reproducibility.
                - "target_column" (str or list): The target column name(s).

        Returns:
            dict: A dictionary containing:
                - "X_train": Processed training feature dataset.
                - "X_test": Processed testing feature dataset.
                - "y_train": Processed training target dataset.
                - "y_test": Processed testing target dataset.

        Raises:
            ValueError: If multiple target columns are provided instead of one.
            ValueError: If the target column is not found in the dataset.
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
            
        # Ensure target column exists
        if target_column not in self.data.columns:
            raise ValueError(f"Error: Target column '{target_column}' not found in dataset!")

        target_data = self.data[target_column]
        # print("Target Data is processed\n" , target_data.head())

        feature_data = self.data.drop(columns=[target_column], axis=1)

        datetime_cols = feature_data.filter(regex = r'(?i)\bdate\b|\btimestamp\b|\btime\b|\bdatum\b', axis = 1).columns

        # Drop datetime columns
        feature_data = feature_data.drop(columns=datetime_cols, axis=1)

        X_train, X_test, y_train, y_test = train_test_split(feature_data, 
                                                            target_data, 
                                                            test_size = test_size, 
                                                            random_state = random_state)

        # Encode categorical features before scaling
        X_train = self.encode_categorical_features(X_train)
        X_test = self.encode_categorical_features(X_test)
        
        # Scale numerical features
        X_train = self.scale_numerical_features(X_train)
        X_test = self.scale_numerical_features(X_test)

        # print(X_test)

        if y_train.dtype == 'object' or y_train.dtype.name == 'category':
            le = LabelEncoder()
            y_train_encoded = le.fit_transform(y_train)
            y_test_encoded = le.transform(y_test)

            y_train = pd.Series(y_train_encoded, name=target_column)
            y_test = pd.Series(y_test_encoded, name=target_column)

        # print(y_train)

        print("\n--- Dataset Size Summary ---")
        # print(f"Original dataset size: {len(processed_data)} rows")
        print(f"Train dataset size: {len(X_train)} rows ({(1 - test_size) * 100:.0f}%)")
        print(f"Test dataset size: {len(X_test)} rows ({test_size * 100:.0f}%)")

        data = {
            "X_train": X_train,
            "X_test": X_test,
            "y_train": y_train,
            "y_test": y_test
        }

        return data 