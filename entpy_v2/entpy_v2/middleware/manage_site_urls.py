# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import set_urlconf
from website_data.models import WebsiteData
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

class ManageSiteUrls(object):
    def process_request(self, request):
        """ In base all'URL tiro fuori il ROOT_URLCONF da utilizzare """
        current_site = False
        website_key_val_dict = False
        try:
            # non ho settato un SITE_ID nelle preferenze, mi baso esclusivamente
            # sul nome dominio, infatti nella tabella site DEVE essere settata una riga per questo dominio
            current_site = get_current_site(request)
            logger.info("site found with domain: " + str(current_site))

            # prelevo tutte le chiavi del dominio trovato
            WebsiteData_obj = WebsiteData()
            website_key_val_dict = WebsiteData_obj.get_all_keys_about_site(site_domain=current_site)

            # identifico il ROOT_URLCONF da utilizzare
            # http://stackoverflow.com/questions/18322262/how-to-setup-custom-middleware-in-django
            # settando request.urlconf, sovrascrivo il valore di ROOT_URLCONF
            # scritto in settings.py
            if website_key_val_dict.get("root_urlconf") == "classic" or website_key_val_dict.get("root_urlconf") == "simple":
                # il sito è attivo ed utilizza le app 'classic' o 'simple'
                request.urlconf = str(website_key_val_dict.get("root_urlconf")) + ".urls"
            else:
                # ROOT_URLCONF di default, (sto visitando entpy.com oppure un
                # sito è scaduto e redirigo qui)
                request.urlconf = settings.ROOT_URLCONF

        except ObjectDoesNotExist:
            logger.error("no site found with current domain: " + str(request.get_host()))

        return None
