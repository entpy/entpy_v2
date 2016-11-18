# -*- coding: utf-8 -*-

from django import forms
from django.conf import settings
from django.core.files import File
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy
from django.core.files.images import get_image_dimensions
from django.templatetags.static import static
from upload_image_box.exceptions import *
import imghdr

import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

# imghdr fix to detect jpeg images
"""
def test_icc_profile_images(h, f):
    if h.startswith('\xff\xd8') and h[6:17] == b'ICC_PROFILE':
        return "jpeg"
imghdr.tests.append(test_icc_profile_images)
"""

# imghdr fix to detect jpeg images -> (https://bugs.python.org/issue16512)
def test_jpeg(h, f):
    """JPEG data in JFIF or Exif format"""
    if not h.startswith(b'\xff\xd8'):#Test empty files, and incorrect start of file
        return None
    else:
        if f:#if we test a file, test end of jpeg
            f.seek(-2,2)
            if f.read(2).endswith(b'\xff\xd9'):
                return 'jpeg'
        else:#if we just test the header, consider this is a valid jpeg and not test end of file
            return 'jpeg'

imghdr.tests.append(test_jpeg)

class UibUploaderInput(forms.ClearableFileInput):

    # override default ClearableFileInput data
    initial_text = '' # ugettext_lazy('Currently')
    input_text = '' # ugettext_lazy('Change')
    clear_checkbox_label = '' # ugettext_lazy('Clear')
    template_with_clear = '' # '%(clear)s <label for="%(clear_checkbox_id)s">%(clear_checkbox_label)s</label>'

    # default template is a simple div
    template_with_initial = '%(uploader_button)s%(modal_window_scheleton)s%(uploader_script)s'

    def __init__(self, attrs=None):
        # set valid checks
        self.max_file_size = 4*1024*1024 # 4MB
        self.min_file_width = 250
        self.min_file_height = 250
        self.mimetypes_allowed = ['jpeg', 'png',]

        # widget settings
	self.default_attrs = {
		'base_modal_title_text': 'Load an image',
                'base_modal_description_text': "To upload a new image click on 'Load an image' button",
		'upload_modal_title_text': 'Image upload...',
		'moving_ball_modal_title_text': 'Please wait...',
		'crop_modal_title_text': 'Crop your image',
		'preview_modal_title_text': 'Image preview',
		'crop_action_button_text': 'Crop',
		'select_image_action_button_text': 'Select image',
		'widget_button_text': 'Load image',
		'preview_action_button_text': 'Confirm image',
		'cancel_button_text': 'Cancel',
		'change_image_button_text': 'Change image',
                'crop_modal_description_text': "Crop your image!",
                'default_uploader_button': '<div data-widget-id="%(widget_id)s" class="uploader_button uploaderButtonClickAction">%(widget_button_text)s</div>', # default upload button
                'callback_function': '', # custom callback function
		'enable_crop': True,
                'widget_id': 'test_id', # only required field
                'static_url': static(''),
	}

        # overriding defaul attributes
        if attrs:
            self.default_attrs.update(attrs)

        self.uploader_button = self.default_attrs["default_uploader_button"]
        self.modal_window_scheleton = '<div id="%(widget_id)s" class="modal_container" data-base-modal-title-text="%(base_modal_title_text)s" data-base-modal-description-text="%(base_modal_description_text)s" data-upload-modal-title-text="%(upload_modal_title_text)s" data-crop-modal-title-text="%(crop_modal_title_text)s" data-preview-modal-title-text="%(preview_modal_title_text)s" data-crop-action-button-text="%(crop_action_button_text)s" data-preview-action-button-text="%(preview_action_button_text)s" data-cancel-button-text="%(cancel_button_text)s" data-change-image-button-text="%(change_image_button_text)s" data-enable-crop="%(enable_crop)s" data-select-image-action-button-text="%(select_image_action_button_text)s" data-crop-modal-description-text="%(crop_modal_description_text)s" data-callback-function="%(callback_function)s" data-moving-ball-modal-title-text="%(moving_ball_modal_title_text)s" data-static-url="%(static_url)s"></div>'
        self.uploader_script = '<script type="text/javascript">$(function(){uploaderImageBox.init("%(widget_id)s");});</script>'
        # self.uploader_options = '<div class="' + str(self.default_attrs["widget_id"]) '_options" style="display: none!important"></div>'
        super(UibUploaderInput , self).__init__(attrs=None)

    # metodo per scrivere nell'html il file input
    # questa funzione viene eseguita al rendering dell'html
    def render(self, name, value, attrs=None):
	logger.debug("attrs list: " + str(self.default_attrs))
        substitutions = {
            'uploader_button': (self.uploader_button % self.default_attrs),
            'modal_window_scheleton': (self.modal_window_scheleton % self.default_attrs),
            'uploader_script': (self.uploader_script % self.default_attrs),
            # 'uploader_options': (self.uploader_options % self.default_attrs),
        }
        template = self.template_with_initial

        return mark_safe(template % substitutions)

    # Function to validate widget, called on form.is_valid()
    def value_from_datadict(self, data, files, name):
        # if a file was uploaded
        parent_validation = super(UibUploaderInput, self).value_from_datadict(data, files, name)
        # logger.debug("files retrieved: " + str(files))
        file_object = files.get('image', None)
        logger.debug("-------------------files: " + str(files))
        logger.debug("-------------------data: " + str(data))
        logger.debug("-------------------file object: " + str(file_object))
        if parent_validation is not None and file_object is not None:
            # check image MIME/Type
            image_type = imghdr.what(file_object)
            if not image_type or image_type not in self.mimetypes_allowed:
                logger.info("imghdr wrong type: " + str(image_type))
                raise ImageExtensionUIBError

            # retrieve image info
            file_size = file_object.size
            file_w, file_h = get_image_dimensions(file_object)

            # image size check
            logger.debug("Image size: " + str(file_size) + " massima: " + str(self.max_file_size))
            if file_size > self.max_file_size:
                raise ImageSizeUIBError

            # image dimensions check
            logger.debug("Image w: " + str(file_w)+ " image h: " + str(file_h))
            if file_w < self.min_file_width or file_h < self.min_file_height:
                raise ImageDimensionsUIBError
            return file_object  # Return valid file object
        else:
            # raise corrupted file error
            raise CorruptedImageUIBError

    class Media:
        css = {
            'all': ("upload_image_box/css/widget.css",)
        }
        js = ("upload_image_box/js/widget.js",)

    # INTRO
    # =====
    #
    # 1 pulsante per aprire popup "upload image"
    # 2 all'interno del popup un ulteriore pulsante per upload immagine
    # 3 alla selezione dell'immagine ricaricare l'iframe con l'immagine uploadata
    #   e il crop di proporzioni fisse
    # 4 ora è possibile fare due cose: modificare l'immagine uploadata con
    #   un'altra (si riparte dallo step 3), oppure confermare il crop
    # 5 alla conferma del crop salvare l'immagine croppata su disco, meglio ancora se su S3
    # come fare tutto ciò come un Django widget? :o
    # Terminerei con una sufficienza (6): wow fortuna che l'ho fatto...
