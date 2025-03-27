from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from sklearn.metrics import accuracy_score, confusion_matrix
from models.data_object_class import DataObject
from .base import BaseModel # Importing the BaseModel class from the same package
dataObj = DataObject()
class ArtificialNeuralNetwork(BaseModel):
    """
    Class representing an Artificial Neural Network (ANN) model.

    This class supports only classification problems and builds an ANN model
    based on the given hyperparameters.

    Attributes:
    -----------
    problem_type : str
        Specifies the type of problem. Must be 'classification'.
    options : dict
        Dictionary containing hyperparameters for the ANN model.
    """
    
    def __init__(self, problem_type="classification", options=None):
        """
        Initializes the ANN model with given hyperparameters.

        Parameters:
        -----------
        problem_type : str
            Defines the type of problem. Only 'classification' is allowed.
        options : dict, optional
            Dictionary containing ANN hyperparameters such as:
            - layer_number (int): Number of hidden layers.
            - units (list): Number of neurons per layer.
            - activation (list): Activation functions per layer.
            - optimizer (str): Optimizer for training.
            - batch_size (int): Number of samples per batch.
            - epochs (int): Number of training iterations.
        """
        # Ensure the ANN only supports classification problems
        if problem_type != "classification":
            raise ValueError("Only classification is supported for ANN")
        
        # If options are not provided, initialize with an empty dictionary
        if options is None:
            options = {}
        
        try:
            # Validate the provided options using BaseModel's validation method
            validated_options = BaseModel.validate_options(options, "ArtificialNeuralNetwork")
            
            # Extract hyperparameters from validated options
            layer_number = validated_options["layer_number"]
            units = validated_options["units"]
            activation = validated_options["activation"]
            optimizer = validated_options["optimizer"]
            batch_size = validated_options["batch_size"]
            epochs = validated_options["epochs"]
            
            if isinstance(units, int):
                units = [units] * layer_number
            if isinstance(activation, str):
                activation = [activation] * layer_number
            # Ensure the number of layers matches the number of units and activations
            if len(units) != layer_number or len(activation) != layer_number:
                raise ValueError("Error: The number of 'units' and 'activation' values must match 'layer_number'.")

            # Create a Sequential ANN model
            model_instance = Sequential()

            # Add the specified number of layers with defined units and activation functions
            for i in range(layer_number):
                model_instance.add(Dense(units=units[i], activation=activation[i]))
            
            # Compile the ANN model with the optimizer and loss function
            model_instance.compile(
                optimizer=optimizer,
                loss="sparse_categorical_crossentropy",  # Used for multi-class classification with integer labels
                metrics=['accuracy']
            )
            
            # Initialize the base class (BaseModel) with the compiled model
            super().__init__(model_instance, problem_type)
            self.model = model_instance
            
            # Store batch size and epochs for later use in training
            self.batch_size = batch_size
            self.epochs = epochs

        except ValueError as ve:
            print(f"Value Error during ANN initialization: {ve}")
        except Exception as e:
            print(f"Unexpected error during ANN initialization: {e}")

    def train(self, X_train, y_train):
        """
        Trains the ANN model using the provided training data.
        """    
        try:
            # self.X_train=dataObj["split_data"]["X_train"]
            # self.y_train=dataObj["split_data"]["y_train"]
            self.X_train = X_train
            self.y_train = y_train      
            if self.X_train is None or self.y_train is None:
                raise ValueError("Error: Training data is missing. Ensure data is loaded and split correctly.")

            self.model_history = self.model.fit(
                x=X_train, y=y_train,  # Training data
                batch_size=self.batch_size,  # Number of samples per training step
                epochs=self.epochs  # Number of training iterations
            )
        except ValueError as ve:
            print(f"Value Error during training: {ve}")
        except Exception as e:
            print(f"Unexpected error during training: {e}")


    def save_weights(self, filepath="ann_weights.h5"):
        """
        Saves the trained model's weights to a file.

        Parameters:
        -----------
        filepath : str, optional
            Path where the weights will be saved (default is 'ann_weights.h5').
        """
        try:
            self.model.save_weights(filepath)
            print(f"Model weights saved successfully to {filepath}.")
        except Exception as e:
            print(f"Error saving weights: {e}")

    def load_weights(self, filepath="ann_weights.h5"):
        """
        Loads pre-trained model weights from a file.

        Parameters:
        -----------
        filepath : str, optional
            Path from where the weights will be loaded (default is 'ann_weights.h5').
        """
        try:
            self.model.load_weights(filepath)
            print(f"Model weights loaded successfully from {filepath}.")
        except FileNotFoundError:
            print(f"Error: The file {filepath} was not found. Please check the file path.")
        except Exception as e:
            print(f"Error loading weights: {e}")

    def evaluate(self, X_test, y_test):
        """
        Evaluates the trained model on the test set.

        Returns:
        --------
        dict
            A dictionary containing:
            - Accuracy of the model on test data.
            - Confusion matrix showing classification performance.
        """
        try:
            self.X_test = X_test
            self.y_test = y_test            
             
            if self.X_test is None or self.y_test is None:
                raise ValueError("Error: Test data is missing. Ensure data is loaded and split correctly.")

            # Predict probabilities for each class and get the class with the highest probability
            self.predictions = self.model.predict(self.X_test).argmax(axis=1)

            # Compute accuracy score
            self.accuracy = accuracy_score(self.y_test, self.predictions)

            # Compute confusion matrix
            self.conf_matrix = confusion_matrix(self.y_test, self.predictions)

            # Return results as a dictionary
            return {"Accuracy": self.accuracy, "Confusion Matrix": self.conf_matrix}

        except ValueError as ve:
            print(f"Value Error during evaluation: {ve}")
        except Exception as e:
            print(f"Unexpected error during evaluation: {e}")
            return {"Accuracy": None, "Confusion Matrix": None}