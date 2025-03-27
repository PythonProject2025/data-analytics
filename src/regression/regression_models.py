"""
Contains regression models alongwith hyperparameter tuning.
"""

from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline,Pipeline
from sklearn.model_selection import GridSearchCV
import numpy as np

class RegressionModels:
    def __init__(self):
        self.model = None
        self.best_params = None

    def train_linear_regression(self, dataobj): # x_train, y_train
        """
        Train a Linear Regression model.
        """
        self.model = LinearRegression()
        self.model.fit(dataobj['split_data']['X_train'], dataobj['split_data']['y_train'])
        return self.model
    
    def train_polynomial_regression(self, dataobj, param_grid=None, cv=3): # x_train, y_train
        print(type(dataobj['split_data']['X_train']))
        estimator = Pipeline([("polynomial_features", PolynomialFeatures()),("linear_regression", LinearRegression())])
        grid_search = GridSearchCV(estimator=estimator, param_grid=param_grid, cv=cv, scoring="r2")
        grid_search.fit(dataobj['split_data']['X_train'], dataobj['split_data']['y_train'])
        self.model = grid_search.best_estimator_
        self.best_params_poly = grid_search.best_params_

        return self.model

 
    def train_ridge(self, dataobj, param_grid=None, cv=3, subsample_ratio=0.3): # x_train, y_train
        
        # x_train, y_train
        X_train = dataobj["split_data"]["X_train"]
        y_train = dataobj["split_data"]["y_train"]

        # Subsample the data for hyperparameter tuning
        n_samples = X_train.shape[0]
        subsample_size = int(subsample_ratio * n_samples)
        subsample_indices = np.random.choice(n_samples, subsample_size, replace=False)
        X_train_sub = X_train.iloc[subsample_indices]
        y_train_sub = y_train.iloc[subsample_indices]
                
        ridge_pipeline = Pipeline([
        ("polynomial_features", PolynomialFeatures()),
        ("ridge_regression", Ridge(max_iter=2000,tol=1e-2))
        ])
        grid_search = GridSearchCV(estimator=ridge_pipeline, param_grid=param_grid, cv=cv, scoring="r2")
        grid_search.fit(X_train_sub,y_train_sub)
        #grid_search.fit(dataobj['split_data']['X_train'], dataobj['split_data']['y_train'])
        self.model = grid_search.best_estimator_
        self.best_params_ridge = grid_search.best_params_
        self.results_ridge = grid_search.cv_results_
        self.best_degree_ridge = self.best_params_ridge['polynomial_features__degree']

        return self.model

    def train_lasso(self, dataobj, param_grid=None, cv=3, subsample_ratio=0.3): # x_train, y_train
            
            # x_train, y_train
            X_train = dataobj["split_data"]["X_train"]
            y_train = dataobj["split_data"]["y_train"]

            # Subsample the data for hyperparameter tuning
            n_samples = X_train.shape[0]
            subsample_size = int(subsample_ratio * n_samples)
            subsample_indices = np.random.choice(n_samples, subsample_size, replace=False)
            X_train_sub = X_train.iloc[subsample_indices]
            y_train_sub = y_train.iloc[subsample_indices]
    
                
            lasso_pipeline = Pipeline([
            ("polynomial_features", PolynomialFeatures()),
            ("lasso_regression", Lasso(max_iter=2000,tol=1e-2))
            ])    
            
            grid_search = GridSearchCV(estimator=lasso_pipeline, param_grid=param_grid, cv=cv, scoring="r2")
            grid_search.fit(X_train_sub,y_train_sub)
            #grid_search.fit(dataobj['split_data']['X_train'], dataobj['split_data']['y_train'])
            self.model = grid_search.best_estimator_
            self.best_params_lasso = grid_search.best_params_
            self.results_lasso = grid_search.cv_results_
            self.best_degree_lasso = self.best_params_lasso['polynomial_features__degree']

            return self.model
