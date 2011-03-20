from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class PublicNoteManager(models.Manager):
    def get_query_set(self):
        return super(PublicNoteManager, self).get_query_set().filter(is_public= True)

class PrivateNoteManager(models.Manager):
    def get_query_set(self):                   
        return super(PrivateNoteManager, self).get_query_set().filter(is_public= False)
            
class Note(models.Model):
    """
    The App first actor Note model
    
    """           
    
    text = models.TextField(blank= True, null=True)
    owner = models.ForeignKey(User)
    is_public = models.BooleanField(default= False)
    top = models.DecimalField(max_digits=5, decimal_places=2, default='0')
    left = models.DecimalField(max_digits=5, decimal_places=2, default='0')    
    last_modified = models.TimeField(auto_now=True, auto_now_add=False)
    
    objects = models.Manager()
    private = PrivateNoteManager()
    public = PublicNoteManager()   
    
    def __unicode__(self):
        return "%s ..." % self.text[:30]
            
    def get_absolute_url(self):
        return "/memo/notes/%i/" % self.pk   
        
class NoteFollower(models.Model):
    follower = models.ForeignKey(User)
    note = models.ForeignKey(Note)
    top = models.DecimalField(max_digits=5, decimal_places=2, default='0')
    left = models.DecimalField(max_digits=5, decimal_places=2, default='0')
    
    class Meta:
        unique_together = ("follower", "note")
        
    def clean(self):           
        if self.note.owner == self.follower:
            raise ValidationError('Owner and follower cant be the same user') 
               
    def get_absolute_url(self):
        return "/memo/follower_notes/%i/" % self.pk    