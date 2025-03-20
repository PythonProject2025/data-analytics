# File: models/knn_model.py
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import GridSearchCV
from classification.base_model import ClassifierClass
from models.data_object_class import DataObject

class KNNModel(ClassifierClass):
    def __init__(self, data_train, data_test, target_train, target_test,n_neighbours,p):
        super().__init__(data_train, data_test, target_train, target_test)
        self.param_grid = {'n_neighbors': [3, 5, 7], 'weights': ['uniform', 'distance'], 'p': [1, 2]}
        self.model = None
        self.n_neighbours=n_neighbours
        self.p=p

    def train(self):
        grid_search = GridSearchCV(KNeighborsClassifier(metric='minkowski'), self.param_grid, cv=3, scoring='accuracy')
        grid_search.fit(self.data_train, self.target_train)
        print(f"Best parameters for KNN: {grid_search.best_params_}")
        data_object=DataObject()
        #n_neighbors = int(input("Enter the number of neighbors (e.g., 3, 5, 7): "))
        #weights = input("Enter the weight function (e.g., 'uniform', 'distance'): ")
        #p = int(input("Enter the power parameter (e.g., 1, 2): "))
        weights = data_object.classification["KNN"]["weights"]

        self.model = KNeighborsClassifier(n_neighbors=self.n_neighbours, weights=weights, p=self.p)
        self.model.fit(self.data_train, self.target_train)