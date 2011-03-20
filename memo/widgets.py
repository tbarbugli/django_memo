from django.forms.widgets import CheckboxInput
from django.utils.safestring import mark_safe 

class ShareCheckBox(CheckboxInput):    
    def render(self, name, value, attrs=None):  
        checkbox = super(ShareCheckBox, self).render(name, value, attrs)
        final_attrs = self.build_attrs(attrs, type='checkbox', name=name)   
        format_dict = {
            "id": final_attrs["id"], "cb": checkbox, 
            "label": final_attrs["label"]
        }
        return mark_safe(u"""
            <script type="text/javascript">
            $().ready(function(){
                $("#%(id)s").button();
            })
            </script>
            <div class="share">%(cb)s <label for="%(id)s">%(label)s</label></div>
            """ % format_dict)