'''
    Template filter for in_list function
'''
from django import template

register = template.Library()

@register.filter(name='in_list')
def in_list(value, arg):
    return value in arg.split(',')