import json

class DataObject:
    """Unified data model for managing raw data, user selections, and processed results."""
    def __init__(self):
        
        # Raw Data Handling
        self.raw_data = None  # Stores uploaded file data

        # Preprocessing Configuration
        self.data_filtering= {
            "filepath":{},
            "Outlier Detection": {
                "Method": "IQR", # IQR or Isolation Forest
                "Parameters": {"contamination": None,
                               "column_names": []}#(Range: 0 - 0.5) TAKE USER INPUT
            },
            "Smoothing": {
                "Method": "SMA", #SMA or TES
                "parameters": {
                    # If SMA, then only window size otherwise options 
                    # from seasonal periods
                    "window_size": None,#(Range: 5-100 ) #TAKE USER INPUT
                    "seasonal_periods": None,#(Range: 1-12) #TAKE USER INPUT
                    "trend": None,#add/mul/None TAKE USER INPUT
                    "seasonal": None,#add/mul/None TAKE USER INPUT
                    "smoothing_level": None,# Range: (0 to 1) TAKE USER INPUT
                    "smoothing_trend": None,# Range: (0 to 1) TAKE USER INPUT
                    "smoothing_seasonal": None,# Range: (0 to 1) TAKE USER INPUT
                }
            },
            "Train-Test Split": {
                "parameters": {
                    "test_size": None,
                    "random_state": None,
                    "target_column": None
                },
                "split_data": {"X_train": None, 
                               "X_test": None, 
                               "y_train": None, 
                               "y_test": None}
                
            }
        }

        # AI Model Configuration
        self.ai_model = {
            "problem_type" :{},
            "Selected Model":{},
            "RandomForest": {
                "n_estimators": 0, # {"min": 10, "max": 500, "default": 200},
                "max_depth": 0, #{"min": 3, "max": 50, "default": 20},
                "min_samples_split": 0, #{"min": 4, "max": 10, "default": 5},
                "min_samples_leaf": 0 #{"min": 1, "max": 10, "default": 1}
            },
            "CatBoost": {
                "n_estimators": 0, #{"min": 100, "max": 1000, "default": 500},
                "learning_rate": 0, #{"min": 0.01, "max": 0.1, "default": 0.03},
                "max_depth": 0, #{"min": 4, "max": 10, "default": 6},
                "reg_lambda": 0, #{"min": 1, "max": 10, "default": 3}
            },
            "ArtificialNeuralNetwork": {
                "Layer Number": 0 , #{"min": 1, "max": 6, "default": 3},
                "Units": 0, #{"min": 1, "max": 256, "default": [128, 64, 4]},
                "Activation Function": None, #{"allowed": ["relu", "sigmoid", "tanh", "softmax"], "default": ["relu", "relu", "softmax"]},
                "Optimizer": None, #{"allowed": ["adam", "sgd", "rmsprop"], "default": "adam"},
                "Batch Size": 0, #{"min": 16, "max": 128, "default": 30},
                "Epochs": 0, # {"min": 10, "max": 300, "default": 100}
            },
            "XGBoost": {
                "n_estimators": 0, #{"min": 100, "max": 1000, "default": 200},
                "learning_rate": 0 ,# {"min": 0.01, "max": 0.3, "default": 0.3},
                "min_split_loss": 0 ,#{"min": 3, "max": 10, "default": 10},
                "max_depth": 0, #{"min": 0, "max": 10, "default": 6}
            }
        }

        # Classification & Regression Config
        self.classification = {
            "Inputs": {"x_train": None, "x_test": None, "y_train": None, "y_test": None,"y_label":None},
            "Model_Selection": {"RandomForest": {}, "SVC": {}, "KNN": {}},
            "RandomForest": {"n_estimators": {50, 100, 150},
                             "max_depth": {5, 10, 20}
                             },
            "SVC": {"C": {0.1, 1, 10},
                    "kernel":"linear", 
                    "max_depth": {"min": 0.01, "max": 0.1, "default": 0.03},
                    "gamma": "auto"
                    },
            "KNN": {"n_neighbours": {3, 5, 7},
                    "weights": "distance",
                    "p": {1, 2}
                    }
        }

        self.regression = {
            "Selected Model":{},
            "Model_Selection": {
                "Linear Regression": {},
                "Polynomial Regression": {"polynomial_degree": []}, #5,7,8,2,9(only single digit integer upto comma seperated 5 values)
                "Ridge Regression": {"polynomial_degree_ridge": [], "alpha_values_ridge": []},#alpha float(limit4digits) 0-1 upto 5 values
                "Lasso Regression": {"polynomial_degree_lasso": [], "alpha_values_lasso": []}
            }
        }

        # Image Processing
        self.image_processing = {
            "fileio": {"zipFilePath": "", # input 
                       "isZipped": True},
            "model_params": {"activation_fn": "relu", # input
                             "optimizer": "adam"}, # input
            "training_params": {"epochs": 10}, # input
            "train_test_split": {"test_size": 0.2, # input
                                 "random_state": 42}, # input
            "label_dict": {},
            "model": None,
            "splits": None,
            "image_path":None
        }
        
        self.preprocessed = {
                "Categorical Encoding": {"Encoded Features": "X categorical columns transformed"},
                "Train-Test Split": {"Training Data": "X samples", "Test Data": "Y samples"}
        }
        
    
        # Outputs for Different Models
        self.outputs = {
            "Data Processing":{
                "Outlier Detection": {"Method": "Isolation Forest", # IQR or Isolation Forest
                                      "Removed Outliers": "X rows removed",
                                      "Original data size": "No of rows, No of columns",
                                      "Cleaned data size":  "No of rows, No of columns",
                                      "cleaned_data": None # Outlier output data
                                      },
                
                "Interpolation": {
                    "Method": "Spline Interpolation",
                    "Filled Missing Values": "X values interpolated",
                    "Interpolated_Data": None
                },
                "Smoothing": {
                    # Either SMA or TES will be given as Output
                    "Method": "Simple Moving Average",
                    "SMA": {"Smoothed Values": "X window size applied"},
                    "TES": {    "seasonal_periods": "input given by the user", 
                                "trend": "input given by the user", 
                                "seasonal": "input given by the user",
                                "smoothing level(alpha)": "input given by the user",
                                "smoothing trend(beta)":  "input given by the user",
                                "smoothing seasonal(gamma)":"input given by the user"},
                    "smoothed_data": None
                }
            },
            "Regression": {
                "Linear_Regression": {
                    "r2_score_linear": 0.0,
                    "graph_params": {
                        "x_data": None,
                        "y_test": None,
                        "x_label": "",
                        "y_label": "",
                        "dataframe": None,
                        "y_pred": None
                    }
                },
                "Polynomial_Regression": {
                    "best_polynomial_degree": 0,
                    "r2_score_polynomial": 0.0,
                    "graph_params": {
                        "x_data": None,
                        "y_test": None,
                        "y_pred": None,
                        "x_label": "",
                        "y_label": "",
                        "best_params_polynomial": 0
                    }
                },
                "Ridge_Regression": {
                    "best_degree_ridge": 0,
                    "best_alpha_ridge": 0.0,
                    "r2_score_ridge": 0.0,
                    "graph_params": {
                        "regression_models": None,
                        "results_ridge": None  
                    }
                },
                "Lasso_Regression": {
                    "best_degree_lasso": 0,
                    "best_alpha_lasso": 0.0,
                    "r2_score_lasso": 0.0,
                    "graph_params": {
                        "regression_models": None,
                        "results_lasso": None
                    }
                }
            },
            "Classification": { 
                "RandomForest": {
                    "Accuracy": 0.0,
                    "MSE": 0.0,
                    "Confusion Matrix": [
                        [0, 0, 0, 0],
                        [0, 0, 0, 0],
                        [0, 0, 0, 0],
                        [0, 0, 0, 0]
                    ]
                }      
            },
            "AI_Classification": {
                "RandomForest": {"Accuracy": 0.0, 
                                 "Confusion Matrix": [
                                    [0, 0, 0, 0],
                                    [0, 0, 0, 0],
                                    [0, 0, 0, 0],
                                    [0, 0, 0, 0]
                                ]},
                "CatBoost": {"Accuracy": 0.0,
                             "Confusion Matrix": [
                                    [0, 0, 0, 0],
                                    [0, 0, 0, 0],
                                    [0, 0, 0, 0],
                                    [0, 0, 0, 0]
                                ]},
                "ArtificialNeuralNetwork": {"Accuracy": 0.0,
                                           "Confusion Matrix": [
                                    [0, 0, 0, 0],
                                    [0, 0, 0, 0],
                                    [0, 0, 0, 0],
                                    [0, 0, 0, 0]
                                ]}
            },
            "AI_Regression": {
                "RandomForest": {"MAE": 0.0, "MSE": 0.0, "R2": 0.0},
                "CatBoost": {"MAE": 0.0, "MSE": 0.0, "R2": 0.0},
                "XGBoost": {"MAE": 0.0, "MSE": 0.0, "R2": 0.0}
            },
            "Image_Processing": {
                "testLoss": 0.0,
                "testAccuracy": 0.0,
                "confusionMatrix": {
                    "labels": [],
                    "values": [], # in percentage
                    "xlabel": "",
                    "ylabel": "",
                    "title": "",
                    "unique_labels": [],
                    "tick_marks": []       
                },
                "image_predictions": {
                    "predicted_label": 0,
                    "predicted_prob": 0.0
                }
            },
            "Graph Params": {"x_data": None, "y_test": None, "x_label": "", "y_label": "", "y_pred": None}
        }
    
    def update_raw_data(self, data):
        """Stores uploaded raw data."""
        self.raw_data = data

    def update_processed_data(self, data, process_type="Processed Data"):
        """Stores processed data from backend."""
        self.outputs[process_type] = data

    def to_dict(self):
        def convert(obj):
            if isinstance(obj, set):
                return list(obj)  # ✅ Convert set to list
            if isinstance(obj, dict):
                return {k: convert(v) for k, v in obj.items()}  # Recursively convert dict
            if isinstance(obj, list):
                return [convert(i) for i in obj]  # Convert list elements
            return obj

        return convert(self.__dict__)
    
    def to_json(self):
        """Convert object to JSON string, ensuring sets are serializable."""
        return json.dumps(self.to_dict())
