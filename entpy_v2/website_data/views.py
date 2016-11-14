# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse, Http404
from website_data.models import ThemeKeys

def create_defaults(request):
    """View to create default keys and themes"""
    ThemeKeys_obj = ThemeKeys()
    ThemeKeys_obj.create_default_keys()

    return HttpResponse("Default creati o aggiornati")
