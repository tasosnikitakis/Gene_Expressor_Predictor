Gene Expression-Based Cancer Type Classification
Project Overview
This project serves as a full-stack demonstration of bioinformatics data analysis, machine learning, and web application development. The core goal is to build and deploy a machine learning model capable of predicting different types of cancer (BRCA, KIRC, COAD, LUAD, PRAD) based on their gene expression (RNA-Seq) profiles.

The project encompasses the entire data science pipeline, from raw data processing to a live, interactive web application.

GitHub Repository: https://github.com/tasosnikitakis/Gene_Expressor_Predictor
Live Application Demo: [Link to your deployed application (e.g., on PythonAnywhere, Heroku)]

Technical Stack
Data Analysis & Machine Learning: Python, Pandas, NumPy, Scikit-learn, Matplotlib, Seaborn, Jupyter Notebook

Backend: Django

Frontend: HTML5, CSS3, JavaScript (ES6+), Chart.js

Dataset
This project uses the "Gene Expression Cancer RNA-Seq" dataset from the UCI Machine Learning Repository, containing 801 samples and 20,531 gene features across five tumor types.

Project Structure
.
├── core/                       # Django project directory
├── data/                       # Pre-processed data for the app
├── model/                      # Saved ML model and transformers
├── predictor/                  # Django app for our predictor
├── .gitignore
├── manage.py
├── README.md
└── requirements.txt

How to Run This Project Locally
Prerequisites
Python 3.8+ & pip

Git

1. Clone & Setup
# Clone the repository
git clone https://github.com/tasosnikitakis/Gene_Expressor_Predictor
cd Gene_Expressor_Predictor

# Set up and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows, use `.\venv\Scripts\activate`

# Install dependencies
pip install -r requirements.txt

2. Run Migrations
Set up the initial Django database tables.

python manage.py migrate

3. Start the Web Server
python manage.py runserver

The application will be accessible at http://127.0.0.1:8000 in your browser.

Methodology
1. Dimensionality Reduction
Given the high dimensionality (>20,000 features), Principal Component Analysis (PCA) was essential. The data was first scaled using StandardScaler. Analysis showed that the first 387 principal components were required to explain 95% of the variance in the data. This significantly reduced the feature space, making the model more efficient and less prone to overfitting.

2. Model Training & Performance
A Random Forest Classifier (n_estimators=100) was trained on the PCA-transformed data. The dataset was split into 80% for training and 20% for testing, using stratification to maintain class proportions.

The model achieved a respectable accuracy of ~86% on the unseen test set.

A deeper look at the classification report revealed key insights into the model's real-world performance on this imbalanced dataset:

Strong Performance: The model was highly effective at identifying KIRC (Kidney) and PRAD (Prostate) cancers, with high precision and recall.

Imbalance Effects:

For BRCA (Breast), the majority class, the model achieved 100% recall but lower precision (~73%), indicating it correctly found all true BRCA samples but also mislabeled some other cancer types as BRCA.

For LUAD (Lung), a minority class, the model struggled with recall (~57%), failing to identify nearly half of the true lung cancer samples.

This outcome highlights a classic challenge in machine learning. While the model is effective, its performance reflects the underlying data imbalance. Future work could involve techniques like SMOTE (Synthetic Minority Over-sampling Technique) to create a more balanced training set and potentially improve recall for minority classes.

3. Web Application
A Django application was built to serve the model via a RESTful API. The frontend uses Chart.js to visualize the PCA data and JavaScript's Fetch API to communicate with the backend for live predictions.
