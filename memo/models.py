from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

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
    
    text = models.TextField(null=True)
    owner = models.ForeignKey(User)
    visibility = models.CharField(max_length=30, choices= VISIBILITY_CHOICES)
    color = models.ForeignKey('Color')
    top = models.DecimalField(max_digits=5, decimal_places=2)
    left = models.DecimalField(max_digits=5, decimal_places=2)    
    last_modified = models.TimeField(auto_now=True, auto_now_add=False)
    
    private = PrivateNoteManager()
    public = PublicNoteManager()   
    
class Color(models.Model):
    name = models.CharField(max_length=30)
    code = models.CharField(max_length=7, validators= [hex_color_validator])  
    
    def __unicode__(self):
        return unicode(self.name)