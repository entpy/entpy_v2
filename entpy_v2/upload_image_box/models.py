# -*- coding: utf-8 -*-

from django.db import models
from django.conf import settings
from datetime import timedelta
from django.utils import timezone
from upload_image_box.exceptions import *
from .settings import *
from PIL import Image
from PIL.ExifTags import TAGS
import os, logging, shutil, uuid, cStringIO

# Get an instance of a logger
logger = logging.getLogger(__name__)

def get_image_path(self, filename):
    return os.path.join(self.upload_to_base_path, self.upload_to, filename)

class cropUploadedImages(models.Model):
    image = models.ImageField(max_length=500, upload_to=get_image_path)
    thumbnail_image = models.ForeignKey('self', null=True)
    upload_to_base_path = APP_BASE_DIRECTORY # default file upload base dir
    upload_to = '' # default file upload custom dir

    def __unicode__(self):
        return self.image.name

    def delete(self, *args, **kwargs):
        # delete thumbnail image first
        if self.thumbnail_image:
            self.thumbnail_image.delete()
        # You have to prepare what you need before delete the model
        storage, path = self.image.storage, self.image.path
        # Delete the model before the file
        super(cropUploadedImages, self).delete(*args, **kwargs)
        # Delete the file after the model
        storage.delete(path)
        logger.info("cropUploadedImages DELETE -> storage: " + str(storage) + " | path: " + str(path))

    def retrieve_crop_info(self, request):
        """Function to retrieve info about javascript crop plugin"""
        crop_info = {}

	if request:
            crop_info["file_id"] = request.POST.get("file_id") # BAD
            crop_info["height"] = int(float(request.POST.get("height", 0)))
            crop_info["width"] = int(float(request.POST.get("width", 0)))
            crop_info["x"] = int(float(request.POST.get("x", 0)))
            crop_info["y"] = int(float(request.POST.get("y", 0)))
            crop_info["rotate"] = int(float(request.POST.get("rotate", 0)))
            crop_info["enable_crop"] = request.POST.get("enable_crop")

	    logger.debug("=== crop info START ===")
	    logger.debug("file_id: " + str(crop_info["file_id"]))
	    logger.debug("height: " + str(crop_info["height"]))
	    logger.debug("width: " + str(crop_info["width"]))
	    logger.debug("x: " + str(crop_info["x"]))
	    logger.debug("y: " + str(crop_info["y"]))
	    logger.debug("rotate" + str(crop_info["rotate"]))
	    logger.debug("=== crop info END ===")

	return crop_info

    def get_crop_box(self, crop_info):
	"""Function to retrieve a crop box"""
	return_var = False
	if crop_info:
	    return_var = (crop_info["x"], crop_info["y"], crop_info["x"]+crop_info["width"], crop_info["y"]+crop_info["height"])

        return return_var

    def save_image(self, tmp_uploaded_image_obj, crop_info, custom_crop_directory_name=None):
        """Function to (crop and) save uploaded image"""
	valid_image_row_saved = None
        if tmp_uploaded_image_obj:
	    if USE_BOTO:
		# retrieve boto images save path directory name
		images_save_path = self.build_boto_crop_directory(custom_crop_directory_name)
	    else:
		# retrieve images save path directory name
		images_save_path = self.build_crop_image_directory(custom_crop_directory_name)
		# create images save path directory name
		self.create_cropped_image_directory(images_save_path)

            # retrieve a valid image with or without crop
            valid_image = self.create_valid_image(tmp_uploaded_image_obj=tmp_uploaded_image_obj, crop_info=crop_info)
            if FORCE_JPEG:
                # convert image to jpeg
                valid_image = self.convert_image_to_jpeg(image=valid_image, image_name=tmp_uploaded_image_obj.image.path)
            # get dimensions about image
            cropped_width, cropped_height = valid_image.size
            if cropped_width >= CROPPED_IMG_MIN_WIDTH and cropped_height >= CROPPED_IMG_MIN_HEIGHT:
                # create thumbnail from valid image
                cropped_image_thumbnail = self.create_image_thumbnail(image=valid_image)
                # todo create cropped (or not) image name
                valid_image_name = self.get_image_name(tmp_uploaded_image_obj.image.path)
                # todo create thumbnail image name append "_thumb" postfix to valid_image_name
                thumbnail_image_name = self.get_image_thumbnail_name(valid_image_name)

		"""
                logger.debug("valid image name: " + str(valid_image_name))
                logger.debug("valid image: " + str(valid_image))
                logger.debug("thumbnail image name: " + str(thumbnail_image_name))
                logger.debug("thumbnail image: " + str(cropped_image_thumbnail))
		"""

		# save valid cropped (or not) image and thumbnail image into
                # cloud or filesystem
		if USE_BOTO:
		    valid_image_saved = self.write_image_into_cloud(image_obj=valid_image, image_path=images_save_path + valid_image_name, image_name=valid_image_name)
		    thumbnail_image_saved = self.write_image_into_cloud(image_obj=cropped_image_thumbnail, image_path=images_save_path + thumbnail_image_name, image_name=thumbnail_image_name)
		    # save valid cropped (or not) image and thumbnail image into database
		    thumbnail_row_saved = self.write_image_into_db(image_path=images_save_path + thumbnail_image_name, thumbnail_image=None)
		    valid_image_row_saved = self.write_image_into_db(image_path=images_save_path + valid_image_name, thumbnail_image=thumbnail_row_saved)
		else:
		    valid_image_saved = self.write_image_into_fs(image_obj=valid_image, save_full_path=images_save_path + valid_image_name)
		    thumbnail_image_saved = self.write_image_into_fs(image_obj=cropped_image_thumbnail, save_full_path=images_save_path + thumbnail_image_name)
		    # save valid cropped (or not) image and thumbnail image into database
		    thumbnail_row_saved = self.write_image_into_db(image_path=APP_BASE_DIRECTORY + CROPPED_IMG_DIRECTORY + custom_crop_directory_name + "/" + thumbnail_image_name, thumbnail_image=None)
		    valid_image_row_saved = self.write_image_into_db(image_path=APP_BASE_DIRECTORY + CROPPED_IMG_DIRECTORY + custom_crop_directory_name + "/" + valid_image_name, thumbnail_image=thumbnail_row_saved)

        return valid_image_row_saved

    def write_image_into_cloud(self, image_obj, image_path, image_name):
        """
        Function to write an object (image) into cloud storage
        (Es. Amazon S3 or Aruba Object Cloud Storage)
        """
	import boto3
        if image_obj and image_path and image_name:
	    # create s3 connection
	    s3 = boto3.resource(
                's3',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_REGION_NAME,
            )
	    # set bucket
	    s3_bucket = s3.Bucket(self.get_bucket_name())
            # retrieve image type
            image_type = self.get_image_type(image_name=image_name)
            # upload object (image) to S3 => http://boto3.readthedocs.org/en/latest/reference/services/s3.html?highlight=metadata#S3.Client.put_object
            s3_bucket.put_object(
                Key=image_path, # to build the "folder" structure like "office/3/123456789.jpg"
                Body=self.prepare_image_to_cloud(image=image_obj, image_name=image_name),
                ACL = 'public-read',
                ContentType=image_type["mimetype"],
            )

        return image_obj

    def check_if_bucket_exists(self, s3_resource, bucket_name):
        """
        Function to check if a bucket exists on S3
        https://boto3.readthedocs.org/en/latest/guide/migrations3.html 'Accessing a Bucket'
        Non utilizzata perchè rallenta troppo la chiamata
        """
        import botocore
        return_var = True
        try:
            s3_resource.meta.client.head_bucket(Bucket=bucket_name)
        except botocore.exceptions.ClientError as e:
            # If a client error is thrown, then check that it was a 404 error.
            # If it was a 404 error, then the bucket does not exist.
            error_code = int(e.response['Error']['Code'])
            if error_code == 404:
                logger.error("ATTENZIONE: il bucket '" + str(bucket_name) + "' NON esiste su S3.")
                return_var = False

        return return_var

    def convert_image_to_jpeg(self, image, image_name):
        """Function to convert an image to jpeg"""
	file_name, file_extension = os.path.splitext(image_name)

	# logger.info("(convert_image_to_jpeg) image ext: " + str(file_extension))
	if (file_extension == ".jpg") or (file_extension == ".jpeg"):
	    bg = Image.new("RGB", image.size)
	    bg.paste(image)
	else:
	    if image.mode == 'RGBA':
	        bg = Image.new("RGBA", image.size, (255,255,255,255))
	        bg.paste(image, (0,0), image)
	    else:
	        bg = Image.new("RGB", image.size)
	        bg.paste(image)

        return bg

    def prepare_image_to_cloud(self, image, image_name):
        """
        Function to retrieve output image
        http://stackoverflow.com/questions/6685500/upload-resized-image-to-s3
        """
        return_var = False
        if image and image_name:
            image_type = self.get_image_type(image_name=image_name)
            #NOTE, we're saving the image into a cStringIO object to avoid writing to disk
            out_im = cStringIO.StringIO()
            #You MUST specify the file type because there is no file name to discern it from
            image.save(out_im, image_type["format"])
            #Note we're setting contents from the in-memory string provided by cStringIO
            return_var = out_im.getvalue()

        return return_var

    def write_image_into_fs(self, image_obj, save_full_path):
        """Function to write an image obj to fs"""
        if image_obj and save_full_path:
            image_obj.save(save_full_path)
            logger.debug("image: " + str(image_obj) + " saved on fs (" + str(save_full_path) + ")")

        return image_obj

    def create_image_thumbnail(self, image):
        """Function to create an image thumbnail"""
        thumb = None
        if image:
            thumb = image.copy()
            size = [CROPPED_IMG_MIN_WIDTH,CROPPED_IMG_MIN_HEIGHT]
            thumb.thumbnail(size, Image.ANTIALIAS)
            # logger.debug("thumbnail image: " + str(image))

        return thumb

    def create_valid_image(self, tmp_uploaded_image_obj, crop_info=False):
        """Function to retrieve a valid image with or without crop"""
        # open tmp uploaded image
        image = Image.open(tmp_uploaded_image_obj.image.path)

        # check if image must be cropped or not
        if crop_info["enable_crop"]:
            cropped_image = image.crop(self.get_crop_box(crop_info))
        else:
            cropped_image = image

        return cropped_image

    def create_cropped_image_directory(self, directory):
        """Function to create crop image directory if not exists"""
        if not os.path.exists(directory):
            os.makedirs(directory)

    def get_image_name(self, full_image_path):
	"""Function to retrieve image name about a full image path, ie. '/tmp/image/file1.png' -> must return 'file1.png' """
	head, tail = os.path.split(full_image_path)
	file_name, file_extension = os.path.splitext(full_image_path)
        if FORCE_JPEG:
            # force jpeg
            file_extension = '.jpg'
	# file name collision low risk (if file exists generate a new name)
	new_file_name = str(uuid.uuid4()) + file_extension

        # if os.path.isfile(fname)
        # TODO: controllo se il file esiste:
        #       - se esiste lancio ancora la stessa funzione in modo ricorsivo

	return new_file_name

    def get_image_thumbnail_name(self, valid_image_name):
	"""Function to retrieve thumbnail image name about a full image path, ie. '/tmp/image/file1.png' -> must return 'file1.png' """
	file_name, file_extension = os.path.splitext(valid_image_name)
        if FORCE_JPEG:
            # force jpeg
            file_extension = '.jpg'
	# file name collision low risk (if file exists generate a new name)
	new_file_name = str(file_name) + "_thumb" + str(file_extension)

	return new_file_name

    def get_image_type(self, image_name):
	"""Function to retrieve image type and file extension"""
	return_var = False
        # http://www.sitepoint.com/web-foundations/mime-types-complete-list/
        mimetypes = {
                '.jpg': { 'format': 'JPEG', 'mimetype': 'image/jpeg', },
                '.jpeg': { 'format': 'JPEG', 'mimetype': 'image/jpeg', },
                '.png': { 'format': 'PNG', 'mimetype': 'image/png', },
        }
	if image_name:
            if FORCE_JPEG:
                return_var = mimetypes.get('.jpeg')
            else:
                file_name, file_extension = os.path.splitext(image_name)
                return_var = mimetypes.get(file_extension)

	return return_var

    def build_crop_image_directory(self, custom_crop_directory_name=None):
	"""Function to build crop image directory"""
	crop_image_directory = settings.MEDIA_ROOT + "/" + APP_BASE_DIRECTORY + CROPPED_IMG_DIRECTORY + custom_crop_directory_name + "/"
        logger.debug("crop_image_directory: " + str(crop_image_directory))

	return crop_image_directory

    def build_boto_crop_directory(self, custom_crop_directory_name=None):
        """Function to retrieve boto directory path"""
        return_var = False
        if settings.BOTO_APP_DIR:
	    # custom boto directory
	    return_var = settings.BOTO_APP_DIR + custom_crop_directory_name + "/"
	elif BOTO_APP_DIR:
	    # default boto directory
	    return_var = BOTO_APP_DIR + custom_crop_directory_name + "/"

        return return_var

    def get_bucket_name(self):
        """Function to retrieve boto bucket name"""
        return_var = False
        if settings.BOTO_BUCKET:
	    # custom boto directory
	    return_var = settings.BOTO_BUCKET
	elif BOTO_BUCKET:
	    # default boto directory
	    return_var = BOTO_BUCKET

        return return_var

    def get_custom_crop_directory(self, request):
        """Function to retrieve crop directory name"""
        return_var = ""
        if request.session.get('CUSTOM_CROPPED_IMG_DIRECTORY'):
            return_var = str(request.session.get('CUSTOM_CROPPED_IMG_DIRECTORY'))

        return return_var

    def write_image_into_db(self, image_path, thumbnail_image=None):
	"""Function to save image into database"""
	return_var = False
        crop_uploaded_images_obj = cropUploadedImages()
        crop_uploaded_images_obj.image = image_path
        # saving thumbnail image if exists
        if thumbnail_image:
            crop_uploaded_images_obj.thumbnail_image = thumbnail_image
	crop_uploaded_images_obj.save()
	return_var = crop_uploaded_images_obj

	return return_var

    def get_image_obj_from_id(self, book_image_id):
        """Function to retrieve and image obj from an image id"""
	logger.debug("id immagine: " + str(book_image_id))
	return_var = None
	try:
	    image_obj = cropUploadedImages.objects.get(pk=book_image_id)
	except cropUploadedImages.DoesNotExist:
	    # image not found
	    pass
        else:
            return_var = image_obj

        return return_var


