import io
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
from data_filtering.Smoothing_final import SmoothingMethods
from data_filtering.Spline_Interpolation_final import SplineInterpolator
from data_filtering.Scaling_Encoding_Train_Test import EncodeAndScaling
from models.data_object_class import DataObject

class DataFilteringFileAPIView(APIView):
    
    def post(self, request):
        data_dict = request.data.get("dataobject", {})
        if not data_dict:
            return Response({"error": "Invalid request, 'dataobject' missing"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Load data into DataObject
        data_object = DataObject()
        data_object.data_filtering = data_dict.get("data_filtering", {})
        data_object.raw_data = pd.read_csv(data_object.data_filtering["filepath"])  # Stores uploaded file data
        dataset = data_object.raw_data
        # Step 1: Outlier Detection
        data_object.outputs["Data Processing"]["Outlier Detection"] = self.run_outlier_detection(
            dataset, data_object.data_filtering["Outlier Detection"]
        )

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

        data_object = DataObject()
        cleaned_outlier_data_json = request.data.get("cleaned_data", "[]")
        if not cleaned_outlier_data_json:
            return Response({"error": "Cleaned data missing from request"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            cleaned_outlier_data = pd.read_json(io.StringIO(cleaned_outlier_data_json))
        except ValueError as e:
            return Response({"error": f"Invalid JSON format: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        # Step 2: Interpolation
        data_object.outputs["Data Processing"]["Interpolation"] = self.run_interpolation(cleaned_outlier_data)

        response_data = {
            "step": "Interpolation",
            "method": data_object.outputs["Data Processing"]["Interpolation"]["Method"],
            "filled_missing_values": data_object.outputs["Data Processing"]["Interpolation"]["Filled_Missing_Values"],
            "interpolated_data": data_object.outputs["Data Processing"]["Interpolation"]["Interpolated_Data"].to_json(orient="records")
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
        data_dict = request.data.get("dataobject", {})

        if not data_dict:
            return Response({"error": "Invalid request, 'dataobject' missing"}, status=status.HTTP_400_BAD_REQUEST)

        # Load data into DataObject
        data_object = DataObject()
        data_object.data_filtering = data_dict.get("data_filtering", {})
        interpolated_data_json = request.data.get("interpolated_data", "[]")
        if not interpolated_data_json:
            return Response({"error": "Interpolated data missing from request"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            interpolated_data = pd.read_json(io.StringIO(interpolated_data_json))
        except ValueError as e:
            return Response({"error": f"Invalid JSON format: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        data_object.outputs["Data Processing"]["Smoothing"] = self.run_smoothing(
            interpolated_data, data_object.data_filtering["Smoothing"]
        )
        
        smoothing_result = data_object.outputs["Data Processing"]["Smoothing"]

        # Convert the smoothed data to JSON format for response
        if "smoothed_data" in smoothing_result:
            smoothing_result["smoothed_data"] = smoothing_result["smoothed_data"].to_json(orient="records")

        # Return full response from run_smoothing()
        return Response(smoothing_result, status=status.HTTP_200_OK)

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
            data = {"Method": "Simple Moving Average",
                    "SMA": {
                            "Window Size Applied": window_size
                        },
                    "smoothed_data": smoothed_data
            }
        
        elif method_name == "TES":
            tes_params = data_object["parameters"]

            smoothed_data = smoother.apply_tes(
                interpolated_data,
                tes_params["seasonal_periods"],
                tes_params["trend"],
                tes_params["seasonal"],
                tes_params["smoothing_level"],
                tes_params["smoothing_trend"],
                tes_params["smoothing_seasonal"]
            )

            # Return all values inside a structured dictionary
            data = {
                "Method": "Triple Exponential Smoothing",
                "TES": tes_params,
                "smoothed_data": smoothed_data
            }
            
        return data
