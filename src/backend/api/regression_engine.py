import numpy as np
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import pandas as pd
from regression.metrics import metrics
from regression.regression_models import RegressionModels
from models.data_object_class import DataObject

class RegressionAPIView(APIView):
    def post(self, request):
        data_dict = request.data.get("dataobject", {})

        if not data_dict:
            return Response({"error": "Invalid request, 'dataobject' missing"}, status=status.HTTP_400_BAD_REQUEST)

        # Extract train-test split data
        data_object = DataObject()
        data_object.data_filtering = data_dict.get("data_filtering", {})
        data_object.regression = data_dict.get("regression", {})
        try:
            split_data=data_object.data_filtering["Train-Test Split"]["split_data"]

            # ✅ Ensure all keys exist before conversion
            if not all(k in split_data for k in ["X_train", "X_test", "y_train", "y_test"]):
                return {"error": "Missing one or more training/testing data in DataObject!"}

            # ✅ Convert lists (from JSON) back to NumPy arrays
            X_train = np.array([list(d.values()) for d in split_data["X_train"]]) if split_data["X_train"] else None
            X_test = np.array([list(d.values()) for d in split_data["X_test"]]) if split_data["X_test"] else None
            y_train = np.array(split_data["y_train"]) if split_data["y_train"] else None
            y_test = np.array(split_data["y_test"]) if split_data["y_test"] else None

            # ✅ Check if data is valid before proceeding
            if any(val is None or (isinstance(val, np.ndarray) and val.size == 0) for val in [X_train, X_test, y_train, y_test]):
                return {"error": "Some train-test data is empty or invalid!"}
            print(X_train)
        except KeyError:
            return {"error": "Missing training/testing data in DataObject!"}

        # Extract regression model selection
        regression_models = RegressionModels()
        model_type = data_object.regression["Selected Model"]
        if model_type == "Linear Regression":
            # Linear Regression
            model = regression_models.train_linear_regression(data_object.data_filtering['Train-Test Split']) # 1st change x_train, y_train 
            r2, y_pred = metrics.evaluate_model(model, data_object.data_filtering['Train-Test Split'])  # 2nd change x_test, y_test 
            data_object.outputs['Regression']['Linear_Regression']['r2_score_linear'] = r2
            data_object.outputs['Regression']['Linear_Regression']['graph_params']['y_pred'] = y_pred
    
        # Polynomial Regression
        elif model_type == "Polynomial Regression":             
            param_grid = {'polynomial_features__degree': data_object.regression['Model_Selection']['Polynomial Regression']['polynomial_degree']}
            model = regression_models.train_polynomial_regression(data_object.data_filtering['Train-Test Split'], param_grid=param_grid) # 1st change x_train,y_train 
            print(f"Best HyperParameter(Polynomial) ==> Degree: {regression_models.best_params_poly['polynomial_features__degree']}")
            r2, y_pred = metrics.evaluate_model(model, data_object.data_filtering['Train-Test Split']) # 2nd change x_test, y_test 
            data_object.outputs['Regression']['Polynomial_Regression']['r2_score_polynomial'] = r2
            data_object.outputs['Regression']['Polynomial_Regression']['graph_params']['y_pred'] = y_pred
            data_object.outputs['Regression']['Polynomial_Regression']['best_polynomial_degree'] = regression_models.best_params_poly['polynomial_features__degree']
            
            print(f"regression completed successfully")
            print(data_object.outputs['Regression']['Polynomial_Regression']['r2_score_polynomial'])
            print(data_object.outputs['Regression']['Polynomial_Regression']['graph_params']['y_pred'])
            print(data_object.outputs['Regression']['Polynomial_Regression']['best_polynomial_degree'])
        #    polynomial_plot(x_test["Datum"], y_test, y_pred, "Datum", "pH-Wert", regression_models.best_params_poly['polynomial_features__degree']) ==>  How labels will be handeled and which group will handle it?
        
        elif model_type == "Ridge Regression":     
            # Ridge Regression   
            param_grid = {
                'polynomial_features__degree': data_object.regression['Model_Selection']['Ridge_Regression']['polynomial_degree_ridge'],
                'ridge_regression__alpha': data_object.regression['Model_Selection']['Ridge_Regression']['alpha_values_ridge']
            }
            model = regression_models.train_ridge(data_object.data_filtering['Train-Test Split'], param_grid=param_grid) # 1st change x_train,y_train 
            print("Best HyperParameters(Ridge) ==> alpha:", regression_models.best_params_ridge['ridge_regression__alpha'],
               ", Polynomial Degree:", regression_models.best_params_ridge['polynomial_features__degree'])
            r2, y_pred = metrics.evaluate_model(model, data_object.data_filtering['Train-Test Split']) # 2nd change x_test, y_test 
            data_object.outputs['Regression']['Ridge_Regression']['r2_score_ridge'] = r2
            data_object.outputs['Regression']['Ridge_Regression']['best_degree_ridge'] = regression_models.best_params_ridge['polynomial_features__degree']
            data_object.outputs['Regression']['Ridge_Regression']['best_alpha_ridge'] = regression_models.best_params_ridge['ridge_regression__alpha']
        #    print(f"R2 Score (Ridge Regression): {r2}") Remove Later
            data_object.outputs['Regression']['Ridge_Regression']['graph_params']['regression_models'] = regression_models
        #    ridge_plot(regression_models)
        
        elif model_type == "Lasso Regression": 
            # Lasso Regression
            param_grid = {
                'polynomial_features__degree': data_object.regression['Model_Selection']['Lasso_Regression']['polynomial_degree_lasso'],
                'lasso_regression__alpha': data_object.regression['Model_Selection']['Lasso_Regression']['alpha_values_lasso']
            }
            model = regression_models.train_lasso(data_object.data_filtering['Train-Test Split'], param_grid=param_grid) # 1st change x_train,y_train 
        #    print("Best HyperParameters(Lasso) ==> alpha:", regression_models.best_params_lasso['lasso_regression__alpha'],
        #        ", Polynomial Degree:", regression_models.best_params_lasso['polynomial_features__degree'])
            r2, y_pred = metrics.evaluate_model(model, data_object.data_filtering['Train-Test Split']) # 2nd change x_test, y_test
            data_object.outputs['Regression']['Lasso_Regression']['r2_score_lasso'] = r2
            data_object.outputs['Regression']['Lasso_Regression']['best_degree_lasso'] = regression_models.best_params_lasso['polynomial_features__degree']
            data_object.outputs['Regression']['Lasso_Regression']['best_alpha_lasso'] = regression_models.best_params_lasso['lasso_regression__alpha']
        #    print(f"R2 Score (Lasso Regression): {r2}")
            data_object.outputs['Regression']['Lasso_Regression']['graph_params']['regression_models'] = regression_models
        #    lasso_plot(regression_models)
        
        
        return Response(data_object.outputs, status=status.HTTP_200_OK)
