# -*- coding: utf-8 -*-

from urlparse import urlparse
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import set_urlconf
from django.utils import timezone
from website_data.models import WebsitePreferences
from django.contrib.sites.models import Site
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

class ManageSiteUrls(object):
    def process_request(self, request):
        """ In base all'URL tiro fuori il ROOT_URLCONF da utilizzare """
        current_site = False
        website_preferences_dict = False
        try:
            # non ho settato un SITE_ID nelle preferenze, mi baso esclusivamente
            # sul nome dominio, infatti nella tabella site DEVE essere settata una riga per questo dominio
            current_site = get_current_site(request)
            Site.objects.clear_cache()
            logger.info("site found with domain: " + str(current_site.id))
            logger.info("site expiring date: " + str(current_site.customsite.expiring_date))

            # prelevo tutte le chiavi del dominio trovato
            WebsitePreferences_obj = WebsitePreferences()
            website_preferences_dict = WebsitePreferences_obj.get_preferences_about_site(site_domain=current_site)

            # se è una chiamata ajax non setto il valore di ROOT_URLCONF
            current_url = urlparse(request.build_absolute_uri())
            current_url_path = current_url.path
            logger.info("url path: " + str(current_url_path))

            # identifico il ROOT_URLCONF da utilizzare
            # http://stackoverflow.com/questions/18322262/how-to-setup-custom-middleware-in-django
            # settando request.urlconf, sovrascrivo il valore di ROOT_URLCONF
            # scritto in settings.py

            if (website_preferences_dict.get("root_urlconf") == "classic" or website_preferences_dict.get("root_urlconf") == "simple") and current_url_path != "/ajax/":
                # il sito ha un tema settato 'classic' o 'simple'
                # TODO: controllo se il sito è attivo e non scaduto oppure se è a pagamento
                # settare le preferenze in CustomSites (expiring_date e site_status)
                if not current_site.customsite.site_status and (not current_site.customsite.expiring_date or timezone.now().date() > current_site.customsite.expiring_date):
                    # sito scaduto e non a pagamento
                    pass
                else:
                    request.urlconf = str(website_preferences_dict.get("root_urlconf")) + ".urls"
            else:
                # ROOT_URLCONF di default, (sto visitando entpy.com oppure un
                # sito è scaduto e redirigo qui, oppure chiamata /ajax/)
                # request.urlconf = settings.ROOT_URLCONF (è settato di default)
                pass

        except ObjectDoesNotExist:
            logger.error("no site found with current domain: " + str(request.get_host()))

        return None
