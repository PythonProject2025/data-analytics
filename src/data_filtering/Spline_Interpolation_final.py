import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline

class SplineInterpolator:
    def __init__(self, data):
        """
        Initializes the SplineInterpolator class with a dataset.
        :param data: Pandas DataFrame containing the dataset.
        """
        self.data = data  # Dataset
        self.numeric_columns = self.data.select_dtypes(include=["number"]).columns  # Select numeric columns

    def check_column_validity(self, column_name):
        """Checks if a column can be interpolated (at least 2 known numeric values)."""
        known_values = self.data[column_name].dropna()
        return len(known_values) >= 2

    def fill_missing_values(self):
        """Applies cubic spline interpolation to fill missing values in numeric columns."""
        cleaned_data = self.data.copy()

        for column in self.numeric_columns:
            if not self.check_column_validity(column):
                print(f"Skipping column '{column}': Not enough known values for interpolation.")
                continue

            known_indices = cleaned_data[cleaned_data[column].notnull()].index
            missing_indices = cleaned_data[cleaned_data[column].isnull()].index

            x_known = known_indices
            y_known = cleaned_data.loc[known_indices, column]

            # Create cubic spline interpolator
            cubic_spline = CubicSpline(x_known, y_known)

            # Fill missing values
            for idx in missing_indices:
                cleaned_data.at[idx, column] = cubic_spline(idx)

        return cleaned_data  # Return the cleaned dataset

    # def plot_interpolation(self):
    #     """Plots original and interpolated data for each numeric column."""
    #     for column in self.numeric_columns:
    #         if not self.check_column_validity(column):
    #             continue

    #         plt.figure(figsize=(10, 6))
    #         known_data = self.data[self.data[column].notnull()]
    #         interpolated_data = self.data[self.data[column].isnull() == False]

    #         plt.scatter(known_data.index, known_data[column], color="blue", label="Original Data (Known)")
    #         plt.scatter(interpolated_data.index, interpolated_data[column], color="red", label="Interpolated Data")

    #         plt.title(f"Cubic Spline Interpolation for {column}")
    #         plt.xlabel("Index")
    #         plt.ylabel(column)
    #         plt.legend()
    #         plt.grid(True)
    #         plt.show()
