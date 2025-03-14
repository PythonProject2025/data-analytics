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
from ai_model.models.base import BaseModel

# Import AI models for classification and regression
from ai_model.models.random_forest import RandomForest
from ai_model.models.catboost_model import Catboost  # Ensure the class name in catboost_model.py is "CatBoost"
from ai_model.models.ann import ArtificialNeuralNetwork
from ai_model.models.xgboost_model import XGBoost


# Optional Debugging: Uncomment during development
# print("✅ Models package successfully loaded!")

# Exposing modules for easy access
__all__ = [
    "BaseModel",
    "RandomForest",
    "Catboost",
    "ArtificialNeuralNetwork",
    "XGBoost",
]
