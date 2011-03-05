from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.views.generic import UpdateView, CreateView, DeleteView
from django.template import RequestContext
from django.http import Http404 
from django.contrib.auth.models import User
from memo.models import *
from memo.forms import NoteForm, NoteFollowerForm

class NoteDeleteView(DeleteView):
    queryset = Note.objects.all()
    success_url = "/memo"    
    
    def get_object(self, queryset=None):    
        self.object = None
        user = self.request.user
        obj = super(NoteUpdateView, self).get_object(queryset)
        if obj.owner != user:            
            raise Http404(u"User is not allowed") 
        return obj
        
class NoteUpdateView(UpdateView):
    queryset = Note.objects.all()        
    ajax_form = NoteForm
    ajax_template = "_ajax_form"
    
    def get(self, request, *args, **kwargs):            
        if request.is_ajax():
            self.template_name_suffix = self.ajax_template
            self.form_class = self.ajax_form
        return super(NoteUpdateView, self).get(request, *args, **kwargs)
        
    def get_form_kwargs(self):
        kwargs = super(NoteUpdateView, self).get_form_kwargs()
        kwargs["prefix"] = self.object.id
        return kwargs
        
    def get_object(self, queryset=None):    
        self.object = None
        user = self.request.user
        obj = super(NoteUpdateView, self).get_object(queryset)
        if obj.owner != user:            
            raise Http404(u"User is not allowed") 
        return obj

class NoteFollowerUpdateView(NoteUpdateView):
    queryset = NoteFollower.objects.all() 
    ajax_form = NoteFollowerForm 
    
    def get_object(self, queryset=None):    
        self.object = None
        user = self.request.user
        obj = super(NoteUpdateView, self).get_object(queryset)
        if obj.follower != user:            
            raise Http404(u"User is not allowed") 
        return obj

class NoteCreateView(CreateView):
    model = Note     
    
    def post(self, request, *args, **kwargs):  
        if request.POST['owner'] != unicode(request.user.id):
            raise Http404(u"User is not allowed")    
        return super(NoteCreateView, self).post(request, *args, **kwargs)
        
@login_required              
def dashboard(request, user_id= None):
    """
    returns the user note
    
    """ 
    if user_id is not None:
        queryset = Note.public.filter(owner__id= user_id)
        template_name = "memo/public_note_list.html"
        forms = []   
        followings = []
    else:
        queryset = Note.objects.filter(owner= request.user) 
        template_name = "memo/note_list.html"             
        initial = {'owner': request.user}
        initial['color'] = Color.default()            
        forms = [NoteForm(initial= initial)] 
        f_qs = NoteFollower.objects.filter(follower= request.user)            
        followings = [NoteFollowerForm(instance= nf, prefix= nf.id) for nf in f_qs]

    forms += [NoteForm(instance= note, prefix= note.id) for note in queryset]          
    users = Note.public.exclude(owner__id= request.user.id).values('owner__username', 'owner__id').distinct()
    context = {"forms": forms, "users": users,
       "user": request.user, "followings": followings}   
    return render_to_response(template_name,
                              context,
                              context_instance=RequestContext(request))     
        
    