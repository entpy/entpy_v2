from django.contrib import admin
from upload_image_box.models import cropUploadedImages
from upload_image_box.models import tmpUploadedImages

admin.site.register(cropUploadedImages)
admin.site.register(tmpUploadedImages)
