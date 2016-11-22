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
        """Function to create default keys and themes"""
        keys_dict = self.get_keys_dictionary()

        for key, val in keys_dict.iteritems():
            # creo l'eventuale tema se non esiste
            Themes_obj, theme_created = Themes.objects.get_or_create(name=val.get("theme"))

            # creo l'eventuale chiave del tema
            if not ThemeKeys.objects.filter(name=key).exists():
                ThemeKeys_obj = ThemeKeys()
                ThemeKeys_obj.name = key
                ThemeKeys_obj.theme = Themes_obj
                ThemeKeys_obj.save()

        return True

    def get_keys_dictionary(self):
        """Function to return all theme keys with related default"""
        classic_theme = "classic"
        return {
            # classic theme
            'classic_index_title' : { 'theme' : classic_theme, 'default' : 'Titolo pagina home' },
            'classic_index_subtitle' : { 'theme' : classic_theme, 'default' : 'Sottotitolo pagina' },
            'classic_index_block1' : { 'theme' : classic_theme, 'default' : '<div><div class="col-md-4"><div class="feature-left"><div><h3>Titolo1</h3><p>Facilis ipsum reprehenderit nemo molestias. Aut cum mollitia reprehenderit.</p></div></div></div><div class="col-md-4"><div class="feature-left"><div><h3>Titolo2</h3><p>Facilis ipsum reprehenderit nemo molestias. Aut cum mollitia reprehenderit.</p></div></div></div><div class="col-md-4"><div class="feature-left"><div><h3>Titolo3</h3><p>Facilis ipsum reprehenderit nemo molestias. Aut cum mollitia reprehenderit.</p></div></div></div></div>' },
            'classic_index_block2' : { 'theme' : classic_theme, 'default' : '<div class="col-md-12 text-center heading-section"><h3>Titolo sezione1</h3><p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque ut lectus vestibulum, fringilla tellus in, lacinia ligula. Vivamus id odio maximus, semper justo suscipit, convallis diam.</p></div>' },
            'classic_index_block3' : { 'theme' : classic_theme, 'default' : '<div class="col-md-12 text-center animate-box"><p><img src="{% static "classic/images/macbook.png" %}" alt="Home page image" class="img-responsive"></p></div>' },
            'classic_index_block4' : { 'theme' : classic_theme, 'default' : '<div><div class="col-md-4"><div class="feature-text"><h3><span class="number">01.</span> Titolo1</h3><p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque ut lectus vestibulum, fringilla tellus in, lacinia ligula. Vivamus id odio maximus, semper justo suscipit, convallis diam.</p></div></div><div class="col-md-4"><div class="feature-text"><h3><span class="number">02.</span> Titolo2</h3><p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque ut lectus vestibulum, fringilla tellus in, lacinia ligula. Vivamus id odio maximus, semper justo suscipit, convallis diam.</p></div></div><div class="col-md-4"><div class="feature-text"><h3><span class="number">03.</span> Titolo3</h3><p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque ut lectus vestibulum, fringilla tellus in, lacinia ligula. Vivamus id odio maximus, semper justo suscipit, convallis diam.</p></div></div></div>' },
            'classic_index_block5' : { 'theme' : classic_theme, 'default' : '<div class="col-md-6 col-md-offset-3 text-center heading-section animate-box fadeInUp animated"><h3>[editami qui...]</h3><p>[editami qui...]</p></div>' },
            'classic_about_title' : { 'theme' : classic_theme, 'default' : 'Titolo pagina chi siamo' },
            'classic_about_subtitle' : { 'theme' : classic_theme, 'default' : 'Sottotitolo pagina' },
            'classic_about_block1' : { 'theme' : classic_theme, 'default' : '<div class="col-md-6 col-md-offset-3 text-center heading-section animate-box fadeInUp animated"><h3>[editami qui...]</h3><p>[editami qui...]</p></div>' },
            'classic_about_block2' : { 'theme' : classic_theme, 'default' : '<div class="col-md-12 animate-box"><figure><img src="{% static "classic/images/about-image.jpg" %}" alt="Chi Siamo" class="img-responsive"></figure></div>' },
            'classic_about_block3' : { 'theme' : classic_theme, 'default' : '<div class="col-md-8 col-md-offset-2 animate-box"><h3>Titolo paragrafo1</h3><p>Lorem ipsum dolor sit amet, consectetur adipisicing elit. Aut rerum perspiciatis, debitis pariatur atque vitae sed blanditiis nobis sint, reprehenderit quas, natus corrupti! Ipsum cum possimus corporis aut architecto! Delectus enim adipisci quidem possimus voluptates! Aut ut aliquid molestias laudantium.</p><p>Lorem ipsum dolor sit amet, consectetur adipisicing elit.</p></div>' },
            'classic_services_title' : { 'theme' : classic_theme, 'default' : 'Titolo pagina servizi' },
            'classic_services_subtitle' : { 'theme' : classic_theme, 'default' : 'Sottotitolo pagina' },
            'classic_services_block1' : { 'theme' : classic_theme, 'default' : '<div class="col-md-8 col-md-offset-2 text-center heading-section animate-box"><h3>Cosa facciamo</h3><p>Lorem ipsum dolor sit amet, consectetur adipisicing elit. Velit est facilis maiores, perspiciatis accusamus asperiores sint consequuntur debitis.</p></div>' },
            'classic_services_block2' : { 'theme' : classic_theme, 'default' : '<div class="col-md-4 col-sm-4"><div class="services animate-box"><h3>Titolo blocco1</h3><p>Lorem ipsum dolor sit amet, consectetur adipisicing elit. Velit est facilis maiores, perspiciatis accusamus asperiores sint consequuntur debitis.</p></div></div><div class="col-md-4 col-sm-4"><div class="services animate-box"><h3>Titolo blocco2</h3><p>Lorem ipsum dolor sit amet, consectetur adipisicing elit. Velit est facilis maiores, perspiciatis accusamus asperiores sint consequuntur debitis.</p></div></div><div class="col-md-4 col-sm-4"><div class="services animate-box"><h3>Titolo blocco3</h3><p>Lorem ipsum dolor sit amet, consectetur adipisicing elit. Velit est facilis maiores, perspiciatis accusamus asperiores sint consequuntur debitis.</p></div></div><div class="col-md-4 col-sm-4"><div class="services animate-box"><h3>Titolo blocco4</h3><p>Lorem ipsum dolor sit amet, consectetur adipisicing elit. Velit est facilis maiores, perspiciatis accusamus asperiores sint consequuntur debitis.</p></div></div><div class="col-md-4 col-sm-4"><div class="services animate-box"><h3>Titolo blocco5</h3><p>Lorem ipsum dolor sit amet, consectetur adipisicing elit. Velit est facilis maiores, perspiciatis accusamus asperiores sint consequuntur debitis.</p></div></div><div class="col-md-4 col-sm-4"><div class="services animate-box"><h3>Titolo blocco6</h3><p>Lorem ipsum dolor sit amet, consectetur adipisicing elit. Velit est facilis maiores, perspiciatis accusamus asperiores sint consequuntur debitis.</p></div></div>' },
            'classic_services_block3' : { 'theme' : classic_theme, 'default' : '<div class="col-md-12"><div class="col-md-3 service-bg service-1"></div><div class="col-md-8 col-md-push-1"><h2>Titolo paragrafo1</h2><p>Lorem ipsum dolor sit amet, consectetur adipisicing elit. Totam quae modi earum eligendi eaque quis laudantium aperiam sunt atque recusandae, fugiat veritatis repellendus incidunt nostrum voluptatibus. Eveniet ex magnam repellat sunt molestiae, quibusdam culpa dignissimos recusandae voluptatum necessitatibus provident commodi?</p><ul><li>Nome servizio1</li><li>Nome servizio2</li><li>Nome servizio3</li><li>Nome servizio4</li></ul></div></div><div class="col-md-12"><div class="col-md-3 col-md-push-8 service-bg service-2"></div><div class="col-md-7 col-md-pull-3"><h2>Titolo paragrafo2</h2><p>Lorem ipsum dolor sit amet, consectetur adipisicing elit. Totam quae modi earum eligendi eaque quis laudantium aperiam sunt atque recusandae, fugiat veritatis repellendus incidunt nostrum voluptatibus. Eveniet ex magnam repellat sunt molestiae, quibusdam culpa dignissimos recusandae voluptatum necessitatibus provident commodi?</p><ul><li>Nome servizio5</li><li>Nome servizio6</li><li>Nome servizio7</li><li>Nome servizio8</li></ul></div></div>' },
            'classic_contacts_title' : { 'theme' : classic_theme, 'default' : 'Titolo pagina contatti' },
            'classic_contacts_subtitle' : { 'theme' : classic_theme, 'default' : 'Sottotitolo pagina' },
            'classic_contacts_block1' : { 'theme' : classic_theme, 'default' : '<div class="col-md-12"><h3 class="section-title">Contatti</h3><p>Lorem ipsum dolor sit amet, consectetur adipisicing elit. Velit est facilis maiores, perspiciatis accusamus asperiores sint consequuntur debitis.</p><ul class="contact-info"><li><i class="icon-location-pin"></i>Indirizzo del negozio</li><li><i class="icon-phone2"></i>+39 123456789</li><li><i class="icon-mail"></i><a href="mailto:tuaemail@mail.com">tuaemail@mail.com</a></li><li><i class="icon-clock"></i>Lunedì-Venerdì 9.00-19.00</li></ul></div>' },
        }

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

    """
    def get_defaults_key_values(self):
        ""Function to retrieve all key defaults as dictionary""
        return {
            # valori di default tema "classico"
            'classic_index_title_default' : 'Titolo pagina home',
            'classic_index_subtitle_default' : 'Sottotitolo pagina',
            'classic_index_block1_default' : '<div><div class="col-md-4"><div class="feature-left"><div><h3>Titolo1</h3><p>Facilis ipsum reprehenderit nemo molestias. Aut cum mollitia reprehenderit.</p></div></div></div><div class="col-md-4"><div class="feature-left"><div><h3>Titolo2</h3><p>Facilis ipsum reprehenderit nemo molestias. Aut cum mollitia reprehenderit.</p></div></div></div><div class="col-md-4"><div class="feature-left"><div><h3>Titolo3</h3><p>Facilis ipsum reprehenderit nemo molestias. Aut cum mollitia reprehenderit.</p></div></div></div></div>',
            'classic_index_block2_default' : '<div class="col-md-12 text-center heading-section"><h3>Titolo sezione1</h3><p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque ut lectus vestibulum, fringilla tellus in, lacinia ligula. Vivamus id odio maximus, semper justo suscipit, convallis diam.</p></div>',
            'classic_index_block3_default' : '<div class="col-md-12 text-center animate-box"><p><img src="{% static "classic/images/macbook.png" %}" alt="Home page image" class="img-responsive"></p></div>',
            'classic_index_block4_default' : '<div><div class="col-md-4"><div class="feature-text"><h3><span class="number">01.</span> Titolo1</h3><p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque ut lectus vestibulum, fringilla tellus in, lacinia ligula. Vivamus id odio maximus, semper justo suscipit, convallis diam.</p></div></div><div class="col-md-4"><div class="feature-text"><h3><span class="number">02.</span> Titolo2</h3><p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque ut lectus vestibulum, fringilla tellus in, lacinia ligula. Vivamus id odio maximus, semper justo suscipit, convallis diam.</p></div></div><div class="col-md-4"><div class="feature-text"><h3><span class="number">03.</span> Titolo3</h3><p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque ut lectus vestibulum, fringilla tellus in, lacinia ligula. Vivamus id odio maximus, semper justo suscipit, convallis diam.</p></div></div></div>',
            'classic_index_block5_default' : '<div class="col-md-6 col-md-offset-3 text-center heading-section animate-box fadeInUp animated"><h3>[editami qui...]</h3><p>[editami qui...]</p></div>',
            'classic_about_title_default' : 'Titolo pagina chi siamo',
            'classic_about_subtitle_default' : 'Sottotitolo pagina',
            'classic_about_block1_default' : '<div class="col-md-6 col-md-offset-3 text-center heading-section animate-box fadeInUp animated"><h3>[editami qui...]</h3><p>[editami qui...]</p></div>',
            'classic_about_block2_default' : '<div class="col-md-12 animate-box"><figure><img src="{% static "classic/images/about-image.jpg" %}" alt="Chi Siamo" class="img-responsive"></figure></div>',
            'classic_about_block3_default' : '<div class="col-md-8 col-md-offset-2 animate-box"><h3>Titolo paragrafo1</h3><p>Lorem ipsum dolor sit amet, consectetur adipisicing elit. Aut rerum perspiciatis, debitis pariatur atque vitae sed blanditiis nobis sint, reprehenderit quas, natus corrupti! Ipsum cum possimus corporis aut architecto! Delectus enim adipisci quidem possimus voluptates! Aut ut aliquid molestias laudantium.</p><p>Lorem ipsum dolor sit amet, consectetur adipisicing elit.</p></div>',
            'classic_services_title_default' : 'Titolo pagina servizi',
            'classic_services_subtitle_default' : 'Sottotitolo pagina',
            'classic_services_block1_default' : '<div class="col-md-8 col-md-offset-2 text-center heading-section animate-box"><h3>Cosa facciamo</h3><p>Lorem ipsum dolor sit amet, consectetur adipisicing elit. Velit est facilis maiores, perspiciatis accusamus asperiores sint consequuntur debitis.</p></div>',
            'classic_services_block2_default' : '<div class="col-md-4 col-sm-4"><div class="services animate-box"><h3>Titolo blocco1</h3><p>Lorem ipsum dolor sit amet, consectetur adipisicing elit. Velit est facilis maiores, perspiciatis accusamus asperiores sint consequuntur debitis.</p></div></div><div class="col-md-4 col-sm-4"><div class="services animate-box"><h3>Titolo blocco2</h3><p>Lorem ipsum dolor sit amet, consectetur adipisicing elit. Velit est facilis maiores, perspiciatis accusamus asperiores sint consequuntur debitis.</p></div></div><div class="col-md-4 col-sm-4"><div class="services animate-box"><h3>Titolo blocco3</h3><p>Lorem ipsum dolor sit amet, consectetur adipisicing elit. Velit est facilis maiores, perspiciatis accusamus asperiores sint consequuntur debitis.</p></div></div><div class="col-md-4 col-sm-4"><div class="services animate-box"><h3>Titolo blocco4</h3><p>Lorem ipsum dolor sit amet, consectetur adipisicing elit. Velit est facilis maiores, perspiciatis accusamus asperiores sint consequuntur debitis.</p></div></div><div class="col-md-4 col-sm-4"><div class="services animate-box"><h3>Titolo blocco5</h3><p>Lorem ipsum dolor sit amet, consectetur adipisicing elit. Velit est facilis maiores, perspiciatis accusamus asperiores sint consequuntur debitis.</p></div></div><div class="col-md-4 col-sm-4"><div class="services animate-box"><h3>Titolo blocco6</h3><p>Lorem ipsum dolor sit amet, consectetur adipisicing elit. Velit est facilis maiores, perspiciatis accusamus asperiores sint consequuntur debitis.</p></div></div>',
            'classic_services_block3_default' : '<div class="col-md-12"><div class="col-md-3 service-bg service-1"></div><div class="col-md-8 col-md-push-1"><h2>Titolo paragrafo1</h2><p>Lorem ipsum dolor sit amet, consectetur adipisicing elit. Totam quae modi earum eligendi eaque quis laudantium aperiam sunt atque recusandae, fugiat veritatis repellendus incidunt nostrum voluptatibus. Eveniet ex magnam repellat sunt molestiae, quibusdam culpa dignissimos recusandae voluptatum necessitatibus provident commodi?</p><ul><li>Nome servizio1</li><li>Nome servizio2</li><li>Nome servizio3</li><li>Nome servizio4</li></ul></div></div><div class="col-md-12"><div class="col-md-3 col-md-push-8 service-bg service-2"></div><div class="col-md-7 col-md-pull-3"><h2>Titolo paragrafo2</h2><p>Lorem ipsum dolor sit amet, consectetur adipisicing elit. Totam quae modi earum eligendi eaque quis laudantium aperiam sunt atque recusandae, fugiat veritatis repellendus incidunt nostrum voluptatibus. Eveniet ex magnam repellat sunt molestiae, quibusdam culpa dignissimos recusandae voluptatum necessitatibus provident commodi?</p><ul><li>Nome servizio5</li><li>Nome servizio6</li><li>Nome servizio7</li><li>Nome servizio8</li></ul></div></div>',
            'classic_contacts_title_default' : 'Titolo pagina contatti',
            'classic_contacts_subtitle_default' : 'Sottotitolo pagina',
            'classic_contacts_block1_default' : '<div class="col-md-12"><h3 class="section-title">Contatti</h3><p>Lorem ipsum dolor sit amet, consectetur adipisicing elit. Velit est facilis maiores, perspiciatis accusamus asperiores sint consequuntur debitis.</p><ul class="contact-info"><li><i class="icon-location-pin"></i>Indirizzo del negozio</li><li><i class="icon-phone2"></i>+39 123456789</li><li><i class="icon-mail"></i><a href="mailto:tuaemail@mail.com">tuaemail@mail.com</a></li><li><i class="icon-clock"></i>Lunedì-Venerdì 9.00-19.00</li></ul></div>',
        }
    """

