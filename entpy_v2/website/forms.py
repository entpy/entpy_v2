# -*- coding: utf-8 -*-

from django import forms

class ValidateCodeForm(forms.Form):
    """
    Form to validate a coupon code, this form is not related with any object
    """

    promo_code = forms.CharField(max_length=10, required=True)
