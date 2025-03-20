# base_model.py
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay,
    mean_squared_error
)
import matplotlib.pyplot as plt
import numpy as np
#from data_object_final import data_object

outputs = {
    'accuracy': None,  # Accuracy of the model
    'report': None,  # Classification report
    'cm': None,  # Confusion matrix
    'mse': None  # Mean squared error
}

class ClassifierClass:


    def __init__(self, data_train, data_test, target_train, target_test):
        self.data_train = data_train
        self.data_test = data_test
        self.target_train = target_train
        self.target_test = target_test
        #self.target_labels = target_labels

    def set_model(self, model):
        self.current_model = model
        print(f"Model set to: {type(model).__name__}")

    def evaluate(self, model):
        model.fit(self.data_train, self.target_train)
        target_pred = model.predict(self.data_test)

        accuracy = accuracy_score(self.target_test, target_pred)
        report = classification_report(self.target_test, target_pred)
        cm = confusion_matrix(self.target_test, target_pred)
        mse = mean_squared_error(self.target_test, target_pred)
        
        # Save outputs to the dictionary
        outputs['accuracy'] = accuracy
        outputs['report'] = report
        outputs['cm'] = cm
        outputs['mse'] = mse
        """
        data_object.outputs["Classification"][model] = {
            "accuracy": accuracy,
            "mse": mse,
            "cm": cm.tolist()  # Convert to list for JSON serialization
        }
        """
        """
        # Print all classification outputs
        print("Classification Outputs:")
        for model, metrics in data_object.outputs["Classification"].items():
            print(f"\nModel: {model}")
            for metric, value in metrics.items():
                print(f"{metric}: {value}")
        """
        
        # Print classification outputs
        print("Model Accuracy:", accuracy)
        print("\nClassification Report:\n", report)
        print("\nConfusion Matrix:")
        print(cm)
        print(f"Mean Squared Error: {mse:.4f}")

        return accuracy, report, cm, mse
        
"""
    def display_confusion_matrix(self, cm):
        cm_percent = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis] * 100
        disp = ConfusionMatrixDisplay(confusion_matrix=cm_percent, display_labels=self.target_labels)
        disp.plot(cmap="Blues", values_format=".1f")
        for text in disp.text_.flatten():
            text.set_text(text.get_text() + '%')
        plt.title("Confusion Matrix (%)")
        plt.show()"
"""