import pandas as pd # Importing pandas for data manipulation
from imblearn.over_sampling import SMOTE # Importing SMOTE for handling class imbalance

def load_classification_data(filepath):
    """
    Loads and preprocesses the classification dataset.

    Parameters:
    filepath : str
        Path to the dataset.

    Returns:
    pd.DataFrame
        Preprocessed dataset with categorical encoding and SMOTE applied.
    """
    try:
        # Defining column names for the dataset
        column_names = ["buying", "maint", "doors", "persons", "lug_boot", "safety", "car"]
        
        # Loading the dataset into a Pandas DataFrame
        data = pd.read_csv(filepath, names=column_names, header=None)
        
        if data.empty:
            raise ValueError("Error: The classification dataset is empty.")
        
        # Encode categorical features using factorize() to convert categorical values to numeric
        for column in data.columns:
            data[column] = pd.factorize(data[column])[0]
            
        # Separating features (X) and target variable (y)
        X = data.drop(columns=["car"], errors="ignore")  # Features
        y = data["car"]  # Target variable
        
        if X.empty or y.empty:
            raise ValueError("Error: Features or target column is missing in classification dataset.")
        
        # Applying SMOTE (Synthetic Minority Over-sampling Technique) for class balancing
        sm = SMOTE(random_state=42)
        
        # Generating synthetic samples for the minority class
        X_res, y_res = sm.fit_resample(X, y)
        
        # Combining the resampled features and target into a new DataFrame
        data = pd.concat(
            [pd.DataFrame(X_res, columns=X.columns), pd.DataFrame(y_res, columns=["car"])],
            axis=1
        )
        return data  # Return the processed dataset
    
    except FileNotFoundError:
        print(f"Error: The file '{filepath}' was not found.")
        return None
    except ValueError as ve:
        print(ve)
        return None
    except Exception as e:
        print(f"Unexpected error while loading classification data: {e}")
        return None

def load_regression_data(filepath):
    """
    Loads and preprocesses the regression dataset.

    Parameters:
    filepath : str
        Path to the dataset.

    Returns:
    pd.DataFrame
        Preprocessed dataset with categorical encoding applied.
    """
    try:
        # Loading the dataset
        data = pd.read_csv(filepath)

        if data.empty:
            raise ValueError("Error: The regression dataset is empty.")

        # Dropping irrelevant or non-numeric columns (e.g., "date" column if present)
        data = data.drop(columns=["date"], errors="ignore")

        # Defining categorical columns that need to be encoded
        categorical_columns = ["WeekStatus", "Day_of_week", "Load_Type"]

        # Encoding categorical columns using factorize() to convert them into numerical values
        for column in categorical_columns:
            if column in data.columns:  # Checking if the column exists in the dataset
                data[column] = pd.factorize(data[column])[0]

        return data  # Return the processed dataset

    except FileNotFoundError:
        print(f"Error: The file '{filepath}' was not found.")
        return None
    except ValueError as ve:
        print(ve)
        return None
    except Exception as e:
        print(f"Unexpected error while loading regression data: {e}")
        return None
