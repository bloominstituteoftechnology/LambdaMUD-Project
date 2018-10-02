"""
WSGI config for adv_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

# The Web Server needs to communicate with the Web Application. 
# WSGI specifies the rules which needs to be implemented by the Web Application side 
# and the Web Server side so that they can interact with each other. 

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'adv_project.settings')

application = get_wsgi_application()
