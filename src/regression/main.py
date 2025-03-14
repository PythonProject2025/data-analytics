from data_handler import DataHandler
from regression_models import RegressionModels
from data_object_final_edited import DataObject
from metrics import evaluate_model
from visualization_trial import regression_plot, residual_plot, polynomial_plot, ridge_plot, lasso_plot
import matplotlib.pyplot as plt

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
    
    # Linear Regression
    model = regression_models.train_linear_regression(dataobj.data_filtering['Train-Test Split']) # 1st change x_train, y_train 
    r2, y_pred = evaluate_model(model, dataobj.data_filtering['Train-Test Split'])  # 2nd change x_test, y_test 
    dataobj.outputs['Regression']['Linear_Regression']['r2_score_linear'] = r2
    dataobj.outputs['Regression']['Linear_Regression']['graph_params']['y_pred'] = y_pred
    
    
    #print(f"R2 Score (Linear Regression): {r2}")    Remove later

    # Plot regression and residuals in one window
    # fig, axs = plt.subplots(1, 2, figsize=(12, 6))
    # regression_plot(x_test["Datum"], y_test, "Datum", "pH-Wert", data_handler.data, ax=axs[0])  ==>  How labels will be handeled and which group will handle it?
    # residual_plot(y_test, y_pred, ax=axs[1])
    # plt.tight_layout()
    # plt.show()

        # Polynomial Regression
                        
    param_grid = {'polynomial_features__degree': dataobj.regression['Model_Selection']['Polynomial_Regression']['polynomial_degree']}
    model = regression_models.train_polynomial_regression(dataobj.data_filtering['Train-Test Split'], param_grid=param_grid) # 1st change x_train,y_train 
    #    print(f"Best HyperParameter(Polynomial) ==> Degree: {regression_models.best_params_poly['polynomial_features__degree']}") Remove later
    r2, y_pred = evaluate_model(model, dataobj.data_filtering['Train-Test Split']) # 2nd change x_test, y_test 
    dataobj.outputs['Regression']['Polynomial_Regression']['r2_score_polynomial'] = r2
    dataobj.outputs['Regression']['Polynomial_Regression']['graph_params']['y_pred'] = y_pred
    dataobj.outputs['Regression']['Polynomial_Regression']['best_polynomial_degree'] = regression_models.best_params_poly['polynomial_features__degree']
        
        #print(f"R2 Score (Polynomial Regression): {r2}") Remove Later
    #    polynomial_plot(x_test["Datum"], y_test, y_pred, "Datum", "pH-Wert", regression_models.best_params_poly['polynomial_features__degree']) ==>  How labels will be handeled and which group will handle it?

        # Ridge Regression
                
    param_grid = {
            'polynomial_features__degree': dataobj.regression['Model_Selection']['Ridge_Regression']['polynomial_degree_ridge'],
            'ridge_regression__alpha': dataobj.regression['Model_Selection']['Ridge_Regression']['alpha_values_ridge']
        }
    model = regression_models.train_ridge(dataobj.data_filtering['Train-Test Split'], param_grid=param_grid) # 1st change x_train,y_train 
    #    print("Best HyperParameters(Ridge) ==> alpha:", regression_models.best_params_ridge['ridge_regression__alpha'],
    #        ", Polynomial Degree:", regression_models.best_params_ridge['polynomial_features__degree'])
    r2, y_pred = evaluate_model(model, dataobj.data_filtering['Train-Test Split']) # 2nd change x_test, y_test 
    dataobj.outputs['Regression']['Ridge_Regression']['r2_score_ridge'] = r2
    dataobj.outputs['Regression']['Ridge_Regression']['best_degree_ridge'] = regression_models.best_params_ridge['polynomial_features__degree']
    dataobj.outputs['Regression']['Ridge_Regression']['best_alpha_ridge'] = regression_models.best_params_ridge['ridge_regression__alpha']
    #  print(f"R2 Score (Ridge Regression): {r2}") Remove Later
    dataobj.outputs['Regression']['Ridge_Regression']['graph_params']['regression_models'] = regression_models
    #    ridge_plot(regression_models)

        # Lasso Regression
                
    param_grid = {
            'polynomial_features__degree': dataobj.regression['Model_Selection']['Lasso_Regression']['polynomial_degree_lasso'],
            'lasso_regression__alpha': dataobj.regression['Model_Selection']['Lasso_Regression']['alpha_values_lasso']
        }
    model = regression_models.train_lasso(dataobj.data_filtering['Train-Test Split'], param_grid=param_grid) # 1st change x_train,y_train 
    #    print("Best HyperParameters(Lasso) ==> alpha:", regression_models.best_params_lasso['lasso_regression__alpha'],
    #        ", Polynomial Degree:", regression_models.best_params_lasso['polynomial_features__degree'])
    r2, y_pred = evaluate_model(model, dataobj.data_filtering['Train-Test Split']) # 2nd change x_test, y_test
    dataobj.outputs['Regression']['Lasso_Regression']['r2_score_lasso'] = r2
    dataobj.outputs['Regression']['Lasso_Regression']['best_degree_lasso'] = regression_models.best_params_lasso['polynomial_features__degree']
    dataobj.outputs['Regression']['Lasso_Regression']['best_alpha_lasso'] = regression_models.best_params_lasso['lasso_regression__alpha']
    #    print(f"R2 Score (Lasso Regression): {r2}")
    dataobj.outputs['Regression']['Lasso_Regression']['graph_params']['regression_models'] = regression_models
    #    lasso_plot(regression_models)

if __name__ == "__main__":
    main()