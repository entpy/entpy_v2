# -*- coding: utf-8 -*-

from django import forms
from django.contrib import admin
from upload_image_box.widgets import UibUploaderInput
from website_data.models import *

class EditTextSiteForm(forms.Form):
    """
    Form to edit all text about a site
    """

    # custom upload button template
    custom_upload_button = '<div data-widget-id="%(widget_id)s" class="uploaderButtonClickAction upload_profile_image_button btn btn-success bootstrap-trigger">%(widget_button_text)s</div>'
    # form fields
    widget_attr = {
            'widget_id': 'uploader_1',
            'enable_crop': True,
            'default_uploader_button': custom_upload_button,
            'callback_function': 'saveProfileImage',
            'base_modal_title_text': "Seleziona un'immagine",
            'base_modal_description_text': "Per caricare un'immagine clicca sul pulsante sotto.",
            'upload_modal_title_text': 'Caricamento in corso, attendi...',
            'moving_ball_modal_title_text': 'Caricamento in corso, attendi...',
            'crop_modal_title_text': 'Seleziona area immagine',
            'preview_modal_title_text': 'Anteprima immagine',
            'crop_action_button_text': 'Conferma immagine',
            'select_image_action_button_text': 'Seleziona immagine',
            'widget_button_text': 'Carica immagine',
            'preview_action_button_text': 'Conferma immagine',
            'cancel_button_text': 'Chiudi',
            'change_image_button_text': 'Cambia immagine',
            'crop_modal_description_text': "Seleziona la porzione dell'immagine per il tuo profilo",
    }
    uploaded_image = forms.CharField(label="Carica immagine", widget=UibUploaderInput(attrs=widget_attr))
    image_id = forms.CharField(widget=forms.HiddenInput())
    image_type = forms.CharField(widget=forms.HiddenInput())

    """
    def __init__(self, *args, **kwargs):


        # parent forms.Form init
        super(EditTextSiteForm, self).__init__(*args, **kwargs)

        ThemeKeys_obj = ThemeKeys()
        keys_list = ThemeKeys_obj.get_defaults_keys()

        if keys_list:
            for theme in keys_list:
                for key_name in keys_list[theme]:
                    self.fields[key_name] = forms.CharField(
                        label=key_name,
                        required=False,
                        widget=forms.Textarea(attrs={"placeholder" : key_name, "theme_name" : theme})) 
        """


class PersonAdmin(admin.ModelAdmin):
    form = EditTextSiteForm
