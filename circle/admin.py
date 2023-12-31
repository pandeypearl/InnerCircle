''' 
    Script to manage the administrative aspects of the circle application. 
'''
from django.contrib import admin
from .models import Group, Member, Note

# Register your models here.
class GroupAdmin(admin.ModelAdmin):
    list_display = ('group_name', 'created')

admin.site.register(Group, GroupAdmin)

class MemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'relationship', 'user', 'created')

admin.site.register(Member, MemberAdmin)

class NoteAdmin(admin.ModelAdmin):
    list_display = ('subject', 'created')

admin.site.register(Note, NoteAdmin)