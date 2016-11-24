# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.conf import settings
from django.utils import formats
from django.contrib.auth.models import User
from website_data.models import *
import logging, json

# Get an instance of a logger
logger = logging.getLogger(__name__)

class ajaxManager():

    __json_response = None
    __valid_action_list = ()
    cookie_key = ""
    cookie_value = ""
    cookie_expiring = ""

    def __init__(self, request=None):
        # list of valid methods
        self.__valid_action_list += ('save_site_block',)
        self.__valid_action_list += ('upload_image',)

        # retrieve action to perform
        self.ajax_action = request.POST.get("ajax_action")
        # ajax request (POST data)
        self.request = request

    def check_if_action_is_valid(self):
        """Function to check if an ajax action is valid"""

        return self.ajax_action in self.__valid_action_list

    def check_if_is_post(self):
        """Function to check if a request is performed via POST"""
        return_var = False
        if self.request.method == 'POST':
            return_var = True

        return return_var

    def attach_cookie_to_response(self, response):
        """Function to attach a cookie to response"""
        return_var = None
        if response and self.cookie_key:
            # cookie with expiring in time from next votation
            response.set_cookie(key=self.cookie_key, value=self.cookie_value, max_age=self.cookie_expiring)
            return_var = response

        return response

    def perform_ajax_action(self):
        """Function to perform ajax action"""
        # check if request method is POST
        if self.check_if_is_post():
            # check if ajax action is valid
            if self.check_if_action_is_valid():
                # ajax action is valid
                logger.debug("ajax_action: " + str(self.ajax_action))
                code = compile("self." + self.ajax_action + "()", '<string>', 'exec')
                exec(code)
            else:
                # return a JSON error response
                self.set_json_response(json_response=json.dumps('{ "error": True, "msg": :"Invalid action"}'))
                logger.error("ATTENZIONE: ajax action non valida (" + str(self.ajax_action) + ")")
        else:
            # return a JSON error response
            self.set_json_response(json_response=json.dumps('{ "error": True, "msg": :"Please call this page via POST method"}'))
            logger.error("ATTENZIONE: ajax action chiamata senza metodo POST (" + str(self.ajax_action) + ")")

        return True

    def get_json_response(self):
        """Function to retrieve json response"""

        return self.__json_response

    def set_json_response(self, json_response=None):
        """Function to set json response"""
        if json_response:
            self.__json_response = json_response

        return True

    """
    +----------------------+
    |                      |
    |     AZIONI AJAX      |
    |                      |
    +----------------------+
    """

    def save_site_block(self):
        """Function to save a site block"""
        logger.debug("ajax_function: @@save_site_block@@")
        logger.debug("parametri della chiamata: " + str(self.request.POST))
        msg = ""
        success_flag = False
        block_key = self.request.POST.get("block_key")
        block_val = self.request.POST.get("block_val")


        if self.request.user.is_superuser:
            WebsiteData_obj = WebsiteData()

            # current site id
            current_site = get_current_site(self.request)

            # salvo tutti i valori delle chiavi nel relativo sito
            WebsiteData_obj.set_all_keys_about_site(site_id=current_site.id, post=self.request.POST)
            success_flag = True
        else:
            msg = "Attenzione: la chiamata non è avvenuta dall'amministratore"

        if success_flag:
            data = {'success' : True}
        else:
            data = {'error' : True, 'msg' : msg}

        # build JSON response
        json_data_string = json.dumps(data)
        self.set_json_response(json_response=json_data_string)

        return True

    # TODO:
    # permettere l'upload solo se si è amministratori
    def upload_image(self):
        import base64
        """Function to upload an image with html editor"""
        logger.debug("ajax_function: @@upload_image@@")
        logger.debug("parametri della chiamata: " + str(self.request.POST))
        msg = ""
        success_flag = False
        image_data = self.request.FILES["image_data"]

        with open('/tmp/name.jpg', 'wb+') as destination:
            for chunk in image_data.chunks():
                destination.write(chunk)

        """
        if self.request.user.is_superuser:
            WebsiteData_obj = WebsiteData()

            # current site id
            current_site = get_current_site(self.request)

            # salvo tutti i valori delle chiavi nel relativo sito
            WebsiteData_obj.set_all_keys_about_site(site_id=current_site.id, post=self.request.POST)
            success_flag = True
        else:
            msg = "Attenzione: la chiamata non è avvenuta dall'amministratore"
        """

        if success_flag:
            data = {'success' : True}
        else:
            data = {'error' : True, 'msg' : msg}

        # build JSON response
        json_data_string = json.dumps(data)
        self.set_json_response(json_response=json_data_string)

        return True
