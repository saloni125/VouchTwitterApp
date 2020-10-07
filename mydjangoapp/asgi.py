"""
ASGI config for mydjangoapp project.

"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mydjangoapp.settings')

application = get_asgi_application()
