from django.shortcuts import render

def home(request):
    """
    Renders the main portfolio homepage.
    """
    # You can pass context to the template here if needed in the future
    context = {
        'project_title': 'Gene Expression Cancer Classifier',
        'project_description': 'A full-stack web application that uses a machine learning model to predict cancer types from RNA-Seq data.',
        'project_link': '/predictor/' # Link to your other Django app
    }
    return render(request, 'portfolio/home.html', context)
