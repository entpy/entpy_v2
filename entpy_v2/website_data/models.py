# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from django.contrib.sites.models import Site
from django.conf import settings
from upload_image_box.models import cropUploadedImages 
import logging, sys

# force utf8 read data
reload(sys);
sys.setdefaultencoding("utf8")

# Get an instance of a logger
logger = logging.getLogger(__name__)

class Themes(models.Model):
    id_theme = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)

    # On Python 3: def __str__(self):
    def __unicode__(self):
        return str(self.name)

    class Meta:
        verbose_name = "Tema"
        verbose_name_plural = "Temi"

    def get_all_list(self):
        """Function to retrieve all themes"""
        return list(Themes.objects.all())

class ThemeKeys(models.Model):
    id_key = models.AutoField(primary_key=True)
    name = models.CharField(max_length=500)
    theme = models.ForeignKey(Themes)

    # On Python 3: def __str__(self):
    def __unicode__(self):
        return str(self.theme.name) + " " + str(self.name)

    class Meta:
        verbose_name = "Chiave del tema"
        verbose_name_plural = "Chiavi dei temi"

    def get_all_keys(self):
        """Function to retrieve all keys"""
        return list(ThemeKeys.objects.all())

    def get_obj_by_name(self, key_name):
        return_var = False

        try:
            return_var = ThemeKeys.objects.get(name=key_name)
        except ThemeKeys.DoesNotExist:
            pass

        return return_var

    def create_default_keys(self):
        """Function to create default keys"""
        keys_list = self.get_defaults_keys()

        for theme_name in keys_list:
            # creo l'eventuale tema se non esiste
            Themes_obj, theme_created = Themes.objects.get_or_create(name=theme_name)

            # creo l'eventuale chiave del tema
            for theme_key in keys_list[theme_name]:
                if not ThemeKeys.objects.filter(name=theme_key).exists():
                    ThemeKeys_obj = ThemeKeys()
                    ThemeKeys_obj.name = theme_key
                    ThemeKeys_obj.theme = Themes_obj
                    ThemeKeys_obj.save()

        return True

    def get_defaults_keys(self):
        """Function to retrieve all keys list"""
        keys_list = {
            # classic theme
            "classic" : [
                'classic_index_title',
                'classic_index_subtitle',
                'classic_index_first_content',
                'classic_index_section_one_title',
                'classic_index_section_one_content',
                'classic_index_second_content',
                'classic_index_section_two_title',
                'classic_index_section_two_content',
                'classic_about_title',
                'classic_about_subtitle',
                'classic_about_section_one_title',
                'classic_about_section_one_content',
                'classic_about_section_two_title',
                'classic_about_section_two_content_one',
                'classic_about_section_two_content_two',
                'classic_services_title',
                'classic_services_subtitle',
                'classic_services_section_one_title',
                'classic_services_section_one_content',
                'classic_services_blocks',
                'classic_services_first_service_title',
                'classic_services_first_service_content',
                'classic_services_first_service_list',
                'classic_services_second_service_title',
                'classic_services_second_service_content',
                'classic_services_second_service_list',
                'classic_contacts_title',
                'classic_contacts_subtitle',
                'classic_contacts_section_one_title',
                'classic_contacts_section_one_content',
                'classic_contacts_address1',
                'classic_contacts_phone1',
                'classic_contacts_email1',
                'classic_contacts_timetables1',
                'classic_contacts_section_one_maps_position',
                'classic_base_twitter_page_url',
                'classic_base_facebook_page_url',
                'classic_base_site_name',
            ],
            # simple theme
            "simple" : []
        }

        return keys_list

class WebsiteData(models.Model):
    id_website_data = models.AutoField(primary_key=True)
    key = models.ForeignKey(ThemeKeys)
    val = models.TextField(null=True)
    site = models.ForeignKey(Site, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Valore chiave"
        verbose_name_plural = "Valori chiavi"

    # On Python 3: def __str__(self):
    def __unicode__(self):
        return str(self.site) + " -> " + str(self.key.name)

    def get_all_keys_about_site(self, site_domain):
        """Function to retrieve a dictionary with all keys about a site id"""
        return dict(WebsiteData.objects.filter(site__domain=site_domain).values_list('key__name','val'))

    # TODO
    def set_all_keys_about_site(self, site_id, post):
        """Function to set all keys about a site starting from a POST dictionary"""
        ThemeKeys_obj = ThemeKeys()

        Site_obj = Site.objects.get(pk=site_id)
        # logger.info("valori da salvare per il sito '" + str(site_id) + "': " + str(post))

        if post:
            for key, val in post.iteritems():
                ThemeKeys_saved_obj = ThemeKeys_obj.get_obj_by_name(key_name=key)
                if ThemeKeys_saved_obj:
                    logger.info("chiave: " + str(key))
                    logger.info("valore: " + str(val))
                    logger.info("===")
                    try: 
                        # modifico l'oggetto già presente
                        WebsiteData_obj = WebsiteData.objects.get(key=ThemeKeys_saved_obj, site=Site_obj)
                    except WebsiteData.DoesNotExist:
                        # creo l'oggetto
                        WebsiteData_obj = WebsiteData()
                        pass
                    WebsiteData_obj.key = ThemeKeys_saved_obj
                    WebsiteData_obj.val = val
                    WebsiteData_obj.site = Site_obj
                    WebsiteData_obj.save()

        return True

class WebsitePreferenceKeys(models.Model):
    id_website_preference_key = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = "Chiave preferenza sito"
        verbose_name_plural = "Chiavi preferenza sito"

    # On Python 3: def __str__(self):
    def __unicode__(self):
        return str(self.name)

    def create_default_keys(self):
        """Function to create default keys"""
        keys_list = ['root_urlconf',]

        for key_name in keys_list:
            # creo l'eventuale chiave
                if not WebsitePreferenceKeys.objects.filter(name=key_name).exists():
                    WebsitePreferenceKeys_obj = WebsitePreferenceKeys()
                    WebsitePreferenceKeys_obj.name = key_name
                    WebsitePreferenceKeys_obj.save()

        return True

class WebsitePreferences(models.Model):
    id_website_preference = models.AutoField(primary_key=True)
    key = models.ForeignKey(WebsitePreferenceKeys)
    val = models.CharField(max_length=200)
    site = models.OneToOneField(Site, related_name='site_preferences')

    class Meta:
        verbose_name = "Preferenza sito"
        verbose_name_plural = "Preferenze sito"

    # On Python 3: def __str__(self):
    def __unicode__(self):
        return str(self.site.domain) + " -> key: " + str(self.key)+ " | val: " + str(self.val)

    def get_preferences_about_site(self, site_domain):
        """Function to retrieve all preferences about a site"""
        return dict(WebsitePreferences.objects.filter(site__domain=site_domain).values_list('key__name','val'))

class SiteImages(models.Model):
    image_id = models.OneToOneField(cropUploadedImages, primary_key=True)
    site = models.ForeignKey(Site)
    image_code = models.CharField(max_length=100)
    upload_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Immagine sito"
        verbose_name_plural = "Immagini sito"

    def __unicode__(self):
        return self.image_id.image.url
