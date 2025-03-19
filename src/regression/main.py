from data_handler import DataHandler
from regression_models import RegressionModels
from data_object_final_edited import DataObject
from metrics import evaluate_model
from visualization_trial import regression_plot, residual_plot, polynomial_plot, ridge_plot, lasso_plot
import matplotlib.pyplot as plt
import numpy as np


def main():
    
# Configuration
    file_path = "data\RegressionPredictionData.csv"  # Relative path
    target_variable = "pH-Wert"  # Replace with actual target column name
    test_size = 0.2

# Initialize dataHandler class
    data_handler = DataHandler(file_path=file_path, target_variable=target_variable)

# Load and split data
    x, y = data_handler.load_data()
    x_train, x_test, y_train, y_test = data_handler.split_data(test_size)
# Initialize RegressionModels class
    regression_models = RegressionModels()
    dataobj = DataObject()
    
# Storing dataframes in the data object
    dataobj.data_filtering['Train-Test Split']['split_data'] = {'x_train': x_train, 'x_test': x_test, 'y_train': y_train, 'y_test': y_test}

# ---------------------------------------------------  Linear Regression ---------------------------------------

    model = regression_models.train_linear_regression(dataobj.data_filtering['Train-Test Split'])
    r2, y_pred = evaluate_model(model, dataobj.data_filtering['Train-Test Split']) 
    dataobj.outputs['Regression']['Linear_Regression']['r2_score_linear'] = r2
    dataobj.outputs['Regression']['Linear_Regression']['graph_params']['y_pred'] = y_pred
    print('R2_Linear: ',dataobj.outputs['Regression']['Linear_Regression']['r2_score_linear'])
    print('y_pred: ',dataobj.outputs['Regression']['Linear_Regression']['graph_params']['y_pred'])
    print(dataobj.data_filtering['Train-Test Split']['split_data']['x_test']['Datum'])
    
# Plot regression and residuals in one window
    fig, axs = plt.subplots(1, 2, figsize=(12, 6))
    
    x_label = "Datum" 
    y_label = "pH-Wert"
    
    dataobj.outputs['Regression']['Linear_Regression']['graph_params']['x_label'] = x_label # Given by User, Type: String
    dataobj.outputs['Regression']['Linear_Regression']['graph_params']['y_label'] = y_label # Given by User, Type: String
    
    regression_plot(dataobj.data_filtering['Train-Test Split']['split_data']['x_test'][x_label], 
                    dataobj.data_filtering['Train-Test Split']['split_data']['y_test'], 
                    dataobj.outputs['Regression']['Linear_Regression']['graph_params']['x_label'], 
                    dataobj.outputs['Regression']['Linear_Regression']['graph_params']['y_label'], 
                    ax=axs[0])
    
    residual_plot(dataobj.data_filtering['Train-Test Split']['split_data']['y_test'], 
                  dataobj.outputs['Regression']['Linear_Regression']['graph_params']['y_pred'], 
                  ax=axs[1])
    
    plt.tight_layout()
    plt.show()

# -------------------------------------------- Polynomial Regression ------------------------------------------
# Test Input
    dataobj.regression['Model_Selection']['Polynomial_Regression']['polynomial_degree'] = [1, 2, 3, 4, 5]                
    param_grid = {'polynomial_features__degree': dataobj.regression['Model_Selection']['Polynomial_Regression']['polynomial_degree']}
    
    model = regression_models.train_polynomial_regression(dataobj.data_filtering['Train-Test Split'], param_grid=param_grid)
    r2, y_pred = evaluate_model(model, dataobj.data_filtering['Train-Test Split']) 
    dataobj.outputs['Regression']['Polynomial_Regression']['r2_score_polynomial'] = r2
    dataobj.outputs['Regression']['Polynomial_Regression']['graph_params']['y_pred'] = y_pred
    dataobj.outputs['Regression']['Polynomial_Regression']['best_polynomial_degree'] = regression_models.best_params_poly['polynomial_features__degree']
    print(dataobj.outputs['Regression']['Polynomial_Regression']['r2_score_polynomial'])
    print(dataobj.outputs['Regression']['Polynomial_Regression']['best_polynomial_degree'])
    print(dataobj.outputs['Regression']['Polynomial_Regression']['graph_params']['y_pred'])
    
