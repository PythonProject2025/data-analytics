import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest

class OutlierDetection:
    def __init__(self, data):
        """
        Initializes the OutlierDetection class with a dataset.
        :param data: Pandas DataFrame containing the dataset.
        """
        self.data = data  # Dataset
        self.numeric_columns = self.data.select_dtypes(include=["number"]).columns  # Select numeric columns

    def is_numeric_columns(self, dataset, column_names):
        """Checks if the values in the given columns are numeric."""
        return all(dataset[column].dtype in 
                   [np.float64, np.int64] 
                   for column in column_names)

    def detect_outliers_iqr(self, dataset, column_names):
        """Replaces outliers with NaN using the IQR method."""

        is_numeric = self.is_numeric_columns(dataset, column_names)  # Check if columns are numeric
        
        if not is_numeric:
            raise ValueError("Non-numeric columns detected. Please select numeric columns for IQR outlier detection.")

        # A data placeholder so as to not change the raw data
        cleaned_data = dataset.copy()

        # Apply IQR on selected column_names
        column_data = cleaned_data[column_names]

        # Calculate IQR for each column
        Q1 = column_data[column_names].quantile(0.25)
        Q3 = column_data[column_names].quantile(0.90)  # Adjusted Q3 for flexibility
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        # Replace outliers with NaN
        num_outliers = 0  # Counter for total outliers
        for column in column_names:
            outliers = (cleaned_data[column] < lower_bound[column]) | (cleaned_data[column] > upper_bound[column])
            num_outliers += outliers.sum()
            cleaned_data[column] = cleaned_data[column].mask(outliers, np.nan)  # Replace outliers with NaN

        return cleaned_data, num_outliers  # Return cleaned dataset & number of outliers

    def detect_outliers_isolation_forest(self, dataset, contamination, column_names):
        """Replaces outliers with NaN using Isolation Forest."""
        is_numeric = self.is_numeric_columns(dataset, column_names)  # Check if columns are numeric
        
        if not is_numeric:
            raise ValueError("Non-numeric columns detected. Please select numeric columns for Isolation Forest outlier detection.")

        cleaned_data = self.data.copy()
        selected_data = cleaned_data[self.numeric_columns]

        # Fit Isolation Forest
        i_forest = IsolationForest(contamination=contamination, random_state=42)
        i_forest.fit(selected_data)
        predictions = i_forest.predict(selected_data)

        # Create mask for outliers
        outlier_mask = predictions == -1
        num_outliers = np.sum(outlier_mask)  # Count total outliers detected

        # Replace outliers with NaN instead of dropping rows
        cleaned_data.loc[outlier_mask, self.numeric_columns] = np.nan

        return cleaned_data, num_outliers  # Return cleaned dataset & number of outliers