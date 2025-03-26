import numpy as np
import matplotlib.pyplot as plt

class Testing:
    """
    A class for testing a trained model by making predictions and visualizing results.

    Attributes
    ----------
    model : object
        The trained machine learning model.
    X_test : numpy.ndarray
        The test dataset features.
    y_test : numpy.ndarray
        The test dataset labels.
    label_dict : dict, optional
        A dictionary mapping class indices to class labels.

    Methods
    -------
    set_label_dict(label_dict)
        Stores a reverse mapping of the label dictionary.
    make_predictions()
        Generates predictions using the trained model.
    plot_image(pred_tuple, index)
        Displays a sample test image along with its predicted and true labels.
    get_predicted_tuple()
        Converts model output to class labels and probabilities.
    """

    def __init__(self, model, dataObj):
        """
        Initializes the Testing class with the trained model and test data.

        Parameters
        ----------
        model : object
            The trained machine learning model.
        dataObj : dict
            The data object dictionary consistings of:
                X_test : numpy.ndarray
                    The test dataset features.
                y_test : numpy.ndarray
                    The test dataset labels.
        """
        self.label_dict = None
        self.model = model
        self.X_test = dataObj["X_test"]
        self.y_test = dataObj["y_test"]


    def set_label_dict(self, label_dict):
        """
        Stores the reverse mapping of a label dictionary.

        Parameters
        ----------
        label_dict : dict
            A dictionary mapping class names to class indices.
        """
        self.label_dict = {value: key for key, value in label_dict.items()}


    def make_predictions(self, X_test_reshaped):
        """
        Makes predictions using the trained model.

        Returns
        -------
        numpy.ndarray
            The predicted output from the model.
        """
        # Predict using the trained model
        return self.model.predict(X_test_reshaped)


    def get_predicted_result(self, pred):
        """
        Shows the prediction of the test image provided by the user.

        Parameters
        ----------
        pred : numpy array
            An array containing the predicted values from the model
        
        Raises
        ------
        ValueError
            If the label dictionary is not set.
        """
        if self.label_dict is None:
            raise ValueError("Label dictionary not set. Use set_label_dict() first.")
        
        pred_prob = np.max(pred)
        pred_label = self.label_dict[np.argmax(pred)]


        print(f"Predicted label: {pred_label}")
        print(f"Predicted probability: {pred_prob:.2f}")

        data = {
            "predicted_label": pred_label,
            "predicted_prob": pred_prob
        }

        return data

    def get_predicted_tuple(self):

        """
        Converts model predictions to a tuple of (index, predicted label, probability).

        Returns
        -------
        list of tuples
            Each tuple contains (predicted class index, predicted class name, prediction probability).
        """
        X_test_reshaped = self.X_test[..., np.newaxis]  # Add channel dimension for CNN
        preds = self.make_predictions(X_test_reshaped)
        
        # Convert predictions to labels (argmax)
        pred_tuple = [(np.argmax(pred), self.label_dict[np.argmax(pred)], np.max(pred)) for pred in preds]
        return pred_tuple
