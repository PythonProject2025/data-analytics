import sys
import os
import zipfile
import numpy as np
import pandas as pd
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from sklearn.model_selection import train_test_split


# Data Loading from CSV file and Preprocessing Class
class DataLoadingAndPreprocessing:
    """
         A class to handle data loading and preprocessing.

         Attributes:
             image_size (tuple): Size of images (default is (28, 28)).
             data (DataFrame): Loaded data as a Pandas DataFrame.
             labels (list): List of labels.
             label_dict (dict): Dictionary mapping labels to integers.
             images (list): List of processed images.

         Methods:
             data_loader(dataset_name, is_zipped=True)
                 Loads and preprocesses image dataset.

             get_label_dict()
                 Returns label dictionary.

             encode_labels()
                 Encodes labels into numeric values.

             create_labels(folder_name, is_zipped=True)
                 Creates and encodes labels from directory structure.

             unzip_folder(current_path, folder_name, data_dir)
                 Unzips dataset if necessary.

             normalize_dataset()
                 Normalizes dataset to the range [0,1].

             split_dataset(test_size=0.2, random_state=42)
                 Splits dataset into training and test sets.
         """

    def __init__(self, image_size=(28, 28)):
        """  Initializes the data loader.
              Args:
              image_size (tuple): The target size of images.
        """

        self.data = None
        self.labels = None
        self.label_dict = None
        self.image_size = image_size
        self.images = []

    def get_label_dict(self):
      """    Retrieves the label dictionary.

                      Returns:
                          dict: Mapping of label names to integers.
               """
      return self.label_dict

    def data_loader(self, dataObj):
        """
        This method loads the data from the dataset folder (zipped or unzipped), creates labels, encodes them,
        loads the dataset and normalizes the dataset.

        Parameters:
        dataObj: dict
            A data object dictionary containing
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
            img = load_img(image_path, target_size=self.image_size, color_mode='grayscale')
            self.images.append(img)

        # Return the normalized images to be stored in the data object
        self.normalize_dataset()
    
    def load_image(self, dataObj):
        """
        This method loads an image from the given path and returns it as a numpy array.

        Parameters:
        dataObj: dict
            A data object dictionary containing
                image_path: str
                    The path to the image file
        
        Returns:
        numpy.ndarray: The image as a numpy array
        """
        image_path = dataObj['image_path']
        img = load_img(image_path, target_size = (28, 28), color_mode='grayscale')
        img_arr = np.array(img)
        img_arr = np.expand_dims(img_arr, axis = -1)
        img_arr = np.expand_dims(img_arr, axis = 0)
        img_arr = img_arr / 255.0 

        return img_arr
    
    def split_dataset(self, dataObj):
        """
        Splits the dataset into training and testing sets.

        This method partitions the preprocessed dataset into training and test
        sets, ensuring reproducibility with a fixed random state.

        Args:
            dataObj (dict): The data object dictionary consisting of:
                test_size (float): The proportion of the dataset to include in the test split. Defaults to 0.2.
                random_state (int): The seed used by the random number generator for reproducibility. Defaults to 42.

        Returns:
            tuple: A tuple containing four numpy arrays:
                - X_train (numpy.ndarray): Training images.
                - y_train (numpy.ndarray): Training labels.
                - X_test (numpy.ndarray): Test images.
                - y_test (numpy.ndarray): Test labels.
                """
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
        """
                    Encodes the labels into numerical values.

                    This method assigns a unique integer to each label and maps the dataset labels
                    to their corresponding numerical values.

                    Returns:
                        None
                """
        self.label_dict = {label: i for i, label in enumerate(self.labels)}
        # Set the labels for the data
        self.data['label'] = self.data['label'].map(self.label_dict)

    def create_labels(self, data_dir):
        """
                    Creates and encodes labels from the dataset folder.

                    This method assumes that the dataset consists of subdirectories named after
                    the class labels, each containing images of that class. It processes these
                    subdirectories, encodes the labels numerically, and stores them in a DataFrame.

                    Args:
                        data_dir (str): The name of the folder containing the dataset.
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
        """
                Extracts a ZIP file if it is not already unzipped.

                This method checks if the dataset directory exists. If not, it attempts to
                extract the ZIP file containing the dataset.

                Args:
                    current_path (str): The path where the script is executed.
                    zip_file (str): The name of the zipfile.
                    data_dir (str): The directory where the dataset should be extracted.

                Returns:
                    None
        """
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
        """
              Normalizes the dataset by converting images to numpy arrays and scaling pixel values.

              This method ensures that pixel values are in the range [0,1] for better training
              efficiency in deep learning models.

              Returns:
                  None
          """
        self.images = np.array(self.images)
        self.labels = np.array(self.data['label'])
        # Normalization
        self.images = self.images / 255.0

        print("The Dataset has been Processed Successfully!\n",
              f"Total images:\t {len(self.images)}")
