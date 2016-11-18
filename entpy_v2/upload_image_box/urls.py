from django.conf.urls import url
from upload_image_box import views

urlpatterns = [
    url(r'^upload/', views.upload, name='upload'),
    url(r'^crop/', views.crop, name='crop'),
]
