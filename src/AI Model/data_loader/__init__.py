"""
This package handles data loading, preprocessing, and transformation.

Modules:
--------
- data_loader: Contains functions for loading, preprocessing, and transforming datasets.
"""

# ✅ Import data processing utilities
from .data_loader import load_data, preprocess_data, split_data

# ✅ Exposing modules for easy access
__all__ = ["load_data", "preprocess_data", "split_data"]
