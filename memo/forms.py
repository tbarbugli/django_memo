from django.forms import *
from memo.widgets import * 
from memo.models import *

class NoteForm(ModelForm):       

    class Meta:
        model = Note  
        widgets = {  
            'is_public': ShareCheckBox(attrs={'label': 'Share'}),
            'text': HiddenInput(attrs={'class': 'text'}), 
            'top': HiddenInput(attrs={'class': 'top'}),
            'left': HiddenInput(attrs={'class': 'left'}),
            'owner': HiddenInput()
        } 

class NoteFollowerForm(ModelForm):
    
    class Meta:
        model = NoteFollower  
        widgets = { 
            'top': HiddenInput(attrs={'class': 'top'}),
            'left': HiddenInput(attrs={'class': 'left'}),
            'follower': HiddenInput(attrs={'class': 'follower'}),   
            'note': HiddenInput(attrs={'class': 'note'}), 
        }