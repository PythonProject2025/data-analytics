"""
This package handles data loading, preprocessing, and transformation.

Modules:
--------
- data_loader: Contains functions for loading, preprocessing, and transforming datasets.
"""

# Import data processing utilities
from .data_loader import load_classification_data, load_regression_data

# Exposing modules for easy access
__all__ = ["load_classification_data", "load_regression_data"]
