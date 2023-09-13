"""
    Module for cache_bust template tag.
"""
import os
import uuid
from django import template
from django.conf import settings

#Register tag library
register = template.Library()

@register.simple_tag(name='cache_bust')
def cache_bust():
    """
        Function for cache_bust template tag that clears the
        browser cache each time a static file is called so changes 
        can be applied during development.
    """
    if settings.DEBUG:
        version = uuid.uuid1()
    else:
        version = os.environ.get('PROJECT_VERSION')
        if version is None:
            version = '1'

    return '__v__={version}'.format(version=version)