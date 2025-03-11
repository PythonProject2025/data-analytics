from models.ai_pipeline import run_ai_classification, run_ai_regression
from data_object_final_edited import DataObject  # Import DataObject

# Create a data_object instance
data_object = DataObject()

# 🛠 Step 1: Manually Set Sample Data for Testing
data_object.data_filtering["Train-Test Split"]["split_data"]["x_train"] = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
data_object.data_filtering["Train-Test Split"]["split_data"]["x_test"] = [[9, 10, 11]]
data_object.data_filtering["Train-Test Split"]["split_data"]["y_train"] = [0, 1, 0]
data_object.data_filtering["Train-Test Split"]["split_data"]["y_test"] = [1]

# Debugging: Print values to confirm assignment
print("\n🔍 Debugging: Checking Assigned Data in DataObject")
print("x_train:", data_object.data_filtering["Train-Test Split"]["split_data"]["x_train"])
print("x_test:", data_object.data_filtering["Train-Test Split"]["split_data"]["x_test"])
print("y_train:", data_object.data_filtering["Train-Test Split"]["split_data"]["y_train"])
print("y_test:", data_object.data_filtering["Train-Test Split"]["split_data"]["y_test"])

# Step 2: Assign Hyperparameters for AI models
data_object.ai_model["RandomForest"] = {
    "n_estimators": 10,
    "max_depth": 5,
    "min_samples_split": 2,
    "min_samples_leaf": 1
}

data_object.ai_model["CatBoost"] = {
    "n_estimators": 100,
    "learning_rate": 0.05,
    "max_depth": 4,
    "reg_lambda": 2
}

data_object.ai_model["ArtificialNeuralNetwork"] = {
    "layer_number": 2,
    "units": [64, 4],
    "activation": ["relu", "softmax"],
    "optimizer": "adam",
    "batch_size": 32,
    "epochs": 5
}

data_object.ai_model["XGBoost"] = {
    "n_estimators": 50,
    "learning_rate": 0.1,
    "min_split_loss": 1,
    "max_depth": 3
}

# Step 3: Run AI Models and Print Results
print("\n Running AI Classification Test...")
classification_results = run_ai_classification()
print(classification_results)

print("\n Running AI Regression Test...")
regression_results = run_ai_regression()
print(regression_results)
