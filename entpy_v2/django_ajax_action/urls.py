from django.conf.urls import url
from django_ajax_action import views

urlpatterns = [
    url(r'^$', views.ajax_action, name='ajax_action'),
]
