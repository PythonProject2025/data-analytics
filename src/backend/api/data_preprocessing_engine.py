import os
import sys
import pandas as pd
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# Ensure the correct module path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "models")))

# Import processing classes
from data_filtering.Outlier_final import OutlierDetection
from data_filtering.Smoothing_final_1 import SmoothingMethods
from data_filtering.Spline_Interpolation_final import SplineInterpolator
from data_filtering.Scaling_and_Encoding_final import EncodeAndScaling
from models.data_object_class import DataObject

class DataFilteringFileAPIView(APIView):
    
    def post(self, request):
        print("Received request data:", request.data)
        data_dict = request.data.get("dataobject", {})
        if not data_dict:
            return Response({"error": "Invalid request, 'dataobject' missing"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Load data into DataObject
        data_object = DataObject()
        data_object.data_filtering = data_dict.get("data_filtering", {})
        # Retrieve dataset from DataObject's raw_data
        data_object.raw_data = pd.read_csv(data_object.data_filtering["filepath"])  # Stores uploaded file data
        dataset = data_object.raw_data
        print(data_object.data_filtering["Outlier Detection"])
        # Step 1: Outlier Detection
        data_object.outputs["Data Processing"]["Outlier Detection"] = self.run_outlier_detection(
            dataset, data_object.data_filtering["Outlier Detection"]
        )

        print("Outlier Detection completed successfully.")
        print(data_object.outputs["Data Processing"]["Outlier Detection"])

        # Convert DataFrame to JSON for response
        response_data = {
            "step": "Outlier Detection",
            "method": data_object.outputs["Data Processing"]["Outlier Detection"]["Method"],
            "removed_outliers": data_object.outputs["Data Processing"]["Outlier Detection"]["Removed Outliers"],
            "original_data_size": data_object.outputs["Data Processing"]["Outlier Detection"]["Original data size"],
            "cleaned_data_size": data_object.outputs["Data Processing"]["Outlier Detection"]["Cleaned data size"],
            "cleaned_data": data_object.outputs["Data Processing"]["Outlier Detection"]["cleaned_data"].to_json(orient="records") # FIXED
        }
        return Response(response_data, status=status.HTTP_200_OK)

    def run_outlier_detection(self,dataset, data_object):
        """Runs the outlier detection based on the method defined in DataObject."""
        data = {}

        # Extract selected method from DataObject
        method_name = data_object["Method"]
        column_names = data_object["Parameters"]["column_names"]
        print(method_name,column_names)
        # Initialize Outlier Detection with dataset
        detector = OutlierDetection(dataset)
        original_size = dataset.shape  # Store original dataset size

        if method_name == "IQR":
            cleaned_data, removed_outliers = detector.detect_outliers_iqr(dataset,column_names)

            data = {
                        "Method": "IQR",
                        "Removed Outliers": removed_outliers,
                        "Original data size": original_size,
                        "Cleaned data size": cleaned_data.shape, 
                        "cleaned_data": cleaned_data
                }

        elif method_name == "Isolation Forest":
            
            contamination = data_object["Parameters"]["contamination"]
            cleaned_data, removed_outliers = detector.detect_outliers_isolation_forest(dataset, contamination, column_names)

            data = {
                        "Method": "Isolation Forest",
                        "Removed Outliers": removed_outliers,
                        "Original data size": original_size,
                        "Cleaned data size": cleaned_data.shape,
                        "cleaned_data": cleaned_data
                    }
            
        return data

class InterpolationAPIView(APIView):
    
    def post(self, request):
        print("Received request data:", request.data)
        data_dict = request.data.get("dataobject", {})

        if not data_dict:
            return Response({"error": "Invalid request, 'dataobject' missing"}, status=status.HTTP_400_BAD_REQUEST)

        # Load data into DataObject
        data_object = DataObject()
        cleaned_outlier_data = pd.DataFrame.from_dict(data_dict.get("cleaned_data", {}))

        # Step 2: Interpolation
        data_object.outputs["Data Processing"]["Interpolation"] = self.run_interpolation(cleaned_outlier_data)

        print("Interpolation completed successfully.")
        print(data_object.outputs["Data Processing"]["Interpolation"])

        response_data = {
            "step": "Interpolation",
            "method": data_object.outputs["Data Processing"]["Interpolation"]["Method"],
            "filled_missing_values": data_object.outputs["Data Processing"]["Interpolation"]["Filled_Missing_Values"],
            "interpolated_data": data_object.outputs["Data Processing"]["Interpolation"]["Interpolated_Data"].to_dict()
        }
        return Response(response_data, status=status.HTTP_200_OK)

    def run_interpolation(self,cleaned_outlier_data):
        """Runs the cubic spline interpolation on the dataset after outlier detection."""

        # Initialize the Interpolator
        interpolator = SplineInterpolator(cleaned_outlier_data)
        interpolated_data = interpolator.fill_missing_values()

        # Efficiently update only values inside the predefined structure
        data = {
                "Method": "Spline Interpolation",
                "Filled_Missing_Values": cleaned_outlier_data.isna().sum().sum() - interpolated_data.isna().sum().sum(),
                "Interpolated_Data": interpolated_data
        }

        return data
    
class SmoothingAPIView(APIView):
    
    def post(self, request):
        print("Received request data:", request.data)
        data_dict = request.data.get("dataobject", {})

        if not data_dict:
            return Response({"error": "Invalid request, 'dataobject' missing"}, status=status.HTTP_400_BAD_REQUEST)

        # Load data into DataObject
        data_object = DataObject()
        interpolated_data = pd.DataFrame.from_dict(data_dict.get("interpolated_data", {}))

        # Step 3: Smoothing
        data_object.outputs["Data Processing"]["Smoothing"] = self.run_smoothing(
            interpolated_data, data_object.data_filtering["Smoothing"]
        )

        print("Smoothing completed successfully.")
        print(data_object.outputs["Data Processing"]["Smoothing"])

        response_data = {
            "step": "Smoothing",
            "method": data_object.outputs["Data Processing"]["Smoothing"]["Method"],
            "smoothed_data": data_object.outputs["Data Processing"]["Smoothing"]["smoothed_data"].to_dict()
        }
        return Response(response_data, status=status.HTTP_200_OK)

    def run_smoothing(self,interpolated_data, data_object):
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

class ScalingEncodingAPIView(APIView):
    
    def post(self, request):
        print("Received request data:", request.data)
        data_dict = request.data.get("dataobject", {})

        if not data_dict:
            return Response({"error": "Invalid request, 'dataobject' missing"}, status=status.HTTP_400_BAD_REQUEST)

        # Load data into DataObject
        data_object = DataObject()
        smoothed_data = pd.DataFrame.from_dict(data_dict.get("smoothed_data", {}))

        # Step 4: Scaling & Encoding
        data_object.data_filtering["Train-Test Split"]["split_data"] = self.run_encoding_scaling_train_test_split(
            smoothed_data, data_object.data_filtering["Train-Test Split"]
        )

        print("Encoding, Scaling, Train-Test Split completed successfully.")
        print(data_object.data_filtering["Train-Test Split"]["split_data"])

        response_data = {
            "step": "Scaling & Encoding",
            "processed_data": data_object.data_filtering["Train-Test Split"]["split_data"].to_dict()
        }
        return Response(response_data, status=status.HTTP_200_OK)

    def run_encoding_scaling_train_test_split(self, data, params):
        """Runs encoding, scaling, and train-test splitting."""
        processor = EncodeAndScaling(data)
        processed_data = processor.preprocess(params["parameters"])
        return processed_data
