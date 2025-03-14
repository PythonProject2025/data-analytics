"""
This package contains GUI components for user interaction with AI models.

Modules:
--------
- ai_pipeline_ui: Gradio interface for selecting and running AI models.
"""

from .ai_pipeline import run_selected_model

# Exposing UI components for easy import
__all__ = ["run_selected_model"]
