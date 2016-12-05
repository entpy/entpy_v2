# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.core.mail import send_mail
from django.http import HttpResponse, Http404

@ensure_csrf_cookie
def index(request, action = False):
    """Index view"""
    context = {}
    if action == "edit":
        context = {
            'edit': True,
        }
    return render(request, 'simple/index.html', context)
