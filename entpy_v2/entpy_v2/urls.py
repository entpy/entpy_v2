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
from django.conf.urls import url
# from django.contrib import admin
from website import views

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^$', views.www_index, name='www_index'),
    url(r'^chi-siamo/$', views.www_about, name='www_about'),
    url(r'^servizi/$', views.www_services, name='www_services'),
    url(r'^contatti/$', views.www_contact_us, name='www_contact_us'),
    url(r'^404/$', views.www_404, name='www_404'),
    url(r'^send_info_email/$', views.send_info_email, name='send_info_email'),

    # landing
    url(r'^realizzazione-siti/$', views.l_www_landing1, name='l_www_landing1'),
]
