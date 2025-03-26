import numpy as np

# Training Class
class Training:
    """
        A class for testing a trained model by making predictions and visualizing results.

        Attributes:
        ----------
        model : object
            The trained machine learning model.
        X_test : numpy.ndarray
            The test dataset features.
        y_test : numpy.ndarray
            The test dataset labels.

        Methods:
        -------
        make_predictions(use_cnn=False):
            Generates predictions using the trained model.

        plot_image(index, use_cnn=False):
            Displays a sample test image along with its predicted and true labels.

        get_predicted_labels(y_predicted):
            Converts model output to class labels.
     """
    def __init__(self, model):
        """
                 Initializes the Training class with the model and training data.

                 Parameters:
                 ----------
                 model : object
                     The neural network model to be trained.
                
        """
        self.model = model
        # self.X_train, self.y_train, _, _ = data
    
    def train_nn(self, dataObj, epochs = 10):
         """
                 Trains the neural network model on the training data.

                 Parameters:
                 ----------
                 dataObj : dict
                     Data object dictionary containing training and test datasets (X_train, y_train, X_test, y_test).
                 epochs : int, optional
                     Number of training epochs (default is 10).
        """
         # Train the neural network model
         # Reshape the data to include the channel dimension (28, 28, 1) for CNN
         X_train = dataObj["X_train"]
         y_train = dataObj["y_train"]

         X_train_reshaped = X_train[..., np.newaxis]  # Add channel dimension for CNN

         self.model.fit(X_train_reshaped, y_train, epochs = epochs)