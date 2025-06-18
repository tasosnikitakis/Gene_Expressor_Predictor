import os
import pickle
import numpy as np
import pandas as pd
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render

# --- Load Models and Pre-processed Data at Server Start ---

# For robust path handling
PROJECT_ROOT = settings.BASE_DIR
print(f"Project base directory is: {PROJECT_ROOT}")

# Construct paths to the model and data files
model_path = os.path.join(PROJECT_ROOT, 'model', 'random_forest_model.pkl')
pca_plot_data_path = os.path.join(PROJECT_ROOT, 'data', 'pca_plot_data.csv')
x_test_path = os.path.join(PROJECT_ROOT, 'data', 'X_test_data.csv')
y_test_path = os.path.join(PROJECT_ROOT, 'data', 'y_test_data.csv')

# Globals to hold our models and data, initialized to None
model = None
pca_plot_df = None
X_test_df = None
y_test_df = None

# --- NEW: More Robust File Loading with Detailed Logging ---
files_to_load = {
    "Model": model_path,
    "PCA Plot Data": pca_plot_data_path,
    "X Test Data": x_test_path,
    "Y Test Data": y_test_path
}

print("\n--- Checking for model and data files ---")
all_files_found = True
for name, path in files_to_load.items():
    if os.path.exists(path):
        print(f"✔ Found {name} at: {path}")
    else:
        print(f"❌ ERROR: Could not find {name}. Expected at: {path}")
        all_files_found = False

# Load the files only if all of them were found
if all_files_found:
    try:
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        
        pca_plot_df = pd.read_csv(pca_plot_data_path)
        X_test_df = pd.read_csv(x_test_path)
        y_test_df = pd.read_csv(y_test_path)
        
        print("\n✅ Model and pre-processed data loaded successfully into memory.")

    except Exception as e:
        print(f"\n❌ CRITICAL ERROR: An error occurred while loading the files: {e}")
        # Ensure globals are reset to None if loading fails
        model = pca_plot_df = X_test_df = y_test_df = None
else:
    print("\n❌ CRITICAL ERROR: One or more files were not found. The API endpoints will not work.")
# --- END of New Loading Logic ---


# --- Django Views ---

def index(request):
    """
    Renders the main page of the application (index.html).
    """
    return render(request, 'predictor/index.html')

def get_pca_data(request):
    """
    API endpoint to provide the data for the scatter plot.
    """
    if pca_plot_df is not None:
        data = pca_plot_df.to_dict(orient='records')
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'error': 'PCA plot data not available because a file failed to load on startup.'}, status=500)

def predict(request):
    """
    API endpoint to predict the cancer type for a random sample from the test set.
    """
    if model is None or X_test_df is None or y_test_df is None:
        return JsonResponse({'error': 'Model or test data not available because a file failed to load on startup.'}, status=500)

    try:
        # Select a random sample from the pre-processed test set
        random_index = np.random.randint(0, len(X_test_df))
        # Get the DataFrame row
        sample_df_row = X_test_df.iloc[[random_index]]
        # Get the true label
        true_label = y_test_df.iloc[random_index]['Class']
        
        # --- FIX: Convert to NumPy array to avoid feature name warning ---
        sample_data = sample_df_row.values
        
        # Make a prediction
        prediction = model.predict(sample_data)[0]

        # Prepare the response
        response = {
            'sample_name': f"Test Sample #{random_index}",
            'predicted_class': prediction,
            'true_class': true_label
        }
        return JsonResponse(response)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
