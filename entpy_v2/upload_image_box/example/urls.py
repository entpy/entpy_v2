from django.conf.urls import patterns, url
from upload_image_box.example import views

urlpatterns = patterns('',
    url(r'^', views.upload_example, name='upload_example'),
)
