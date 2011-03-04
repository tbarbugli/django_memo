from django.forms import *
from memo.models import Note
from memo.fields import HexColorField 

class NoteForm(ModelForm):   
    text = Textarea(attrs={'cols': 80, 'rows': 20})           
    owner = HiddenInput()
    top = HiddenInput()
    left = HiddenInput()   
    last_modified = HiddenInput()
    
    class Meta:
        model = Note
        
	class Media:
		js = ("/media/js/jquery/jquery-1.5.1.pack.js")