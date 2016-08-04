from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import HttpResponse
import json

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

@ensure_csrf_cookie
def www_contact_us(request):
    """Contact us page view"""
    return render(request, 'website/www_contact_us.html', {})

def www_404(request):
    """404 page view"""
    return render(request, 'website/www_404.html', {})

@require_POST
def send_info_email(request):
    """View to send an email"""
    if request.method == "POST":
        # prelevo i dati e invio la mail
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        body = request.POST.get("msg")
        subject = "Richiesta informazioni"
        data = {'success' : True}
    else:
        data = {'success' : False}

    # retrieve JSON response
    return HttpResponse(json.dumps(data), content_type="application/json")
