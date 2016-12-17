# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib import messages
from django.core.mail import send_mail, EmailMessage, EmailMultiAlternatives
from django.http import HttpResponse, Http404, HttpResponseRedirect
from website.models import Promotion, Campaign
from entpy_v2.consts import project_constants
import logging, json

@ensure_csrf_cookie
def www_index(request):
    """Home page view"""
    return render(request, 'website/www_index.html', {})

@ensure_csrf_cookie
def www_about(request):
    """About us page view"""
    return render(request, 'website/www_about.html', {})

@ensure_csrf_cookie
def www_services(request):
    """Services page view"""
    return render(request, 'website/www_services.html', {})

@ensure_csrf_cookie
def www_portfolio(request):
    """Portfolio page view"""
    return render(request, 'website/www_portfolio.html', {})

@ensure_csrf_cookie
def www_contact_us(request, promo_code=None):
    """Contact us page view"""

    context = {
            'promo_code' : promo_code,
    }

    return render(request, 'website/www_contact_us.html', context)

@ensure_csrf_cookie
def www_404(request):
    """404 page view"""
    return render(request, 'website/www_404.html', {})

@require_POST
@ensure_csrf_cookie
def send_info_email(request):
    """View to send an email"""
    if request.method == "POST":
        # retrieve email data
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        promo_code = request.POST.get("promo_code")
        txt_message = "Nome: " + name + "\nMittente: " + str(email) + "\nTelefono:" + str(phone) + "\nMessaggio: " + request.POST.get("msg") + "\nCodice promozionale: " + str(promo_code)
        html_message = "Nome: " + name + "<br />Mittente: " + str(email) + "<br />Telefono:" + str(phone) + "<br />Messaggio: " + request.POST.get("msg") + "\nCodice promozionale: " + str(promo_code)
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

# TODO
@ensure_csrf_cookie
def l_www_landing1(request):
    """Landing page1: sito web gratis"""

    data = {}

    """
    theme_name
    domain_name
    user_name
    user_email
    business_name
    business_info
    """

    if request.method == "POST":
        # retrieve email data
        user_name = request.POST.get("user_name")
        user_email = request.POST.get("user_email")
        domain_name = request.POST.get("domain_name")
        theme_name = request.POST.get("theme_name")
        business_name = request.POST.get("business_name")
        business_info = request.POST.get("business_info")

        # body della mail
        txt_message = """
            Nome: """ + user_name + """\n
            Email: """ + user_email + """\n
            Dominio scelto: """ + domain_name + """.entpy.com\n
            Tema scelto: """ + theme_name + """\n
            Nome attività: """ + business_name + """\n
            Informazioni attività: """ + business_info
        
        html_message = """
            Nome: """ + user_name + """<br />
            Email: """ + user_email + """<br />
            Dominio scelto: <b>""" + domain_name + """</b>.entpy.com<br />
            Tema scelto: """ + theme_name + """<br />
            Nome attività: """ + business_name + """<br />
            Informazioni attività: """ + business_info

        # subject della mail
        subject = "Richiesta sito web gratis"

        # send email
        msg = EmailMultiAlternatives(
            subject=subject,
            body=txt_message,
            from_email="no-reply@entpy.com",
            to=["info@entpy.com"],
            reply_to=[user_email],
        )
        msg.attach_alternative(html_message, "text/html")
        send_status = msg.send()

        # data = {'success' : True, "send_status" : send_status }
        messages.add_message(request, messages.SUCCESS, 'Grazie per aver richiesto il sito, verrai ricontattato/a il prima possibile alla mail indicata!')
	return HttpResponseRedirect("/sito-web-gratis")

    return render(request, 'website/l/www_landing1.html', data)

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

@require_POST
def create_promotion_AJAX(request):
    """ View to create a promo code via AJAX call"""

    http_response = None
    promotion_obj = Promotion()
    campaign_obj = Campaign()
    promotion_type = request.POST.get("promotion_type")
    extra_text = request.POST.get("extra_text")

    if not promotion_type or not promotion_type:
        raise Http404()

    # creo una nuova promozione
    if promotion_type == Promotion.PROMOTION_TYPE_SERVICE["key"]:
        id_promotion = promotion_obj.create_promotion(
            name = "Promozione per un servizio (sconto del " + str(project_constants.SERVICE_BONUS_DISCOUNT) + "%)",
            description = "Lo sconto è da applicare sul servizio: " + str(extra_text),
            promo_type = Promotion.PROMOTION_TYPE_SERVICE["key"],
            expiring_date = None,
        )
    elif promotion_type == Promotion.PROMOTION_TYPE_WIZARD["key"]:
        id_promotion = promotion_obj.create_promotion(
            name = "Promozione per un obiettivo (sconto del " + str(project_constants.WIZARD_BONUS_DISCOUNT) + "%)",
            description = "Lo sconto è da applicare sull'obiettivo: " + str(extra_text),
            promo_type = Promotion.PROMOTION_TYPE_WIZARD["key"],
            expiring_date = None,
        )

    if id_promotion:
        # associo la promozione creata ad una campagna
        id_campaign = campaign_obj.add_frontend_post_campaign(id_promotion=id_promotion)

        # prelevo le info della campagna creata
        campaign_details = campaign_obj.get_campaign_details(id_campaign=id_campaign)

        # create http response
        http_response = HttpResponse(json.dumps(campaign_details), content_type="application/json")

    # return a JSON response
    return http_response
