import sys
import os
import zipfile
import numpy as np
import pandas as pd
from tensorflow.keras.preprocessing.image import load_img
from sklearn.model_selection import train_test_split

# Data Loading from CSV file and Preprocessing Class
class DataLoadingAndPreprocessing:
    def __init__(self, image_size = (28, 28)):
        #Read the CSV file
        self.data = None
        self.labels = None
        self.label_dict = None
        self.image_size = image_size
        self.images = []

    def get_label_dict(self):
        return self.label_dict

    def data_loader(self, dataObj):
        """
        This method loads the data from the dataset folder (zipped or unzipped), creates labels, encodes them,
        loads the dataset and normalizes the dataset. 

        Parameters:
        dataset_name: str
            The name of the folder where the images are stored
        is_zipped: bool
            If the dataset is zipped or not
        """
        zipfile_path = dataObj['zipFilePath']
        is_zipped = dataObj['isZipped']

        # Get the name of the folder where the images are stored
        data_dir_name = os.path.basename(zipfile_path).split('.')[0]
        # Assuming that the files are unzipped in the same directory where the code is being executed
        current_path = os.path.dirname(os.path.abspath(sys.argv[0]))
        data_dir = os.path.join(current_path, data_dir_name)

        # Unzip the folder if it is not already unzipped
        if is_zipped == True:
            print("Unzipping the dataset...")
            self.unzip_folder(current_path, zipfile_path, data_dir)

        # Create encoded labels and map them to the data
        self.create_labels(data_dir)
        
        for image_path in self.data['path']:
            # Load image
            img = load_img(image_path, target_size = self.image_size, color_mode = 'grayscale')
            self.images.append(img)

        # Return the normalized images to be stored in the data object
        self.normalize_dataset()
    
    def split_dataset(self, dataObj):
        test_size = dataObj['test_size']
        random_state = dataObj['random_state']

        X_train, X_test, y_train, y_test = train_test_split(self.images,
                                                            self.labels,
                                                            test_size = test_size, 
                                                            random_state = random_state)
        # Now X_train, X_test, y_train, y_test are ready for training
        print(f"Training data shape: {X_train.shape}, Labels shape: {y_train.shape}")
        print(f"Testing data shape: {X_test.shape}, Labels shape: {y_test.shape}")

        data = {"X_train": X_train, 
                "y_train": y_train, 
                "X_test": X_test, 
                "y_test": y_test,
                "train_shape": X_train.shape,
                "test_shape": X_test.shape}

        return data

    def encode_labels(self):
        # Encode the labels
        self.label_dict = {label: i for i, label in enumerate(self.labels)}
        # Set the labels for the data
        self.data['label'] = self.data['label'].map(self.label_dict)

    def create_labels(self, data_dir):
        """
        Parameters:
        folder_name: str
            The name of the folder where the images are stored
        
        Returns:
        None
        """
        data = []

        # The directory names are taken as labels
        self.labels = os.listdir(data_dir)

        for label in self.labels:
            label_dir = os.path.join(data_dir, label)

            img_files = [file for file in os.listdir(label_dir) if file.lower().endswith(('.png', '.jpg', '.jpeg'))]

            data.extend({"image_name": file, 
                         "label": label, 
                         "path": os.path.relpath(os.path.join(label_dir, file))} for file in img_files)
        
        # Creata a dataframe to store the information
        self.data = pd.DataFrame(data)
        # Encode the labels
        self.encode_labels()

    def unzip_folder(self, current_path, zip_file, data_dir):
        # zip_file = os.path.join(current_path, folder_name)
        print(zip_file)

        if not os.path.exists(data_dir):
            if os.path.exists(zip_file):
                print(f"Extracting dataset... ")
                with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                    zip_ref.extractall(current_path)  # Extract to the script's location
                print(f"Dataset extracted to: {data_dir}")
            else:
                print(" The dataset is not found.")

    def normalize_dataset(self):
       self.images = np.array(self.images)
       self.labels = np.array(self.data['label'])
       #Normalization
       self.images = self.images / 255.0

       print("The Dataset has been Processed Successfully!\n", 
              f"Total images:\t {len(self.images)}")