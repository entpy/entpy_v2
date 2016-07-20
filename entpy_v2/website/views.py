from django.shortcuts import render

def www_index(request):
    """Home page view"""

    context = {}

    return render(request, 'website/www/www_index.html', context)
