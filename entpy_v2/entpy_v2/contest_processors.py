# -*- coding: utf-8 -*-

# contest processor to manage common vars
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.sites.models import Site
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import set_urlconf
from entpy_v2.consts import project_constants
from website_data.models import WebsiteData
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

def common_contest_processors(request):
    """Common template context processor function"""

    # TODO: in base all'URL tiro fuori la stringa corretta e altre
    # informazioni per comporre il sito, capire come tirare fuori le immagini
    current_site = False
    website_key_val_dict = False
    try:
        # non ho settato un SITE_ID nelle preferenze, mi baso esclusivamente
        # sul nome dominio, infatti nella tabella site è settata una riga con
        # questo dominio
        current_site = get_current_site(request)
        logger.info("site found with domain: " + str(current_site))

        # prelevo tutte le chiavi del dominio trovato
        WebsiteData_obj = WebsiteData()
        website_key_val_dict = WebsiteData_obj.get_all_keys_about_site(site_domain=current_site)

        # TODO: capire come fare
        # setto il corretto urlconfig come ROOT
        #if current_site == "127.0.0.1:8000":
        set_urlconf("simple.urls")
        #request.urlconf = "classic.urls"

    except ObjectDoesNotExist:
        logger.error("no site found with current domain: " + str(request.get_host()))

    return {
            'project_constants': project_constants,
            'current_site': current_site,
            'website_key_val_dict': website_key_val_dict,
    }
