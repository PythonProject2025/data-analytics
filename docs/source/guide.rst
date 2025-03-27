Step-by-Step Usage Guide
========================
This guide provides a clear walkthrough of how to use the Data Analytics UI, from uploading files and selecting modules to processing data, interpreting results, and refining your analysis. Follow each step to make the most of the platform’s features.

Uploading a File and Selecting a Module
---------------------------------------

1. **Upload a file** using the file uploader on the main page.

   Supported file types:
   - ``.csv`` for structured data
   - ``.zip`` for image datasets

2. **Conditional Navigation**:

   - If a **CSV file** is uploaded:
   - The UI automatically navigates to the **Data Filtering Page**.
   - If a **ZIP file** is uploaded:
   - The UI automatically navigates to the **Image Processing Page**.

3. **For CSV files**, the user can select one of the following:
   - **Filtering Process**
   - **Scaling and Encoding**

Processing the Data and Generating Outputs
------------------------------------------

**For CSV Files (Data Filtering Page):**

1. **Filtering Process** (must be done step-by-step):
   
   a. Outlier Detection  
   b. Interpolation  
   c. Smoothing  
   d. Scaling and Encoding

   After each step:
   - The user can **export the intermediate data**.
   - Results can be **compared** with previous steps.

2. **Direct Scaling and Encoding**:
   - The user can skip filtering and go straight to scaling/encoding.

3. **Send Processed Data**:
   - After completing either filtering or encoding,
   - Clicking the **Send** button forwards the data to:
   - **Regression & Classification Page**, or
   - **AI Model Page**, based on user selection.

**For ZIP Files (Image Processing Page):**

- The system navigates directly to the **Image Processing Module**.
- The user can:
  - Perform various **image processing operations**
  - **Set parameters**
  - View and **save outputs**

Interpreting Results and Refining Analysis
------------------------------------------

1. **Regression & Classification Page**:
   - Users set parameters
   - Train models
   - View prediction outputs and performance metrics

2. **AI Model Page**:
   - Select and configure AI models
   - Visualize and evaluate output results

3. **Image Processing Page**:
   - Tune processing parameters
   - Validate and refine image outputs

4. **Iteration and Export**:
   - At any point, users can:
   - Export current or intermediate results
   - Revisit and refine previous steps
   - Reprocess data/images for improved analysis
