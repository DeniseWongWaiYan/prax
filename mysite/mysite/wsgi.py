import os, sys

# edit your username below
sys.path.append("/home/denisewo/mysite/")

from django.core.wsgi import get_wsgi_application

os.environ['DJANGO_SETTINGS_MODULE'] = "mysite.settings"

application = get_wsgi_application()
