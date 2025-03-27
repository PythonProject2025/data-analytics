# Data Analytics Application

This project is built with a Tkinter GUI and a Django backend, managed via Conda for easy setup and reproducibility.

---

## Requirements

- Python 3.10
- Anaconda or Conda installed

---

## Step 1: Set Up Conda Environment

1. Open **Anaconda Prompt** (or terminal with Conda initialized).
2. Check if conda is installed with the conda --version prompt
3. Navigate to the folder where `env_setup.yml` is located.
4. Run the following command: 
    conda env create -f env_setup.yml
5. After creating the conda enviornment we can activate conda using the following commands: 
    conda env create -f env_setup.yml
    conda activate oopEnv

## Step 2: Run the Application

**Backend**
1. Navigate to the scripts folder in your directory for example:
    cd "C:\Users\YOUR_USERNAME\Path\To\data-analytics\scripts"
2. Run the backend script: 
    run_backend.bat
    This will activate the environment and start the Django development server at:http://127.0.0.1:8000/

**Frontend**
1. From the same scripts folder, run :
    run_frontend.bat
    This will launch the Tkinter GUI application.