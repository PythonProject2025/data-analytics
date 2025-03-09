import numpy as np

# Training Class
class Training:
    def __init__(self, model):
        self.model = model
        # self.X_train, self.y_train, _, _ = data
    
    def train_nn(self, dataObj, epochs = 10):
        # Train the neural network model
        # Reshape the data to include the channel dimension (28, 28, 1) for CNN
        X_train = dataObj["X_train"]
        y_train = dataObj["y_train"]

        X_train_reshaped = X_train[..., np.newaxis]  # Add channel dimension for CNN
        self.model.fit(X_train_reshaped, y_train, epochs = epochs)