from posts import models
from django import template


register= template.Library()

@register.simple_tag(takes_context=True,name='whats_new')
def whats_new(context):
    
    return models.Post.objects.all().order_by('-created_at')[:8]