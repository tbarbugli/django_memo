from django.forms import *
from memo.models import *
from memo.fields import HexColorField 
from memo.widget import ColorRadioSelect

class NoteForm(ModelForm):       
    color = ModelChoiceField(Color.objects.all(), required= True, empty_label=None, widget=ColorRadioSelect)
    class Meta:
        model = Note  
        widgets = { 
            'text': HiddenInput(attrs={'class': 'text'}), 
            'top': HiddenInput(attrs={'class': 'top'}),
            'left': HiddenInput(attrs={'class': 'left'}),
            'last_modified': HiddenInput(),
            'owner': HiddenInput()
        }