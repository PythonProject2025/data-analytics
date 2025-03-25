INFO_TEXT_DF = {
    "process_selection": {
        "Filtering Method": "Applies filter-based methods to clean or reduce data.",
        "Scaling & Encoding": "Applies scaling and encoding operations to prepare data for modeling."
    },
    "segment_frame": {
        "Select Method": "Choose between different filtering techniques like Isolation Forest or IQR.",
        "Contamination Value": "Set the proportion of anomalies expected in the dataset.",
        "Choose Columns": "Select which columns to include for processing."
    },
    "interpolation_frame": {
        "Select Method": "Pick an interpolation method to estimate missing values."
    },
    "smoothing_frame": {
        "Select Method": "Choose a smoothing algorithm for time-series or noisy data.",
        "Window Size": "Set the moving window size for smoothing techniques like SMA.",
        "Seasonal Periods": "Define number of seasonal periods in the data.",
        "Trend": "Specify the type of trend to include in TES.",
        "Seasonal": "Specify the seasonal pattern in TES.",
        "Smoothing Level": "Adjust the level of smoothing.",
        "Smoothing Trend": "Adjust the amount of smoothing for the trend component.",
        "Smoothing Seasonal": "Adjust the amount of smoothing for the seasonal component."
    },
    "scaling_encoding_frame": {
        "Test Size": "Defines the proportion of the dataset used for testing.",
        "Random State": "Seed value for reproducibility in data splitting."
    }
}


INFO_TEXT_IM = {
    "image_processing_frame": {
        "Activation Function": "Select an activation function for neurons in the neural network (e.g., ReLU or Sigmoid).",
        "Epochs": "Set the number of iterations over the entire training dataset.",
        "Optimizer": "Choose the optimization algorithm used for updating model weights during training.",
        "Test Size": "Specify the percentage of data to reserve for testing the model's performance.",
        "Random State": "Seed for shuffling and splitting the dataset to ensure reproducibility."
    },
    "image_train_frame": {
        "Upload Image": "Upload a new image for model prediction or visualization.",
        "Preview Image": "Display a preview of the uploaded image before processing."
    }
}
