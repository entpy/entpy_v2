# -*- coding: utf-8 -*-

from django.contrib import admin
from website.models import Account, Promotion, Campaign
from website.forms import *
from django.contrib import admin, messages
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.template import RequestContext, loader
from django.conf.urls import url
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

class AccountAdmin(admin.ModelAdmin):
    # fileds in add/modify form
    fields = (('first_name', 'last_name'), 'email', 'mobile_phone', 'receive_promotions')

    # table list fields
    list_display = ('email', 'mobile_phone', 'first_name', 'last_name')

    # URLs overwriting to add new admin views (with auth check and without cache)
    def get_urls(self):
        urls = super(AccountAdmin, self).get_urls()
        my_urls = [
            url(r'^code-validator/$', self.admin_site.admin_view(self.code_validator)),
        ]

        # return custom URLs with default URLs
        return my_urls + urls

    def code_validator(self, request):
        """Function to validate a coupon code"""
        can_redeem = False
        promotion_details = {}

        if request.method == 'POST':
            form = ValidateCodeForm(request.POST)

            # cancel operation
            if request.POST.get("cancel", ""):
                messages.add_message(request, messages.WARNING, 'Operazione annullata.')
                return HttpResponseRedirect('/admin/website/account/code-validator') # Redirect after POST

            if form.is_valid():
                post_code = request.POST.get("promo_code")

                # retrieving promotion details
                campaign_obj = Campaign()

                # checking if code exists
                if (not campaign_obj.check_code_validity(code=post_code, validity_check="exists")):
                    messages.add_message(request, messages.ERROR, 'Codice promozionale non esistente.')
                    return HttpResponseRedirect('/admin/website/account/code-validator') # Redirect after POST

                # checking if code is not already validated
                if (not campaign_obj.check_code_validity(code=post_code, validity_check="not_used")):
                    messages.add_message(request, messages.ERROR, 'Codice promozionale già validato.')
                    return HttpResponseRedirect('/admin/website/account/code-validator') # Redirect after POST

                # checking if campaign is not expired
                if (not campaign_obj.check_code_validity(code=post_code, validity_check="not_expired")):
                    messages.add_message(request, messages.ERROR, 'Codice promozionale scaduto.')
                    return HttpResponseRedirect('/admin/website/account/code-validator') # Redirect after POST

                # user can redeem the code
                can_redeem = True

                # show promotion details
                promotion_details = campaign_obj.get_campaign_details(campaign_code=post_code)

                if request.POST.get("redeem_code", ""):
                    # redeem code and redirect to success page
                    campaign_obj.redeem_code(post_code)
                    messages.add_message(request, messages.SUCCESS, 'Codice promozionale validato!')
                    return HttpResponseRedirect('/admin/website/account/code-validator') # Redirect after POST
        else:
            form = ValidateCodeForm() # An unbound form

        context = {
            'form' : form,
            'redeem_code' : can_redeem,
            'promotion_details' : promotion_details,
            'title': "Validatore di codici",
            'opts': self.model._meta,
            'app_label': self.model._meta.app_label,
            'has_permission': request.user.is_superuser,
            'site_url': '/',
        }

        return render(request, 'admin/custom_view/code_validator.html', context)

class PromotionAdmin(admin.ModelAdmin):
    # fileds in add/modify form
    fields = ('name', 'description', 'promo_image', 'expiring_date')

    # table list fields
    list_display = ('name', 'expiring_date')

    # showing only valid promotion
    def queryset(self, request):
        qs = super(PromotionAdmin, self).queryset(request)
        return qs.filter(expiring_date__gte=datetime.now().date()).filter(promo_type=Promotion.PROMOTION_TYPE_FRONTEND["key"])

    def save_model(self, request, obj, form, change):
        """
        Overriding of "save_model" to generate a campaign code after
        promotion saving (only if not exists yet)
        """

        campaign_obj = Campaign()

        # setting promo type to frontend post
        obj.promo_type = Promotion.PROMOTION_TYPE_FRONTEND["key"]
        obj.save()
        id_promotion = obj.id_promotion

        # generating a campaign code, if not exist yet
        campaign_obj.add_frontend_post_campaign(id_promotion=id_promotion)

# Register your models here.
admin.site.register(Account, AccountAdmin)
admin.site.register(Promotion, PromotionAdmin)

admin.site.index_template = "admin/index_custom.html"
