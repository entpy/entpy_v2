Upload Image Box
================

Funzionamento
=============
Si tratta di un widget che permette il caricamento via AJAX di immagini, una finestra ci permetterà di farne il resize, infine si occupa di
salvare la risorsa croppata su S3, funziona anche con directory differenti (es. immagini suddivise per utente).
E' possibile avere più uploader nella stessa pagina senza conflitti.

Installare l'app
----------------
Includere l'app upload_image_box e creare le relative tabelle con makemigration.

1) Creare un form
--------------
Creare un file forms.py con un contenuto simile al seguente:
Il fulcro di tutto è un widget che andrà a sostituire il CharField
NB: se sono presenti più uploader per pagina tutti devono avere il "widget_id" diverso.

# -*- coding: utf-8 -*-

from django import forms
from upload_image_box.widgets import UibUploaderInput
from website_data.models import *

class EditTextSiteForm(forms.Form):
    """Form to edit all text about a site"""

    # custom upload button template
    custom_upload_button = '<div data-widget-id="%(widget_id)s" class="uploaderButtonClickAction upload_profile_image_button btn btn-success bootstrap-trigger">%(widget_button_text)s</div>'
    # form fields
    widget_attr = {
            'widget_id': 'uploader_1',
            'enable_crop': True,
            'default_uploader_button': custom_upload_button,
            'callback_function': 'saveProfileImage',
            'base_modal_title_text': "Seleziona un'immagine",
            'base_modal_description_text': "Per caricare un'immagine clicca sul pulsante sotto.<br />ATTENZIONE: le immagini di nudo non sono consentite e verranno rimosse automaticamente.",
            'upload_modal_title_text': 'Caricamento in corso, attendi...',
            'moving_ball_modal_title_text': 'Caricamento in corso, attendi...',
            'crop_modal_title_text': 'Seleziona area immagine',
            'preview_modal_title_text': 'Anteprima immagine',
            'crop_action_button_text': 'Conferma immagine',
            'select_image_action_button_text': 'Seleziona immagine',
            'widget_button_text': 'Carica immagine',
            'preview_action_button_text': 'Conferma immagine',
            'cancel_button_text': 'Chiudi',
            'change_image_button_text': 'Cambia immagine',
            'crop_modal_description_text': "Seleziona la porzione dell'immagine per il tuo profilo",
    }
    uploaded_image = forms.CharField(label="Carica immagine", widget=UibUploaderInput(attrs=widget_attr))
    image_id = forms.CharField(widget=forms.HiddenInput())
    image_type = forms.CharField(widget=forms.HiddenInput())
    
2) Instanziare il form in una view
----------------------------------
Inizializzare il form creato nello step1 in una view in questo modo:

form = EditTextSiteForm() # An unbound form

Passarlo al context di render (come si fa con tutti i form in pratica):
        context = {'form' : form}
        return render(request, 'admin/custom_view/edit_site.html', context)

3) Creare il file del template
------------------------------
Creare un file .html con un contenuto simile al seguente

{{ form }}

4) Caricare css e librerie js
-----------------------------
Per poter funzionare correttamente l'app ha bisogno dei seguenti file css:

<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/cropper/0.9.1/cropper.min.css">

Allo stesso modo, occorrono i seguenti file js (da notare il form.media al fondo, per caricare il js del widget):
<script src="//ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js" integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa" crossorigin="anonymous"></script>
<script src='//cdn.tinymce.com/4/tinymce.min.js'></script>
<script src="http://malsup.github.com/jquery.form.js"></script> 
<script src="https://cdnjs.cloudflare.com/ajax/libs/cropper/0.9.1/cropper.min.js"></script> 
{{ form.media }}

5) Abilitare il caricamento su S3
---------------------------------
Nel file settings.py del progetto settare le seguenti variabili:
NB: occorre creare il bucket specificato in BOTO_BUCKET su S3, altrimenti non funziona

# Media file settings {{{
BOTO_BUCKET = 'bucket.test'
AWS_ACCESS_KEY_ID = 'your_aws_access_key_id'
AWS_SECRET_ACCESS_KEY = 'your_aws_secret_access_key'
AWS_REGION_NAME = 'eu-west-1'
# Tell django-storages that when coming up with the URL for an item in Cloud Object Storage
BOTO_CUSTOM_DOMAIN = 's3-%s.amazonaws.com/%s' % (AWS_REGION_NAME, BOTO_BUCKET)
BOTO_APP_DIR = 'test/'
MEDIA_URL = "https://%s/" % BOTO_CUSTOM_DOMAIN # used with cropped images
MEDIA_URL_TMP = '/tmp/' # used with temporary images
MEDIA_ROOT = '/tmp/images'
# Media file settings }}}

6) Settare il file urls.py del progetto con gli url dell'app e per i file temporanei
------------------------------------------------------------------------------------
Nel file urls.py del progetto aggiungere la seguente riga:

# upload image
url(r'^upload_image/', include('upload_image_box.urls', namespace="upload_image_box")),

Oltre a questo, per poter funzionare dal server di test, aggiungere al fondo della lista degli urls la seguente riga:

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    ...
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.MEDIA_URL_TMP, document_root=settings.MEDIA_ROOT)

7) Verifica finale
------------------
A questo punto, caricando la pagina con l'uploader, si dovrebbe essere in grado di caricare l'immagine, poterla resizare
ed infine caricarla su S3

EXTRA
=====
A caricamento avvenuto viene chiamata la funzione presente nella configurazione del widget
nel file forms.py

'callback_function': 'saveProfileImage',

La funzione viene chiamata con l'id dell'immagine appena inserita

