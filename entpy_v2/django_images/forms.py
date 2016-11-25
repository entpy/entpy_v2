# -*- coding: utf-8 -*-

from django import forms

class ValidateCodeForm(forms.Form):
    """
    Form to upload a new image
    """

    image = forms.CharField()
