from django.contrib.auth.decorators import login_required
from django.conf.urls.defaults import *
from memo.feeds import PublicNoteFeed
from memo.views import *  

urlpatterns = patterns('memo.views',
    (r'^$', 'dashboard'),   
    (r'^public_dashboard/(?P<user_id>\d+)/$', 'dashboard'),     
    (r'^notes/add/$', login_required(NoteCreateView.as_view())), 
    (r'^notes/(?P<pk>\d+)/$', login_required(NoteUpdateView.as_view())),
    (r'^follower_notes/(?P<pk>\d+)/$', 
        login_required(NoteFollowerUpdateView.as_view())),
    (r'^follow/(?P<note_id>\d+)/$', 'follow'),
    (r'^unfollow/(?P<note_id>\d+)/$', 'unfollow'),            
    (r'^notes/(?P<pk>\d+)/delete/$', login_required(NoteDeleteView.as_view())),      
    (r'^notes/(?P<pk>\d+)/feed/$', PublicNoteFeed()), 
)