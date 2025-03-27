Installation Prerequisites
==========================

This project is a **Data Analytics Application** built using a **Tkinter GUI frontend** and a **Django backend**, managed with **Conda** for environment setup and reproducibility.

Before running the application, make sure you have the following installed and configured on your system:

Requirements
------------

- Python 3.10
- Anaconda or Miniconda (for Conda environment management)

Environment Setup
-----------------

1. Open **Anaconda Prompt** (or any terminal with Conda initialized).
2. Confirm Conda is installed:

   .. code-block:: bash

      conda --version

3. Navigate to the directory containing the `env_setup.yml` file.
4. Create the environment using:

   .. code-block:: bash

      conda env create -f env_setup.yml

   The `env_setup.yml` includes the following libraries:

   **pandas==2.2.3, numpy==1.26.4, matplotlib==3.9.2, scikit-learn==1.4.2, Django==5.1.4, djangorestframework, requests, catboost==1.2.7, xgboost==2.1.2, tensorflow==2.16.1, statsmodels==0.14.4, customtkinter, seaborn**

5. Activate the environment:

   .. code-block:: bash

      conda activate oopEnv

Running the Application
-----------------------

**Backend**

1. Navigate to the `scripts` folder:

   .. code-block:: bash

      cd "C:\Users\YOUR_USERNAME\Path\To\data-analytics\scripts"

2. Start the Django backend server:

   .. code-block:: bash

      run_backend.bat

   This will activate the environment and start the Django development server at:
   http://127.0.0.1:8000/

**Frontend**

1. From the same `scripts` folder, run the frontend GUI:

   .. code-block:: bash

      run_frontend.bat

   This will launch the Tkinter desktop application.
