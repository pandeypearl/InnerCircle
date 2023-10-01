from django import template
from django.apps import apps

register = template.Library()

@register.simple_tag(name="get_object_by_id")
def get_object_by_id(app_label, model_name, object_id):
    model = apps.get_model(app_label=app_label, model_name=model_name)
    if model:
        return model.objects.filter(id=object_id).first()
    return None
