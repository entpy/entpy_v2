# -*- coding: utf-8 -*-

"""
Simple E/R scheme
=================

        1-N         1-N
Account -> Campaign <- Promotion
"""

from __future__ import unicode_literals
from django.db import models
from django.core.mail import EmailMessage
from django.conf import settings
from django.utils import timezone
from django.utils.html import format_html, mark_safe
from entpy_v2.CustomImagePIL import CustomImagePIL
import datetime, string, random, logging, sys
from datetime import datetime

# TODO: delete also model image with post_delete signal
# more info here: https://docs.djangoproject.com/en/1.6/topics/signals/

# force utf8 read data
reload(sys);
sys.setdefaultencoding("utf8")

# Get an instance of a logger
logger = logging.getLogger(__name__)

class Account(models.Model):
    id_account = models.AutoField(primary_key=True)
    first_name = models.CharField("Nome", max_length=30)
    last_name = models.CharField("Cognome", max_length=30)
    email = models.EmailField()
    mobile_phone = models.CharField("Numero telefonico", max_length=20, blank=True, null=True)
    receive_promotions = models.BooleanField("Riceve le promozioni", default=0)
    status = models.BooleanField(default=1)

    class Meta:
        verbose_name = "Utente"
        verbose_name_plural = "Utenti"

    # On Python 3: def __str__(self):
    def __unicode__(self):
        return str(self.email)

class Promotion(models.Model):
    PROMOTION_TYPE_FRONTEND = { "key" : "frontend_bonus", "description" : "Pubblica sul frontend" }
    PROMOTION_TYPE_SERVICE = { "key" : "service_bonus", "description" : "Sconto su un servizio" }
    PROMOTION_TYPE_WIZARD = { "key" : "wizard_bonus", "description" : "Sconto su un obiettivo" }

    # promotion type selector for admin
    PROMOTION_TYPES_SELECTOR = (
        (PROMOTION_TYPE_FRONTEND["key"], PROMOTION_TYPE_FRONTEND["description"]),
        (PROMOTION_TYPE_SERVICE["key"], PROMOTION_TYPE_SERVICE["description"]),
        (PROMOTION_TYPE_WIZARD["key"], PROMOTION_TYPE_WIZARD["description"]),
    )

    id_promotion = models.AutoField(primary_key=True)
    name = models.CharField("Titolo promozione", max_length=50)
    description = models.TextField("Contenuto")
    promo_image = models.ImageField("Immagine della promozione", upload_to="promo_images/", blank=True, null=True)
    expiring_date = models.DateField("Scadenza", null=True)
    promo_type = models.CharField(max_length=30, choices=PROMOTION_TYPES_SELECTOR)
    status = models.BooleanField(default=0)
    campaigns = models.ManyToManyField(Account, through='Campaign')
    creation_date = models.DateTimeField(auto_now_add=True)

    # custom model options
    class Meta:
        verbose_name = "Promozione"
        verbose_name_plural = "Promozioni"

    # On Python 3: def __str__(self):
    def __unicode__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        """Overriding save method to handle uploaded image"""

        # saving model
        super(Promotion, self).save(*args, **kwargs) # Call the "real" save() method.

        # resize image
        if self.promo_image:
            img_file_name = str(self.promo_image.path)
            custom_image_PIL_obj = CustomImagePIL(file_path=img_file_name)
            custom_image_PIL_obj.resize_image(filename=self.promo_image.path)

    def get_valid_promotions_list(self, promo_type = PROMOTION_TYPE_FRONTEND["key"]):
        """Return a list of valid promotions (not expired yet)"""

        valid_promotion_list = []
        campaign_obj = Campaign()

        # list of all promotion valid (queryset starts from campaign object)
        filtered_promotions = Campaign.objects.filter(
            id_promotion__promo_type=promo_type).filter(
            id_promotion__expiring_date__gte=datetime.now().date()
        )

        # for every campaign retrieving promo details
        if filtered_promotions:
            for valid_promo in filtered_promotions:
                # retrieving valid campaign id
                id_valid_campaign = valid_promo.id_campaign
                # build dictionary with promotion details
                valid_promotion_list.append(campaign_obj.get_campaign_details(id_campaign=id_valid_campaign))

        return valid_promotion_list

    def create_promotion(self, name, description, promo_type, expiring_date=None):
        """Function to create a new promotion"""
        return_var = False
        promotion_obj = Promotion()

        promotion_obj.name = name
        promotion_obj.description = description
        promotion_obj.promo_type = promo_type
        if expiring_date:
            promotion_obj.expiring_date = expiring_date

        promotion_obj.save()

        # prelevo l'id della promo appena inserita
        return_var = promotion_obj.id_promotion

        return return_var

