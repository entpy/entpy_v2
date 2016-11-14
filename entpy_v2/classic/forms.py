# -*- coding: utf-8 -*-

from django import forms

class EditTextSiteForm(forms.Form):
    """
    Form to edit all text about a site
    """

    self.fields[question_code] = forms.ChoiceField(
        label=question_label,
        choices=answer_choices,
        required=question_info.get("required"),
        widget=forms.TextInput(attrs=widget_attrs)) 
