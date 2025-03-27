from tensorflow import keras
from tensorflow.keras import layers

# Neural Network Class
class NeuralNetwork:
    """
      A class to create and manage a Convolutional Neural Network (CNN) model using TensorFlow and Keras.
      """
    def __init__(self):
        """
               Initializes the NeuralNetwork class.

               Attributes:
               ----------
               model : keras.Sequential or None
                   Stores the CNN model. Initially set to None.
        """
        self.model = None

    @classmethod
    def create_cnn_model(cls, dataObj):
        """
        Create a Convolutional Neural Network (CNN) model with configurable optimizer, loss function, and activation functions.
         The model consists of:
         - Two convolutional layers with ReLU activation.
         - Two max-pooling layers.
         - A fully connected dense layer with 128 neurons and ReLU activation.
         - An output layer with 10 neurons and softmax activation for multi-class classification.

        Args:
            dataObj (dict): Data dictionary containing:
              - optimizer (str): Optimizer to compile the model (e.g., 'adam', 'RMSPROP' & 'adamax').
              - activation_function (str): Activation function for hidden layers (e.g., 'relu', 'sigmoid').
       
        Returns:
            model: A compiled CNN model.
        """
        activation_fn = dataObj['activation_fn']
        optimizer = dataObj['optimizer']

        # Convolutional Neural Network (CNN) with 2 convolutional layers
        cls.model = keras.Sequential([
            layers.Conv2D(32, (3, 3), activation = activation_fn, input_shape = (28, 28, 1)),
            layers.MaxPooling2D((2, 2)),
            layers.Conv2D(64, (3, 3), activation = activation_fn),
            layers.MaxPooling2D((2, 2)),
            layers.Flatten(),
            layers.Dense(128, activation = activation_fn),
            layers.Dense(10, activation ='softmax')
        ])
        cls.model.compile(optimizer = optimizer,
                           loss = 'sparse_categorical_crossentropy',
                           metrics = ['accuracy'])
        return cls.model