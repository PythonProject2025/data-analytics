import numpy as np
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import pandas as pd
from regression import metrics
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
            if not all(k in split_data for k in ["X_train", "X_test", "y_train", "y_test"]):
                return {"error": "Missing one or more training/testing data in DataObject!"}

           
            X_train_list = data_object.data_filtering["Train-Test Split"]["split_data"]["X_train"]
            X_test_list = data_object.data_filtering["Train-Test Split"]["split_data"]["X_test"]
            y_train_list = data_object.data_filtering["Train-Test Split"]["split_data"]["y_train"]
            y_test_list = data_object.data_filtering["Train-Test Split"]["split_data"]["y_test"]
  
            X_train = pd.DataFrame(X_train_list)
            X_test=  pd.DataFrame(X_test_list)
            y_train= pd.DataFrame(y_train_list)
            y_test= pd.DataFrame(y_test_list)
            
            data_object.data_filtering["Train-Test Split"]["split_data"]["X_train"]=X_train
            data_object.data_filtering["Train-Test Split"]["split_data"]["X_test"]=X_test
            data_object.data_filtering["Train-Test Split"]["split_data"]["y_train"]=y_train
            data_object.data_filtering["Train-Test Split"]["split_data"]["y_test"]=y_test
            if any(val is None or (isinstance(val, np.ndarray) and val.size == 0) for val in [X_train, X_test, y_train, y_test]):
                return {"error": "Some train-test data is empty or invalid!"}
        except KeyError:
            return {"error": "Missing training/testing data in DataObject!"}

        # Extract regression model selection
        regression_models = RegressionModels()
        model_type = data_object.regression["Selected Model"]
        
# Linear Regression        
        
        if model_type == "Linear Regression":
            
            model = regression_models.train_linear_regression(data_object.data_filtering['Train-Test Split']) 
            r2, y_pred = metrics.evaluate_model(model, data_object.data_filtering['Train-Test Split'])   
            data_object.outputs['Regression']['Linear_Regression']['r2_score_linear'] = r2
            data_object.outputs['Regression']['Linear_Regression']['graph_params']['y_pred'] = y_pred
            response_data={
                "r2_score_linear": data_object.outputs['Regression']['Linear_Regression']['r2_score_linear'],
                "y_pred":  data_object.outputs['Regression']['Linear_Regression']['graph_params']['y_pred'],
                "y_test":  data_object.data_filtering['Train-Test Split']['split_data']['y_test'],
                "x_label": data_object.outputs['Regression']['Linear_Regression']['graph_params']['x_label'],
                "y_label": data_object.outputs['Regression']['Linear_Regression']['graph_params']['y_label']         
            }
    
# Polynomial Regression

        elif model_type == "Polynomial Regression":   
                      
            param_grid = {'polynomial_features__degree': data_object.regression['Model_Selection']['Polynomial Regression']['polynomial_degree']}
            
            model = regression_models.train_polynomial_regression(data_object.data_filtering['Train-Test Split'], param_grid=param_grid) 
            r2, y_pred = metrics.evaluate_model(model, data_object.data_filtering['Train-Test Split']) 
            data_object.outputs['Regression']['Polynomial_Regression']['r2_score_polynomial'] = r2
            data_object.outputs['Regression']['Polynomial_Regression']['graph_params']['y_pred'] = y_pred
            data_object.outputs['Regression']['Polynomial_Regression']['best_polynomial_degree'] = regression_models.best_params_poly['polynomial_features__degree']
            
            response_data = {
                "r2_score_polynomial": data_object.outputs['Regression']['Polynomial_Regression']['r2_score_polynomial'],
                "y_pred": data_object.outputs['Regression']['Polynomial_Regression']['graph_params']['y_pred'],
                "best_polynomial_degree": data_object.outputs['Regression']['Polynomial_Regression']['best_polynomial_degree'],
                #"x_data":  data_object.data_filtering['Train-Test Split']['split_data']['X_test']['Safety_high'],  # x_label is given by User
                "y_test":  data_object.data_filtering['Train-Test Split']['split_data']['y_test'],
                "x_label": data_object.outputs['Regression']['Polynomial_Regression']['graph_params']['x_label'],
                "y_label": data_object.outputs['Regression']['Polynomial_Regression']['graph_params']['y_label']           
            }
        #    polynomial_plot(x_test["Datum"], y_test, y_pred, "Datum", "pH-Wert", regression_models.best_params_poly['polynomial_features__degree']) ==>  How labels will be handeled and which group will handle it?

