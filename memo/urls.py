from django.conf.urls.defaults import *
from memo.models import Note
from memo.views import NoteUpdateView  

urlpatterns = patterns('memo.views',
    (r'^$', 'list_notes'), 
    (r'notes/$', 'list_notes'), 
    (r'^notes/(?P<pk>\d+)/$', NoteUpdateView.as_view()),   
)