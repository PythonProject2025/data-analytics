from rest_framework.views import APIView
from rest_framework.response import Response
from models.data_object_class import DataObject

class Reg_ClassificationAPIView (APIView):
    
    def post(self, request):
        print("Received request data:", request.data)
        data_dict = request.data.get("dataobject", {})
        if "dataobject" in data_dict:  
            data_dict = data_dict["dataobject"]

        if not data_dict:
            return Response({"error": "Invalid request, 'dataobject' missing"}, status=status.HTTP_400_BAD_REQUEST)

        # Load extracted data into DataObject
        dataObj = DataObject()
        data_train = dataObj.classification["Inputs"]["data_train"]
        data_test = dataObj.classification["Inputs"]["data_test"]
        target_train = dataObj.classification["Inputs"]["target_train"]
        target_test = dataObj.classification["Inputs"]["target_test"]
        target_labels = dataObj.classification["Inputs"]["target_labels"]
        