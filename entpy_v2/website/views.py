from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import ensure_csrf_cookie
from django.core.mail import send_mail
from django.http import HttpResponse
from website.models import Promotion
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
        txt_message = "Nome: " + name + "\nMittente: " + str(email) + "\nTelefono:" + str(phone) + "\nMessaggio: " + request.POST.get("msg")
        html_message = "Nome: " + name + "<br />Mittente: " + str(email) + "<br />Telefono:" + str(phone) + "<br />Messaggio: " + request.POST.get("msg")
        if int(request.POST.get("is_promo", 0)):
            subject = "Richiesta informazioni (promozione)"
        else:
            subject = "Richiesta informazioni"

        # send email
        send_status = send_mail(
            subject=subject,
            message=txt_message,
            from_email="no-reply@entpy.com",
            recipient_list=["info@entpy.com"],
            html_message=html_message,
        )

        data = {'success' : True, "send_status" : send_status }
    else:
        data = {'success' : False, "send_status" : send_status }

    # retrieve JSON response
    return HttpResponse(json.dumps(data), content_type="application/json")

@ensure_csrf_cookie
def l_www_landing1(request):
    """Landing page1"""
    return render(request, 'website/l/www_landing1.html', {})

@ensure_csrf_cookie
def www_wizard(request):
    """Pagina con la scelta guidata"""
    return render(request, 'website/www_wizard.html', {})

@ensure_csrf_cookie
def www_static_site(request):
    """Pagina di info"""
    return render(request, 'website/www_static_site.html', {})

@ensure_csrf_cookie
def www_landing_pages(request):
    """Landing page"""
    return render(request, 'website/www_landing_pages.html', {})

@ensure_csrf_cookie
def www_dynamic_site(request):
    """Dynamic sites"""
    return render(request, 'website/www_dynamic_site.html', {})

@ensure_csrf_cookie
def www_seo(request):
    """SEO"""
    return render(request, 'website/www_seo.html', {})

@ensure_csrf_cookie
def www_app(request):
    """App"""
    return render(request, 'website/www_app.html', {})

@ensure_csrf_cookie
def www_advertising(request):
    """Advertising"""
    return render(request, 'website/www_advertising.html', {})

@ensure_csrf_cookie
def www_our_offers(request):
    """Our Offers"""
    promotion_obj = Promotion()

    # list of all valid promotion (not expired) with type = frontend_post
    valid_promotion_dict = promotion_obj.get_valid_promotions_list()

    context = {
            'promotion_list' : valid_promotion_dict,
    }

    return render(request, 'website/www_our_offers.html', context)
