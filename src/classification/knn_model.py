# File: models/knn_model.py
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import GridSearchCV
from base_model import ClassifierClass
from models.data_object_class import DataObject

class KNNModel(ClassifierClass):
    def __init__(self, data_train, data_test, target_train, target_test, target_labels):
        super().__init__(data_train, data_test, target_train, target_test, target_labels)
        self.param_grid = {'n_neighbors': [3, 5, 7], 'weights': ['uniform', 'distance'], 'p': [1, 2]}
        self.model = None

    def train(self):
        grid_search = GridSearchCV(KNeighborsClassifier(metric='minkowski'), self.param_grid, cv=3, scoring='accuracy')
        grid_search.fit(self.data_train, self.target_train)
        data_object = DataObject()
        print(f"Best parameters for KNN: {grid_search.best_params_}")
        #n_neighbors = int(input("Enter the number of neighbors (e.g., 3, 5, 7): "))
        #weights = input("Enter the weight function (e.g., 'uniform', 'distance'): ")
        #p = int(input("Enter the power parameter (e.g., 1, 2): "))
        n_neighbors = data_object.classification["KNN"]["n_neighbors"],
        weights = data_object.classification["KNN"]["weights"],
        p = data_object.classification["KNN"]["p"]

        self.model = KNeighborsClassifier(n_neighbors=n_neighbors, weights=weights, p=p)
        self.model.fit(self.data_train, self.target_train)