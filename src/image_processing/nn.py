from tensorflow import keras
from tensorflow.keras import layers

# Neural Network Class
class NeuralNetwork:
    def __init__(self):
        self.model = None

    @classmethod
    def create_cnn_model(cls, dataObj):
        """
        Create a Convolutional Neural Network (CNN) model with configurable optimizer, loss function, and activation functions.
 
        Args:
            optimizer (str): Optimizer to compile the model (e.g., 'adam', 'sgd').
            activation_function (str): Activation function for hidden layers (e.g., 'relu', 'tanh').
            output_activation (str): Activation function for the output layer (e.g., 'softmax', 'sigmoid').
       
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