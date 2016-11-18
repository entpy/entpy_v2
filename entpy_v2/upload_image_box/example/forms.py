# -*- coding: utf-8 -*-

from django.forms import ModelForm
from upload_image_box.models import tmpUploadedImages, cropUploadedImages
from upload_image_box.widgets import UibUploaderInput
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

# example forms {{{
class uploadedImagesNoCropForm(ModelForm):
    class Meta:
        model = tmpUploadedImages
	fields = ("image",)
        custom_upload_button = '<div style="background-color: cyan; display: inline-block; text-align: center; cursor: pointer; color: #666; padding: 10px; margin: 10px; width: 200px; border-radius: 5px;" data-widget-id="%(widget_id)s" class="uploaderButtonClickAction">%(widget_button_text)s</div>'
        widgets = {
            'image': UibUploaderInput(attrs={'widget_id': 'uploader_no_crop', "enable_crop": "", "widget_button_text": "No crop load", "crop_modal_description_text": "Seleziona la porzione dell'immagine per il tuo profilo", "default_uploader_button": custom_upload_button}),
        }

class uploadedImagesCropForm(ModelForm):
    class Meta:
        model = tmpUploadedImages
	fields = ("image",)
        widgets = {
            'image': UibUploaderInput(attrs={'widget_id': 'uploader_crop', "enable_crop": True, "widget_button_text": "Crop load", "crop_modal_description_text": "Seleziona la porzione dell'immagine per il tuo profilo"}),
        }
# example forms }}}
