"""entpy_v2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from website import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.www_index, name='www_index'),
    url(r'^chi-siamo/$', views.www_about, name='www_about'),
    url(r'^servizi/$', views.www_services, name='www_services'),
    url(r'^contatti/(?:(?P<promo_code>[a-zA-Z0-9-]+)/)?$', views.www_contact_us, name='www_contact_us'),
    url(r'^404/$', views.www_404, name='www_404'),
    url(r'^send_info_email/$', views.send_info_email, name='send_info_email'),
    url(r'^scelta-guidata/$', views.www_wizard, name='www_wizard'),
    url(r'^siti-statici/$', views.www_static_site, name='www_static_site'),
    url(r'^landing-pages/$', views.www_landing_pages, name='www_landing_pages'),
    url(r'^siti-dinamici/$', views.www_dynamic_site, name='www_dynamic_site'),
    url(r'^seo/$', views.www_seo, name='www_seo'),
    url(r'^app/$', views.www_app, name='www_app'),
    url(r'^campagne-pubblicitarie/$', views.www_advertising, name='www_advertising'),
    url(r'^offerte/$', views.www_our_offers, name='www_our_offers'),
    url(r'^create_promotion_AJAX/$', views.create_promotion_AJAX, name='create_promotion_AJAX'),

    # landing (in lavorazione...)
    url(r'^sito-web-gratis/$', views.l_www_landing1, name='l_www_landing1'),

    # classic template
    url(r'^classic/', include('classic.urls')),
    # simple template
    url(r'^simple/', include('simple.urls')),

    # upload image
    url(r'^upload_image/', include('upload_image_box.urls', namespace="upload_image_box")),

    # gestione dei temi
    # url(r'^website_data/', include('website_data.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.MEDIA_URL_TMP, document_root=settings.MEDIA_ROOT)
