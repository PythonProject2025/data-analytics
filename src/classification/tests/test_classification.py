import pytest
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

from base_model import ClassifierClass
from random_forest_model import RandomForestModel
from svc_model import SVCModel
from knn_model import KNNModel





"""
Test suite for the Car Evaluation Classification System.
This module contains unit tests for the classification models and their base class.

Key components tested:
1. Base classifier functionality
2. Model inheritance structure
3. Parameter configurations
4. Evaluation metrics
5. Data handling
6. Training and prediction functionality of each model
"""

# Constants used throughout the test suite
FILEPATH = r"C:\Users\Mohamed Desouky\test\ml_project\classification\data\car.data"

@pytest.fixture
def sample_data():
    """
    Fixture providing preprocessed data for testing.
    """
    data = pd.read_csv(FILEPATH, header=None)

    # Dynamically determine column names and assign them
    num_columns = data.shape[1]
    column_names = [f"feature_{i}" for i in range(num_columns - 1)] + ["class"]
    data.columns = column_names

    # Encode categorical features using LabelEncoder
    label_encoders = {col: LabelEncoder().fit(data[col]) for col in data.columns}
    encoded_data = data.apply(lambda col: label_encoders[col.name].transform(col))

    # Extract the unique labels for the target variable
    target_labels = label_encoders["class"].classes_

    # Split data into features and target, then into train and test sets
    X, y = encoded_data.iloc[:, :-1], encoded_data.iloc[:, -1]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    return X_train, X_test, y_train, y_test, target_labels

def test_base_classifier_initialization(sample_data):
    """
    Test the initialization of the base CarEvaluationClassifier.
    """
    X_train, X_test, y_train, y_test, target_labels = sample_data
    classifier = ClassifierClass(X_train, X_test, y_train, y_test, target_labels)

    assert classifier.data_train is not None, "Training data not initialized"
    assert classifier.data_test is not None, "Testing data not initialized"
    assert classifier.target_train is not None, "Training targets not initialized"
    assert classifier.target_test is not None, "Testing targets not initialized"
    assert classifier.target_labels is not None, "Target labels not initialized"

def test_model_training_and_evaluation(sample_data):
    """
    Test the training and evaluation methods of each model class.
    """
    X_train, X_test, y_train, y_test, target_labels = sample_data

    # Test RandomForestModel
    rf_model = RandomForestModel(X_train, X_test, y_train, y_test, target_labels)
    rf_model.train()
    accuracy, report, cm, mse = rf_model.evaluate(rf_model.model)
    assert isinstance(accuracy, float), "RandomForestModel: Accuracy should be a float"
    assert 0 <= accuracy <= 1, "RandomForestModel: Accuracy should be between 0 and 1"
    assert isinstance(report, str), "RandomForestModel: Classification report should be a string"
    assert isinstance(cm, np.ndarray), "RandomForestModel: Confusion matrix should be a numpy array"
    assert mse >= 0, "RandomForestModel: MSE should be non-negative"

    # Test SVCModel
    svc_model = SVCModel(X_train, X_test, y_train, y_test, target_labels)
    svc_model.train()
    accuracy, report, cm, mse = svc_model.evaluate(svc_model.model)
    assert isinstance(accuracy, float), "SVCModel: Accuracy should be a float"
    assert 0 <= accuracy <= 1, "SVCModel: Accuracy should be between 0 and 1"
    assert isinstance(report, str), "SVCModel: Classification report should be a string"
    assert isinstance(cm, np.ndarray), "SVCModel: Confusion matrix should be a numpy array"
    assert mse >= 0, "SVCModel: MSE should be non-negative"

    # Test KNNModel
    knn_model = KNNModel(X_train, X_test, y_train, y_test, target_labels)
    knn_model.train()
    accuracy, report, cm, mse = knn_model.evaluate(knn_model.model)
    assert isinstance(accuracy, float), "KNNModel: Accuracy should be a float"
    assert 0 <= accuracy <= 1, "KNNModel: Accuracy should be between 0 and 1"
    assert isinstance(report, str), "KNNModel: Classification report should be a string"
    assert isinstance(cm, np.ndarray), "KNNModel: Confusion matrix should be a numpy array"
    assert mse >= 0, "KNNModel: MSE should be non-negative"

def test_confusion_matrix_display(sample_data):
    """
    Test the confusion matrix visualization functionality.
    """
    X_train, X_test, y_train, y_test, target_labels = sample_data
    classifier = ClassifierClass(X_train, X_test, y_train, y_test, target_labels)

    # Create a dummy confusion matrix with dimensions matching the number of target labels
    num_classes = len(target_labels)
    dummy_cm = np.zeros((num_classes, num_classes))

    # Fill the diagonal with sample values to simulate predictions
    np.fill_diagonal(dummy_cm, 10)  # Example values for correct predictions

    try:
        classifier.display_confusion_matrix(dummy_cm)
    except Exception as e:
        pytest.fail(f"display_confusion_matrix raised an exception: {e}")

def test_model_param_grids(sample_data):
    """
    Test the parameter grids for each model class.
    """
    X_train, X_test, y_train, y_test, target_labels = sample_data

    # RandomForestModel param grid
    rf_model = RandomForestModel(X_train, X_test, y_train, y_test, target_labels)
    assert isinstance(rf_model.param_grid, dict), "RandomForestModel: param_grid should be a dictionary"
    assert 'n_estimators' in rf_model.param_grid, "RandomForestModel: Missing 'n_estimators' in param_grid"
    assert 'max_depth' in rf_model.param_grid, "RandomForestModel: Missing 'max_depth' in param_grid"

    # SVCModel param grid
    svc_model = SVCModel(X_train, X_test, y_train, y_test, target_labels)
    assert isinstance(svc_model.param_grid, dict), "SVCModel: param_grid should be a dictionary"
    assert 'C' in svc_model.param_grid, "SVCModel: Missing 'C' in param_grid"
    assert 'kernel' in svc_model.param_grid, "SVCModel: Missing 'kernel' in param_grid"
    assert 'gamma' in svc_model.param_grid, "SVCModel: Missing 'gamma' in param_grid"

    # KNNModel param grid
    knn_model = KNNModel(X_train, X_test, y_train, y_test, target_labels)
    assert isinstance(knn_model.param_grid, dict), "KNNModel: param_grid should be a dictionary"
    assert 'n_neighbors' in knn_model.param_grid, "KNNModel: Missing 'n_neighbors' in param_grid"
    assert 'weights' in knn_model.param_grid, "KNNModel: Missing 'weights' in param_grid"
    assert 'p' in knn_model.param_grid, "KNNModel: Missing 'p' in param_grid"