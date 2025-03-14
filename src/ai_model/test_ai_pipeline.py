from gui.ai_pipeline import run_selected_model  # Import the function to run only selected model
from data_object_final_edited import DataObject  # Import DataObject

# Create a data_object instance
data_instance = DataObject()

# Step 1: Manually Set Sample Data for Testing
data_instance.data_filtering["Train-Test Split"]["split_data"]["x_train"] = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
data_instance.data_filtering["Train-Test Split"]["split_data"]["x_test"] = [[9, 10, 11]]
data_instance.data_filtering["Train-Test Split"]["split_data"]["y_train"] = [0, 1, 0]
data_instance.data_filtering["Train-Test Split"]["split_data"]["y_test"] = [1]

# Debugging: Print values to confirm assignment
print("\n🔍 Debugging: Checking Assigned Data in DataObject")
for key, value in data_instance.data_filtering["Train-Test Split"]["split_data"].items():
    print(f"{key}: {value}")

# Step 2: Assign Hyperparameters for AI models
ai_model_name = "RandomForest"  # 🔹 Change this to test different models

data_instance.ai_model["selected_model"] = ai_model_name  # Select the model to run

data_instance.ai_model["RandomForest"] = {
    "n_estimators": 10,
    "max_depth": 5,
    "min_samples_split": 2,
    "min_samples_leaf": 1
}

data_instance.ai_model["CatBoost"] = {
    "n_estimators": 100,
    "learning_rate": 0.05,
    "max_depth": 4,
    "reg_lambda": 2
}

data_instance.ai_model["ArtificialNeuralNetwork"] = {
    "layer_number": 2,
    "units": [64, 4],
    "activation": ["relu", "softmax"],
    "optimizer": "adam",
    "batch_size": 32,
    "epochs": 5
}

data_instance.ai_model["XGBoost"] = {
    "n_estimators": 50,
    "learning_rate": 0.1,
    "min_split_loss": 1,
    "max_depth": 3
}

# Step 3: Run the Selected AI Model and Print Results
print(f"\nRunning AI Model: {ai_model_name}...")
selected_model_result = run_selected_model(data_instance)
print(selected_model_result)
