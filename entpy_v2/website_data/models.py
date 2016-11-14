# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from django.contrib.sites.models import Site
from django.conf import settings
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

class ThemeKeys(models.Model):
    id_key = models.AutoField(primary_key=True)
    name = models.CharField(max_length=500)
    theme = models.ForeignKey(Themes)

    # On Python 3: def __str__(self):
    def __unicode__(self):
        return str(self.theme.name) + " " + str(self.name)

    def get_all_keys(self):
        """Function to retrieve all saved keys"""
        return list(ThemeKeys.objects.all())

    # TODO
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
        verbose_name = "WebsiteData"
        verbose_name_plural = "WebsiteData"

    # On Python 3: def __str__(self):
    def __unicode__(self):
        return str(self.site) + " -> " + str(self.key.name)

    # TODO
    def get_all_keys_about_site(self, site_domain):
        """Function to retrieve a dictionary with all keys about a site id"""
        return dict(WebsiteData.objects.filter(site__domain=site_domain).values_list('key','val'))
