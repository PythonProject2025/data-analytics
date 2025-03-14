# File: models/random_forest_model.py
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from base_model import ClassifierClass
from models.data_object_class import DataObject

class RandomForestModel(ClassifierClass):
    def __init__(self, data_train, data_test, target_train, target_test, target_labels):
        super().__init__(data_train, data_test, target_train, target_test, target_labels)
        self.param_grid = {'n_estimators': [50, 100, 150], 'max_depth': [5, 10, 20]}
        self.model = None

    def train(self):
        grid_search = GridSearchCV(RandomForestClassifier(random_state=42), self.param_grid, cv=3, scoring='accuracy')
        grid_search.fit(self.data_train, self.target_train)
        
        data_object = DataObject()

        print(f"Best parameters for RandomForest: {grid_search.best_params_}")
        #n_estimators = int(input("Enter the number of estimators (e.g., 50, 100, 150): "))
        #max_depth = int(input("Enter the maximum depth (e.g., 5, 10, 20): "))
        n_estimators=data_object.classification["RandomForest"]["n_estimators"]
        max_depth=data_object.classification["RandomForest"]["max_depth"]
        random_state=42
        

        self.model = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth, random_state=42)
        self.model.fit(self.data_train, self.target_train)

