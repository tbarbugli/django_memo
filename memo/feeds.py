from django.contrib.syndication.views import Feed
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from memo.models import Note

class PublicNoteFeed(Feed):
    description_template = 'feeds/note_description.html'
    
    def get_object(self, request, pk):         
        return get_object_or_404(User, pk= pk)    
        
    def link(self, obj):   
        return "/memo/public_dashboard/%s/" % obj.id
            
    def description(self, obj):
        return "%s Public notes recently edited" % obj.username 
    
    def title(self, obj):
        return "%s Public notes" % obj.username

    def items(self, obj):
        return Note.public.filter(owner=obj).order_by('-last_modified')[:30]

    def item_link(self, item):
        return "/memo/public_dashboard/%s/" % item.owner.id     