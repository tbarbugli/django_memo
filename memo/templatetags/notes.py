from django import template
register = template.Library()

@register.inclusion_tag('memo/note_ajax_form.html')
def render_note_form(form):
    return {'form': form}

@register.inclusion_tag('memo/follow_note_ajax_form.html')
def render_follownote_form(form):
    return {'form': form}