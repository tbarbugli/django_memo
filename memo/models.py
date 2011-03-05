from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

VISIBILITY_CHOICES = (
    ('private', 'private'),
    ('public', 'public'),
)

hex_color_validator = RegexValidator('^\#([a-fA-F0-9]{6}|[a-fA-F0-9]{3})$', message="A valid hex color code is needed")

class PublicNoteManager(models.Manager):
    def get_query_set(self):
        return super(PublicNoteManager, self).get_query_set().filter(visibility= 'public')

class PrivateNoteManager(models.Manager):
    def get_query_set(self):
        return super(PrivateNoteManager, self).get_query_set().filter(visibility= 'private')
            
class Note(models.Model):
    """
    The App first actor Note model
    
    """           
    
    text = models.TextField(blank= True, null=True)
    owner = models.ForeignKey(User)
    visibility = models.CharField(max_length=30, choices= VISIBILITY_CHOICES, default="private")
    color = models.ForeignKey('Color', null= False, blank= False)
    top = models.DecimalField(max_digits=5, decimal_places=2, default='0')
    left = models.DecimalField(max_digits=5, decimal_places=2, default='0')    
    last_modified = models.TimeField(auto_now=True, auto_now_add=False)
    
    objects = models.Manager()
    private = PrivateNoteManager()
    public = PublicNoteManager()   
    
    def get_absolute_url(self):
        return "/memo/notes/%i/" % self.pk   
        
class Color(models.Model):
    name = models.CharField(max_length=30)
    code = models.CharField(max_length=7, validators= [hex_color_validator])  
    
    @staticmethod
    def default():
        """
        first draft implementation
        """                       
        for color in Color.objects.all():
            return color
            
    def __unicode__(self):
        return unicode(self.code)

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