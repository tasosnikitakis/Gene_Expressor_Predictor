from django.urls import path
from . import views

# This is a list of URL patterns for the 'portfolio' app.
urlpatterns = [
    # The root path of the site will call the 'home' view
    path('', views.home, name='home'),
]
