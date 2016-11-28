# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.contrib.sites.models import Site
from django.db import models

# custom file upload dir
def custom_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'site_{0}/{1}'.format(instance.site.id, filename)

# Create your models here.
class uploadedImages(models.Model):
    id_uploaded_image = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to=custom_path)
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    # thumbnail_image = models.ForeignKey('self', null=True)

    def __unicode__(self):
        return self.image.name

