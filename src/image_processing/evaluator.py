import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt


# Evaluation Class (Separate for model evaluation and confusion matrix)
class Evaluation:
    """
    A class for evaluating a trained model and visualizing its performance using a confusion matrix.
    """

    def __init__(self, model):
        """
        Initializes the Evaluation class.
  
        Parameters:
        ----------
        model : keras.Model
            The trained model to be evaluated.
        """
        self.model = model

    def evaluate_model(self, dataObj):
        """
        Evaluates the model on the test dataset.
        
        Attributes:
        ----------
        X_test : numpy.ndarray
            The test dataset features.
        y_test : numpy.ndarray
            The true labels for the test dataset.
            
        Returns:
        ------
        - test_acc: Test accuracy.
        - test_loss: Test loss.
        """
        X_test = dataObj["X_test"]
        y_test = dataObj["y_test"]
        # Evaluate the model performance on the test dataset
        X_test_reshaped = X_test[..., np.newaxis]  # Add channel dimension for CNN
        test_loss, test_acc = self.model.evaluate(X_test_reshaped, y_test)

        print(f"Test accuracy: {test_acc}")
        print(f"Test loss: {test_loss}")

        return test_loss, test_acc

    def get_confusion_matrix(self, dataObj, pred_tuple):
        """
        Generates the confusion matrix.

        Parameters:
        ----------
        pred_tuple : tuple
            A tuple containing the predicted labels and indicies for the test dataset.

        Returns:
        --------
        dict: A dictionary containing six key value pairs:
            - labels: Unique labels from the dataset
            - values: The confusion matrix values in percentage
            - xlabel: X-axis label to be used for visualization.
            - ylabel: Y-axis label to be used for visualization.
            - title: Graph title to be used for visualization.
            - tick_marks: Tick marks to be used for visualization.
        """
        y_test = dataObj["y_test"]

        pred_ind = [tup[0] for tup in pred_tuple]
        pred_label = [tup[1] for tup in pred_tuple]
      
        cm = tf.math.confusion_matrix(labels = y_test, 
                                      predictions = pred_ind).numpy()
        
        # Normalize the confusion matrix to percentages
        cm_percentage = cm.astype('float') / cm.sum(axis = 1)[:, np.newaxis] * 100
        cm_percentage = np.nan_to_num(cm_percentage)  # Handle division by zero for empty classes

        # Set up the figure and axis
        # fig, ax = plt.subplots(figsize = (10, 7))

        # Display the confusion matrix as an image
        # cax = ax.matshow(cm_percentage, cmap = 'viridis')

        # Add a colorbar
        # fig.colorbar(cax)

        # Annotate each cell with the corresponding percentage
        # for i in range(cm_percentage.shape[0]):
        #  for j in range(cm_percentage.shape[1]):
        #     text = f'{cm_percentage[i, j]:.2f}%\n({int(cm[i, j])})'
        #     text_color = 'white'
        #     ax.text(j, i, text,
        #             ha = 'center', va = 'center',
        #             color=text_color)

        # Add labels for axes
        # ax.set_xlabel('Predicted Labels')
        # ax.set_ylabel('True Labels')

        # Set tick marks and labels
        unique_labels = np.unique(pred_label)
        tick_marks = np.arange(len(unique_labels))
        # ax.set_xticks(tick_marks)
        # ax.set_yticks(tick_marks)
        # ax.set_xticklabels(unique_labels, rotation = 45)
        # ax.set_yticklabels(unique_labels)

        # # Add gridlines and a title
        # ax.grid(False)
        # ax.set_title('Normalized Confusion Matrix (in %)')

        # # Adjust layout for better visualization
        # plt.tight_layout()
        # plt.show()

        data = {
           "labels": unique_labels,
           "values": cm_percentage, # in percentage
           "xlabel": "Predicted Labels",
           "ylabel": "True Labels",
           "title": "Normalized Confusion Matrix (in %)",
           "tick_marks": tick_marks   
        }

        return data
