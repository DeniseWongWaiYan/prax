import os, sys

# edit your username below
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.append(BASE_DIR)
print(sys.path.append(BASE_DIR))

from django.core.wsgi import get_wsgi_application

os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'

application = get_wsgi_application()
