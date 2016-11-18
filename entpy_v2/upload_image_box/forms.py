# -*- coding: utf-8 -*-

from django.forms import ModelForm
from upload_image_box.models import tmpUploadedImages, cropUploadedImages
from upload_image_box.widgets import UibUploaderInput
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

class tmpUploadImagesCropForm(ModelForm):
    class Meta:
        model = tmpUploadedImages
	fields = ("image",)
        widgets = {
            'image': UibUploaderInput(attrs={'widget_id': 'tmp_uploader_image',}),
        }
