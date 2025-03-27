.. Software Architecture Overview
.. ******************************

.. This project presents a modular and user-friendly **Data Analytics Desktop Application** developed using a **Tkinter-based front end** and a **Django-powered back end**. The application facilitates seamless interaction between users and various data processing and machine learning tasks through RESTful API integration.

Front End: Tkinter GUI
~~~~~~~~~~~~~~~~~~~~~~

The front end provides an intuitive graphical user interface with a multi-page layout. Each page corresponds to a specific task or process and dynamically updates based on user interaction. Key functionalities include:

- **File Uploading**:
  
  - Users can upload `.csv` or `.zip` files through the GUI.
  - `.csv` files are routed to data analysis processes.
  - `.zip` files are routed to image processing workflows.

- **Process Selection**:
  
  For `.csv` files, users choose between:
  
  - Data Filtering & Preprocessing
  - Regression & Classification
  - AI Model-based Analysis

- **Dynamic UI Rendering**:
  
  UI elements (e.g., sliders, dropdowns, radio buttons) change depending on the selected process or model type.

- **Result Display**:
  
  Graphs (e.g., regression plots, residuals, confusion matrices), metrics, and predictions are rendered directly within the GUI using embedded plotting libraries such as ``matplotlib``.


.. automodule:: main_sphinx
    :members:
    :undoc-members:
    :show-inheritance:

.. automodule:: pages.aimodel_page
    :members:
    :undoc-members:
    :show-inheritance:

.. automodule:: pages.data_filtering_page
    :members:
    :undoc-members:
    :show-inheritance:

.. automodule:: pages.file_upload_page
    :members:
    :undoc-members:
    :show-inheritance:

.. automodule:: pages.image_processing_page
    :members:
    :undoc-members:
    :show-inheritance:

.. automodule:: pages.process_selection_page
    :members:
    :undoc-members:
    :show-inheritance:

.. automodule:: pages.regression_classification
    :members:
    :undoc-members:
    :show-inheritance:

.. automodule:: pages.help_page
    :members:
    :undoc-members:
    :show-inheritance:


Back End: Django API
~~~~~~~~~~~~~~~~~~~~

The Django backend serves as the processing engine and is structured around modular views and serializers. Key responsibilities include:

- **Process Handling**:

  Performs data transformations, model training, predictions, and visualizations.

- **Modular APIs**:

  Four dedicated API routes handle distinct functionality:

  1. **Data Filtering & Preprocessing**
  2. **Regression & Classification**
  3. **AI Models**
  4. **Image Processing**


.. automodule:: backend.api.image_processing_engine
    :members:
    :undoc-members:
    :show-inheritance:

.. automodule:: backend.api.data_preprocessing_engine
    :members:
    :undoc-members:
    :show-inheritance:

.. automodule:: backend.api.ai_models_engine
    :members:
    :undoc-members:
    :show-inheritance:
    
.. automodule:: backend.api.scaling_encoding_engine
    :members:
    :undoc-members:
    :show-inheritance:

.. automodule:: backend.api.regression_engine
    :members:
    :undoc-members:
    :show-inheritance:

.. automodule:: backend.api.classification_engine
    :members:
    :undoc-members:
    :show-inheritance: