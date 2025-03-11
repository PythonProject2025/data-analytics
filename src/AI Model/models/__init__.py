"""
This package contains machine learning models for classification and regression.

Modules:
--------
- base: Contains the BaseModel class for shared functionalities like hyperparameter validation.
- random_forest: Implements Random Forest for both classification and regression.
- catboost_model: Implements CatBoost for classification and regression.
- ann: Implements Artificial Neural Networks (ANN) for classification.
- xgboost_model: Implements XGBoost for regression.
- ai_pipeline: Manages model selection, training, and evaluation for AI tasks.
"""

# Import BaseModel first (since all models inherit from it)
from .base import BaseModel

# Import AI models for classification and regression
from .random_forest import RandomForest
from .catboost_model import Catboost
from .ann import ArtificialNeuralNetwork
from .xgboost_model import XGBoost
from .ai_pipeline import run_ai_classification, run_ai_regression

# Exposing modules for easy access
__all__ = [
    "BaseModel",
    "RandomForest",
    "Catboost",
    "ArtificialNeuralNetwork",
    "XGBoost",
    "run_ai_classification",
    "run_ai_regression"
]