class Campaign(models.Model):
    id_campaign = models.AutoField(primary_key=True)
    id_account = models.ForeignKey(Account, db_column="id_account", null=True)
    id_promotion = models.ForeignKey(Promotion, db_column="id_promotion")
    code = models.CharField(max_length=10)
    status = models.BooleanField(default=0)

    # On Python 3: def __str__(self):
    def __unicode__(self):
        return str(self.id_campaign)

    def generate_random_code(self, depth = 0):
        """
        Generating a random promo code, if the generated code already
        exists, than recursively call this function to generate a new ones.
        Max recursion depth: 50
        """

        # generating a random code
        random_code = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))

        try:
            # checking if code already exists
            Campaign.objects.get(code=random_code)

            # than recall this function to generate a new ones
            if depth < 50:
                random_code = Campaign.generate_random_code(self, depth+1)
            else:
                logger.error("ATTENZIONE: non sono riuscito a generare un nuovo codice | depth level: " + str(depth))
                random_code = "PROMOCODE1"
        except (KeyError, Campaign.DoesNotExist):
            # Yo!
            pass

        return random_code

    def add_frontend_post_campaign(self, id_promotion):
        """Function to add a campaign for frontend_post campaign"""
        campaign_obj = Campaign()
        return_var = False

        if id_promotion:
            if not Campaign.objects.filter(id_promotion__id_promotion=id_promotion).exists():
                # if a campaign code does not exists yet, then creating a new ones
                campaign_obj = Campaign(
                    id_promotion = Promotion(id_promotion=id_promotion),
                    code = campaign_obj.generate_random_code()
                )
                campaign_obj.save()
                return_var = campaign_obj.id_campaign

        return return_var

    def add_campaign_user(self, id_account, id_promotion):
            """
            Function to add a row from db, starting from "id_account" and "id_promotion"
            Return true on success
            """
            create_campaign = False

            if not Campaign.objects.filter(id_account=id_account, id_promotion=id_promotion).exists():
                # creo la campagna e genero un codice random
                create_campaign = True

            if create_campaign:
                campaign_obj = Campaign(
                    id_account = Account(id_account=id_account),
                    id_promotion = Promotion(id_promotion=id_promotion),
                    code = self.generate_random_code()
                )
                campaign_obj.save()

            return True

    def get_campaign_details(self, id_campaign=None, campaign_code=None):
        """
        Function to retrieve all details about a campaign.
        First by id_campaign, if id_campaign is null campaign_code will
        be used.
        Return a dictionary like this:
            campaign_details = {
                'title' : 'promo title',
                'content' : 'promo content'
                ...
            }
        """

        campaign_details = {}
        campaign_obj = None

        try:
                if (id_campaign):
                    campaign_obj = Campaign.objects.select_related().get(id_campaign=id_campaign)
                elif (campaign_code):
                    campaign_obj = Campaign.objects.select_related().get(code=campaign_code)

                if (campaign_obj):
                    promotion_obj = campaign_obj.id_promotion
                    account_obj = campaign_obj.id_account

                    campaign_details["name"] = promotion_obj.name
                    campaign_details["description"] = promotion_obj.description
                    campaign_details["expiring_in"] = promotion_obj.expiring_date

                    # retrieving custom expiring in string (frontend or backend)
                    expiring_in_days = campaign_obj.get_expiring_in_days(campaign_details["expiring_in"])
                    campaign_details["expiring_in_readable_frontend"] = campaign_obj.get_expiring_in_text(expiring_in_days)
                    campaign_details["expiring_in_readable_backend"] = campaign_obj.get_expiring_in_text(expiring_in_days, True)

                    if promotion_obj.promo_image:
                        campaign_details["image_relative_path"] = promotion_obj.promo_image.url
                    campaign_details["code"] = campaign_obj.code
                    # a frontend_post promotion has not recipients
                    if (account_obj):
                        campaign_details["receiver_email"] = account_obj.email
                        campaign_details["receiver_first_name"] = account_obj.first_name
                        campaign_details["receiver_last_name"] = account_obj.last_name
        except(KeyError, Campaign.DoesNotExist):
            # id_campaign doesn't exists
            pass

        return campaign_details

    def get_expiring_in_text(self, expiring_in_days=None, is_frontend=False):
            """Function to build a string about promotion expiring in"""

            expiring_in_string = ""

            if (is_frontend):
                if (expiring_in_days == 0):
                    expiring_in_string = "<br /><b>Approfittane subito, l'offerta scade OGGI!</b>"
                if (expiring_in_days == 1):
                    expiring_in_string = "<br /><b>Approfittane subito, l'offerta scade domani!</b>"
                elif (expiring_in_days > 1):
                    expiring_in_string = "<br /><b>Approfittane subito, l'offerta scade tra " + str(expiring_in_days) + " giorni</b>"
            else:
                if (expiring_in_days == 0):
                    expiring_in_string = "L'offerta scade <span class=\"expiring_today\">OGGI</span>!"
                if (expiring_in_days == 1):
                    expiring_in_string = "L'offerta scade domani!"
                elif (expiring_in_days > 1):
                    expiring_in_string = "L'offerta scade tra " + str(expiring_in_days) + " giorni"

            return expiring_in_string

    def check_code_validity(self, code, validity_check=None):
            """
            Function to check if a code is not used yet or if the
            promotion isn't expired
            Validity checks available:
                - not_used
                - not_expired
                - exists
            """

            return_var = False

            try:
                campaign_obj = Campaign.objects.select_related().get(code=code)
                promotion_obj = campaign_obj.id_promotion

                if (validity_check == 'not_used'):
                    if ((not campaign_obj.status) or (promotion_obj.promo_type == Promotion.PROMOTION_TYPE_FRONTEND["key"])):
                        return_var = True

                if (validity_check == 'not_expired'):
                    if ((promotion_obj.expiring_date is None) or (promotion_obj.expiring_date >= datetime.now().date())):
                        return_var = True

                if (validity_check == 'exists'):
                    if (campaign_obj.id_campaign):
                        return_var = True

            except(KeyError, Campaign.DoesNotExist):
                # code not exists
                pass

            return return_var

    def redeem_code(self, code):
        """Function to redeem a coupon code"""

        return_var = False

        try:
            # setting code status = 1 (code used)
            campaign_obj = Campaign.objects.get(code=code)
            campaign_obj.status = 1
            campaign_obj.save()
            return_var = True
            logger.info("codice " + str(code) + " validato con successo")

        except(KeyError, Campaign.DoesNotExist):
            # code not exists
            pass

        return return_var

    def get_expiring_in_days(self, expiring_date=None):
        """Function to calculate expiring in between two date"""

        return_var = None

        if (expiring_date):
            return_var = (expiring_date - datetime.now().date()).days

        return return_var
