from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.views.generic import UpdateView, CreateView, DeleteView
from django.views.generic.detail import SingleObjectMixin
from django.template import RequestContext
from django.http import Http404 
from memo.models import Note, NoteFollower
from memo.forms import NoteForm, NoteFollowerForm
from django.contrib.auth.views import redirect_to_login
from django.core.urlresolvers import reverse

class UserNote(SingleObjectMixin):
    """
    this class in meant to be used to create Mixins
    that checks the ownerships during get_object
    by checking that object_ownership_check
    and user are the same
    
    """
    
    object = None
    request = None
    object_ownership_check = "owner"
    
    def get_object(self, queryset=None):   
        self.object = None
        user = self.request.user
        obj = SingleObjectMixin.get_object(self, queryset)
        owner = getattr(obj, self.object_ownership_check, None)
        if owner is None or owner != user:            
            raise Http404(u"User is not allowed") 
        return obj

class NoteDeleteView(UserNote, DeleteView):
    queryset = Note.objects.all()
    success_url = "/memo"    
    
    def get(self, request, *args, **kwargs):      
        return self.post(request, *args, **kwargs)
            
class NoteUpdateView(UserNote, UpdateView):
    queryset = Note.objects.all()        
    form_class = NoteForm
    template_name_suffix = "_ajax_form"
        
    def get_form_kwargs(self): 
        """
        use the object id as form prefix
        """ 
        kwargs = super(NoteUpdateView, self).get_form_kwargs()
        kwargs["prefix"] = self.object.id
        return kwargs
        
class NoteCreateView(UserNote, CreateView):
    model = Note     
    
    def post(self, request, *args, **kwargs):  
        if request.POST['owner'] != unicode(request.user.id):
            raise Http404(u"User is not allowed")    
        return super(NoteCreateView, self).post(request, *args, **kwargs)

class NoteFollowerUpdateView(NoteUpdateView):
    queryset = NoteFollower.objects.all() 
    form_class = NoteFollowerForm 
    template_name_suffix = "_form"
    object_ownership_check = "follower"  
            
@login_required
def follow(request, note_id):
    note = get_object_or_404(Note, pk= note_id, is_public= True)
    fn = NoteFollower(note_id =note_id, follower= request.user) 
    fn.top = note.top
    fn.left = note.left
    fn.save()    
    return HttpResponse("") 
    
@login_required
def unfollow(request, note_id):   
    NoteFollower.objects.filter(follower= request.user, 
                                note__id= note_id).delete()
    return HttpResponse("")
                          
def dashboard(request, user_id= None):
    """
    returns the user note
    
    """
    if user_id is not None and unicode(request.user.id) == user_id:
        return redirect("memo.views.dashboard")
    elif user_id is None and not request.user.is_authenticated():
        return redirect_to_login(reverse("memo.views.dashboard"))
    if user_id is not None:
        queryset = Note.public.filter(owner__id= user_id)
        template_name = "memo/public_note_list.html"
        forms = []   
        followings = []    
    else:
        queryset = Note.objects.filter(owner= request.user) 
        template_name = "memo/note_list.html"             
        initial = {'owner': request.user}            
        forms = [NoteForm(initial= initial)] 
        f_qs = NoteFollower.objects.filter(follower= request.user)
        f_qs = NoteFollower.objects.exclude(note__is_public= False)        
        followings = [NoteFollowerForm(instance= nf, prefix= nf.id) for nf in f_qs]

    forms += [NoteForm(instance= note, prefix= note.id) for note in queryset]          
    users = Note.public.exclude(owner__id= request.user.id).values('owner__username', 'owner__id').distinct()
    context = {"forms": forms, "users": users,
       "user": request.user, "followings": followings}   
    return render_to_response(template_name,
                              context,
                              context_instance=RequestContext(request))     
        
