INFO_TEXT_DF = {
    "process_selection": {
        "Filtering Method": "Applies filter-based methods to clean or reduce data.",
        "Scaling & Encoding": "Applies scaling and encoding operations to prepare data for modeling."
    },
    "segment_frame": {
        "Select Method": "The Interquartile Range (IQR) is a statistical measure of data spread, calculated as the difference between the third quartile (Q3) and the first quartile (Q1), representing the middle 50 percent  of the dataset and commonly used for outlier detection. Isolation Forest: Isolation Forest is an anomaly detection algorithm that isolates outliers by recursively partitioning data using random splits, leveraging the fact that anomalies are easier to isolate due to their rarity and distinctiveness",
        "Contamination Value": "Contamination value is the estimated proportion of outliers in the dataset, typically ranging from 0 (no outliers) to 0.5 (half the data could be outliers",
        "Choose Columns": "Select which columns to include for processing."
    },
    "interpolation_frame": {
        "Select Method": "Pick an interpolation method to estimate missing values."
    },
    "smoothing_frame": {
        "Select Method": "Choose a smoothing algorithm for time-series or noisy data.",
        "Window Size": "Defines the window size used for calculating the moving average, determining how many past values contribute to each averaged point.",
        "Seasonal Periods": "Defines the number of seasonal periods in the dataset, indicating the length of one complete cycle.",
        "Trend": "Specifies the trend component type—can be 'add' (additive), 'mul' (multiplicative), or None (no trend).",
        "Seasonal": "Defines the seasonal component type—can be 'add' (additive), 'mul' (multiplicative), or None (no seasonality).",
        "Smoothing Level": "The alpha parameter that controls how much weight recent observations get in the smoothing process.",
        "Smoothing Trend": "The beta parameter that adjusts the smoothing of the trend component.",
        "Smoothing Seasonal": "The gamma parameter that influences the smoothing of the seasonal component."
    },
    "scaling_encoding_frame": {
        "Test Size": "Proportion of the dataset allocated for testing, typically between 0 and 1.",
        "Random State": "Controls the randomness of the train-test split to ensure reproducibility."
    }
}


INFO_TEXT_IM = {
    "image_processing_frame": {
        "Activation Function": "\n1- ReLU (Rectified Linear Unit)\n  Short Form: \"Fast and Simple\"\n  How it works: Outputs x if x > 0, else 0\n  Why used: Speeds up training, avoids vanishing gradient\n\n2- Sigmoid\n  Short Form: \"Smooth between 0 and 1\"\n  How it works: Converts input to a value between 0 and 1\n  Why used: Good for probabilities or binary classification",
        "Epochs": "Set the number of iterations over the entire training dataset.",
        "Optimizer": "\n1-Adam (Adaptive Moment Estimation)\n  Short Form: \"Smart and Fast\"\n  Key Idea: Combines momentum + adaptive learning rate\n  Best for: Most deep learning problems\n\n2-RMSprop (Root Mean Square Propagation)\n  Short Form: \"Stable Learner\"\n  Key Idea: Adjusts learning rate based on recent gradients\n  Best for: RNNs, noisy data\n\n3-Adamax\n  Short Form: \"Adam's big brother\"\n  Key Idea: Variant of Adam that handles large gradients better\n  Best for: High-dimensional parameter spaces",
        "Test Size": "Specify the percentage of data to reserve for testing the model's performance.",
        "Random State": "Seed for shuffling and splitting the dataset to ensure reproducibility."
    },
    "image_train_frame": {
        "Upload Image": "Upload a new image for model prediction or visualization.",
        "Preview Image": "Display a preview of the uploaded image before processing."
    }
}


