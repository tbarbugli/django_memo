from django import template
from memo.models import NoteFollower
register = template.Library()

@register.inclusion_tag('memo/note_ajax_form.html')
def render_note_form(form):
    return {'form': form}

@register.inclusion_tag('memo/public_note_ajax_form.html')
def render_publicnote_form(form, user):
    followed_notes = []                        
    if user.is_authenticated():
        followed_notes = NoteFollower.objects.filter(follower= user).values_list("note__id", flat= True)
    return {'form': form, 'followed_notes': followed_notes, 
            'can_follow': user.is_authenticated()} 
        
@register.inclusion_tag('memo/follow_note_ajax_form.html')
def render_follownote_form(form):
    return {'form': form}