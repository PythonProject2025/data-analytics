import numpy as np
import matplotlib.pyplot as plt

# Testing Class (Separate for making predictions and visualizations)
class Testing:
    def __init__(self, model, dataObj):
        self.label_dict = None
        self.model = model
        self.X_test = dataObj["X_test"]
        self.y_test = dataObj["y_test"]

    def set_label_dict(self, label_dict):
        # Store the reverse mapping of label dictionary
        self.label_dict = {value: key for key, value in label_dict.items()}

    def make_predictions(self, X_test_reshaped):
        # Predict using the trained model
        return self.model.predict(X_test_reshaped)

    def plot_image(self, pred_tuple, index):
        # Convert predictions to labels (argmax)
        pred_ind, pred_label, pred_prob = pred_tuple[index]

        # Print the name of the predicted label from the label dictionary
        true_label = self.label_dict[self.y_test[index]]

        print(f"Predicted label: {pred_label}")
        print(f"Predicted probability: {pred_prob:.2f}")
        print(f"True label: {true_label}")

        # Visualize a sample image and show predictions
        plt.matshow(self.X_test[index])
        plt.show()


    def get_predicted_tuple(self):
        X_test_reshaped = self.X_test[..., np.newaxis]  # Add channel dimension for CNN
        preds = self.make_predictions(X_test_reshaped)
        
        # Convert predictions to labels (argmax)
        pred_tuple = [(np.argmax(pred), self.label_dict[np.argmax(pred)], np.max(pred)) for pred in preds]

        return pred_tuple