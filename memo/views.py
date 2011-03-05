from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.views.generic import UpdateView
from django.template import RequestContext
from django.http import Http404 
from memo.models import Note
from memo.forms import NoteForm

class NoteUpdateView(UpdateView):
    queryset = Note.objects.all() 
    form_class = NoteForm
       
    def get_form_kwargs(self):
        kwargs = super(NoteUpdateView, self).get_form_kwargs()
        kwargs["prefix"] = self.object.id
        return kwargs
        
    def get_object(self, queryset=None):
        obj = super(NoteUpdateView, self).get_object(queryset)
        if obj.owner != self.request.user:
            pass
            #raise Http404(u"User is not allowed") 
        return obj
         
@login_required
def list_notes(request, user_id= None):
    """
    returns the user note
    
    """
    queryset = Note.objects.filter(owner= request.user)        
    forms = [NoteForm(instance= note, prefix= note.id) for note in queryset]
    forms.append(NoteForm())   
    return render_to_response('memo/note_list.html',
                              {"forms": forms},
                              context_instance=RequestContext(request))     
        
    