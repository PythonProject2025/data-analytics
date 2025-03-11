# Description: This file is the main entry point for the project. It loads the data, trains the models, evaluates the models, and plots the results.
# Importing necessary model classes from their respective modules
from models.random_forest import RandomForest
from models.catboost_model import Catboost
from models.ann import ArtificialNeuralNetwork
from models.xgboost_model import XGBoost

# Importing functions to load datasets
from models.data_loader.data_loader import load_classification_data, load_regression_data

# Defining paths to datasets (Ensure these paths are correct)
classification_path = r"C:\Users\vibho\Documents\Visual studio code\OOPs MAIT\Data for Project\Classification dataset\car+evaluation\car.data"
regression_path = r"C:\Users\vibho\Documents\Visual studio code\OOPs MAIT\Data for Project\Regression datasets\steel+industry+energy+consumption\Steel_industry_data.csv"

# Loading the datasets
classification_data = load_classification_data(classification_path)
regression_data = load_regression_data(regression_path)

# List of models to be trained and evaluated
models = [
    # Random Forest for Classification
    RandomForest(problem_type="classification", options={
            "n_estimators": 200, # Number of trees in the forest
            "max_depth": 20, # Maximum depth of the tree
            "min_samples_split": 5, # Minimum samples required to split an internal node
            "min_samples_leaf": 1 # Minimum samples required at a leaf node
        }), 
    
    # CatBoost for Classification
    Catboost(problem_type="classification", options={
            "n_estimators": 500, # Number of boosting iterations
            "learning_rate": 0.03, # Step size at each iteration
            "max_depth": 6, # Depth of each tree
            "reg_lambda": 3 # Regularization term to prevent overfitting
        }),
    
    # Artificial Neural Network (ANN) for Classification
    ArtificialNeuralNetwork(problem_type="classification", options={
            "layer_number": 3, # Number of hidden layers
            "units": [128, 64, 4], # Neurons in each layer
            "activation": ["relu", "relu", "softmax"], # Activation functions for each layer
            "optimizer": "adam", # Optimization algorithm
            "batch_size": 30, # Number of training samples used in each batch
            "epochs": 100  # Number of times the model sees the entire dataset during training
        }),
    
    # Random Forest for Regression
    RandomForest(problem_type="regression", options={
            "n_estimators": 200, # Number of trees in the forest
            "max_depth": 20, # Maximum depth of the tree
            "min_samples_split": 5, # Minimum samples required to split an internal node
            "min_samples_leaf": 1 # Minimum samples required at a leaf node
        }),
    
    # CatBoost for Regression
    Catboost(problem_type="regression", options={
            "n_estimators": 500, # Number of boosting iterations
            "learning_rate": 0.03, # Step size at each iteration
            "max_depth": 6, # Depth of each tree
            "reg_lambda": 3 # Regularization term to prevent overfitting
        }),
    
    # XGBoost for Regression
    XGBoost(problem_type="regression", options={
            "n_estimators": 200, # Number of trees in the ensemble
            "learning_rate": 0.3, # Step size at each iteration
            "min_split_loss": 10, # Minimum loss required to split a node
            "max_depth": 6 # Depth of each tree
        })
]

# Loop through the models, train, evaluate, and plot the results.
for model in models:
    if model.problem_type == "classification": # If it's a classification model
        model.split_data(classification_data, target_column="car") # Split dataset into train/test
        model.train() # Train the model
        results = model.evaluate() # Evaluate model performance
        print(f'{model.__class__.__name__} ({model.problem_type}): {results}') # Print accuracy and confusion matrix
        model.plot_results() # Plot the confusion matrix
        
    elif model.problem_type == "regression": # If it's a regression model
        model.split_data(regression_data, target_column="Usage_kWh") # Split dataset into train/test
        model.train() # Train the model
        results = model.evaluate() # Evaluate model performance (MAE, MSE, R² score)
        print(f'{model.__class__.__name__} ({model.problem_type}): {results}') # Print regression metrics
        model.plot_results() # Plot the regression results
