from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from memo.models import * 
from memo.forms import *

class OwnershipTest(TestCase):
    """
    tests for note views
    
    """
    
    fixtures = ("test_data.json",)
    
    def setUp(self):
        self.tom, c = User.objects.get_or_create(username="tom") 
        self.tom.set_password("tom")
        self.tom.save()
        self.charlie, c = User.objects.get_or_create(username="charlie")
        self.charlie.set_password("charlie")
        self.charlie.save()
        self.tom_session = Client()
        self.tom_session.login(username="tom", password="tom")
        self.charlie_session = Client()
        self.charlie_session.login(username="charlie", password="charlie")
        self.tom_private_note, c = Note.objects.get_or_create(owner= self.tom)
               
    def test_get_private_note(self):
        note_url = reverse('note', args=(self.tom_private_note.pk,))  
        self.assertEquals(self.tom_session.get(note_url).status_code, 200) 
        self.assertEquals(self.tom_session.post(note_url).status_code, 200)
        self.assertEquals(self.charlie_session.get(note_url).status_code, 404)
        self.assertEquals(self.charlie_session.post(note_url).status_code, 404)        
               
    def test_createprivate_note(self):
        note_post_dict = {
            "text": "test note",
            "is_public": False,
            "top": 0,
            "left": 0,
            "owner": self.tom.id
        }             
        note_url = reverse('note') 
        response = self.tom_session.post(note_url, note_post_dict)
        self.assertEquals(response.status_code, 302)
        response = self.tom_session.post(note_url, note_post_dict, 
            follow= True)
        self.assertEquals(response.status_code, 200)
        
    def test_delete_note(self):
        note = Note(owner= self.tom)
        note.save()
        note_url = reverse('delete_note', args= (note.pk,))
        response = self.charlie_session.get(note_url) 
        self.assertEquals(response.status_code, 404)
        response = self.tom_session.get(note_url, follow= True)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(Note.objects.filter(pk= note.pk).count(), 0)        
        
    def test_dashboard(self):      
        note_url = reverse('memo.views.dashboard')        
        response = self.charlie_session.get(note_url)
        self.assertEquals(response.status_code, 200)
        response = self.tom_session.get(note_url)
        self.assertEquals(response.status_code, 200)
        response = Client().get(note_url)
        self.assertEquals(response.status_code, 302)        
        note_url = reverse('memo.views.dashboard', args=(self.tom.pk,))
        response = self.charlie_session.get(note_url)
        self.assertEquals(response.status_code, 200)
        response = self.tom_session.get(note_url)
        self.assertEquals(response.status_code, 302)
        response = Client().get(note_url)
        self.assertEquals(response.status_code, 200)
        
    def test_follow_unfollow(self):                
        note = Note(owner= self.tom, is_public= True)
        note.save()       
        follow_url = reverse('memo.views.follow', args=(note.pk,)) 
        unfollow_url = reverse('memo.views.unfollow', args=(note.pk,)) 
        response = self.charlie_session.post(follow_url, follow= True)
        self.assertEquals(response.status_code, 200)
        NoteFollower.objects.get(follower= self.charlie, note__id= note.pk)            
        response = self.charlie_session.post(unfollow_url, follow= True)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(NoteFollower.objects.filter(follower= self.charlie, 
            note__id= note.pk).count(), 0)
        note.is_public = False
        note.save()
        response = self.charlie_session.post(follow_url, follow= True)
        self.assertEquals(response.status_code, 404) 
    
    def test_edit_following(self):
        note = Note(owner= self.tom, is_public= True)
        note.save()       
        follow_url = reverse('memo.views.follow', args=(note.pk,))
        self.charlie_session.post(follow_url, follow= True)         
        notefollower = NoteFollower.objects.get(follower= self.charlie, 
            note__id= note.pk)
        notefollower_dict = {   
            '%s-note' % notefollower.id: note.id,
            '%s-follower' % notefollower.id: self.charlie.id,
            '%s-top' % notefollower.id: '1',
            '%s-left' % notefollower.id: '1'
        }               
        follownote_url = reverse('notefollower', args=(notefollower.pk,))
        response = self.charlie_session.post(follownote_url, notefollower_dict) 
        self.assertEquals(response.status_code, 302)