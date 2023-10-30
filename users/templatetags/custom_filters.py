'''
    Custom template filters for project.
'''
from django import template

register = template.Library()

@register.filter(name='get_member_groups')
def get_member_groups(member, member_groups_dict):
    return member_groups_dict.get(member.id, [])