class tmpUploadedImages(models.Model):
    image = models.ImageField(max_length=500, upload_to=get_image_path)
    upload_date = models.DateTimeField(auto_now=True)

    # upload file attributes
    upload_to_base_path = APP_BASE_DIRECTORY # default file upload base dir
    upload_to = '' # default file upload custom dir

    def __unicode__(self):
        return self.image.name

    def save(self, *args, **kwargs):
	# Did we have rotated the image?
	# We pop it to remove from kwargs when we pass these along
	# image_rotated = kwargs.pop('image_rotated',False)

	super(tmpUploadedImages, self).save(*args, **kwargs)

	if self.image and ENABLE_AUTO_ROTATING_IF_REQUIRED:
	    # filename = self.get_source_filename()
	    image = Image.open(self.image)

	    try:
		exifdict = image._getexif()
	    except:
		logger.info("errore con _getexif, probabilmente l'immagine non è jpg")
		pass
	    else:
		if exifdict is not None and len(exifdict):
		    orientation_key = 274 # cf ExifTags
		    if orientation_key in exifdict:
			orientation = exifdict[orientation_key]
			logger.info("tmp image orientation: " + str(orientation))

			rotate_values = {
			    3: 180,
			    6: 270,
			    8: 90
			}

			if orientation in rotate_values:
			    # Rotate and save the picture
			    logger.info("ruoto l'immagine di " + str(rotate_values[orientation]) + "°")
			    rotated_image_obj = image.rotate(rotate_values[orientation])
			    # Save rotated image
			    rotated_image_obj.save(self.image.path)
		    else:
			logger.info("exifdict esiste, ma non è presente l'attributo orientation")
		else:
		    logger.info("exifdict vuoto")

    def delete(self, *args, **kwargs):
        # You have to prepare what you need before delete the model
        storage, path = self.image.storage, self.image.path
        # Delete the model before the file
        super(tmpUploadedImages, self).delete(*args, **kwargs)
        # Delete the file after the model
        storage.delete(path)
        logger.info("tmpUploadedImages DELETE -> storage: " + str(storage) + " | path: " + str(path))

    def delete_old_tmp_images(self):
        """Function to delete tmp uploaded images older than 5 minutes (as default)"""
        # if upload_date < (now - timedelta 5) -> delete tmp image
        max_validity_datetime = timezone.now() - timedelta(seconds=UPLOADED_IMG_TMP_MAX_LIFETIME) # older than 5 minutes
        old_tmp_images = tmpUploadedImages.objects.filter(upload_date__lte=max_validity_datetime)
        # loop over old images
        if old_tmp_images:
            for old_image in old_tmp_images:
                old_image.delete()
                # logger.info("elimino-> tmp image: " + str(old_image.image.path) + " | upload date: " + str(old_image.upload_date))

	return True