# Ridge Regression
        
        elif model_type == "Ridge Regression":     
            param_grid = {
                'polynomial_features__degree': data_object.regression['Model_Selection']['Ridge Regression']['polynomial_degree_ridge'],
                'ridge_regression__alpha': data_object.regression['Model_Selection']['Ridge Regression']['alpha_values_ridge']
            }
            
            model = regression_models.train_ridge(data_object.data_filtering['Train-Test Split'], param_grid=param_grid) 
            r2, y_pred = metrics.evaluate_model(model, data_object.data_filtering['Train-Test Split'])  
            data_object.outputs['Regression']['Ridge_Regression']['r2_score_ridge'] = r2
            data_object.outputs['Regression']['Ridge_Regression']['best_degree_ridge'] = regression_models.best_params_ridge['polynomial_features__degree']
            data_object.outputs['Regression']['Ridge_Regression']['best_alpha_ridge'] = regression_models.best_params_ridge['ridge_regression__alpha']
            data_object.outputs['Regression']['Ridge_Regression']['graph_params']['results_ridge'] = regression_models.results_ridge        # Add "results_ridge" in DataObject File
            
            response_data = {
                "r2_score_ridge": data_object.outputs['Regression']['Ridge_Regression']['r2_score_ridge'],
                "best_degree_ridge": data_object.outputs['Regression']['Ridge_Regression']['best_degree_ridge'],
                "best_alpha_ridge": data_object.outputs['Regression']['Ridge_Regression']['best_alpha_ridge'],
                "results_ridge": data_object.outputs['Regression']['Ridge_Regression']['graph_params']['results_ridge'],   # Add "results_ridge" in DataObject File
                "Ridge_Regression": data_object.outputs['Regression']['Ridge_Regression']
            }

        # Lasso Regression
        
        elif model_type == "Lasso Regression": 

            param_grid = {
                'polynomial_features__degree': data_object.regression['Model_Selection']['Lasso Regression']['polynomial_degree_lasso'],
                'lasso_regression__alpha': data_object.regression['Model_Selection']['Lasso Regression']['alpha_values_lasso']
            }
            
            model = regression_models.train_lasso(data_object.data_filtering['Train-Test Split'], param_grid=param_grid) 
            r2, y_pred = metrics.evaluate_model(model, data_object.data_filtering['Train-Test Split'])
            
            data_object.outputs['Regression']['Lasso_Regression']['r2_score_lasso'] = r2
            data_object.outputs['Regression']['Lasso_Regression']['best_degree_lasso'] = regression_models.best_params_lasso['polynomial_features__degree']
            data_object.outputs['Regression']['Lasso_Regression']['best_alpha_lasso'] = regression_models.best_params_lasso['lasso_regression__alpha']
            data_object.outputs['Regression']['Lasso_Regression']['graph_params']['results_lasso'] = regression_models.results_lasso        # Add "results_lasso" in DataObject File
            

            response_data = {
                "r2_score_lasso": data_object.outputs['Regression']['Lasso_Regression']['r2_score_lasso'],
                "best_degree_lasso": data_object.outputs['Regression']['Lasso_Regression']['best_degree_lasso'],
                "best_alpha_lasso": data_object.outputs['Regression']['Lasso_Regression']['best_alpha_lasso'],
                "results_lasso": data_object.outputs['Regression']['Lasso_Regression']['graph_params']['results_lasso'],     # Add "results_lasso" in DataObject File
                "Lasso_Regression": data_object.outputs['Regression']['Lasso_Regression']
            }
            
        return Response(response_data, status=status.HTTP_200_OK)