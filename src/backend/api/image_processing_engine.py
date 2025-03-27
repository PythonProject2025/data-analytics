from image_processing.dataloader import DataLoadingAndPreprocessing
from image_processing.nn import NeuralNetwork
from image_processing.train import Training
from image_processing.evaluator import Evaluation
from image_processing.test import Testing
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import sys
import os
# Dynamically add the src directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
# Now you can import from models
from models.data_object_class import DataObject


class  ImageProcessingAPIView (APIView):
    def post(self, request):
        data_dict = request.data.get("dataobject", {})
        if "dataobject" in data_dict:  
            data_dict = data_dict["dataobject"]

        if not data_dict:
            return Response({"error": "Invalid request, 'dataobject' missing"}, status=status.HTTP_400_BAD_REQUEST)

        # Load extracted data into DataObject
        dataObj = DataObject()
        dataObj.image_processing = data_dict.get("image_processing", {})
        if not dataObj.image_processing["fileio"]["zipFilePath"]:
            return Response({"error": "Missing zipFilePath in request"}, status=status.HTTP_400_BAD_REQUEST)
        
        # dir_name is to be given by the user.
        # This is a placeholder value.
        # NOTE: The dataset should be unzipped in the same directory as the code.
        # dataObj.image_processing["fileio"]["zipFilePath"] = "A:\\EVERYTHING_TH_KOELN\\OOP\\image-processing-oop\\Numbers_images_dataset"
        # dataObj.image_processing["fileio"]["isZipped"] = False
        
        # Step 1: Data Loading and Preprocessing
        data_loader = DataLoadingAndPreprocessing()
        data_loader.data_loader(dataObj.image_processing["fileio"])

        # We need to give this to dictionary to the Testing class
        dataObj.image_processing["label_dict"] = data_loader.get_label_dict()

        # Step 2 : Preprocessing the data and split it
        # Test size and random state can be given by the user
        dataObj.image_processing["splits"] = data_loader.split_dataset(dataObj.image_processing["train_test_split"])
        # Show the split to the user.
        # What are the labels

        # Step 3: Create the Neural Network
        # The activation function, loss function and the optimzer can be changed by the user
        dataObj.image_processing["model"] = NeuralNetwork.create_cnn_model(dataObj.image_processing["model_params"])

        # Train the model
        trainer = Training(dataObj.image_processing["model"])
        # Number of epochs can be changed by the user
        trainer.train_nn(dataObj.image_processing['splits'], 
                        epochs = dataObj.image_processing["training_params"]["epochs"]) 

        # Step 4: Evaluate Model

        # Step 5: Make Predictions and Visualize Confusion Matrix
        testing = Testing(dataObj.image_processing['model'],
                        dataObj.image_processing['splits'])
        # Set the label dictionary in the Testing class
        testing.set_label_dict(dataObj.image_processing['label_dict'])

        y_predicted_tuple = testing.get_predicted_tuple()

        #testing.plot_image(y_predicted_tuple, index = 100)
        
        # Step 5: Visualize Test Image and Prediction
        # These are placeholder functions. Actual method to be implemented by the GUI team 
        evaluator = Evaluation(dataObj.image_processing['model'])
        dataObj.outputs["Image_Processing"]["testLoss"], dataObj.outputs["Image_Processing"]["testAccuracy"] = evaluator.evaluate_model(dataObj.image_processing['splits'])
        dataObj.outputs["Image_Processing"]["confusionMatrix"] = evaluator.get_confusion_matrix(dataObj.image_processing["splits"], 
                                                                                            pred_tuple = y_predicted_tuple)

        evaluator.get_confusion_matrix(dataObj.image_processing["splits"], pred_tuple = y_predicted_tuple)
        
        img = data_loader.load_image(dataObj.image_processing)
        pred = testing.make_predictions(img)
        dataObj.outputs["Image_Processing"]["image_predictions"] = testing.get_predicted_result(pred)
    
        response_data = {
            "testLoss": dataObj.outputs["Image_Processing"]["testLoss"],
            "testAccuracy": dataObj.outputs["Image_Processing"]["testAccuracy"],
            "confusionMatrix": dataObj.outputs["Image_Processing"]["confusionMatrix"],
            "image_predictions": dataObj.outputs["Image_Processing"]["image_predictions"]
        }
        return Response(response_data, status=status.HTTP_200_OK)