"""
image_processing
================

A package for loading image data, building and training neural networks,
evaluating model performance, and testing predictions.

Modules:
--------
- dataloader: Provides data loading and preprocessing functionality
- nn: Defines a neural network class and its architecture
- train: Handles training the neural network
- evaluator: Evaluates the trained model (accuracy, confusion matrix, etc.)
- test: Offers methods for making predictions and visualizing results
"""
from image_processing.dataloader import DataLoadingAndPreprocessing
from image_processing.nn import NeuralNetwork
from image_processing.train import Training
from image_processing.evaluator import Evaluation
from image_processing.test import Testing

_all_ = [
    "DataLoadingAndPreprocessing",
    "NeuralNetwork",
    "Training",
    "Evaluation",
    "Testing",
]