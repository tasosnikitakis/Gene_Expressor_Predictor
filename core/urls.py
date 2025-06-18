from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # This line includes all the URL patterns from our 'predictor' app.
    # Any URL starting with 'predictor/' will be handled by predictor/urls.py.
    # We are also setting up the root URL ('') to redirect to our app.
    path('', include('predictor.urls')),
    path('predictor/', include('predictor.urls')),
]
