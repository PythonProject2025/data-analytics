import io
import os
import sys
import pandas as pd
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# Ensure the correct module path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "models")))
from models.data_object_class import DataObject
from data_filtering.Scaling_Encoding_Train_Test import EncodeAndScaling

class ScalingEncodingAPIView(APIView):
    
    def post(self, request):
        data_dict = request.data.get("dataobject", {})

        if not data_dict:
            return Response({"error": "Invalid request, 'dataobject' missing"}, status=status.HTTP_400_BAD_REQUEST)

        # Load data into DataObject
        data_object = DataObject()
        data_object.data_filtering = data_dict.get("data_filtering", {})
        smoothed_data_json = request.data.get("smoothed_data", "[]")
        if not smoothed_data_json:
            return Response({"error": "Smoothed data missing from request"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            smoothed_data = pd.read_json(io.StringIO(smoothed_data_json))
        except ValueError as e:
            return Response({"error": f"Invalid JSON format: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        # Scaling & Encoding
        data_object.data_filtering["Train-Test Split"]["split_data"] = self.run_encoding_scaling_train_test_split(
            smoothed_data, data_object.data_filtering["Train-Test Split"]
        )

        
        split_data = data_object.data_filtering["Train-Test Split"]["split_data"]
        
        # Ensuring all DataFrame values are converted properly
        for key, value in split_data.items():
            if isinstance(value, pd.DataFrame):
                split_data[key] = value.to_dict(orient="records")  # Convert DataFrame to list of dictionaries
            elif isinstance(value, pd.Series):
                split_data[key] = value.tolist()  # Convert Series to a list
                
        response_data = {
            "step": "Scaling & Encoding",
            "processed_data": split_data
        }
        return Response(response_data, status=status.HTTP_200_OK)

    def run_encoding_scaling_train_test_split(self, data, params):
        """Runs encoding, scaling, and train-test splitting."""
        processor = EncodeAndScaling(data)
        processed_data = processor.preprocess(params["parameters"])
        return processed_data