INFO_TEXT_AI = {
    "problem_selection": {
        "type": "Select whether you are solving a Regression or Classification problem."
    },
    "RandomForest": {
        "n_estimators": "Number of trees in the forest (default: 100). Increasing this generally improves performance but increases computation time.",
        "max_depth": "Maximum depth of a tree. Controls how complex each tree can be.",
        "min_samples_split": "Minimum number of samples required to split a node (default: 2). Higher values prevent overfitting.",
        "min_samples_leaf": "Minimum number of samples required to be at a leaf node (default: 1). Higher values smooth out predictions"
    },
    "CatBoost": {
        "n_estimators": "Number of boosting iterations (default: 1000). Higher values may improve accuracy but increase computation time.",
        "learning_rate": "Step size for updating weights (default: 0.03). Smaller values may require more iterations.",
        "max_depth": "Depth of each tree (default: 6). Higher values may increase complexity and risk overfitting.",
        "reg_lambda": "L2 regularization coefficient to avoid overfitting (default: 3)."
    },
    "ArtificialNeuralNetwork": {
        "Layer Number": "Number of hidden layers in the neural network.",
        "Units": "Number of neurons in each hidden layer.",
        "Activation Function": "Activation functions like 'relu', 'sigmoid', or 'tanh'.",
        "Optimizer": "Options like 'adam', 'sgd', etc.",
        "Batch Size": "Number of samples per training batch (default: 32).",
        "Epochs": "Number of training iterations (default: 10)."
    },
    "XGBoost": {
        "n_estimators": "Number of boosting rounds. Controls the number of trees added to the model.",
        "learning_rate": "Controls the contribution of each tree. Smaller values require more boosting rounds.",
        "min_split_loss": "Minimum loss reduction required to make a further partition on a leaf node.",
        "max_depth": "Maximum depth of a tree. Increasing this increases model complexity."
    }
}

INFO_TEXT_RG = {
    "Polynomial Regression": {
        "Polynomial Degree": "Defines the degree of the polynomial curve (e.g., 2 for quadratic, 3 for cubic) to fit the data. Higher degrees capture complex non-linear patterns but may overfit, making the model too sensitive to training data. GridSearchCV tests a list of degrees and selects the best one by balancing bias and variance."
    },
    "Ridge Regression": {
        "Polynomial Degree": "Defines the degree of the polynomial curve (e.g., 2 for quadratic, 3 for cubic) to fit the data. Higher degrees capture complex non-linear patterns but may overfit, making the model too sensitive to training data. GridSearchCV tests a list of degrees and selects the best one by balancing bias and variance.",
        "Alpha": "A regularization parameter that controls model complexity. Higher alpha values increase generalization, while lower values allow more complexity. GridSearchCV tests a list of alphas (e.g., [0.0001, 0.001, 0.01, 0.1, 1]) and selects the best one by balancing bias and variance. Use multiples of 10; values above 1 are not allowed."
    },
    "Lasso Regression": {
        "Polynomial Degree": "Defines the degree of the polynomial curve (e.g., 2 for quadratic, 3 for cubic) to fit the data. Higher degrees capture complex non-linear patterns but may overfit, making the model too sensitive to training data. GridSearchCV tests a list of degrees and selects the best one by balancing bias and variance.",
        "Alpha": "A regularization parameter that controls model complexity. Higher alpha values increase generalization, while lower values allow more complexity. GridSearchCV tests a list of alphas (e.g., [0.0001, 0.001, 0.01, 0.1, 1]) and selects the best one by balancing bias and variance. Use multiples of 10; values above 1 are not allowed."
    }
}

INFO_TEXT_CS = {
    "Metrics": {
        "accuracy": "The proportion of correctly classified instances out of the total instances.",
        "classification_report": "Provides precision, recall, F1-score, and support for each class.",
        "confusion_matrix": "A matrix showing the counts of true positives, false positives, true negatives, and false negatives.",
        "mean_squared_error": "The average of the squares of the errors between predicted and actual values."
    },
    "RandomForest": {
        "n_estimators": "The number of trees in the forest. Higher values generally improve performance at the cost of increased computation time.",
        "max_depth": "The maximum depth of each tree. Controls the complexity of the model and helps prevent overfitting.",
        "random_state": "Seed used by the random number generator for reproducibility."
    },
    "SVC": {
        "C": "Regularization parameter. The strength of the regularization is inversely proportional to C. Lower values specify stronger regularization.",
        "kernel": "Specifies the kernel type to be used in the algorithm.",
        "gamma": "Kernel coefficient for 'rbf' and other kernels. Controls the influence of training examples."
    },
    "KNN": {
        "n_neighbors": "The number of neighbors to consider for classification.",
        "weights": "Weight function used in prediction. 'uniform' assigns equal weight to all neighbors, 'distance' assigns weights inversely proportional to distance.",
        "p": "Power parameter for the Minkowski metric. p=1 is equivalent to Manhattan distance, p=2 is equivalent to Euclidean distance."
    },
    "Processing": {
        "test_size": "The proportion of the dataset to include in the test split.",
        "random_state": "Controls the shuffling applied to the data before applying the split."
    }
}
