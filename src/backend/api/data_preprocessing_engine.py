from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import pandas as pd
from sklearn.ensemble import IsolationForest

# Global variable to store uploaded data
uploaded_data = None

class DataFilteringFileAPIView(APIView):
    
    #Handles CSV file uploads.

    def post(self, request):
        global uploaded_data
        try:
            # Access the uploaded file
            csv_file = request.FILES.get('file')
            if not csv_file:
                return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)

            # Load the file into a pandas DataFrame
            uploaded_data = pd.read_csv(csv_file)
            return Response({"message": "File uploaded successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DataFilteringParamsAPIView(APIView):
    
    #Processes data based on parameters.

    def post(self, request):
        global uploaded_data
        if uploaded_data is None:
            return Response({"error": "No file uploaded. Please upload a file first."}, status=status.HTTP_400_BAD_REQUEST)

        try:

            Filter_method = request.data.get("Filter_method")
            method = request.data.get("Outlier_method")
            column_name = request.data.get("column_name")
            contamination = request.data.get("contamination")

            print (Filter_method)
            print(method)
            print(column_name)
            print(contamination)
            if column_name not in uploaded_data.columns:
                return Response({"error": f"Column '{column_name}' not found in the dataset"}, status=status.HTTP_400_BAD_REQUEST)

            # Initialize the outlier detection class
            outlier_detector = OutlierDetection(uploaded_data, column_name)
            print("pop")
            if Filter_method == "Outlier Detection":
            # Apply the selected method
                if method == "IQR":
                    cleaned_data = outlier_detector.detect_outliers_iqr()
                elif method == "Isolation Forest":
                    cleaned_data = outlier_detector.detect_outliers_isolation_forest(contamination=contamination)
                else:
                    return Response({"error": "Invalid method. Choose 'iqr' or 'isolation_forest'."}, status=status.HTTP_400_BAD_REQUEST)
            else:
                    return Response({"error": "Invalid method. Choose 'Outlier."}, status=status.HTTP_400_BAD_REQUEST)

            # Convert cleaned data to JSON for response                         
            cleaned_data_json = cleaned_data.to_dict(orient="records")
            #Raw_data_json = Raw_data.to_dict(orient="records")
            return Response({"cleaned_data": cleaned_data_json} , status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# OutlierDetection class for processing data
class OutlierDetection:
    def __init__(self, data, column_name):
        self.data = data
        self.column_name = column_name

    def detect_outliers_iqr(self):
        column_data = self.data[self.column_name]
        Q1 = column_data.quantile(0.25)
        Q3 = column_data.quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        cleaned_data = self.data[(column_data >= lower_bound) & (column_data <= upper_bound)]
        return cleaned_data

    def detect_outliers_isolation_forest(self, contamination=0.1):
        column_data = self.data[self.column_name].values.reshape(-1, 1)
        i_forest = IsolationForest(contamination=contamination, random_state=42)
        i_forest.fit(column_data)
        predictions = i_forest.predict(column_data)
        cleaned_data = self.data[predictions == 1]
        return cleaned_data
