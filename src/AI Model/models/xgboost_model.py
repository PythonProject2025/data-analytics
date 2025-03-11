from xgboost import XGBRegressor
from .base import BaseModel

class XGBoost(BaseModel):
    """
    A class to implement the XGBoost model for regression.

    This class extends BaseModel and allows setting hyperparameters dynamically
    while ensuring they fall within valid ranges.

    Attributes:
    -----------
    problem_type : str
        Defines the type of problem being solved (only regression supported).
    options : dict
        Contains hyperparameters such as n_estimators, learning_rate, min_split_loss, and max_depth.
    """    
    def __init__(self, problem_type="regression", options=None):
        """
        Initializes the XGBoost model with validated hyperparameters.

        Parameters:
        -----------
        problem_type : str, default="regression"
            Defines whether the model is for regression (classification is not supported).
        options : dict, optional
            A dictionary containing model hyperparameters.
        """
        
        # Ensure that only regression is supported in this implementation
        if problem_type != "regression":
            raise ValueError("XGBoost supports only regression in this implementation")
        
        # Ensure options is a dictionary if not provided
        if options is None:
            options = {} # If no options are provided, use an empty dictionary
        
        try:
            # Validate and ensure the provided hyperparameters fall within allowed ranges
            validated_options = BaseModel.validate_options(options, "XGBoost")
            
            # Extract validated hyperparameters
            n_estimators = validated_options["n_estimators"] # Number of boosting rounds (trees)
            learning_rate = validated_options["learning_rate"] # Step size shrinkage to prevent overfitting
            min_split_loss = validated_options["min_split_loss"] # Minimum loss reduction required for further partitioning
            max_depth = validated_options["max_depth"] # Maximum depth of a tree
            
            # Initialize the XGBoost regression model with validated hyperparameters
            model_instance = XGBRegressor(
                n_estimators=n_estimators,
                learning_rate=learning_rate,
                min_split_loss=min_split_loss,
                max_depth=max_depth
            )
            
            # Pass the initialized model instance to the BaseModel class
            super().__init__(model_instance, problem_type)

        except Exception as e:
            # Catch and print any errors that occur during initialization
            print(f"Error initializing XGBoost model: {e}")
            raise
