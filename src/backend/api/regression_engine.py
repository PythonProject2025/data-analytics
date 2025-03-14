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
        split_data=data_object.data_filtering["Train-Test Split"]["split_data"]
        X_train = pd.DataFrame(split_data.get("x_train", []))
        X_test = pd.DataFrame(split_data.get("x_test", []))
        y_train = pd.Series(split_data.get("y_train", []))
        y_test = pd.Series(split_data.get("y_test", []))
        
        if X_train.empty or X_test.empty or y_train.empty or y_test.empty:
            return Response({"error": "Train-test split data missing or empty"}, status=status.HTTP_400_BAD_REQUEST)

        # Extract regression model selection
        regression_models = RegressionModels()
        dataobj = DataObject()
        model_type = dataobj.regression["Model_Selection"]
        if model_type == "Linear_Regression":
            # Linear Regression
            model = regression_models.train_linear_regression(dataobj.data_filtering['Train-Test Split']) # 1st change x_train, y_train 
            r2, y_pred = metrics.evaluate_model(model, dataobj.data_filtering['Train-Test Split'])  # 2nd change x_test, y_test 
            dataobj.outputs['Regression']['Linear_Regression']['r2_score_linear'] = r2
            dataobj.outputs['Regression']['Linear_Regression']['graph_params']['y_pred'] = y_pred
    
        # Polynomial Regression
        elif model_type == "Polynomial_Regression":             
            param_grid = {'polynomial_features__degree': dataobj.regression['Model_Selection']['Polynomial_Regression']['polynomial_degree']}
            model = regression_models.train_polynomial_regression(dataobj.data_filtering['Train-Test Split'], param_grid=param_grid) # 1st change x_train,y_train 
        #    print(f"Best HyperParameter(Polynomial) ==> Degree: {regression_models.best_params_poly['polynomial_features__degree']}") Remove later
            r2, y_pred = metrics.evaluate_model(model, dataobj.data_filtering['Train-Test Split']) # 2nd change x_test, y_test 
            dataobj.outputs['Regression']['Polynomial_Regression']['r2_score_polynomial'] = r2
            dataobj.outputs['Regression']['Polynomial_Regression']['graph_params']['y_pred'] = y_pred
            dataobj.outputs['Regression']['Polynomial_Regression']['best_polynomial_degree'] = regression_models.best_params_poly['polynomial_features__degree']
            
            #print(f"R2 Score (Polynomial Regression): {r2}") Remove Later
        #    polynomial_plot(x_test["Datum"], y_test, y_pred, "Datum", "pH-Wert", regression_models.best_params_poly['polynomial_features__degree']) ==>  How labels will be handeled and which group will handle it?
        
        elif model_type == "Ridge_Regression":     
            # Ridge Regression   
            param_grid = {
                'polynomial_features__degree': dataobj.regression['Model_Selection']['Ridge_Regression']['polynomial_degree_ridge'],
                'ridge_regression__alpha': dataobj.regression['Model_Selection']['Ridge_Regression']['alpha_values_ridge']
            }
            model = regression_models.train_ridge(dataobj.data_filtering['Train-Test Split'], param_grid=param_grid) # 1st change x_train,y_train 
        #   print("Best HyperParameters(Ridge) ==> alpha:", regression_models.best_params_ridge['ridge_regression__alpha'],
        #        ", Polynomial Degree:", regression_models.best_params_ridge['polynomial_features__degree'])
            r2, y_pred = metrics.evaluate_model(model, dataobj.data_filtering['Train-Test Split']) # 2nd change x_test, y_test 
            dataobj.outputs['Regression']['Ridge_Regression']['r2_score_ridge'] = r2
            dataobj.outputs['Regression']['Ridge_Regression']['best_degree_ridge'] = regression_models.best_params_ridge['polynomial_features__degree']
            dataobj.outputs['Regression']['Ridge_Regression']['best_alpha_ridge'] = regression_models.best_params_ridge['ridge_regression__alpha']
        #    print(f"R2 Score (Ridge Regression): {r2}") Remove Later
            dataobj.outputs['Regression']['Ridge_Regression']['graph_params']['regression_models'] = regression_models
        #    ridge_plot(regression_models)
        
        elif model_type == "Lasso_Regression": 
            # Lasso Regression
            param_grid = {
                'polynomial_features__degree': dataobj.regression['Model_Selection']['Lasso_Regression']['polynomial_degree_lasso'],
                'lasso_regression__alpha': dataobj.regression['Model_Selection']['Lasso_Regression']['alpha_values_lasso']
            }
            model = regression_models.train_lasso(dataobj.data_filtering['Train-Test Split'], param_grid=param_grid) # 1st change x_train,y_train 
        #    print("Best HyperParameters(Lasso) ==> alpha:", regression_models.best_params_lasso['lasso_regression__alpha'],
        #        ", Polynomial Degree:", regression_models.best_params_lasso['polynomial_features__degree'])
            r2, y_pred = metrics.evaluate_model(model, dataobj.data_filtering['Train-Test Split']) # 2nd change x_test, y_test
            dataobj.outputs['Regression']['Lasso_Regression']['r2_score_lasso'] = r2
            dataobj.outputs['Regression']['Lasso_Regression']['best_degree_lasso'] = regression_models.best_params_lasso['polynomial_features__degree']
            dataobj.outputs['Regression']['Lasso_Regression']['best_alpha_lasso'] = regression_models.best_params_lasso['lasso_regression__alpha']
        #    print(f"R2 Score (Lasso Regression): {r2}")
            dataobj.outputs['Regression']['Lasso_Regression']['graph_params']['regression_models'] = regression_models
        #    lasso_plot(regression_models)
        
        
        return Response(data_object.outputs, status=status.HTTP_200_OK)
