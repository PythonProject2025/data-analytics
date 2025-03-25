import pandas as pd
from sklearn.model_selection import train_test_split
from models.data_object_class import DataObject
from sklearn.metrics import (
    mean_squared_error, 
    mean_absolute_error, 
    r2_score, 
    accuracy_score, 
    confusion_matrix
)
import matplotlib.pyplot as plt
import seaborn as sns
dataObj = DataObject()
class BaseModel:
    """
    Base class for all models that centralizes hyperparameter validation 
    and common functionalities like data splitting, training, and evaluation.
    
    Attributes:
    -----------
    HYPERPARAMETER_RANGES : dict
        Defines the valid range of hyperparameters for different model types.
    """

    # Dictionary defining allowed hyperparameter ranges for different model types
    HYPERPARAMETER_RANGES = {
        "RandomForest": {
            "n_estimators": {"min": 10, "max": 500, "default": 200},
            "max_depth": {"min": 3, "max": 50, "default": 20},
            "min_samples_split": {"min": 4, "max": 10, "default": 5},
            "min_samples_leaf": {"min": 1, "max": 10, "default": 1}
        },
        "CatBoost": {
            "n_estimators": {"min": 100, "max": 1000, "default": 500},
            "learning_rate": {"min": 0.01, "max": 0.1, "default": 0.03},
            "max_depth": {"min": 4, "max": 10, "default": 6},
            "reg_lambda": {"min": 1, "max": 10, "default": 3}
        },
        "ArtificialNeuralNetwork": {
            "layer_number": {"min": 1, "max": 6, "default": 3},
            "units": {"min": 1, "max": 256, "default": [128, 64, 4]},
            "activation": {"allowed": ["relu", "sigmoid", "tanh", "softmax"], "default": ["relu", "relu", "softmax"]},
            "optimizer": {"allowed": ["adam", "sgd", "rmsprop"], "default": "adam"},
            "batch_size": {"min": 16, "max": 128, "default": 30},
            "epochs": {"min": 10, "max": 300, "default": 100}
        },
        "XGBoost": {
            "n_estimators": {"min": 100, "max": 1000, "default": 200},
            "learning_rate": {"min": 0.01, "max": 0.3, "default": 0.3},
            "min_split_loss": {"min": 3, "max": 10, "default": 10},
            "max_depth": {"min": 0, "max": 10, "default": 6}
        }
    }
    
    @staticmethod
    def validate_options(options, model_type):
        """
        Validates and ensures that the provided hyperparameters fall within allowed ranges.
        
        Parameters:
        -----------
        options : dict
        The dictionary containing model hyperparameters.
        model_type : str
        The type of model being validated.
        
        Returns:
        --------
        dict
        A dictionary of validated hyperparameters with out-of-range values replaced with defaults.
        """
        try:
            # Retrieve hyperparameter rules for the given model
            rules = BaseModel.HYPERPARAMETER_RANGES.get(model_type, {})
            validated = {}  # Always return a valid dictionary
            for key, rule in rules.items():
                # Prioritize user-selected values, fallback to defaults if missing
                value = options.get(key, rule.get("default")) if options else rule.get("default")
                # Handle cases where rule is a dictionary with "min" and "max"
                if isinstance(rule, dict):
                    if "min" in rule and "max" in rule:
                        if isinstance(value, list):  # Validate list values individually
                            validated[key] = [v if rule["min"] <= v <= rule["max"] else rule["default"] for v in value]
                        else:
                            validated[key] = value if rule["min"] <= value <= rule["max"] else rule["default"]
                    
                    # Handle categorical options (e.g., activation functions)
                    elif "allowed" in rule:
                        validated[key] = value if value in rule["allowed"] else rule["default"]
                    else:
                        validated[key] = value  # Directly assign if no validation rule applies
                else:
                    validated[key] = value  # Directly assign if rule is not a dictionary
                    
            return validated if validated else rules  # Always return valid hyperparameter dictionary
        
        except Exception as e:
            print(f"Error validating hyperparameters: {e}")
            return options  # Return the original options if validation fails



    def __init__(self, model, problem_type="classification"):
        """
        Initializes the BaseModel with a given model and problem type.

        Parameters:
        -----------
        model : obj
            The ML model instance (e.g., RandomForestClassifier, ANN, etc.).
        problem_type : str
            The type of problem (either "classification" or "regression").
        """        
        self.model = model
        self.problem_type = problem_type
        self.X_train, self.X_test, self.y_train, self.y_test = None, None, None, None

    # def split_data(self, data, target_column, test_size=0.2):
    #     """
    #     Splits the given dataset into training and testing sets.

    #     Parameters:
    #     -----------
    #     data : pd.DataFrame
    #         The dataset containing features and target values.
    #     target_column : str
    #         The column name of the target variable.
    #     test_size : float
    #         The proportion of data to be used for testing.
    #     """
    #     try:
    #         target_column = dataObj["parameters"]["target_column"]
    #         test_size = dataObj["parameters"]["test_size"]
    #         random_state = dataObj["parameters"]["random_state"]            
    #         X = data.drop(columns=[target_column])  # Features
    #         y = data[target_column]  # Target variable
    #         self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
    #             X, y, test_size=test_size, random_state=42
    #         )
    #     except KeyError:
    #         print(f"Error: Column '{target_column}' not found in dataset.")
    #     except Exception as e:
    #         print(f"Unexpected error in data splitting: {e}")

    def train(self, X_train, y_train):
        """
        Trains the model using the training data.
        """       
        try:
            self.X_train = X_train
            self.y_train = y_train
            # self.y_train=self.y_train.values.reshape(-1,1)
            # self.X_train=dataObj["split_data"]["X_train"]
            # self.y_train=dataObj["y_train"]            
            if self.X_train is None or self.y_train is None:
                raise ValueError("Training data is missing. Ensure data is loaded and split correctly.")
            self.model.fit(self.X_train,self.y_train)
        except Exception as e:
            print(f"Error during model training: {e}")

    def evaluate(self, X_test, y_test):
        """
        Evaluates the trained model on the test data.

        Returns:
        --------
        dict
            A dictionary containing evaluation metrics (accuracy for classification, error metrics for regression).
        """        
        try:
            # self.X_test=dataObj["split_data"]["X_test"]
            # self.y_test=dataObj["split_data"]["y_test"]
            self.X_test = X_test
            self.y_test = y_test
            self.predictions = self.model.predict(self.X_test)
            if self.problem_type == "classification":
                self.accuracy = accuracy_score(self.y_test, self.predictions)
                self.conf_matrix = confusion_matrix(self.y_test, self.predictions)
                print(self.accuracy)
                print(self.conf_matrix)
                return {"Accuracy": self.accuracy, "Confusion Matrix": self.conf_matrix.tolist()}
            elif self.problem_type == "regression":
                mae = mean_absolute_error(self.y_test, self.predictions)
                mse = mean_squared_error(self.y_test, self.predictions)
                r2 = r2_score(self.y_test, self.predictions)
                return {"MAE": mae, "MSE": mse, "R2": r2}
            else:
                raise ValueError("Unsupported problem type.")
        except Exception as e:
            print(f"Error during model evaluation: {e}")
            return {}

    def plot_results(self):
        """
        Generates plots for classification (confusion matrix) and regression (scatter plot of predictions).
        """        
        try:
            if self.problem_type == "classification":
                sns.heatmap(self.conf_matrix, annot=True, fmt="d", cmap="Blues")
                plt.xlabel("Predicted")
                plt.ylabel("Actual")
                plt.title("Confusion Matrix")
                plt.show()
            elif self.problem_type == "regression":
                plt.scatter(self.y_test, self.predictions, alpha=0.5)
                plt.plot([self.y_test.min(), self.y_test.max()],
                         [self.y_test.min(), self.y_test.max()],
                         "r--", lw=2)
                plt.xlabel("Actual")
                plt.ylabel("Predicted")
                plt.title("Regression Results")
                plt.show()
        except Exception as e:
            print(f"Error during result plotting: {e}")
