# -*- coding: utf-8 -*-

# contest processor to manage common vars
from django.conf import settings
from entpy_v2.consts import project_constants
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

def common_contest_processors(request):
    """Common template context processor function"""

    return {
            'project_constants': project_constants,
    }
