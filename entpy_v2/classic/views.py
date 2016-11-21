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
    return render(request, 'classic/index.html', context)

@ensure_csrf_cookie
def about(request, action = False):
    """About view"""
    context = {}
    if action == "edit":
        context = {
            'edit': True,
        }
    return render(request, 'classic/about.html', context)

@ensure_csrf_cookie
def services(request, action = False):
    """Services view"""
    context = {}
    if action == "edit":
        context = {
            'edit': True,
        }
    return render(request, 'classic/services.html', context)

@ensure_csrf_cookie
def contacts(request, action = False):
    """Contacts view"""
    context = {}
    if action == "edit":
        context = {
            'edit': True,
        }
    return render(request, 'classic/contacts.html', context)
