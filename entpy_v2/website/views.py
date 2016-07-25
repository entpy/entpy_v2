from django.shortcuts import render

def www_index(request):
    """Home page view"""
    return render(request, 'website/www_index.html', {})

def www_about(request):
    """About us page view"""
    return render(request, 'website/www_about.html', {})

def www_services(request):
    """Services page view"""
    return render(request, 'website/www_services.html', {})

def www_portfolio(request):
    """Portfolio page view"""
    return render(request, 'website/www_portfolio.html', {})

def www_contact_us(request):
    """Contact us page view"""
    return render(request, 'website/www_contact_us.html', {})

def www_404(request):
    """404 page view"""
    return render(request, 'website/www_404.html', {})
