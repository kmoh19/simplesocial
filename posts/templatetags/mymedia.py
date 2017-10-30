from posts import models
from django import template
from simplesocial.settings import MEDIA_URL


register= template.Library()

@register.simple_tag(takes_context=True,name='serve_js')
def serve_js(context,option):
    
    post_obj=models.Post.objects.filter(pk=context['post'].pk)[0]
    
    #print('#####inside#####',option,post_obj.js_file_1.name)
    
    if option == 1:
        result=MEDIA_URL+post_obj.js_file_1.name
    else:
        result=MEDIA_URL+post_obj.js_file_2.name   
    
    return result