# Polynomial fit

    x_label = "Datum" 
    y_label = "pH-Wert"
    
    dataobj.outputs['Regression']['Polynomial_Regression']['graph_params']['x_label'] = x_label # Given by User, Type: String
    dataobj.outputs['Regression']['Polynomial_Regression']['graph_params']['y_label'] = y_label # Given by User, Type: String
    
    polynomial_plot(dataobj.data_filtering['Train-Test Split']['split_data']['x_test'][x_label], 
                    dataobj.data_filtering['Train-Test Split']['split_data']['y_test'], 
                    dataobj.outputs['Regression']['Polynomial_Regression']['graph_params']['y_pred'], 
                    dataobj.outputs['Regression']['Polynomial_Regression']['graph_params']['x_label'], 
                    dataobj.outputs['Regression']['Polynomial_Regression']['graph_params']['y_label'], 
                    regression_models.best_params_poly['polynomial_features__degree'])
    
# --------------------------------------------------- Ridge Regression ----------------------------------------------------------
# Test Input

    dataobj.regression['Model_Selection']['Ridge_Regression']['polynomial_degree_ridge'] = [4, 5, 6]
    dataobj.regression['Model_Selection']['Ridge_Regression']['alpha_values_ridge'] = [0.001,0.01,0.1,1]     
       
    param_grid = {
        'polynomial_features__degree': dataobj.regression['Model_Selection']['Ridge_Regression']['polynomial_degree_ridge'],
        'ridge_regression__alpha': dataobj.regression['Model_Selection']['Ridge_Regression']['alpha_values_ridge']
    }
    
    model = regression_models.train_ridge(dataobj.data_filtering['Train-Test Split'], param_grid=param_grid)
    r2, y_pred = evaluate_model(model, dataobj.data_filtering['Train-Test Split'])
    dataobj.outputs['Regression']['Ridge_Regression']['r2_score_ridge'] = r2
    dataobj.outputs['Regression']['Ridge_Regression']['best_degree_ridge'] = regression_models.best_params_ridge['polynomial_features__degree']
    dataobj.outputs['Regression']['Ridge_Regression']['best_alpha_ridge'] = regression_models.best_params_ridge['ridge_regression__alpha']
    dataobj.outputs['Regression']['Ridge_Regression']['graph_params']['results_ridge'] = regression_models.results_ridge   
    
    print(dataobj.outputs['Regression']['Ridge_Regression']['r2_score_ridge'])
    print(dataobj.outputs['Regression']['Ridge_Regression']['best_degree_ridge'])
    print(dataobj.outputs['Regression']['Ridge_Regression']['best_alpha_ridge'])

# Plot of R2 score vs regularization strength

    ridge_plot(dataobj.outputs['Regression']['Ridge_Regression']['graph_params']['results_ridge'],
               dataobj.outputs['Regression']['Ridge_Regression'])


# --------------------------------------------------- Lasso Regression ---------------------------------------------------
# Test Input 

    dataobj.regression['Model_Selection']['Lasso_Regression']['polynomial_degree_lasso'] = [1,2,3]
    dataobj.regression['Model_Selection']['Lasso_Regression']['alpha_values_lasso'] = [0.001,0.01,0.1,1]
            
    param_grid = {
        'polynomial_features__degree': dataobj.regression['Model_Selection']['Lasso_Regression']['polynomial_degree_lasso'],
        'lasso_regression__alpha': dataobj.regression['Model_Selection']['Lasso_Regression']['alpha_values_lasso']
    }
    
    model = regression_models.train_lasso(dataobj.data_filtering['Train-Test Split'], param_grid=param_grid) 
    r2, y_pred = evaluate_model(model, dataobj.data_filtering['Train-Test Split'])
    
    dataobj.outputs['Regression']['Lasso_Regression']['r2_score_lasso'] = r2
    dataobj.outputs['Regression']['Lasso_Regression']['best_degree_lasso'] = regression_models.best_params_lasso['polynomial_features__degree']
    dataobj.outputs['Regression']['Lasso_Regression']['best_alpha_lasso'] = regression_models.best_params_lasso['lasso_regression__alpha']

    dataobj.outputs['Regression']['Lasso_Regression']['graph_params']['results_lasso'] = regression_models.results_lasso
    print(dataobj.outputs['Regression']['Lasso_Regression']['r2_score_lasso'])
    print(dataobj.outputs['Regression']['Lasso_Regression']['best_degree_lasso'])
    print(dataobj.outputs['Regression']['Lasso_Regression']['best_alpha_lasso'])    

# Plot of R2 score vs regularization strength 
 
    lasso_plot(dataobj.outputs['Regression']['Lasso_Regression']['graph_params']['results_lasso'],
               dataobj.outputs['Regression']['Lasso_Regression'])

if __name__ == "__main__":
    main()