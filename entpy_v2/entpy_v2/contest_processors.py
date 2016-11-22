# -*- coding: utf-8 -*-

# contest processor to manage common vars
from django.conf import settings
from entpy_v2.consts import project_constants
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ObjectDoesNotExist
from website_data.models import WebsiteData, WebsitePreferences, ThemeKeys, WebsitePreferenceKeys
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

def common_contest_processors(request):
    """Common template context processor function"""

    # TODO: in base all'URL tiro fuori la stringa corretta e altre
    # informazioni per comporre il sito, capire come tirare fuori le immagini
    current_site = False
    website_key_val_dict = False
    default_key_val_dict = False

    preferences_key_val_dict = False
    default_preferences_key_val_dict = False
    try:
        # non ho settato un SITE_ID nelle preferenze, mi baso esclusivamente
        # sul nome dominio, infatti nella tabella site DEVE essere settata una riga per questo dominio
        current_site = get_current_site(request)
        logger.info("site found with domain: " + str(current_site))

        # prelevo tutte le chiavi del dominio trovato
        WebsiteData_obj = WebsiteData()
        website_key_val_dict = WebsiteData_obj.get_all_keys_about_site(site_domain=current_site)

        # prelevo tutte le chiavi con i relativi default dei temi
        ThemeKeys_obj = ThemeKeys()
        default_key_val_dict = ThemeKeys_obj.get_keys_dictionary()

        # prelevo le preferenze del sito
        WebsitePreferences_obj = WebsitePreferences()
        preferences_key_val_dict = WebsitePreferences_obj.get_preferences_about_site(site_domain=current_site)

        # prelevo le preferenze di default
        WebsitePreferenceKeys_obj = WebsitePreferenceKeys()
        default_preferences_key_val_dict = WebsitePreferenceKeys_obj.get_keys_dictionary()
    except ObjectDoesNotExist:
        logger.error("no site found with current domain: " + str(request.get_host()))

    return {
            'project_constants': project_constants,
            'current_site': current_site,
            'website_key_val_dict': website_key_val_dict,
            'default_key_val_dict': default_key_val_dict,
            'preferences_key_val_dict': preferences_key_val_dict,
            'default_preferences_key_val_dict': default_preferences_key_val_dict,
    }
