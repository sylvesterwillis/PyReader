import os
import sys	
sys.path.append('/home/ubuntu/public_html/PyReader/rssreader/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'rssreader.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
