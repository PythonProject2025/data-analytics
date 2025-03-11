import os
import sys
import pandas as pd

# Ensure the correct module path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "models")))

# Import Outlier Detection Class and DataObject
from Outlier_final import OutlierDetection
from Smoothing_final_1 import SmoothingMethods
from data_object_final import DataObject  
from Spline_Interpolation_final import SplineInterpolator
from data_object_final import DataObject

# -------------------- FUNCTION: RUN OUTLIER DETECTION -------------------- #
def run_outlier_detection(dataset, data_object):
    """Runs the outlier detection based on the method defined in DataObject."""
    data = {}

    # Extract selected method from DataObject
    method_name = data_object["Method"]
    column_names = data_object["Parameters"]["column_names"]

    # Initialize Outlier Detection with dataset
    detector = OutlierDetection(dataset)
    original_size = dataset.shape  # Store original dataset size

    if method_name == "IQR":
        cleaned_data, removed_outliers = detector.detect_outliers_iqr(dataset, column_names = column_names)

        data = {
                    "Method": "IQR",
                    "Removed Outliers": removed_outliers,
                    "Original data size": original_size,
                    "Cleaned data size": cleaned_data.shape, 
                    "cleaned_data": cleaned_data
            }

    elif method_name == "Isolation Forest":
        contamination = data_object["Outlier Detection"]["Parameters"]["contamination"]
        cleaned_data, removed_outliers = detector.detect_outliers_isolation_forest(dataset, contamination, column_names)

        data = {
                    "Method": "Isolation Forest",
                    "Removed Outliers": removed_outliers,
                    "Original data size": original_size,
                    "Cleaned data size": cleaned_data.shape,
                    "cleaned_data": cleaned_data
                }
        
    return data

# -------------------- FUNCTION: RUN INTERPOLATION -------------------- #
def run_interpolation(cleaned_outlier_data,data_object):
    """Runs the cubic spline interpolation on the dataset after outlier detection."""

    column_names = data_object["Parameters"]["column_names"]
    # Store original data size (before interpolation)
    original_size = cleaned_outlier_data.shape

    # Initialize the Interpolator
    interpolator = SplineInterpolator(cleaned_outlier_data)
    interpolated_data = interpolator.fill_missing_values()

    # Efficiently update only values inside the predefined structure
    data = {"Method": "Spline Interpolation",
            "Filled_Missing_Values": interpolated_data.shape[0] - original_size[0],
            "Interpolated_Data": interpolated_data
    }

    return data

# -------------------- FUNCTION: RUN SMOOTHING -------------------- #
def run_smoothing(interpolated_data, data_object):
    """Runs the smoothing process based on the method defined in DataObject."""
    data = {}

    # Extract selected method from DataObject
    method_name = data_object["Method"]
    smoothing_config = data_object["parameters"]

    # Initialize Smoothing with dataset
    smoother = SmoothingMethods(interpolated_data)
    
    if method_name == "SMA":
        window_size = smoothing_config["window_size"]
        smoothed_data = smoother.calculate_sma(interpolated_data, window_size)

        # Efficiently update only values inside the predefined structure
        data = {"SMA": {"Method": "Simple Moving Average",
                        "Window Size Applied": window_size},
                "smoothed_data": smoothed_data
        }

    elif method_name == "TES":
        seasonal_periods = smoothing_config["parameters"]["seasonal_periods"]
        trend = smoothing_config["TES"]["parameters"]["trend"]
        seasonal = smoothing_config["TES"]["parameters"]["seasonal"]
        smoothing_level = smoothing_config["TES"]["parameters"]["smoothing_level"]
        smoothing_trend = smoothing_config["TES"]["parameters"]["smoothing_trend"]
        smoothing_seasonal = smoothing_config["TES"]["parameters"]["smoothing_seasonal"]

        smoothed_data = smoother.apply_tes(seasonal_periods, 
                                           trend, 
                                           seasonal, 
                                           smoothing_level, 
                                           smoothing_trend, 
                                           smoothing_seasonal)

        # Efficiently update only values inside the predefined structure
        data = {"TES": {"Method": "Triple Exponential Smoothing",
                        "Seasonal Periods": seasonal_periods,
                        "Trend": trend,
                        "Seasonal": seasonal,
                        "Smoothing Level": smoothing_level,
                        "Smoothing Trend": smoothing_trend,
                        "Smoothing Seasonal": smoothing_seasonal},
                "smoothed_data": smoothed_data
        }

    return data

# -------------------- FUNCTION: RETURN FINAL DATA OBJECT -------------------- #
def get_final_results():
    """Returns the final DataObject output for GUI processing."""
    return data_object.outputs

# -------------------- MAIN EXECUTION -------------------- #
if __name__ == "__main__":
    # -------------------- INITIALIZE DATA OBJECT -------------------- #
    # Create DataObject instance and fetch the dataset

    data_object = DataObject()  

    # Retrieve dataset from DataObject's raw_data
    data_object.raw_data = pd.read_csv("/Users/niharikav/Desktop/MAIT_Notes/OOPS/OOPS project/Steel_industry_data.csv")  # Stores uploaded file data
    dataset = data_object.raw_data

    data_object.data_filtering["Outlier Detection"]["Parameters"]["column_names"] = ["Lagging_Current_Reactive.Power_kVarh"]

    # Run Outlier Detection
    data_object.outputs["Data Processing"]["Outlier Detection"] = run_outlier_detection(dataset,
                                                                                        data_object.data_filtering["Outlier Detection"])

    print("Outlier Detection completed successfully.")
    print(data_object.outputs["Data Processing"]["Outlier Detection"])

    # Retrieve cleaned data from Outlier Detection
    cleaned_outlier_data = data_object.outputs["Data Processing"]["Outlier Detection"]["cleaned_data"]
    # Run Interpolation
    data_object.outputs["Data Processing"]["Interpolation"] = run_interpolation(cleaned_outlier_data)

    print("Interpolation completed successfully.")
    print(data_object.outputs["Data Processing"]["Interpolation"])

    interpolated_data = data_object.outputs["Data Processing"]["Interpolation"]["Interpolated_Data"]
    # Run Smoothing
    data_object.outputs["Data Processing"]["Smoothing"] = run_smoothing(interpolated_data, 
                  data_object.data_filtering["Smoothing"])

    print("Smoothing completed successfully.")
    print(data_object.outputs["Data Processing"]["Smoothing"])

    # Return final results (to be handled by GUI)
    final_results = get_final_results()