# -*- coding: utf-8 -*-

from django import forms
from django.contrib import admin
from website_data.models import *

class EditTextSiteForm(forms.Form):
    """
    Form to edit all text about a site
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

class PersonAdmin(admin.ModelAdmin):
    form = EditTextSiteForm
