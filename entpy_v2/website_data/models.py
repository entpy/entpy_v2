# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from django.conf import settings
import logging, sys

# force utf8 read data
reload(sys);
sys.setdefaultencoding("utf8")

# Get an instance of a logger
logger = logging.getLogger(__name__)

class WebsiteData(models.Model):
    id_website_data = models.AutoField(primary_key=True)
    key = models.CharField("Key", max_length=500)
    val = models.TextField("Val", null=True)
    site = models.ForeignKey(Site)

    class Meta:
        verbose_name = "WebsiteData"
        verbose_name_plural = "WebsiteData"

    # On Python 3: def __str__(self):
    def __unicode__(self):
        return str(self.email)
