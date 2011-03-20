from django.contrib import admin
from memo.models import Note
  
class NoteAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'owner') 
    
admin.site.register(Note, NoteAdmin)