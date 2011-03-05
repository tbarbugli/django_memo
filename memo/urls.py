from django.conf.urls.defaults import *
from memo.models import Note
from memo.views import *  

urlpatterns = patterns('memo.views',
    (r'^$', 'dashboard'),   
    (r'^public_dashboard/(?P<user_id>\d+)/$', 'dashboard'),     
    (r'^notes/add/$', NoteCreateView.as_view()), 
    (r'^notes/(?P<pk>\d+)/$', NoteUpdateView.as_view()),
    (r'^follower_notes/(?P<pk>\d+)/$', NoteFollowerUpdateView.as_view()),
    (r'^follow/(?P<note_id>\d+)/$', 'follow'),
    (r'^unfollow/(?P<note_id>\d+)/$', 'unfollow'),            
    (r'^notes/(?P<pk>\d+)/delete/$', NoteDeleteView.as_view()),   
)