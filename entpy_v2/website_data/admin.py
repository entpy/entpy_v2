from django.contrib import admin, messages
from django.conf.urls import url
from django.shortcuts import render
from django.contrib.sites.models import Site
from django.http import HttpResponseRedirect, HttpResponse
from website_data.models import *
from website_data.forms import *
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

class WebsiteDataAdmin(admin.ModelAdmin):

    # URLs overwriting to add new admin views (with auth check and without cache)
    def get_urls(self):
        urls = super(WebsiteDataAdmin, self).get_urls()
        my_urls = [
            # url(r'^edit-site/(?:(?P<site_id>\d+)/)$', self.admin_site.admin_view(self.edit_site)),
            url(r'^create-defaults/$', self.admin_site.admin_view(self.create_defaults)),
        ]

        # return custom URLs with default URLs
        return my_urls + urls

    """
    def edit_site(self, request, site_id):
        ""Function to select a site to edit""

        WebsiteData_obj = WebsiteData()
        Site_obj = Site.objects.get(pk=site_id)

        if request.method == 'POST':
            form = EditTextSiteForm(request.POST)

            if form.is_valid():
                # TODO: salvo i valori delle relative chiavi
                WebsiteData_obj.set_all_keys_about_site(site_id=site_id, post=request.POST)

                # pagina di successo con i dati aggiornati precompilati
                messages.add_message(request, messages.SUCCESS, 'Dati salvati con successo.')
                return HttpResponseRedirect('/admin/website_data/websitedata/edit-site/' + str(site_id)) # Redirect after POST
        else:
            form = EditTextSiteForm() # An unbound form
            # precompilo la post con eventuali valori presenti
            request.POST = WebsiteData_obj.get_all_keys_about_site(site_domain=Site_obj.domain)
            # logger.info("chiavi salvate in db per il sito " + str(site_id) + ": " + str(request.POST))

        context = {
            'form' : form,
            'post': request.POST,
            'title': "Modifica informazioni sito: " + str(Site_obj.domain),
            'opts': self.model._meta,
            'app_label': self.model._meta.app_label,
            'has_permission': request.user.is_superuser,
            'site_url': '/',
        }

        return render(request, 'admin/custom_view/edit_site.html', context)
    """

    def create_defaults(self, request):
        """Function to create default keys and themes"""
        ThemeKeys_obj = ThemeKeys()
        ThemeKeys_obj.create_default_keys()

        WebsitePreferenceKeys_obj = WebsitePreferenceKeys()
        WebsitePreferenceKeys_obj.create_default_keys()

        context = {
            'title': "Creazione chiavi e temi di default",
            'opts': self.model._meta,
            'app_label': self.model._meta.app_label,
            'has_permission': request.user.is_superuser,
            'site_url': '/',
        }

        messages.add_message(request, messages.SUCCESS, 'Valori di default creati con successo.')

        return render(request, 'admin/custom_view/create_defaults.html', context)

    def get_model_perms(self, request):
        """
        https://stackoverflow.com/questions/2431727/django-admin-hide-a-model

        Return empty perms dict thus hiding the model from admin index.
        Per far funzionare le custom view dell'app website_data ma nascondendo
        tutti i modelli, in questo modo gli url funzionano ma nell'admin non si
        vede nessun modello da modificare/aggiungere.
        """
        return {}

class CustomSiteInstanceInline(admin.StackedInline):
    model = CustomSites

class WebsitePreferencesInstanceInline(admin.TabularInline):
    model = WebsitePreferences

# Define a new Site admin
class SiteAdmin(admin.ModelAdmin):
    list_filter = ('domain', 'name')
    inlines = [CustomSiteInstanceInline, WebsitePreferencesInstanceInline]

# TODO: pagine aggiuntive per l'admin (da usare solo per debug o manutenzione)
"""
admin.site.register(Themes)
admin.site.register(ThemeKeys)
admin.site.register(WebsitePreferences)
admin.site.register(WebsitePreferenceKeys)
admin.site.register(CustomSites)
"""

admin.site.unregister(Site)
admin.site.register(Site, SiteAdmin)
admin.site.register(WebsiteData, WebsiteDataAdmin)
