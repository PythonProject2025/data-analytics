"""
Class DataHandler is used for loading from a csv file into a dataframe
and splitting dataset into training and testing data.
"""

import pandas as pd
from sklearn.model_selection import train_test_split


class DataHandler:
    def __init__(self, file_path=None, target_variable=None):
        self.file_path = file_path
        self.target_variable = target_variable
        self.data = None
        self.x = None
        self.y = None

    def set_file_path(self, file_path):
        self.file_path = file_path

    def set_target_variable(self, target_variable):
        self.target_variable = target_variable

    def load_data(self):
        self.data = pd.read_csv(self.file_path)
        self.data = self.data.drop(0, axis=0).reset_index(
            drop=True
        )  # only for testing, use correct exception handling before prod
        self.y = self.data[self.target_variable]
        self.x = self.data.drop(self.target_variable, axis=1)
        return self.x, self.y

    def split_data(self, test_size=0.2, random_state=None):
        return train_test_split(
            self.x,
            self.y,
            test_size=test_size,
        )  # Random state removed from return due to matrix shape error, validate and add again.