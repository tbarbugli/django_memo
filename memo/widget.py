from django.forms.widgets import RadioSelect, RadioFieldRenderer, RadioInput
from django.utils.safestring import mark_safe 
from django.utils.encoding import force_unicode     
from django.utils.html import conditional_escape

class UIRadioInput(RadioInput):    
    def __unicode__(self):
        if 'id' in self.attrs:
            label_for = ' for="%s_%s"' % (self.attrs['id'], self.index)
        else:
            label_for = ''
        choice_label = conditional_escape(force_unicode(self.choice_label)) 
        return mark_safe(u'%s<label%s>%s</label>' % (self.tag(), label_for,  choice_label))
        
class UIRadioFieldRenderer(RadioFieldRenderer):
    def render(self):
        """Outputs a <ul> for this set of radio fields."""
        return mark_safe(u'%s' % u'\n'.join([u'%s'
                % force_unicode(w) for w in self]))
    def __iter__(self):
        for i, choice in enumerate(self.choices):
            yield UIRadioInput(self.name, self.value, self.attrs.copy(), choice, i)
                
class ColorRadioSelect(RadioSelect):    
    renderer = UIRadioFieldRenderer     
    def render(self, name, value=None, attrs=None):
        radio = super(ColorRadioSelect, self).render(name, value, attrs)   
        radio_dict = {'id': attrs["id"], "radio": radio}
        return mark_safe(u"""
            <script type="text/javascript">
            $().ready(function(){
                $("#%(id)s").buttonset(); 
                $("#id_color").children("label").each(function(){
                    $(this).css("background", $(this).text()); $(this).html("&nbsp;")
                });
            })
            </script>
            <div id="%(id)s" class="color_buttons">%(radio)s</div>
            """ % radio_dict)