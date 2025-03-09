# data_processing.py
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

def load_and_preprocess_data(filepath):
    # Load the data
    data = pd.read_csv(filepath, header=None)

    # Define column names
    data.columns = ["buying", "maint", "doors", "persons", "lug_boot", "safety", "class"]

    # Encode categorical features and target variable
    label_encoders = {col: LabelEncoder().fit(data[col]) for col in data.columns}
    data = data.apply(lambda col: label_encoders[col.name].transform(col))

    # Extract the unique labels for the target variable
    target_labels = label_encoders["class"].classes_

    # Separate features and target, then split the data
    X, y = data.iloc[:, :-1], data.iloc[:, -1]
    data_train, data_test, target_train, target_test = train_test_split(X, y, test_size=0.2, random_state=42)

    return data_train, data_test, target_train, target_test, target_labels


