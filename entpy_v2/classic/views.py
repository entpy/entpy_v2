# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.core.mail import send_mail
from django.http import HttpResponse, Http404

@ensure_csrf_cookie
def index(request):
    """Index view"""
    return render(request, 'classic/index.html', {})

@ensure_csrf_cookie
def about(request):
    """About view"""
    return render(request, 'classic/about.html', {})

@ensure_csrf_cookie
def services(request):
    """Services view"""
    return render(request, 'classic/services.html', {})

@ensure_csrf_cookie
def contacts(request):
    """Contacts view"""
    return render(request, 'classic/contacts.html', {})
