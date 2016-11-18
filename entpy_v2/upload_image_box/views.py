# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from django.conf import settings
from upload_image_box.settings import *
from upload_image_box.forms import *
from upload_image_box.models import tmpUploadedImages, cropUploadedImages
from upload_image_box.exceptions import *
import logging, json

# Get an instance of a logger
logger = logging.getLogger(__name__)

# View to upload an image
@require_POST
def upload(request):
    data = {'error': True}
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = tmpUploadImagesCropForm(request.POST, request.FILES)
        # check whether it's valid:
        try:
            form.is_valid()
        except CorruptedImageUIBError:
            data = {'error': True, "msg": "Immagine corrotta", "error_code": CorruptedImageUIBError.get_error_code}
            # data = {'error': True, "msg": "Corrupted file", "error_code": CorruptedImageUIBError.get_error_code}
            pass
        except ImageSizeUIBError:
	    data = {'error': True, "msg": "Dimensione del file troppo grossa (max = 4MB)", "error_code": ImageSizeUIBError.get_error_code}
            # data = {'error': True, "msg": "Please check your image size (max allowed = 4MB)", "error_code": ImageSizeUIBError.get_error_code}
            pass
        except ImageDimensionsUIBError:
            data = {'error': True, "msg": "Controlla altezza e larghezza dell'immagine (deve essere almeno di 250x250 px)", "error_code": ImageDimensionsUIBError.get_error_code}
            # data = {'error': True, "msg": "Please check your image dimensions (min allowed = 200x200)", "error_code": ImageDimensionsUIBError.get_error_code}
            pass
        except ImageExtensionUIBError:
            data = {'error': True, "msg": "Controlla l'estensione della dell'immagine (valide solo: '.png', '.jpg', and '.jpeg')", "error_code": ImageExtensionUIBError.get_error_code}
            # data = {'error': True, "msg": "Please check your image extension (only: '.png', '.jpg', and '.jpeg' are valid)", "error_code": ImageExtensionUIBError.get_error_code}
            pass
        else:
            # delete old temporary images
            tmpUploadedImages_obj = tmpUploadedImages()
            tmpUploadedImages_obj.delete_old_tmp_images()

            # upload tmp image
            image_form = form.save(commit=False)
            image_form.upload_to = UPLOADED_IMG_TMP_DIRECTORY
            image_form.save()
            # build JSON success response
            data = {'success': True, "file_id": image_form.id, "file_url": "http://" + str(request.get_host()) + str(settings.MEDIA_URL_TMP) + str(image_form.image)}
            # logger.debug("immagine salvata: " + str(settings.MEDIA_URL) + str(image_form.image))

    return HttpResponse(json.dumps(data), content_type="text/html")

# View to crop an uploaded image
@require_POST
def crop(request):
    data = {'error': True}
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
	try:
	    tmp_uploaded_image = tmpUploadedImages.objects.get(pk=request.POST.get("file_id")) # BAD: another image can be loaded
	except tmpUploadedImages.DoesNotExist:
            data = {'error': True, "msg": "L'immagine uploadata non esiste"}
	    pass
        else:
	    crop_uploaded_images_obj = cropUploadedImages()
            # retrieve crop info
	    crop_info = crop_uploaded_images_obj.retrieve_crop_info(request)
            # retrieve custom crop directory name (could be found in session if exists)
            custom_crop_directory_name = crop_uploaded_images_obj.get_custom_crop_directory(request)
            # crop uploaded image
            saved_image_obj = crop_uploaded_images_obj.save_image(tmp_uploaded_image, crop_info, custom_crop_directory_name)
            if saved_image_obj:
                data = {'success' : True, 'image_id': saved_image_obj.id}
            else:
		data = {'error': True, "msg": "Immagine troppo piccola (deve essere almeno di 250x250 px)", "error_code": ImageDimensionsUIBError.get_error_code}

    return HttpResponse(json.dumps(data), content_type="application/json")
