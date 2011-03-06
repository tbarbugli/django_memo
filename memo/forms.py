from django.forms import *
from memo.models import *
from memo.widget import ColorRadioSelect

class NoteForm(ModelForm):       
    color = ModelChoiceField(Color.objects.all(), empty_label=None, 
        widget=ColorRadioSelect)

    class Meta:
        model = Note  
        widgets = { 
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