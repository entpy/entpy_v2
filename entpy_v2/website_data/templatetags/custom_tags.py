# -*- coding: utf-8 -*-

from django import template
from django.utils.safestring import mark_safe
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

register = template.Library()

@register.filter
def str_cat(arg1, arg2):
    """Custom filter to concatenate arg1 with arg2"""
    return str(arg1) + str(arg2)

@register.filter
def get_item(dictionary, key):
    """Custom filter to retrieve a value from a dictionary"""
    return dictionary.get(key)

@register.simple_tag
def get_theme_val(saved_dictionary, default_dictionary, key, edit_mode):
    # saved_dictionary, default_dictionary, key, edit_mode
    """Custom filter to retrieve saved theme value or default value"""
    return_var = ""

    """
    logger.debug("saved_dictionary: " + str(saved_dictionary))
    logger.debug("default_dictionary: " + str(default_dictionary))
    logger.debug("key: " + str(key))
    logger.debug("edit_mode: " + str(edit_mode))
    """

    if edit_mode and not saved_dictionary.get(key):
        # se sono in modalità di editing e non ho nessun valore salvato, prendo il default
        return_var = str(default_dictionary.get(key, "ATTENZIONE: default non trovato").get("default"))
    else:
        # se non sono in modalità di editing, prendo sempre il valore salvato, anche se è nullo
        return_var = str(saved_dictionary.get(key, ""))

    return mark_safe(return_var)
