import unittest
import os
import shutil
from image_processing.dataloader import DataLoadingAndPreprocessing
from data_object_final import DataObject

# filepath: a:\EVERYTHING_TH_KOELN\OOP\image-processing-oop\image_processing\test_dataloader.py

class TestDataLoadingAndPreprocessing(unittest.TestCase):
    def setUp(self):
        self.data_loader = DataLoadingAndPreprocessing()
        self.dataObj = DataObject()
        self.dataObj.image_processing["fileio"] = {
            "zipFilePath": "A:\\EVERYTHING_TH_KOELN\\OOP\\image-processing-oop\\Numbers_images_dataset.zip",
            "isZipped": True
        }
        self.dataObj.image_processing["train_test_split"] = {
            "test_size": 0.2,
            "random_state": 42
        }
        # Create a mock directory structure for testing
        self.mock_data_dir = "mock_data_dir"
        os.makedirs(self.mock_data_dir, exist_ok=True)
        for label in ["zero", "one"]:
            label_dir = os.path.join(self.mock_data_dir, label)
            os.makedirs(label_dir, exist_ok=True)
            with open(os.path.join(label_dir, "image1.png"), "w") as f:
                f.write("mock image content")

    def tearDown(self):
        # Clean up the mock directory structure
        shutil.rmtree(self.mock_data_dir)

    def test_data_loader(self):
        self.data_loader.data_loader(self.dataObj.image_processing["fileio"])
        self.assertIsNotNone(self.data_loader.data)
        self.assertIsNotNone(self.data_loader.images)
        self.assertGreater(len(self.data_loader.images), 0)

    def test_get_label_dict(self):
        self.data_loader.data_loader(self.dataObj.image_processing["fileio"])
        label_dict = self.data_loader.get_label_dict()
        self.assertIsInstance(label_dict, dict)

    def test_split_dataset(self):
        self.data_loader.data_loader(self.dataObj.image_processing["fileio"])
        splits = self.data_loader.split_dataset(self.dataObj.image_processing["train_test_split"])
        self.assertIn('X_train', splits)
        self.assertIn('X_test', splits)
        self.assertIn('y_train', splits)
        self.assertIn('y_test', splits)

if __name__ == '__main__':
    unittest.main()