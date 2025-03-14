from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from .base import BaseModel

class RandomForest(BaseModel):
    """
    A class to implement the Random Forest model for both classification and regression.

    This class extends BaseModel and allows setting hyperparameters dynamically
    while ensuring they fall within valid ranges.

    Attributes:
    -----------
    problem_type : str
        Defines whether the model is for classification or regression.
    options : dict
        Contains hyperparameters such as n_estimators, max_depth, min_samples_split, and min_samples_leaf.
    """
        
    def __init__(self, problem_type="classification", options=None):
        """
        Initializes the RandomForest model with validated hyperparameters.

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
            # Validate and ensure the provided hyperparameters fall within allowed ranges
            validated_options = BaseModel.validate_options(options, "RandomForest")
            
            # Extract validated hyperparameters
            n_estimators = validated_options["n_estimators"]
            max_depth = validated_options["max_depth"]
            min_samples_split = validated_options["min_samples_split"]
            min_samples_leaf = validated_options["min_samples_leaf"]
            
            # Initialize the RandomForest model based on the problem type
            if problem_type == "classification":
                model_instance = RandomForestClassifier(
                n_estimators=n_estimators, # Number of trees in the forest
                max_depth=max_depth, # Maximum depth of the trees
                min_samples_split=min_samples_split, # Min samples required to split a node
                min_samples_leaf=min_samples_leaf, # Min samples required per leaf
                class_weight='balanced' # Automatically adjusts class weights to handle imbalanced data
                )
            elif problem_type == "regression":
                model_instance = RandomForestRegressor(
                n_estimators=n_estimators, # Number of trees in the forest
                max_depth=max_depth, # Maximum depth of the trees
                min_samples_split=min_samples_split, # Min samples required to split a node
                min_samples_leaf=min_samples_leaf # Min samples required per leaf
                )
            else:
                raise ValueError("Only classification or regression are supported")
            
            # Pass the initialized model instance to the BaseModel class\
            super().__init__(model_instance, problem_type)
        
        except Exception as e:
            # Catch and print any errors that occur during initialization
            print(f"Error initializing RandomForest model: {e}")
            raise 
