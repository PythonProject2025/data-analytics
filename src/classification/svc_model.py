# File: models/svc_model.py
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV
from classification.base_model import ClassifierClass
from models.data_object_class import DataObject

class SVCModel(ClassifierClass):
    def __init__(self, data_train, data_test, target_train, target_test):
        super().__init__(data_train, data_test, target_train, target_test)
        self.param_grid = {'C': [0.1, 1, 10], 'kernel': ['linear', 'rbf'], 'gamma': ['scale', 'auto']}
        self.model = None

    def train(self):
        grid_search = GridSearchCV(SVC(), self.param_grid, cv=3, scoring='accuracy')
        grid_search.fit(self.data_train, self.target_train)
        data_object = DataObject()
        print(f"Best parameters for SVC: {grid_search.best_params_}")
        #C = float(input("Enter the value for C (e.g., 0.1, 1, 10): "))
        #kernel = input("Enter the kernel type (e.g., 'linear', 'rbf'): ")
        #gamma = input("Enter the gamma value (e.g., 'scale', 'auto'): ")
        C = data_object.classification["SVC"]["C"],
        kernel = data_object.classification["SVC"]["kernel"],
        gamma = data_object.classification["SVC"]["gamma"]

        self.model = SVC(C=C, kernel=kernel, gamma=gamma)
        self.model.fit(self.data_train, self.target_train)

