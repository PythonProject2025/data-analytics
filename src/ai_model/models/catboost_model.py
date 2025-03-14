from catboost import CatBoostClassifier, CatBoostRegressor
from .base import BaseModel

class Catboost(BaseModel):
    """
    A class to implement the CatBoost model for both classification and regression.

    This class extends BaseModel and allows setting hyperparameters dynamically
    while ensuring they fall within valid ranges.

    Attributes:
    -----------
    problem_type : str
        Defines whether the model is for classification or regression.
    options : dict
        Contains hyperparameters such as n_estimators, learning_rate, max_depth, and reg_lambda.
    """
    
    def __init__(self, problem_type="classification", options=None):
        """
        Initializes the CatBoost model with validated hyperparameters.

        Parameters:
        -----------
        problem_type : str, default="classification"
            Defines whether the model is for classification or regression.
        options : dict, optional
            A dictionary containing model hyperparameters.
        """
        
        if options is None:
            options = {} # If no options are provided, use an empty dictionary
        
        try:
            validated_options = BaseModel.validate_options(options, "CatBoost")  # Ensure correct key!
      
            # Extract validated hyperparameters
            n_estimators = validated_options["n_estimators"]
            learning_rate = validated_options["learning_rate"]
            max_depth = validated_options["max_depth"]
            reg_lambda = validated_options["reg_lambda"]
            
            # Initialize the CatBoost model based on the specified problem type
            if problem_type == "classification":
                model_instance = CatBoostClassifier(
                n_estimators=n_estimators,       # Number of boosting iterations
                max_depth=max_depth,             # Maximum depth of the trees
                learning_rate=learning_rate,     # Learning rate for gradient boosting
                reg_lambda=reg_lambda,           # Regularization term to prevent overfitting
                auto_class_weights='Balanced',   # Automatically balance classes for imbalanced datasets
                verbose=False                    # Suppress unnecessary logging
                )
            
            elif problem_type == "regression":
                model_instance = CatBoostRegressor(
                n_estimators=n_estimators,
                max_depth=max_depth,
                learning_rate=learning_rate,
                reg_lambda=reg_lambda,
                verbose=False # Disables unnecessary logging during training
                )
            else:
                # If an unsupported problem type is provided, raise an error
                raise ValueError("Only classification or regression are supported")
            
            # Call the parent class constructor to initialize the BaseModel with the model instance
            super().__init__(model_instance, problem_type)
            
        except Exception as e:
            # If any error occurs during initialization, print the error and re-raise it
            print(f"Error initializing Catboost model: {e}")
            raise