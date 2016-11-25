# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models

# Create your models here.
class uploadedImages(models.Model):
    id_uploaded_image = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to="")
    # thumbnail_image = models.ForeignKey('self', null=True)

    def __unicode__(self):
        return self.image.name

