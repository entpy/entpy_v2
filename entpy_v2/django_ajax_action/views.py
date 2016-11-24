from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_POST, require_GET
from django_ajax_action.ajax_manager import ajaxManager
import logging, json

# Get an instance of a logger
logger = logging.getLogger(__name__)

@require_POST
def ajax_action(request):
    """ View to perform an action as function via javascript aka AJAX call"""

    # load and perform action
    ajaxManager_obj = ajaxManager(request=request)
    ajaxManager_obj.perform_ajax_action()
    json_response = ajaxManager_obj.get_json_response()

    # create http response (also attach a cookie if exists)
    http_response = HttpResponse(json_response, content_type="application/json")
    http_response = ajaxManager_obj.attach_cookie_to_response(response=http_response)

    # return a JSON response
    return http_response
