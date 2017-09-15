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

        # XXX: all'aggiunta di nuovi temi definire qui le 'key' e i 'valori di default'
        # NB: se si aggiungono nuove chiavi qui è necessario inserirle anche
        # in db, con l'apposita funzione creata nell'admin ;)
        classic_theme = "classic"
        simple_theme = "simple"

        return {
            # classic theme
            'classic_site_title' : { 'theme' : classic_theme, 'default' : 'Il mio sito' },
            'classic_header_image1' : { 'theme' : classic_theme, 'default' : '<img src="/static/classic/images/cover_bg_1.jpg" alt="Image">' },
            'classic_header_image2' : { 'theme' : classic_theme, 'default' : '<img src="/static/classic/images/cover_bg_1.jpg" alt="Image">' },
            'classic_index_title' : { 'theme' : classic_theme, 'default' : 'Titolo pagina home' },
            'classic_index_subtitle' : { 'theme' : classic_theme, 'default' : 'Sottotitolo pagina' },
            'classic_index_block1' : { 'theme' : classic_theme, 'default' : '<div><div class="col-md-4"><div class="feature-left"><div><h3>Titolo1</h3><p>Facilis ipsum reprehenderit nemo molestias. Aut cum mollitia reprehenderit.</p></div></div></div><div class="col-md-4"><div class="feature-left"><div><h3>Titolo2</h3><p>Facilis ipsum reprehenderit nemo molestias. Aut cum mollitia reprehenderit.</p></div></div></div><div class="col-md-4"><div class="feature-left"><div><h3>Titolo3</h3><p>Facilis ipsum reprehenderit nemo molestias. Aut cum mollitia reprehenderit.</p></div></div></div></div>' },
            'classic_index_block2' : { 'theme' : classic_theme, 'default' : '<div class="col-md-12 text-center heading-section"><h3>Titolo sezione1</h3><p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque ut lectus vestibulum, fringilla tellus in, lacinia ligula. Vivamus id odio maximus, semper justo suscipit, convallis diam.</p></div>' },
            'classic_index_block3' : { 'theme' : classic_theme, 'default' : '<div class="col-md-12 text-center animate-box"><p><img src="/static/classic/images/macbook.png" alt="Home page image" class="img-responsive"></p></div>' },
            'classic_index_block4' : { 'theme' : classic_theme, 'default' : '<div><div class="col-md-4"><div class="feature-text"><h3><span class="number">01.</span> Titolo1</h3><p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque ut lectus vestibulum, fringilla tellus in, lacinia ligula. Vivamus id odio maximus, semper justo suscipit, convallis diam.</p></div></div><div class="col-md-4"><div class="feature-text"><h3><span class="number">02.</span> Titolo2</h3><p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque ut lectus vestibulum, fringilla tellus in, lacinia ligula. Vivamus id odio maximus, semper justo suscipit, convallis diam.</p></div></div><div class="col-md-4"><div class="feature-text"><h3><span class="number">03.</span> Titolo3</h3><p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque ut lectus vestibulum, fringilla tellus in, lacinia ligula. Vivamus id odio maximus, semper justo suscipit, convallis diam.</p></div></div></div>' },
            'classic_index_block5' : { 'theme' : classic_theme, 'default' : '<div class="col-md-6 col-md-offset-3 text-center heading-section animate-box fadeInUp animated"><h3>[editami qui...]</h3><p>[editami qui...]</p></div>' },
            'classic_about_title' : { 'theme' : classic_theme, 'default' : 'Titolo pagina chi siamo' },
            'classic_about_subtitle' : { 'theme' : classic_theme, 'default' : 'Sottotitolo pagina' },
            'classic_about_block1' : { 'theme' : classic_theme, 'default' : '<div class="col-md-6 col-md-offset-3 text-center heading-section animate-box fadeInUp animated"><h3>[editami qui...]</h3><p>[editami qui...]</p></div>' },
            'classic_about_block2' : { 'theme' : classic_theme, 'default' : '<div class="col-md-12 animate-box"><figure><img src="/static/classic/images/about-image.jpg" alt="Chi Siamo" class="img-responsive"></figure></div>' },
            'classic_about_block3' : { 'theme' : classic_theme, 'default' : '<div class="col-md-8 col-md-offset-2 animate-box"><h3>Titolo paragrafo1</h3><p>Lorem ipsum dolor sit amet, consectetur adipisicing elit. Aut rerum perspiciatis, debitis pariatur atque vitae sed blanditiis nobis sint, reprehenderit quas, natus corrupti! Ipsum cum possimus corporis aut architecto! Delectus enim adipisci quidem possimus voluptates! Aut ut aliquid molestias laudantium.</p><p>Lorem ipsum dolor sit amet, consectetur adipisicing elit.</p></div>' },
            'classic_services_title' : { 'theme' : classic_theme, 'default' : 'Titolo pagina servizi' },
            'classic_services_subtitle' : { 'theme' : classic_theme, 'default' : 'Sottotitolo pagina' },
            'classic_services_block1' : { 'theme' : classic_theme, 'default' : '<div class="col-md-8 col-md-offset-2 text-center heading-section animate-box"><h3>Cosa facciamo</h3><p>Lorem ipsum dolor sit amet, consectetur adipisicing elit. Velit est facilis maiores, perspiciatis accusamus asperiores sint consequuntur debitis.</p></div>' },
            'classic_services_block2' : { 'theme' : classic_theme, 'default' : '<div class="col-md-4 col-sm-4"><div class="services animate-box"><h3>Titolo blocco1</h3><p>Lorem ipsum dolor sit amet, consectetur adipisicing elit. Velit est facilis maiores, perspiciatis accusamus asperiores sint consequuntur debitis.</p></div></div><div class="col-md-4 col-sm-4"><div class="services animate-box"><h3>Titolo blocco2</h3><p>Lorem ipsum dolor sit amet, consectetur adipisicing elit. Velit est facilis maiores, perspiciatis accusamus asperiores sint consequuntur debitis.</p></div></div><div class="col-md-4 col-sm-4"><div class="services animate-box"><h3>Titolo blocco3</h3><p>Lorem ipsum dolor sit amet, consectetur adipisicing elit. Velit est facilis maiores, perspiciatis accusamus asperiores sint consequuntur debitis.</p></div></div><div class="col-md-4 col-sm-4"><div class="services animate-box"><h3>Titolo blocco4</h3><p>Lorem ipsum dolor sit amet, consectetur adipisicing elit. Velit est facilis maiores, perspiciatis accusamus asperiores sint consequuntur debitis.</p></div></div><div class="col-md-4 col-sm-4"><div class="services animate-box"><h3>Titolo blocco5</h3><p>Lorem ipsum dolor sit amet, consectetur adipisicing elit. Velit est facilis maiores, perspiciatis accusamus asperiores sint consequuntur debitis.</p></div></div><div class="col-md-4 col-sm-4"><div class="services animate-box"><h3>Titolo blocco6</h3><p>Lorem ipsum dolor sit amet, consectetur adipisicing elit. Velit est facilis maiores, perspiciatis accusamus asperiores sint consequuntur debitis.</p></div></div>' },
            'classic_services_block3' : { 'theme' : classic_theme, 'default' : '<div class="col-md-12"><div class="col-md-3 service-bg service-1"></div><div class="col-md-8 col-md-push-1"><h2>Titolo paragrafo1</h2><p>Lorem ipsum dolor sit amet, consectetur adipisicing elit. Totam quae modi earum eligendi eaque quis laudantium aperiam sunt atque recusandae, fugiat veritatis repellendus incidunt nostrum voluptatibus. Eveniet ex magnam repellat sunt molestiae, quibusdam culpa dignissimos recusandae voluptatum necessitatibus provident commodi?</p><ul><li>Nome servizio1</li><li>Nome servizio2</li><li>Nome servizio3</li><li>Nome servizio4</li></ul></div></div><div class="col-md-12"><div class="col-md-3 col-md-push-8 service-bg service-2"></div><div class="col-md-7 col-md-pull-3"><h2>Titolo paragrafo2</h2><p>Lorem ipsum dolor sit amet, consectetur adipisicing elit. Totam quae modi earum eligendi eaque quis laudantium aperiam sunt atque recusandae, fugiat veritatis repellendus incidunt nostrum voluptatibus. Eveniet ex magnam repellat sunt molestiae, quibusdam culpa dignissimos recusandae voluptatum necessitatibus provident commodi?</p><ul><li>Nome servizio5</li><li>Nome servizio6</li><li>Nome servizio7</li><li>Nome servizio8</li></ul></div></div>' },
            'classic_contacts_title' : { 'theme' : classic_theme, 'default' : 'Titolo pagina contatti' },
            'classic_contacts_subtitle' : { 'theme' : classic_theme, 'default' : 'Sottotitolo pagina' },
            'classic_contacts_block1' : { 'theme' : classic_theme, 'default' : '<div class="col-md-12"><h3 class="section-title">Contatti</h3><p>Lorem ipsum dolor sit amet, consectetur adipisicing elit. Velit est facilis maiores, perspiciatis accusamus asperiores sint consequuntur debitis.</p><ul class="contact-info"><li><i class="icon-location-pin"></i>Indirizzo del negozio</li><li><i class="icon-phone2"></i>+39 123456789</li><li><i class="icon-mail"></i><a href="mailto:tuaemail@mail.com">tuaemail@mail.com</a></li><li><i class="icon-clock"></i>Lunedì-Venerdì 9.00-19.00</li></ul></div>' },
            # simple theme
            'simple_site_title' : { 'theme' : simple_theme, 'default' : 'Moderno' },
            'simple_header_image1' : { 'theme' : simple_theme, 'default' : '<img src="/static/simple/img/full-slide1.jpg" alt="img">' },
            'simple_header_image2' : { 'theme' : simple_theme, 'default' : '<img src="/static/simple/img/full-slide1.jpg" alt="img">' },
            'simple_header_image3' : { 'theme' : simple_theme, 'default' : '<img src="/static/simple/img/full-slide1.jpg" alt="img">' },
            'simple_header_block1' : { 'theme' : simple_theme, 'default' : '<h2>Titolo principale 1</h2><p>Descrizione del titolo principale 1</p><a href="#about" class="slider_btn">Scopri di più</a>' },
            'simple_header_block2' : { 'theme' : simple_theme, 'default' : '<h2>Titolo principale 2</h2><p>Descrizione del titolo principale 2</p><a href="#about" class="slider_btn">Scopri di più</a>' },
            'simple_header_block3' : { 'theme' : simple_theme, 'default' : '<h2>Titolo principale 3</h2><p>Descrizione del titolo principale 3</p><a href="#about" class="slider_btn">Scopri di più</a>' },
            'simple_about_heading' : { 'theme' : simple_theme, 'default' : '<h2 class="wow fadeInLeftBig">Chi Siamo</h2><p>In una terra lontana, dietro le montagne Parole, lontani dalle terre di Vocalia e Consonantia, vivono i testi casuali. Vivono isolati nella cittadina di Lettere, sulle coste del Semantico, un immenso oceano linguistico. Un piccolo ruscello chiamato Devoto Oli attraversa quei luoghi, rifornendoli di tutte le regolalie di cui hanno bisogno.</p>' },
            'simple_about_block1' : { 'theme' : simple_theme, 'default' : '<div class="col-lg-6 col-md-6 col-sm-12"><div class="about_featured"><div class="panel-group" id="accordion1"><!-- START SINGLE FEATURED ITEAM #1--><div class="panel panel-default wow fadeInLeft"><div class="panel-heading"><h4 class="panel-title"><a data-toggle="collapse" data-parent="#accordion1" href="#collapse1"><span class="fa fa-check-square-o"></span>Titolo blocco 1</a></h4></div><div id="collapse1" class="panel-collapse collapse in"><div class="panel-body">In una terra lontana, dietro le montagne Parole, lontani dalle terre di Vocalia e Consonantia, vivono i testi casuali. Vivono isolati nella cittadina di Lettere, sulle coste del Semantico, un immenso oceano linguistico. Un piccolo ruscello chiamato Devoto Oli attraversa quei luoghi, rifornendoli di tutte le regolalie di cui hanno bisogno.</div></div></div><!-- START SINGLE FEATURED ITEAM #2 --><div class="panel panel-default wow fadeInLeft"><div class="panel-heading"><h4 class="panel-title"><a data-toggle="collapse" data-parent="#accordion1" href="#collapse2"><span class="fa fa-check-square-o"></span>Titolo blocco 2</a></h4></div><div id="collapse2" class="panel-collapse collapse"><div class="panel-body"> In una terra lontana, dietro le montagne Parole, lontani dalle terre di Vocalia e Consonantia, vivono i testi casuali. Vivono isolati nella cittadina di Lettere, sulle coste del Semantico, un immenso oceano linguistico. Un piccolo ruscello chiamato Devoto Oli attraversa quei luoghi, rifornendoli di tutte le regolalie di cui hanno bisogno.  </div></div></div><!-- START SINGLE FEATURED ITEAM #3 --><div class="panel panel-default wow fadeInLeft"><div class="panel-heading"><h4 class="panel-title"><a data-toggle="collapse" data-parent="#accordion1" href="#collapse3"><span class="fa fa-check-square-o"></span>Titolo blocco 3 </a></h4></div><div id="collapse3" class="panel-collapse collapse"><div class="panel-body"> In una terra lontana, dietro le montagne Parole, lontani dalle terre di Vocalia e Consonantia, vivono i testi casuali. Vivono isolati nella cittadina di Lettere, sulle coste del Semantico, un immenso oceano linguistico. Un piccolo ruscello chiamato Devoto Oli attraversa quei luoghi, rifornendoli di tutte le regolalie di cui hanno bisogno.  </div></div></div></div></div></div><div class="col-lg-6 col-md-6 col-sm-12"><div class="about_slider"><!-- BEGAIN FEATURED SLIDER --><div class="featured_slider"><!-- SINGLE SLIDE IN THE SLIDER --><div class="single_iteam"><img src="/static/simple/img/feature_img1.jpg" alt="img"></div></div><!-- END FEATURED SLIDER --></div></div>' },
            'simple_about_block2' : { 'theme' : simple_theme, 'default' : '<div class="col-lg-6 col-md-6 col-sm-12"><div class="about_slider"><!-- BEGAIN FEATURED SLIDER --><div class="featured_slider"><!-- SINGLE SLIDE IN THE SLIDER --><div class="single_iteam"><img src="/static/simple/img/feature_img1.jpg" alt="img"></div></div><!-- END FEATURED SLIDER --></div></div><div class="col-lg-6 col-md-6 col-sm-12"><div class="about_featured"><div class="panel-group" id="accordion2"><!-- START SINGLE FEATURED ITEAM #1--><div class="panel panel-default wow fadeInLeft"><div class="panel-heading"><h4 class="panel-title"><a data-toggle="collapse" data-parent="#accordion2" href="#collapse4"><span class="fa fa-check-square-o"></span>Titolo blocco 4 </a></h4></div><div id="collapse4" class="panel-collapse collapse in"><div class="panel-body"> In una terra lontana, dietro le montagne Parole, lontani dalle terre di Vocalia e Consonantia, vivono i testi casuali. Vivono isolati nella cittadina di Lettere, sulle coste del Semantico, un immenso oceano linguistico. Un piccolo ruscello chiamato Devoto Oli attraversa quei luoghi, rifornendoli di tutte le regolalie di cui hanno bisogno.  </div></div></div><!-- START SINGLE FEATURED ITEAM #2 --><div class="panel panel-default wow fadeInLeft"><div class="panel-heading"><h4 class="panel-title"><a data-toggle="collapse" data-parent="#accordion2" href="#collapse5"><span class="fa fa-check-square-o"></span>Titolo blocco 5 </a></h4></div><div id="collapse5" class="panel-collapse collapse"><div class="panel-body"> In una terra lontana, dietro le montagne Parole, lontani dalle terre di Vocalia e Consonantia, vivono i testi casuali. Vivono isolati nella cittadina di Lettere, sulle coste del Semantico, un immenso oceano linguistico. Un piccolo ruscello chiamato Devoto Oli attraversa quei luoghi, rifornendoli di tutte le regolalie di cui hanno bisogno.  </div></div></div><!-- START SINGLE FEATURED ITEAM #3 --><div class="panel panel-default wow fadeInLeft"><div class="panel-heading"><h4 class="panel-title"><a data-toggle="collapse" data-parent="#accordion2" href="#collapse6"><span class="fa fa-check-square-o"></span>Titolo blocco 6 </a></h4></div><div id="collapse6" class="panel-collapse collapse"><div class="panel-body"> In una terra lontana, dietro le montagne Parole, lontani dalle terre di Vocalia e Consonantia, vivono i testi casuali. Vivono isolati nella cittadina di Lettere, sulle coste del Semantico, un immenso oceano linguistico. Un piccolo ruscello chiamato Devoto Oli attraversa quei luoghi, rifornendoli di tutte le regolalie di cui hanno bisogno.  </div></div></div></div></div></div>' },
            'simple_services_heading' : { 'theme' : simple_theme, 'default' : '<h2 class="wow fadeInLeftBig">I Nostri Servizi</h2><p>In una terra lontana, dietro le montagne Parole, lontani dalle terre di Vocalia e Consonantia, vivono i testi casuali. Vivono isolati nella cittadina di Lettere, sulle coste del Semantico, un immenso oceano linguistico. Un piccolo ruscello chiamato Devoto Oli attraversa quei luoghi, rifornendoli di tutte le regolalie di cui hanno bisogno.</p>' },
            'simple_services_block1' : { 'theme' : simple_theme, 'default' : '<div class="col-lg-12 col-md-12"><!-- BEGAIN SERVICE  --><div class="service_area"><div class="row"><div class="col-lg-6 col-md-6 col-sm-6"><!-- BEGAIN SINGLE SERVICE --><div class="single_service wow fadeInLeft"><div class="service_iconarea"><span class="fa fa-line-chart service_icon"></span></div><h3 class="service_title">Titolo servizio1</h3><p>In una terra lontana, dietro le montagne Parole, lontani dalle terre di Vocalia e Consonantia, vivono i testi casuali. Vivono isolati nella cittadina di Lettere, sulle coste del Semantico, un immenso oceano linguistico.</p></div></div><div class="col-lg-6 col-md-6 col-sm-6"><!-- BEGAIN SINGLE SERVICE --><div class="single_service wow fadeInRight"><div class="service_iconarea"><span class="fa fa-suitcase service_icon"></span></div><h3 class="service_title">Titolo servizio2</h3><p>In una terra lontana, dietro le montagne Parole, lontani dalle terre di Vocalia e Consonantia, vivono i testi casuali. Vivono isolati nella cittadina di Lettere, sulle coste del Semantico, un immenso oceano linguistico.</p></div></div><div class="col-lg-6 col-md-6 col-sm-6"><!-- BEGAIN SINGLE SERVICE --><div class="single_service wow fadeInLeft"><div class="service_iconarea"><span class="fa fa-eraser service_icon"></span></div><h3 class="service_title">Titolo servizio3</h3><p>In una terra lontana, dietro le montagne Parole, lontani dalle terre di Vocalia e Consonantia, vivono i testi casuali. Vivono isolati nella cittadina di Lettere, sulle coste del Semantico, un immenso oceano linguistico.</p></div></div><div class="col-lg-6 col-md-6 col-sm-6"><!-- BEGAIN SINGLE SERVICE --><div class="single_service wow fadeInRight"><div class="service_iconarea"><span class="fa fa-paper-plane service_icon"></span></div><h3 class="service_title">Titolo servizio4</h3><p>In una terra lontana, dietro le montagne Parole, lontani dalle terre di Vocalia e Consonantia, vivono i testi casuali. Vivono isolati nella cittadina di Lettere, sulle coste del Semantico, un immenso oceano linguistico.</p></div></div><div class="col-lg-6 col-md-6 col-sm-6"><!-- BEGAIN SINGLE SERVICE --><div class="single_service wow fadeInLeft"><div class="service_iconarea"><span class="fa fa-envelope-o service_icon"></span></div><h3 class="service_title">Titolo servizio5</h3><p>In una terra lontana, dietro le montagne Parole, lontani dalle terre di Vocalia e Consonantia, vivono i testi casuali. Vivono isolati nella cittadina di Lettere, sulle coste del Semantico, un immenso oceano linguistico.</p></div></div><div class="col-lg-6 col-md-6 col-sm-6"><!-- BEGAIN SINGLE SERVICE --><div class="single_service wow fadeInRight"><div class="service_iconarea"><span class="fa fa-support service_icon"></span></div><h3 class="service_title">Titolo servizio6</h3><p>In una terra lontana, dietro le montagne Parole, lontani dalle terre di Vocalia e Consonantia</p></div></div></div></div></div>' },
            'simple_contacts_heading' : { 'theme' : simple_theme, 'default' : '<h2 class="wow fadeInLeftBig">Contattaci</h2><p>In una terra lontana, dietro le montagne Parole, lontani dalle terre di Vocalia e Consonantia, vivono i testi casuali. Vivono isolati nella cittadina di Lettere, sulle coste del Semantico, un immenso oceano linguistico. Un piccolo ruscello chiamato Devoto Oli attraversa quei luoghi, rifornendoli di tutte le regolalie di cui hanno bisogno.</p>' },
            'simple_contacts_block1' : { 'theme' : simple_theme, 'default' : '<div class="col-lg-12 col-md-12"><div class="container"><div class="contact_feature"><!-- BEGAIN CALL US FEATURE --><div class="col-lg-3 col-md-3 col-sm-6"><div class="single_contact_feaured wow fadeInUp"><i class="fa fa-phone"></i><h4>Telefono</h4><p>+39 12345678</p></div></div><!-- BEGAIN CALL US FEATURE --><div class="col-lg-3 col-md-3 col-sm-6"><div class="single_contact_feaured wow fadeInUp"><i class="fa fa-envelope-o"></i><h4>Email</h4><p>tuaemail@mail.com</p></div></div><!-- BEGAIN CALL US FEATURE --><div class="col-lg-3 col-md-3 col-sm-6"><div class="single_contact_feaured wow fadeInUp"><i class="fa fa-map-marker"></i><h4>Indirizzo</h4><p>Indirizzo del negozio</p></div></div><!-- BEGAIN CALL US FEATURE --><div class="col-lg-3 col-md-3 col-sm-6"><div class="single_contact_feaured wow fadeInUp"><i class="fa fa-clock-o"></i><h4>Orari</h4><p>Lunedì-Venerdì 9.00-19.00</p></div></div></div></div></div>' },
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
        # XXX: queste preferenze sono indipendenti dal tema e viaggiano su un
        # dizionario parallelo, sono comuni a tutti i temi, quella
        # fondamentale è 'root_urlconf', che definisce il tema da usare, senza
        # questa preferenza settata per il dominio, viene visualizzato
        # entpy.com
        # NB: se si aggiungono nuove chiavi qui è necessario inserirle anche
        # in db, con l'apposita funzione creata nell'admin ;)
        return {
            'root_urlconf' : { 'default': None }, # il nome del tema, es "classic", "simple", ecc...
            'contacts_maps_position' : { 'default': '45.0711813,7.6828501,17' },
            'twitter_page_url' : { 'default': 'http://www.entpy.com/tw' },
            'facebook_page_url' : { 'default': 'http://www.entpy.com/fb' },
            'google_plus_page_url' : { 'default': 'http://www.entpy.com/g+' },
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
    # site = models.OneToOneField(Site, related_name='site_preferences')
    site = models.ForeignKey(Site, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Preferenza sito"
        verbose_name_plural = "Preferenze sito"

    # On Python 3: def __str__(self):
    def __unicode__(self):
        return str(self.site.domain) + " -> key: " + str(self.key)+ " | val: " + str(self.val)

    def get_preferences_about_site(self, site_domain):
        """Function to retrieve all preferences about a site"""
        return dict(WebsitePreferences.objects.filter(site__domain=site_domain).values_list('key__name','val'))

# classe per estendere il Framweork Site di Django
class CustomSite(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True)
    expiring_date = models.DateTimeField()
    site_status =  models.IntegerField(default=0) # 0 in prova (DEFAULT), 1 a pagamento
    site = models.OneToOneField(Site, related_name='customsite', on_delete=models.CASCADE)

    # On Python 3: def __str__(self):
    def __unicode__(self):
        return 'Customsite of ' + str(self.site.name)

    # TODO
    # all'inserimento in questa tabella:
    # - se site_status non settato o nullo => mettere 'expiring_date' adesso + 1 anno (sito gratis che scade tra 1 anno)
    # - se site_status = 1 => mettere 'expiring_date' a NULL (sito a pagamento senza scadenza)
