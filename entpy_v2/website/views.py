from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import ensure_csrf_cookie
from django.core.mail import send_mail
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
        # retrieve email data
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        message = "Nome: " + name + "\nMittente: " + str(email) + "\nMessaggio: " + request.POST.get("msg")
        subject = "Richiesta informazioni"

        # send email
        send_status = send_mail(
            subject=subject,
            message=message,
            from_email="no-reply@entpy.com",
            recipient_list=["info@entpy.com"],
            html_message=message,
        )

        data = {'success' : True, "send_status" : send_status }
    else:
        data = {'success' : False, "send_status" : send_status }

    # retrieve JSON response
    return HttpResponse(json.dumps(data), content_type="application/json")
