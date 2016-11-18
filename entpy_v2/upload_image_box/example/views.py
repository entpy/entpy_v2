# -*- coding: utf-8 -*-

from django.shortcuts import render
from upload_image_box.example.forms import *
from django.conf import settings
from upload_image_box.settings import *

# Example view
def upload_example(request):
    # if you want to upload inside a custom directory
    # request.session['CUSTOM_CROPPED_IMG_DIRECTORY'] = CUSTOM_CROPPED_IMG_DIRECTORY

    # if a GET (or any other method) we'll create a blank form
    form_no_crop = uploadedImagesNoCropForm()
    form_crop = uploadedImagesCropForm()

    context = {
        "post" : request.POST,
        "form_no_crop": form_no_crop,
        "form_crop": form_crop,
    }

    return render(request, 'upload_image_box/upload_example.html', context)
