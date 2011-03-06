from django.contrib import admin
from memo.models import Note, Color

class ColorAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')

admin.site.register(Color, ColorAdmin)
    
class NoteAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'owner') 
    
admin.site.register(Note, NoteAdmin)