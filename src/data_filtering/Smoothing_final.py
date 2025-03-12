import pandas as pd
import numpy as np
from statsmodels.tsa.holtwinters import ExponentialSmoothing

class SmoothingMethods:
    def __init__(self, data):
        """
        Initialize the SmoothingMethods class with a pandas DataFrame.
        
        Parameters:
            data (pd.DataFrame): The dataset containing the columns to be smoothed.
        """
        self.data = data

    def calculate_sma(self, data, window):
        """
        Apply Simple Moving Average (SMA) to numeric columns.
        """
        # Ensure the input is a DataFrame
        if not isinstance(data, pd.DataFrame):
            raise ValueError("Input data must be a Pandas DataFrame.")
        
        # Select only numeric columns
        numeric_cols = data.select_dtypes(include=['number']).columns.tolist()

        if not numeric_cols:
            raise ValueError("No numeric columns found for SMA.")
        
        data[numeric_cols] = data[numeric_cols].rolling(window=window, min_periods=1).mean()
        return data


    def apply_tes(self, data, seasonal_periods, trend, seasonal, smoothing_level, smoothing_trend, smoothing_seasonal):
        """
        Apply Triple Exponential Smoothing (TES) to numeric columns.
        """
        # Ensure the input is a DataFrame
        if not isinstance(data, pd.DataFrame):
          raise ValueError("Input data must be a Pandas DataFrame.")
        
        # Select only numeric columns
        numeric_cols = data.select_dtypes(include=['number']).columns.tolist()

        if not numeric_cols:
         raise ValueError("No numeric columns found for TES.")

        tes_results = pd.DataFrame(index=self.data.index)
        
        for column in numeric_cols:
            try:
                model = ExponentialSmoothing(
                    self.data[column].astype(float), 
                    trend=trend, 
                    seasonal=seasonal, 
                    seasonal_periods=seasonal_periods
                )
                fitted_model = model.fit(smoothing_level=smoothing_level, 
                                         smoothing_trend=smoothing_trend, 
                                         smoothing_seasonal=smoothing_seasonal)
                tes_results[column] = fitted_model.fittedvalues
            except Exception as e:
                print(f"Warning: TES could not be applied to '{column}' as column contains nulls. Error: {e}")
                tes_results[column] = np.nan  # Fill failed columns with NaN  

        return tes_results
