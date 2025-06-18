from django.urls import path
from . import views

# This is a list of URL patterns for the 'predictor' app.
# Django will look here after being directed from the main project's urls.py.
urlpatterns = [
    # The root path of this app, e.g., /predictor/
    # This will render the main page using the 'index' view.
    path('', views.index, name='index'),

    # API endpoint to get the data for the scatter plot
    # Accessible at /predictor/get_pca_data/
    path('get_pca_data/', views.get_pca_data, name='get-pca-data'),
    
    # API endpoint to trigger a prediction
    # Accessible at /predictor/predict/
    path('predict/', views.predict, name='predict'),
]