class WebsitePreferenceKeys(models.Model):
    id_website_preference_key = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = "Chiave preferenza sito"
        verbose_name_plural = "Chiavi preferenza sito"

    # On Python 3: def __str__(self):
    def __unicode__(self):
        return str(self.name)

    def get_keys_dictionary(self):
        """Function to return all preference keys with related default"""
        return {
            'root_urlconf' : { 'default': None },
            'contacts_maps_position' : { 'default': '45.0711813,7.6828501,17' },
            'twitter_page_url' : { 'default': 'http://www.entpy.com/tw' },
            'facebook_page_url' : { 'default': 'http://www.entpy.com/fb' },
            'site_name' : { 'default': 'Il Mio Sito' },
        }

    def create_default_keys(self):
        """Function to create default keys"""

        # elenco di chiavi con i relativi default (che in questo caso non mi servono)
        keys_list = self.get_keys_dictionary()

        for key in keys_list:
            # creo l'eventuale chiave
                if not WebsitePreferenceKeys.objects.filter(name=key).exists():
                    WebsitePreferenceKeys_obj = WebsitePreferenceKeys()
                    WebsitePreferenceKeys_obj.name = key
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

    """
    def get_defaults_key_values(self):
        ""Function to retrieve all key defaults as dictionary""
        return {
            # valori di default
            'root_urlconf' : None,
            'contacts_maps_position_default' : '45.0711813,7.6828501,17',
            'twitter_page_url_default' : 'tw_page_url',
            'facebook_page_url_default' : 'fb_page_url',
            'site_name_default' : 'Mio Sito',
        }
    """

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
