# Description: This script allows the user to select a model and problem type, retrieves 
# the default hyperparameters, trains the model, evaluates it, and plots the results.

# Import necessary model classes
from models.random_forest import RandomForest
from models.catboost_model import Catboost
from models.ann import ArtificialNeuralNetwork
from models.xgboost_model import XGBoost
from models.base import BaseModel  # Import BaseModel to fetch default hyperparameters

# Import dataset loading functions
from data_loader.data_loader import load_classification_data, load_regression_data

# Define dataset paths
classification_path = r"C:\Users\vibho\Documents\Visual studio code\OOPs MAIT\Data for Project\Classification dataset\car+evaluation\car.data"
regression_path = r"C:\Users\vibho\Documents\Visual studio code\OOPs MAIT\Data for Project\Regression datasets\steel+industry+energy+consumption\Steel_industry_data.csv"

# Load datasets
classification_data = load_classification_data(classification_path)
regression_data = load_regression_data(regression_path)

# Available models
available_models = {
    "RandomForest": RandomForest,
    "CatBoost": Catboost,
    "ArtificialNeuralNetwork": ArtificialNeuralNetwork,
    "XGBoost": XGBoost
}

# Available problem types
problem_types = {
    "classification": ["RandomForest", "CatBoost", "ArtificialNeuralNetwork"],
    "regression": ["RandomForest", "CatBoost", "XGBoost"]
}

# Prompt user to select a model
print("\nAvailable models: RandomForest, CatBoost, ArtificialNeuralNetwork, XGBoost")
selected_model_name = input("Enter the model name you want to run: ").strip()

# Check if the selected model is valid
if selected_model_name not in available_models:
    print(f"❌ Error: '{selected_model_name}' is not a recognized model!")
    exit()

# Prompt user to select the problem type
print("\nAvailable problem types: classification, regression")
selected_problem_type = input("Enter the problem type: ").strip().lower()

# Validate problem type
if selected_problem_type not in problem_types:
    print(f"❌ Error: '{selected_problem_type}' is not a recognized problem type!")
    exit()

# Ensure the selected model supports the chosen problem type
if selected_model_name not in problem_types[selected_problem_type]:
    print(f"❌ Error: '{selected_model_name}' does not support {selected_problem_type}!")
    exit()

# Fetch default hyperparameters for the selected model
default_hyperparameters = BaseModel.validate_options({}, selected_model_name)

# Initialize the selected model with validated default hyperparameters
model_class = available_models[selected_model_name]

# Determine which dataset to use
if selected_problem_type == "classification":
    dataset, target_column = classification_data, "car"
elif selected_problem_type == "regression":
    dataset, target_column = regression_data, "Usage_kWh"

# Check if dataset was properly loaded
if dataset is None:
    print(f"❌ Error: Failed to load dataset for {selected_model_name} ({selected_problem_type})!")
    exit()

# Initialize the model
model = model_class(problem_type=selected_problem_type, options=default_hyperparameters)

# Split data
model.split_data(dataset, target_column)

# Train the model
model.train()

# Evaluate the model
results = model.evaluate()

# Fix confusion matrix issue (convert to list if available)
if "Confusion Matrix" in results:
    results["Confusion Matrix"] = results["Confusion Matrix"]

# Print evaluation results
print(f"\n✅ {selected_model_name} ({selected_problem_type}) Results: {results}")

# Plot results
model.plot_results()