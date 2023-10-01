# from django import template
# from django.contrib.contenttypes.models import ContentType

# register = template.Library()

# @register.filter
# def get_object_by_id(content_type_id, object_id):
#     content_type = ContentType.objects.get_for_id(content_type_id)
#     return content_type.get_object_for_this_type(id=object_id)